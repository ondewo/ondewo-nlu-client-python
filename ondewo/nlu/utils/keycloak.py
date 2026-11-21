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
   *offline* ``refresh_token``. A caller that already holds such an offline token can hand
   it to the provider instead (``refresh_token=``), which skips step 1 entirely: the
   provider starts at step 2 and no password grant is ever sent.
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

import hashlib
import random
import sys
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

from loguru import logger
from weakref import WeakValueDictionary

import requests
import urllib3

from ondewo.nlu.client_config import ClientConfig

# Standard OIDC token endpoint path under a Keycloak realm.
_TOKEN_ENDPOINT_TEMPLATE: str = "{keycloak_url}/realms/{realm}/protocol/openid-connect/token"

# Refresh the access token this many seconds *before* it actually expires so that an
# in-flight call never travels with a token that lapses mid-request.
_EXPIRY_LEEWAY_S: float = 30.0

# Lower bound (in seconds) for the scheduled background-refresh delay so a tiny/zero
# ``expires_in`` cannot spin the refresh thread into a hot loop.
_MIN_REFRESH_DELAY_S: float = 1.0

# First retry delay (seconds) after a FAILED refresh. Deliberately far above
# ``_MIN_REFRESH_DELAY_S``: a failed refresh leaves ``_access_token_expires_at`` unchanged, so the
# ordinary delay computation would clamp to the 1 s floor and a Keycloak outage would become a 1 Hz
# poll per client. ondewo runs one client per call container, so a floor that is harmless for a
# single process is an amplifier against a realm they all share.
_REFRESH_RETRY_BASE_DELAY_S: float = 5.0

# Ceiling (seconds) for the failure backoff: a persistent outage is retried at most this often.
_REFRESH_RETRY_MAX_DELAY_S: float = 300.0

# Exponent cap so ``2 ** n`` cannot grow without bound; 5 * 2^6 = 320 already exceeds the ceiling.
_MAX_REFRESH_RETRY_EXPONENT: int = 6

# HTTP timeout (seconds) for one token-endpoint call. A refresh runs while the provider lock is held,
# and every gRPC call reads its bearer token under that lock, so this bounds how long a hung Keycloak
# can stall the client's calls. A healthy token endpoint answers in well under a second.
_HTTP_TIMEOUT_S: float = 10.0

# The longest slice of a Keycloak error body quoted in an exception. A proxy in front of Keycloak can
# answer a 502 with a whole HTML page, which is noise in a log line and in a traceback.
_MAX_ERROR_BODY_CHARS: int = 500

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
    ) -> "TokenResponse":
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

    def __init__(self, verify_ssl: bool = True) -> None:
        """Store the TLS-verification flag for the token-endpoint POST.

        Args:
            verify_ssl (bool):
                Whether :func:`requests.post` verifies the server's TLS certificate.
                Defaults to ``True`` (secure). When ``False``, urllib3's
                ``InsecureRequestWarning`` is suppressed so the disabled-verification
                path does not emit a warning on every call.
        """
        self._verify_ssl: bool = verify_ssl
        if not verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def post(self, url: str, data: Dict[str, str], timeout: float) -> requests.Response:
        """Send a form-encoded POST to the Keycloak token endpoint."""
        return requests.post(url, data=data, timeout=timeout, verify=self._verify_ssl)


class KeycloakAuthenticationError(Exception):
    """Raised when the Keycloak token endpoint rejects a login or refresh request."""


def _backoff_delay_s(consecutive_failures: int, random_fn: Callable[[], float]) -> float:
    """
    Compute the wait before the next attempt after ``consecutive_failures`` failed refreshes.

    The ceiling grows ``_REFRESH_RETRY_BASE_DELAY_S * 2 ** (failures - 1)`` up to
    :data:`_REFRESH_RETRY_MAX_DELAY_S`, and the returned delay is drawn uniformly from
    ``[base, ceiling]``. The jitter is the load-bearing half: N containers whose refreshes fail in
    the same instant would otherwise retry in lockstep for as long as the outage lasts.

    Args:
        consecutive_failures (int):
            Number of consecutive failed refreshes; values below 1 are treated as 1.
        random_fn (Callable[[], float]):
            Source of a ``[0.0, 1.0)`` fraction (injectable so tests get an exact delay). A value
            outside that range is clamped, so a faulty source can never yield a negative delay or
            one above the ceiling.

    Returns:
        float:
            Seconds to wait before the next refresh attempt.
    """
    exponent: int = min(max(consecutive_failures, 1) - 1, _MAX_REFRESH_RETRY_EXPONENT)
    ceiling_s: float = min(_REFRESH_RETRY_BASE_DELAY_S * float(2**exponent), _REFRESH_RETRY_MAX_DELAY_S)
    fraction: float = min(max(random_fn(), 0.0), 1.0)
    return _REFRESH_RETRY_BASE_DELAY_S + fraction * (ceiling_s - _REFRESH_RETRY_BASE_DELAY_S)


