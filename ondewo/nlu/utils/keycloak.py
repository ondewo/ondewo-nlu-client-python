# Copyright 2021-2025 ONDEWO GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Headless SDK authentication against Keycloak (D18 offline-token flow).

This module implements the headless offline-token authentication described in the
keycloak migration plan (D18) for the *public* SDK client `ondewo-nlu-cai-sdk-public`
(no client secret, Q1):

1. A one-time ROPC login (``grant_type=password`` + ``scope=offline_access``) against
   the public Keycloak client returns a short-lived ``access_token`` and a long-lived
   *offline* ``refresh_token``.
2. The provider auto-refreshes the access token (``grant_type=refresh_token``) before
   it expires and attaches it as the standard ``Authorization: Bearer`` metadata. The
   refresh happens *proactively* in a background daemon thread (mirroring the nodejs /
   js / ts / angular SDKs) that wakes :data:`_EXPIRY_LEEWAY_S` before expiry, and a
   *lazy* read-time check on :meth:`authorization_metadata` remains as a cheap fallback.
3. The auto-refresh loop stops once ``token_expiration_in_s`` has elapsed since login
   (omit it to keep refreshing until the offline session itself expires).

No 2FA is involved: the account is a 2FA-exempt technical user and ROPC bypasses the
browser flow (D14). The client is public, so no ``client_secret`` is sent.
"""
import threading
import time
import weakref
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Protocol,
    Tuple,
)
from weakref import WeakValueDictionary

import requests

from ondewo.nlu.client_config import ClientConfig

# Standard OIDC token endpoint path under a Keycloak realm.
_TOKEN_ENDPOINT_TEMPLATE: str = '{keycloak_url}/realms/{realm}/protocol/openid-connect/token'

# Refresh the access token this many seconds *before* it actually expires so that an
# in-flight call never travels with a token that lapses mid-request.
_EXPIRY_LEEWAY_S: float = 30.0

# Lower bound (in seconds) for the scheduled background-refresh delay so a tiny/zero
# ``expires_in`` cannot spin the refresh thread into a hot loop.
_MIN_REFRESH_DELAY_S: float = 1.0

# HTTP timeout for the (single, fast) token-endpoint calls.
_HTTP_TIMEOUT_S: float = 30.0

# Timeout (seconds) for joining the background refresh thread on stop()/__del__ so a
# refresh stuck in an HTTP call cannot block teardown indefinitely.
_THREAD_JOIN_TIMEOUT_S: float = 5.0


class TokenEndpoint(Protocol):
    """
    Minimal HTTP transport contract for the Keycloak token endpoint.

    `requests.Session`/`requests` satisfy this Protocol; unit tests pass a fake
    transport so the offline-token flow can be exercised without any network.
    """

    def post(
        self,
        url: str,
        data: Dict[str, str],
        timeout: float,
    ) -> 'TokenResponse':
        """Send an ``application/x-www-form-urlencoded`` POST and return the response."""
        ...  # pragma: no cover - abstract Protocol method, never executed


class TokenResponse(Protocol):
    """Minimal response contract: the bits of `requests.Response` the provider reads."""

    status_code: int

    def json(self) -> Dict[str, Any]:
        """Return the parsed JSON body."""
        ...  # pragma: no cover - abstract Protocol method, never executed

    @property
    def text(self) -> str:
        """Return the raw response body (used for error messages)."""
        ...  # pragma: no cover - abstract Protocol property, never executed


class _RequestsTransport:
    """Default :class:`TokenEndpoint` backed by :func:`requests.post`."""

    def post(self, url: str, data: Dict[str, str], timeout: float) -> requests.Response:
        """Send a form-encoded POST to the Keycloak token endpoint."""
        return requests.post(url, data=data, timeout=timeout)


class KeycloakAuthenticationError(Exception):
    """Raised when the Keycloak token endpoint rejects a login or refresh request."""


def _refresh_loop(
    provider_ref: 'weakref.ref[KeycloakTokenProvider]',
    stop_event: threading.Event,
    time_fn: Callable[[], float],
) -> None:
    """
    Background daemon-thread target that proactively refreshes the access token.

    The loop derefs the (weak) provider reference on every wake and exits as soon as it
    resolves to ``None`` — the provider has been garbage-collected (it is held only weakly
    by :data:`_PROVIDER_REGISTRY`), so a strong ``self`` reference here would pin it forever
    and leak the thread. On each iteration it computes the delay until
    :data:`_EXPIRY_LEEWAY_S` before the current access token's expiry, clamps it to
    :data:`_MIN_REFRESH_DELAY_S`, then waits that long on ``stop_event`` (so :meth:`stop`
    interrupts the sleep immediately). When the wait times out it refreshes the access token
    under the provider lock. The loop stops once :meth:`stop` is called or the
    ``token_expiration_in_s`` login deadline has elapsed.

    Args:
        provider_ref (weakref.ref[KeycloakTokenProvider]):
            Weak reference to the owning provider; the loop exits when it derefs to ``None``.
        stop_event (threading.Event):
            Event signalled by :meth:`stop`; also used as the interruptible sleep primitive.
        time_fn (Callable[[], float]):
            Monotonic clock (injectable for deterministic tests).
    """
    while not stop_event.is_set():
        provider: Optional['KeycloakTokenProvider'] = provider_ref()
        if provider is None:
            # The provider has been collected; never resurrect it — just exit the thread.
            return

        now: float = time_fn()
        deadline: Optional[float] = provider._login_deadline
        if deadline is not None and now >= deadline:
            # The bounded auto-refresh window has closed: stop renewing and let the token lapse.
            stop_event.set()
            return

        delay: float = provider._access_token_expires_at - _EXPIRY_LEEWAY_S - now
        if delay < _MIN_REFRESH_DELAY_S:
            delay = _MIN_REFRESH_DELAY_S
        if deadline is not None:
            remaining: float = deadline - now
            if remaining < delay:
                delay = remaining

        # Drop the strong reference before sleeping so a long wait cannot pin the provider.
        provider = None

        # Wait returns True if stop() fired, False on timeout — only a timeout triggers a refresh.
        if stop_event.wait(delay):
            return

        provider = provider_ref()
        if provider is None:
            return
        with provider._lock:
            provider._refresh_if_within_window(now=time_fn())
        provider = None


class KeycloakTokenProvider:
    """
    Acquire and auto-refresh a Keycloak access token for the headless SDK (D18).

    The provider performs a one-time ROPC login with ``scope=offline_access`` against a
    public Keycloak client and then refreshes the access token from the offline refresh
    token. Refresh happens two ways, both within the ``token_expiration_in_s`` window:

    * **Proactively**, in a background daemon thread that wakes :data:`_EXPIRY_LEEWAY_S`
      before the access token's expiry, refreshes, and reschedules from the new expiry
      (mirroring the nodejs / js / ts / angular SDKs).
    * **Lazily**, as a cheap fallback: reading :meth:`authorization_metadata` (or
      :meth:`bearer_metadata`) refreshes the token whenever it is within
      :data:`_EXPIRY_LEEWAY_S` of expiry.

    Both paths are serialised by an internal lock, so every outgoing gRPC call carries a
    fresh ``Authorization: Bearer`` value. Once ``token_expiration_in_s`` has elapsed since
    login the refresh stops, the background thread exits, and the access token is allowed to
    lapse (re-login required). Call :meth:`stop` (or use the provider as a context manager)
    for deterministic teardown of the background thread.

    Attributes:
        keycloak_url (str):
            Base URL of the Keycloak server, e.g. ``https://host/auth``.
        realm (str):
            Keycloak realm name, e.g. ``ondewo-ccai-platform``.
        client_id (str):
            The public SDK client id, e.g. ``ondewo-nlu-cai-sdk-public`` (no secret).
        username (str):
            Technical-user email/username for the ROPC grant.
        password (str):
            Technical-user password for the ROPC grant.
        token_expiration_in_s (Optional[int]):
            Upper bound (in seconds since login) on how long auto-refresh runs. ``None``
            keeps refreshing until the offline session itself expires.
    """

    def __init__(
        self,
        keycloak_url: str,
        realm: str,
        client_id: str,
        username: str,
        password: str,
        token_expiration_in_s: Optional[int] = None,
        transport: Optional[TokenEndpoint] = None,
        time_fn: Optional[Callable[[], float]] = None,
        stop_event: Optional[threading.Event] = None,
        start_background_refresh: bool = True,
    ) -> None:
        """
        Initialize the provider, acquire the offline token, and arm the background refresh.

        Args:
            keycloak_url (str):
                Base URL of the Keycloak server (the part before ``/realms/<realm>``).
            realm (str):
                Keycloak realm name.
            client_id (str):
                The public SDK client id (no ``client_secret`` is ever sent, Q1).
            username (str):
                Technical-user email/username for the ROPC grant.
            password (str):
                Technical-user password for the ROPC grant.
            token_expiration_in_s (Optional[int]):
                Bounds how long the auto-refresh runs (seconds since login). ``None`` =
                until the offline session expires.
            transport (Optional[TokenEndpoint]):
                HTTP transport for the token endpoint. Defaults to :mod:`requests`. Unit
                tests inject a fake transport so no network is required.
            time_fn (Optional[Callable[[], float]]):
                Monotonic clock used for all expiry bookkeeping and the background-refresh
                schedule. Defaults to :func:`time.monotonic`; tests inject a controllable
                fake so the background thread is deterministic.
            stop_event (Optional[threading.Event]):
                Event the background thread waits on (interruptible sleep) and that
                :meth:`stop` signals. Defaults to a fresh :class:`threading.Event`; tests
                inject a controllable one to drive the loop without real sleeps.
            start_background_refresh (bool):
                Whether to spawn the background refresh thread after login. Defaults to
                ``True``; tests set it to ``False`` to drive the loop body directly.

        Raises:
            KeycloakAuthenticationError:
                If the initial ROPC login is rejected by Keycloak.
        """
        self.keycloak_url: str = keycloak_url.rstrip('/')
        self.realm: str = realm
        self.client_id: str = client_id
        self.username: str = username
        self.password: str = password
        self.token_expiration_in_s: Optional[int] = token_expiration_in_s
        self._transport: TokenEndpoint = transport if transport is not None else _RequestsTransport()
        self._time_fn: Callable[[], float] = time_fn if time_fn is not None else time.monotonic

        self._token_endpoint: str = _TOKEN_ENDPOINT_TEMPLATE.format(
            keycloak_url=self.keycloak_url,
            realm=self.realm,
        )

        self._access_token: str = ''
        self._refresh_token: str = ''
        self._access_token_expires_at: float = 0.0
        self._login_deadline: Optional[float] = None

        # Serialises the lazy read-path refresh against the background-thread refresh.
        self._lock: threading.RLock = threading.RLock()
        # Signalled by stop(); also the interruptible sleep primitive for the refresh thread.
        self._stop_event: threading.Event = stop_event if stop_event is not None else threading.Event()
        self._refresh_thread: Optional[threading.Thread] = None

        self._login()

        if start_background_refresh:
            self._start_background_refresh()

    def __enter__(self) -> 'KeycloakTokenProvider':
        """
        Enter the runtime context, returning the provider itself.

        Returns:
            KeycloakTokenProvider:
                This provider, with its background refresh thread running.
        """
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """
        Exit the runtime context and stop the background refresh thread.

        Args:
            exc_type (Any):
                The exception type if the ``with`` block raised, else ``None``.
            exc_value (Any):
                The exception instance if the ``with`` block raised, else ``None``.
            traceback (Any):
                The traceback if the ``with`` block raised, else ``None``.
        """
        self.stop()

    def __del__(self) -> None:
        """Stop the background refresh thread when the provider is garbage-collected."""
        self.stop()

    @property
    def access_token(self) -> str:
        """The most recently issued access token (refreshed lazily and in the background)."""
        return self._access_token

    def authorization_metadata(self) -> Tuple[str, str]:
        """
        Return the ``Authorization: Bearer`` gRPC metadata tuple, refreshing if needed.

        Returns:
            Tuple[str, str]:
                ``('authorization', 'Bearer <access_token>')`` with a token that is valid
                for at least :data:`_EXPIRY_LEEWAY_S` more seconds (when within the
                ``token_expiration_in_s`` window).
        """
        with self._lock:
            self._refresh_if_within_window(now=self._time_fn())
            return ('authorization', f'Bearer {self._access_token}')

    def bearer_metadata(self) -> List[Tuple[str, str]]:
        """
        Return the full gRPC metadata list carrying the bearer token.

        Returns:
            List[Tuple[str, str]]:
                A single-element list with the ``Authorization: Bearer`` tuple, matching
                the shape the services interfaces expect.
        """
        return [self.authorization_metadata()]

    def stop(self) -> None:
        """
        Stop the background refresh loop and join its thread. Idempotent and safe from any state.

        Signals the stop event (interrupting any in-flight :meth:`threading.Event.wait`) and
        joins the background thread with a bounded timeout so teardown — including the
        :meth:`__del__` path — never blocks indefinitely on a stuck refresh.
        """
        self._stop_event.set()
        thread: Optional[threading.Thread] = self._refresh_thread
        # Never join from within the refresh thread itself (would deadlock); only an external
        # caller joins. A daemon thread that outlives this join is reaped at interpreter exit.
        if thread is not None and thread is not threading.current_thread():
            thread.join(timeout=_THREAD_JOIN_TIMEOUT_S)

    # An alias so callers used to ``close()`` get the same deterministic teardown.
    close = stop

    def _start_background_refresh(self) -> None:
        """
        Spawn the daemon thread that proactively refreshes the access token before expiry.

        The thread target receives only a :class:`weakref.ref` to this provider (never a bound
        method or strong ``self``), so the provider — held weakly by :data:`_PROVIDER_REGISTRY`
        — can still be garbage-collected; the loop exits on the next wake when the weakref
        resolves to ``None``.
        """
        provider_ref: 'weakref.ref[KeycloakTokenProvider]' = weakref.ref(self)
        thread: threading.Thread = threading.Thread(
            target=_refresh_loop,
            args=(provider_ref, self._stop_event, self._time_fn),
            name=f'keycloak-token-refresh-{self.client_id}',
            daemon=True,
        )
        self._refresh_thread = thread
        thread.start()

    def _refresh_if_within_window(self, now: float) -> None:
        """
        Refresh the access token if it is near expiry and refresh is still permitted.

        Shared by the lazy read path and the background thread; callers hold :attr:`_lock`.
        Does nothing once ``token_expiration_in_s`` has elapsed since login (the access token
        is then allowed to lapse). Within the window, refreshes via the offline refresh token
        whenever the current access token is within the leeway of its ``exp``.

        Args:
            now (float):
                The current monotonic time, sampled by the caller from :attr:`_time_fn`.
        """
        if self._login_deadline is not None and now >= self._login_deadline:
            # The auto-refresh window has closed: stop renewing and let the token lapse.
            return
        if now < self._access_token_expires_at - _EXPIRY_LEEWAY_S:
            # Current access token is still comfortably valid.
            return
        self._refresh()

    def _login(self) -> None:
        """
        Perform the one-time ROPC login (``grant_type=password`` + ``offline_access``).

        Raises:
            KeycloakAuthenticationError:
                If Keycloak rejects the credentials.
        """
        data: Dict[str, str] = {
            'grant_type': 'password',
            'client_id': self.client_id,
            'username': self.username,
            'password': self.password,
            'scope': 'offline_access',
        }
        payload: Dict[str, Any] = self._post_token_request(data=data, action='login')
        self._store_tokens(payload=payload)
        if self.token_expiration_in_s is not None:
            self._login_deadline = self._time_fn() + self.token_expiration_in_s

    def _refresh(self) -> None:
        """
        Exchange the offline refresh token for a fresh access token.

        Raises:
            KeycloakAuthenticationError:
                If Keycloak rejects the refresh token.
        """
        data: Dict[str, str] = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'refresh_token': self._refresh_token,
        }
        payload: Dict[str, Any] = self._post_token_request(data=data, action='refresh')
        self._store_tokens(payload=payload)

    def _post_token_request(self, data: Dict[str, str], action: str) -> Dict[str, Any]:
        """
        POST a form-encoded request to the token endpoint and return the parsed body.

        Args:
            data (Dict[str, str]):
                The ``application/x-www-form-urlencoded`` form parameters.
            action (str):
                Human-readable action name (``'login'`` / ``'refresh'``) for error messages.

        Returns:
            Dict[str, Any]:
                The parsed JSON token response.

        Raises:
            KeycloakAuthenticationError:
                On a non-2xx status or an unparseable body.
        """
        response: TokenResponse = self._transport.post(
            self._token_endpoint,
            data=data,
            timeout=_HTTP_TIMEOUT_S,
        )
        if response.status_code < 200 or response.status_code >= 300:
            raise KeycloakAuthenticationError(
                f'Keycloak token {action} failed with status {response.status_code}: {response.text}'
            )
        body: Dict[str, Any] = response.json()
        return body

    def _store_tokens(self, payload: Dict[str, Any]) -> None:
        """
        Store the access token, refresh token, and the computed expiry from a token response.

        Args:
            payload (Dict[str, Any]):
                The parsed token endpoint response.

        Raises:
            KeycloakAuthenticationError:
                If the response carries no ``access_token``.
        """
        access_token: str = payload.get('access_token', '')
        if not access_token:
            raise KeycloakAuthenticationError(
                f'Keycloak token response did not contain an access_token: {payload!r}'
            )
        self._access_token = access_token
        # Keycloak always re-issues the refresh token; keep the previous one if absent so a
        # response that omits it (e.g. a same-token refresh) does not blank out the offline token.
        refresh_token: str = payload.get('refresh_token', '')
        if refresh_token:
            self._refresh_token = refresh_token

        expires_in: int = int(payload.get('expires_in', 0))
        self._access_token_expires_at = self._time_fn() + expires_in


# One shared provider per ClientConfig so the ROPC offline-token login happens once for all
# of a client's service stubs (they all read the same auto-refreshed access token). The weak
# reference lets the provider be collected once the config is gone.
_PROVIDER_REGISTRY: 'WeakValueDictionary[int, KeycloakTokenProvider]' = WeakValueDictionary()
_PROVIDER_REGISTRY_LOCK: threading.Lock = threading.Lock()


def get_keycloak_token_provider(config: ClientConfig) -> KeycloakTokenProvider:
    """
    Return the shared :class:`KeycloakTokenProvider` for a client config, creating it once.

    All service stubs built from the same `ClientConfig` share a single provider, so the
    one-time ROPC offline-token login runs once and every stub reads the same auto-refreshed
    access token.

    Args:
        config (ClientConfig):
            A config with the Keycloak headless-auth fields set (`config.use_keycloak`).

    Returns:
        KeycloakTokenProvider:
            The provider bound to this config (created on first call).
    """
    key: int = id(config)
    with _PROVIDER_REGISTRY_LOCK:
        provider: Optional[KeycloakTokenProvider] = _PROVIDER_REGISTRY.get(key)
        if provider is None:
            provider = KeycloakTokenProvider(
                keycloak_url=config.keycloak_url,
                realm=config.realm,
                client_id=config.client_id,
                username=config.user_name,
                password=config.password,
                token_expiration_in_s=config.token_expiration_in_s,
            )
            _PROVIDER_REGISTRY[key] = provider
        return provider
