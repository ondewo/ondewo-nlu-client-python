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
   it expires and attaches it as the standard ``Authorization: Bearer`` metadata.
3. The auto-refresh loop stops once ``token_expiration_in_s`` has elapsed since login
   (omit it to keep refreshing until the offline session itself expires).

No 2FA is involved: the account is a 2FA-exempt technical user and ROPC bypasses the
browser flow (D14). The client is public, so no ``client_secret`` is sent.
"""
import threading
import time
from typing import (
    Any,
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

# HTTP timeout for the (single, fast) token-endpoint calls.
_HTTP_TIMEOUT_S: float = 30.0


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


class KeycloakTokenProvider:
    """
    Acquire and auto-refresh a Keycloak access token for the headless SDK (D18).

    The provider performs a one-time ROPC login with ``scope=offline_access`` against a
    public Keycloak client and then refreshes the access token on demand from the offline
    refresh token. Reading :meth:`authorization_metadata` (or :meth:`bearer_metadata`) lazily
    refreshes the token whenever it is within :data:`_EXPIRY_LEEWAY_S` of expiry, so every
    outgoing gRPC call carries a fresh ``Authorization: Bearer`` value without a background
    thread. Once ``token_expiration_in_s`` has elapsed since login the refresh stops and the
    access token is allowed to lapse (re-login required).

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
    ) -> None:
        """
        Initialize the provider and acquire the offline token immediately.

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

        self._token_endpoint: str = _TOKEN_ENDPOINT_TEMPLATE.format(
            keycloak_url=self.keycloak_url,
            realm=self.realm,
        )

        self._access_token: str = ''
        self._refresh_token: str = ''
        self._access_token_expires_at: float = 0.0
        self._login_deadline: Optional[float] = None

        self._login()

    @property
    def access_token(self) -> str:
        """The most recently issued access token (refreshed lazily on metadata reads)."""
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
        self._ensure_fresh_access_token()
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

    def _ensure_fresh_access_token(self) -> None:
        """
        Refresh the access token if it is near expiry and refresh is still permitted.

        Does nothing once ``token_expiration_in_s`` has elapsed since login (the access
        token is then allowed to lapse). Within the window, refreshes via the offline
        refresh token whenever the current access token is within the leeway of its ``exp``.
        """
        now: float = time.monotonic()
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
            self._login_deadline = time.monotonic() + self.token_expiration_in_s

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
        self._access_token_expires_at = time.monotonic() + expires_in


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