def _refresh_loop(
    provider_ref: "weakref.ref[KeycloakTokenProvider]",
    stop_event: threading.Event,
    time_fn: Callable[[], float],
) -> None:
    """
    Background daemon-thread target that proactively refreshes the access token.

    The loop derefs the (weak) provider reference on every wake and exits as soon as it
    resolves to ``None`` — the provider has been garbage-collected (it is held only weakly
    by :data:`_PROVIDER_REGISTRY`), so a strong ``self`` reference here would pin it forever
    and leak the thread. On each iteration it computes the delay until
    :data:`_EXPIRY_LEEWAY_S` before the current access token's expiry — or, after a failed
    refresh, until the provider's backoff allows the next attempt — clamps it to
    :data:`_MIN_REFRESH_DELAY_S`, then waits that long on ``stop_event`` (so :meth:`stop`
    interrupts the sleep immediately). When the wait times out it refreshes the access token
    under the provider lock. The loop stops once :meth:`stop` is called or the
    ``token_expiration_in_s`` login deadline has elapsed.

    A failed refresh NEVER ends the loop. This function is the thread target and nothing re-arms
    the thread, so an exception escaping it would end proactive refresh for the life of the
    process -- one transient answer from the token endpoint (a 502 from a proxy, a DNS blip, a
    restarting Keycloak, a dead offline session) was enough to let every token lapse. The provider
    records and logs each failure and schedules the retry (:meth:`KeycloakTokenProvider._record_refresh_failure`),
    so the loop only has to keep going.

    Args:
        provider_ref (weakref.ref[KeycloakTokenProvider]):
            Weak reference to the owning provider; the loop exits when it derefs to ``None``.
        stop_event (threading.Event):
            Event signalled by :meth:`stop`; also used as the interruptible sleep primitive.
        time_fn (Callable[[], float]):
            Monotonic clock (injectable for deterministic tests).
    """
    while not stop_event.is_set():
        provider: Optional["KeycloakTokenProvider"] = provider_ref()
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
        if provider._consecutive_refresh_failures > 0:
            # A failed refresh leaves ``_access_token_expires_at`` unchanged, so the computation
            # above would retry at the 1 s floor for the whole outage. Wait for the backoff instead.
            delay = provider._next_refresh_attempt_at - now
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
        try:
            with provider._lock:
                provider._refresh_if_within_window(now=time_fn())
        except Exception as exception:
            # The provider has already recorded, logged and scheduled the retry of the failure that
            # raised here (the access token has expired, so the lazy read path raises it too). This
            # guard exists so the thread survives it; logging it again would double every warning.
            logger.debug(f"Keycloak background refresh will be retried ({type(exception).__name__}: {exception})")
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
            Technical-user password for the ROPC grant. Unused when the provider was handed an
            offline ``refresh_token``: that path never sends a password grant, whether or not a
            password was also supplied.
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
        verify_ssl: bool = True,
        transport: Optional[TokenEndpoint] = None,
        time_fn: Optional[Callable[[], float]] = None,
        random_fn: Optional[Callable[[], float]] = None,
        stop_event: Optional[threading.Event] = None,
        start_background_refresh: bool = True,
        refresh_token: str = "",
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
            verify_ssl (bool):
                Whether the *default* :class:`_RequestsTransport` verifies the Keycloak
                server's TLS certificate. Defaults to ``True`` (secure). Ignored when a
                custom ``transport`` is injected (the flag only touches the default
                transport).
            transport (Optional[TokenEndpoint]):
                HTTP transport for the token endpoint. Defaults to :mod:`requests`. Unit
                tests inject a fake transport so no network is required.
            time_fn (Optional[Callable[[], float]]):
                Monotonic clock used for all expiry bookkeeping and the background-refresh
                schedule. Defaults to :func:`time.monotonic`; tests inject a controllable
                fake so the background thread is deterministic.
            random_fn (Optional[Callable[[], float]]):
                Source of a ``[0.0, 1.0)`` fraction used to jitter the backoff after a FAILED
                background refresh. Defaults to :func:`random.random`; consulted only on the
                failure path, so the healthy schedule is unaffected by it.
            stop_event (Optional[threading.Event]):
                Event the background thread waits on (interruptible sleep) and that
                :meth:`stop` signals. Defaults to a fresh :class:`threading.Event`; tests
                inject a controllable one to drive the loop without real sleeps.
            start_background_refresh (bool):
                Whether to spawn the background refresh thread after login. Defaults to
                ``True``; tests set it to ``False`` to drive the loop body directly.
            refresh_token (str):
                A Keycloak *offline* refresh token handed to this provider instead of a
                password. When non-empty the provider bootstraps with a
                ``grant_type=refresh_token`` exchange and **never sends a password grant**.
                Appended LAST on purpose: the parameter list is part of this class's public
                surface, and inserting mid-list would rebind an external positional caller's
                arguments without any test here noticing.

        Raises:
            KeycloakAuthenticationError:
                If the initial ROPC login -- or, on the handed-off-token path, the initial
                refresh -- is rejected by Keycloak.
        """
        self.keycloak_url: str = keycloak_url.rstrip("/")
        self.realm: str = realm
        self.client_id: str = client_id
        self.username: str = username
        self.password: str = password
        self.token_expiration_in_s: Optional[int] = token_expiration_in_s
        self.verify_ssl: bool = verify_ssl
        self._transport: TokenEndpoint = (
            transport if transport is not None else _RequestsTransport(verify_ssl=verify_ssl)
        )
        self._time_fn: Callable[[], float] = time_fn if time_fn is not None else time.monotonic
        # Jitter source for the background-refresh failure backoff; injectable so a test can make
        # the retry delay exact. Only ever consulted on the failure path.
        self._random_fn: Callable[[], float] = random_fn if random_fn is not None else random.random

        self._token_endpoint: str = _TOKEN_ENDPOINT_TEMPLATE.format(
            keycloak_url=self.keycloak_url,
            realm=self.realm,
        )

        self._access_token: str = ""
        self._refresh_token: str = refresh_token
        self._access_token_expires_at: float = 0.0
        self._login_deadline: Optional[float] = None

        # Serialises the lazy read-path refresh against the background-thread refresh.
        self._lock: threading.RLock = threading.RLock()
        # Signalled by stop(); also the interruptible sleep primitive for the refresh thread.
        self._stop_event: threading.Event = stop_event if stop_event is not None else threading.Event()
        self._refresh_thread: Optional[threading.Thread] = None
        # Refresh-failure bookkeeping shared by the lazy read path and the background thread, so
        # both honour ONE backoff: consecutive failed refreshes, and the monotonic time before
        # which no new refresh request is sent. Both are reset by the next successful refresh.
        self._consecutive_refresh_failures: int = 0
        self._next_refresh_attempt_at: float = 0.0

        if refresh_token:
            # Handed-off offline token: bootstrap with a refresh grant. Keycloak's brute-force
            # detection counts failed *logins*, so N processes refreshing the same offline token in
            # the same millisecond is not the burst the realm penalises, while N password grants is
            # (measured: 3/10 password grants accepted at 0 ms spacing, 10/10 refresh grants).
            self._refresh()
        else:
            self._login()
        self._arm_auto_refresh_deadline()

        if start_background_refresh:
            self._start_background_refresh()

    def __enter__(self) -> "KeycloakTokenProvider":
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

        Within the ``token_expiration_in_s`` window the token returned is valid for at least
        :data:`_EXPIRY_LEEWAY_S` more seconds, or, while a failed refresh is backing off, for
        whatever validity it has left. Once the token has expired and cannot be refreshed this
        raises instead of handing out a token the server would refuse.

        Returns:
            Tuple[str, str]:
                ``('authorization', 'Bearer <access_token>')``.

        Raises:
            KeycloakAuthenticationError:
                If the access token has expired and could not be refreshed.
        """
        with self._lock:
            self._refresh_if_within_window(now=self._time_fn())
            return ("authorization", f"Bearer {self._access_token}")

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

        Once interpreter finalization has begun the join is skipped: CPython >= 3.13 refuses it
        outright (:exc:`PythonFinalizationError`, a :exc:`RuntimeError` subclass), which on the
        :meth:`__del__` path surfaced as an "Exception ignored while calling deallocator"
        traceback on every process exit. The refresh thread is a daemon and is reaped by the
        interpreter regardless, so skipping the join costs nothing at shutdown.
        """
        self._stop_event.set()
        thread: Optional[threading.Thread] = self._refresh_thread
        # Never join from within the refresh thread itself (would deadlock); only an external
        # caller joins. A daemon thread that outlives this join is reaped at interpreter exit,
        # which is also why the join is skipped entirely once finalization is under way.
        if thread is not None and thread is not threading.current_thread() and not sys.is_finalizing():
            try:
                thread.join(timeout=_THREAD_JOIN_TIMEOUT_S)
            except RuntimeError:
                # Finalization can start between the guard above and the join. Catching
                # RuntimeError (the portable base of 3.13+'s PythonFinalizationError) keeps
                # that race from escaping into __del__, where it would only be printed.
                pass

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
        provider_ref: "weakref.ref[KeycloakTokenProvider]" = weakref.ref(self)
        thread: threading.Thread = threading.Thread(
            target=_refresh_loop,
            args=(provider_ref, self._stop_event, self._time_fn),
            name=f"keycloak-token-refresh-{self.client_id}",
            daemon=True,
        )
        self._refresh_thread = thread
        thread.start()

    def _refresh_if_within_window(self, now: float) -> None:
        """
        Refresh the access token if it is near expiry, refresh is permitted and not backing off.

        Shared by the lazy read path and the background thread; callers hold :attr:`_lock`.
        Does nothing once ``token_expiration_in_s`` has elapsed since login (the access token
        is then allowed to lapse). Within the window, refreshes via the offline refresh token
        whenever the current access token is within the leeway of its ``exp``.

        A failed refresh is recorded and backed off (:meth:`_record_refresh_failure`), and it is
        only RAISED once the current access token has actually expired: inside the leeway the
        token is still valid, so the call that triggered the refresh goes out with it rather than
        failing for a refresh it did not need yet. While the backoff runs no request is sent at
        all, so an outage never turns every gRPC call into a token request under this lock.

        Args:
            now (float):
                The current monotonic time, sampled by the caller from :attr:`_time_fn`.

        Raises:
            KeycloakAuthenticationError:
                If the access token has expired and it could not be refreshed, either because the
                refresh failed now or because a previous failure's backoff has not elapsed yet.
        """
        if self._login_deadline is not None and now >= self._login_deadline:
            # The auto-refresh window has closed: stop renewing and let the token lapse.
            return
        if now < self._access_token_expires_at - _EXPIRY_LEEWAY_S:
            # Current access token is still comfortably valid.
            return
        if now < self._next_refresh_attempt_at:
            # A previous refresh failed and its backoff has not elapsed: send nothing.
            if now < self._access_token_expires_at:
                return
            raise KeycloakAuthenticationError(
                f"The Keycloak access token has expired and the refresh is backing off after "
                f"{self._consecutive_refresh_failures} consecutive failure(s); the next attempt is due in "
                f"{self._next_refresh_attempt_at - now:.1f}s"
            )
        try:
            self._refresh()
        except Exception as exception:
            self._record_refresh_failure(exception=exception)
            # Re-read the clock: the failed attempt may itself have taken up to _HTTP_TIMEOUT_S.
            if self._time_fn() < self._access_token_expires_at:
                # Still valid (inside the leeway): serve it, the backoff schedules the retry.
                return
            if isinstance(exception, KeycloakAuthenticationError):
                raise
            raise KeycloakAuthenticationError(
                f"Keycloak token refresh failed ({type(exception).__name__}: {exception})"
            ) from exception
        self._record_refresh_success()

    def _record_refresh_failure(self, exception: BaseException) -> None:
        """
        Count a failed refresh, schedule the next attempt with jittered backoff and log it.

        Deliberately NOT a fallback to a password grant: a refused offline token keeps being
        refused, the lazy read path raises once the access token has expired, and a caller can
        build a new provider. A silent re-login would reintroduce, at the least predictable moment
        (a realm restart invalidates every offline session at once), the login burst the offline
        token exists to avoid. Callers hold :attr:`_lock`.

        The backoff is measured from the moment the failure is RECORDED, not from when the attempt
        started: an attempt that hung for the whole :data:`_HTTP_TIMEOUT_S` would otherwise schedule
        a retry that is already due, and the outage would be polled at the 1 s floor after all.

        Args:
            exception (BaseException):
                What the attempt raised; only its type and message are logged.
        """
        now: float = self._time_fn()
        self._consecutive_refresh_failures += 1
        delay_s: float = _backoff_delay_s(self._consecutive_refresh_failures, self._random_fn)
        self._next_refresh_attempt_at = now + delay_s
        remaining_s: float = self._access_token_expires_at - now
        validity: str = (
            f"the current access token stays valid for {remaining_s:.1f}s"
            if remaining_s > 0
            else "the current access token has expired"
        )
        logger.warning(
            f"Keycloak token refresh failed (attempt {self._consecutive_refresh_failures}); retrying in "
            f"{delay_s:.1f}s, {validity} ({type(exception).__name__}: {exception})"
        )

    def _record_refresh_success(self) -> None:
        """Reset the failure backoff after a successful refresh and log the recovery, if any."""
        if self._consecutive_refresh_failures > 0:
            logger.info(
                f"Keycloak token refresh recovered after {self._consecutive_refresh_failures} failed attempt(s)"
            )
        self._consecutive_refresh_failures = 0
        self._next_refresh_attempt_at = 0.0

    def _login(self) -> None:
        """
        Perform the one-time ROPC login (``grant_type=password`` + ``offline_access``).

        Raises:
            KeycloakAuthenticationError:
                If Keycloak rejects the credentials.
        """
        data: Dict[str, str] = {
            "grant_type": "password",
            "client_id": self.client_id,
            "username": self.username,
            "password": self.password,
            "scope": "offline_access",
        }
        payload: Dict[str, Any] = self._post_token_request(data=data, action="login")
        self._store_tokens(payload=payload)

    def _arm_auto_refresh_deadline(self) -> None:
        """
        Start the ``token_expiration_in_s`` window that bounds the auto-refresh loop.

        Called from ``__init__`` after the initial token acquisition, whichever credential
        produced it. Arming it here rather than inside :meth:`_login` is what makes the bound
        mean the same thing on the handed-off-token path: a provider built from an offline
        token would otherwise refresh for ever while its config asked for a bounded window.
        """
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
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": self._refresh_token,
        }
        payload: Dict[str, Any] = self._post_token_request(data=data, action="refresh")
        self._store_tokens(payload=payload)

    def _post_token_request(self, data: Dict[str, str], action: str) -> Dict[str, Any]:
        """
        POST a form-encoded request to the token endpoint and return the parsed body.

        Every way the exchange can fail surfaces as :class:`KeycloakAuthenticationError`, with the
        original exception chained: a network error (refused connection, DNS failure, timeout), a
        non-2xx status, a body that is not JSON and a JSON body that is not an object. Callers then
        handle ONE exception type, and a proxy's HTML error page cannot escape as a ``ValueError``.

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
                If the endpoint cannot be reached, answers a non-2xx status or an unusable body.
        """
        try:
            response: TokenResponse = self._transport.post(
                self._token_endpoint,
                data=data,
                timeout=_HTTP_TIMEOUT_S,
            )
        except OSError as exception:
            # requests' ConnectionError / Timeout derive from OSError, as do raw socket errors.
            raise KeycloakAuthenticationError(
                f"Keycloak token {action} could not reach the token endpoint ({type(exception).__name__}: {exception})"
            ) from exception
        if response.status_code < 200 or response.status_code >= 300:
            raise KeycloakAuthenticationError(
                f"Keycloak token {action} failed with status {response.status_code}: "
                f"{response.text[:_MAX_ERROR_BODY_CHARS]}"
            )
        try:
            body: Any = response.json()
        except ValueError as exception:
            raise KeycloakAuthenticationError(
                f"Keycloak token {action} returned status {response.status_code} with a body that is not JSON"
            ) from exception
        if not isinstance(body, dict):
            raise KeycloakAuthenticationError(
                f"Keycloak token {action} returned a JSON {type(body).__name__} instead of an object"
            )
        return body

    def _store_tokens(self, payload: Dict[str, Any]) -> None:
        """
        Store the access token, refresh token, and the computed expiry from a token response.

        Args:
            payload (Dict[str, Any]):
                The parsed token endpoint response.

        Raises:
            KeycloakAuthenticationError:
                If the response carries no usable ``access_token`` or a non-numeric ``expires_in``.
        """
        access_token: Any = payload.get("access_token", "")
        if not access_token or not isinstance(access_token, str):
            # Report the field NAMES, never the values. A Keycloak token response is made almost
            # entirely of credentials -- an offline ``refresh_token`` mints access tokens for the
            # life of the offline session -- and rendering the body here wrote them into whatever
            # log, traceback or archived CI report this exception reached. The names are what makes
            # the failure diagnosable ("the body came back without an access_token, carrying
            # refresh_token and expires_in"); the values add nothing to that and cannot be unsent.
            raise KeycloakAuthenticationError(
                "Keycloak token response did not contain an access_token; the response carried "
                f"the fields {sorted(payload)} (values withheld: a token response is credential material)"
            )
        try:
            expires_in: float = float(payload.get("expires_in", 0))
        except (TypeError, ValueError) as exception:
            raise KeycloakAuthenticationError(
                "Keycloak token response carried a non-numeric expires_in (value withheld)"
            ) from exception
        # Validate everything BEFORE assigning anything, so a malformed response never leaves the
        # provider holding a new access token paired with the previous one's expiry.
        self._access_token = access_token
        # Keycloak always re-issues the refresh token; keep the previous one if absent so a
        # response that omits it (e.g. a same-token refresh) does not blank out the offline token.
        refresh_token: Any = payload.get("refresh_token", "")
        if refresh_token and isinstance(refresh_token, str):
            self._refresh_token = refresh_token
        self._access_token_expires_at = self._time_fn() + max(expires_in, 0.0)


# One shared provider per set of Keycloak credentials so the ROPC offline-token login happens
# once for all of a client's service stubs (they all read the same auto-refreshed access token).
# The weak reference lets the provider be collected once the last stub holding it is gone.
#
# The key MUST be derived from the credentials, never from `id(config)`. `BaseServicesInterface`
# keeps only the grpc channel, so the `ClientConfig` in the usual `Client(config=ClientConfig(...))`
# call is unreachable the moment the client is built; CPython then reuses its address for the next
# `ClientConfig`, and a registry keyed by that stale int handed the new client the PREVIOUS user's
# still-alive provider. The second client then silently authenticated as the first user — including
# with credentials that do not exist at all.
_PROVIDER_REGISTRY: "WeakValueDictionary[str, KeycloakTokenProvider]" = WeakValueDictionary()
_PROVIDER_REGISTRY_LOCK: threading.Lock = threading.Lock()


def _provider_registry_key(config: ClientConfig) -> str:
    """
    Derive the registry key identifying the Keycloak identity a config authenticates as.

    Every field the provider is constructed from takes part, so two configs share a provider
    exactly when a shared provider would behave identically for both. The fields are hashed
    rather than stored verbatim because two of them are secrets -- the password and the offline
    refresh token: a plain tuple key would put them in a module-level dict and in the locals of
    this frame, where any traceback renderer that shows locals would print them.

    ``refresh_token`` is not optional here even though it looks like an afterthought. A config
    authenticating with a handed-off offline token carries an EMPTY password, so the field that
    otherwise discriminates two credentials degenerates to ``""`` for every one of them, and two
    tenants' configs would collapse onto one provider -- one project's processes silently
    authenticating as another's.

    Args:
        config (ClientConfig):
            A config with the Keycloak headless-auth fields set (`config.use_keycloak`).

    Returns:
        str:
            A hex digest identifying the credential set.
    """
    fields: List[str] = [
        config.keycloak_url,
        config.realm,
        config.client_id,
        config.user_name,
        config.password,
        "" if config.token_expiration_in_s is None else str(config.token_expiration_in_s),
        str(config.keycloak_verify_ssl),
        config.refresh_token,
    ]
    # "\0" cannot occur in any of the fields, so the join is unambiguous.
    return hashlib.sha256("\0".join(fields).encode("utf-8")).hexdigest()


def get_keycloak_token_provider(config: ClientConfig) -> KeycloakTokenProvider:
    """
    Return the shared :class:`KeycloakTokenProvider` for a client config, creating it once.

    All service stubs built from the same credentials share a single provider, so the one-time
    ROPC offline-token login runs once and every stub reads the same auto-refreshed access token.
    Configs carrying *different* credentials never share a provider.

    Args:
        config (ClientConfig):
            A config with the Keycloak headless-auth fields set (`config.use_keycloak`).

    Returns:
        KeycloakTokenProvider:
            The provider bound to this config's credentials (created on first call).
    """
    key: str = _provider_registry_key(config)
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
                verify_ssl=config.keycloak_verify_ssl,
                refresh_token=config.refresh_token,
            )
            _PROVIDER_REGISTRY[key] = provider
        return provider
