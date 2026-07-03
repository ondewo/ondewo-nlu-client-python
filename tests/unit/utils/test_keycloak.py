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
"""Hermetic unit tests for the D18 Keycloak headless offline-token helper.

No network is touched: a fake HTTP transport captures the token-endpoint requests and
returns queued fake responses, and the module clock is monkeypatched to drive expiry.
The proactive background-refresh thread is driven deterministically via an injected clock
and a controllable stop event — no real sleeps, so the suite stays fast and non-flaky.
"""
import gc
import threading
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)

import pytest

from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.utils import keycloak as keycloak_module
from ondewo.nlu.utils.keycloak import (
    _EXPIRY_LEEWAY_S,
    _HTTP_TIMEOUT_S,
    _MIN_REFRESH_DELAY_S,
    _refresh_loop,
    _RequestsTransport,
    KeycloakAuthenticationError,
    KeycloakTokenProvider,
    get_keycloak_token_provider,
)

# Bound exactly once so a refactor that changes only an input or only an expectation cannot
# silently make a test tautological.
KEYCLOAK_URL: str = 'https://kc.example.com/auth'
REALM: str = 'ondewo-ccai-platform'
CLIENT_ID: str = 'ondewo-nlu-cai-sdk-public'
USERNAME: str = 'tech-user@example.com'
PASSWORD: str = 's3cr3t'
EXPECTED_TOKEN_ENDPOINT: str = (
    'https://kc.example.com/auth/realms/ondewo-ccai-platform/protocol/openid-connect/token'
)


class FakeResponse:
    """Minimal `requests.Response` stand-in satisfying the `TokenResponse` Protocol."""

    def __init__(self, status_code: int, body: Dict[str, Any]) -> None:
        """Store the canned HTTP status code and JSON body.

        Args:
            status_code (int):
                The HTTP status code the provider sees on `response.status_code`.
            body (Dict[str, Any]):
                The JSON body returned by `json()` and reflected in `text`.
        """
        self.status_code: int = status_code
        self._body: Dict[str, Any] = body

    def json(self) -> Dict[str, Any]:
        """Return the canned JSON body.

        Returns:
            Dict[str, Any]:
                The stored response body.
        """
        return self._body

    @property
    def text(self) -> str:
        """Return the raw body representation used in error messages.

        Returns:
            str:
                `repr()` of the stored body.
        """
        return repr(self._body)


class FakeTransport:
    """Fake token endpoint: records every POST and replays queued responses in order."""

    def __init__(self, responses: List[FakeResponse]) -> None:
        """Queue the responses to replay and initialise the recorded-call log.

        Args:
            responses (List[FakeResponse]):
                Responses returned by successive `post()` calls, in order.
        """
        self._responses: List[FakeResponse] = list(responses)
        self.calls: List[Dict[str, str]] = []

    def post(self, url: str, data: Dict[str, str], timeout: float) -> FakeResponse:
        """Record the POST and return the next queued response.

        Args:
            url (str):
                The token-endpoint URL the provider posted to.
            data (Dict[str, str]):
                The form-encoded request parameters.
            timeout (float):
                The request timeout (recorded only via the call log shape, unused here).

        Returns:
            FakeResponse:
                The next queued response.

        Raises:
            AssertionError:
                If more POSTs are made than responses were queued.
        """
        self.calls.append({'url': url, **data})
        if not self._responses:
            raise AssertionError('FakeTransport received more POSTs than queued responses')
        return self._responses.pop(0)


def _token_body(access_token: str, refresh_token: str, expires_in: int) -> Dict[str, Any]:
    """Build a Keycloak-shaped token-endpoint JSON body.

    Args:
        access_token (str):
            The `access_token` field value.
        refresh_token (str):
            The `refresh_token` field value.
        expires_in (int):
            The access-token lifetime in seconds.

    Returns:
        Dict[str, Any]:
            A token response body with access/refresh tokens, lifetime, and `token_type`.
    """
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_in': expires_in,
        'token_type': 'Bearer',
    }


def _build_provider(
    transport: FakeTransport,
    token_expiration_in_s: int | None = None,
) -> KeycloakTokenProvider:
    """Construct a `KeycloakTokenProvider` wired to the fake transport and shared test fixtures.

    The proactive background-refresh thread is disabled (`start_background_refresh=False`) so
    the lazy read-path assertions on exact `transport.calls` counts stay deterministic; the
    background loop is covered explicitly in `TestBackgroundRefresh` by driving `_refresh_loop`.

    Args:
        transport (FakeTransport):
            The fake token endpoint backing the provider.
        token_expiration_in_s (int | None):
            Optional upper bound on auto-refresh; `None` keeps refreshing unbounded.

    Returns:
        KeycloakTokenProvider:
            A provider that has already performed its one-time ROPC login via `transport`.
    """
    return KeycloakTokenProvider(
        keycloak_url=KEYCLOAK_URL,
        realm=REALM,
        client_id=CLIENT_ID,
        username=USERNAME,
        password=PASSWORD,
        token_expiration_in_s=token_expiration_in_s,
        transport=transport,
        start_background_refresh=False,
    )


class TestLogin:
    """The one-time ROPC offline-token login and the metadata it produces."""

    def test_ropc_login_sends_offline_access_scope_and_no_secret(self) -> None:
        """Login posts grant_type=password with offline_access scope and no client_secret (Q1)."""
        transport: FakeTransport = FakeTransport([FakeResponse(200, _token_body('acc-1', 'off-1', 300))])

        provider: KeycloakTokenProvider = _build_provider(transport)

        assert provider.access_token == 'acc-1'
        assert len(transport.calls) == 1
        login_call: Dict[str, str] = transport.calls[0]
        assert login_call['url'] == EXPECTED_TOKEN_ENDPOINT
        assert login_call['grant_type'] == 'password'
        assert login_call['client_id'] == CLIENT_ID
        assert login_call['username'] == USERNAME
        assert login_call['password'] == PASSWORD
        assert login_call['scope'] == 'offline_access'
        # Q1: public client — never send a client_secret.
        assert 'client_secret' not in login_call

    def test_authorization_metadata_is_bearer(self) -> None:
        """`authorization_metadata()` returns the `('Authorization', 'Bearer <token>')` tuple."""
        transport: FakeTransport = FakeTransport([FakeResponse(200, _token_body('acc-1', 'off-1', 300))])

        provider: KeycloakTokenProvider = _build_provider(transport)

        key, value = provider.authorization_metadata()
        assert key == 'Authorization'
        assert value == 'Bearer acc-1'

    def test_bearer_metadata_shape(self) -> None:
        """`bearer_metadata()` wraps the authorization tuple in a single-element list."""
        transport: FakeTransport = FakeTransport([FakeResponse(200, _token_body('acc-1', 'off-1', 300))])

        provider: KeycloakTokenProvider = _build_provider(transport)

        metadata: List[Tuple[str, str]] = provider.bearer_metadata()
        assert metadata == [('Authorization', 'Bearer acc-1')]

    def test_login_failure_raises(self) -> None:
        """A non-2xx login response raises `KeycloakAuthenticationError`."""
        transport: FakeTransport = FakeTransport([FakeResponse(401, {'error': 'invalid_grant'})])

        with pytest.raises(KeycloakAuthenticationError):
            _build_provider(transport)

    def test_missing_access_token_raises(self) -> None:
        """A 2xx response that omits `access_token` raises `KeycloakAuthenticationError`."""
        transport: FakeTransport = FakeTransport([FakeResponse(200, {'refresh_token': 'off-1', 'expires_in': 300})])

        with pytest.raises(KeycloakAuthenticationError):
            _build_provider(transport)


class TestRefresh:
    """Lazy access-token refresh driven by the monkeypatched module clock."""

    def test_refresh_uses_offline_refresh_token(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Past expiry, the next metadata read refreshes via grant_type=refresh_token (no secret).

        Args:
            monkeypatch (pytest.MonkeyPatch):
                Fixture used to replace the module clock with a controllable fake.
        """
        clock: Dict[str, float] = {'now': 1000.0}
        monkeypatch.setattr(keycloak_module.time, 'monotonic', lambda: clock['now'])

        transport: FakeTransport = FakeTransport([
            FakeResponse(200, _token_body('acc-1', 'off-1', 300)),
            FakeResponse(200, _token_body('acc-2', 'off-2', 300)),
        ])
        provider: KeycloakTokenProvider = _build_provider(transport)

        # Advance the clock past the access-token lifetime so the next read refreshes.
        clock['now'] = 1000.0 + 300.0
        _, value = provider.authorization_metadata()

        assert value == 'Bearer acc-2'
        assert len(transport.calls) == 2
        refresh_call: Dict[str, str] = transport.calls[1]
        assert refresh_call['grant_type'] == 'refresh_token'
        assert refresh_call['client_id'] == CLIENT_ID
        assert refresh_call['refresh_token'] == 'off-1'
        assert 'client_secret' not in refresh_call

    def test_no_refresh_while_token_still_valid(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Repeated reads inside the validity window do not trigger any extra HTTP call.

        Args:
            monkeypatch (pytest.MonkeyPatch):
                Fixture used to replace the module clock with a controllable fake.
        """
        clock: Dict[str, float] = {'now': 1000.0}
        monkeypatch.setattr(keycloak_module.time, 'monotonic', lambda: clock['now'])

        transport: FakeTransport = FakeTransport([FakeResponse(200, _token_body('acc-1', 'off-1', 300))])
        provider: KeycloakTokenProvider = _build_provider(transport)

        # Read several times well inside the validity window: still exactly one HTTP call.
        clock['now'] = 1000.0 + 100.0
        provider.authorization_metadata()
        provider.authorization_metadata()

        assert len(transport.calls) == 1

    def test_refresh_keeps_previous_offline_token_when_omitted(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """A refresh response without a refresh_token reuses the prior offline token.

        Args:
            monkeypatch (pytest.MonkeyPatch):
                Fixture used to replace the module clock with a controllable fake.
        """
        clock: Dict[str, float] = {'now': 1000.0}
        monkeypatch.setattr(keycloak_module.time, 'monotonic', lambda: clock['now'])

        transport: FakeTransport = FakeTransport([
            FakeResponse(200, _token_body('acc-1', 'off-1', 300)),
            # A refresh response that omits refresh_token — provider keeps the old one.
            FakeResponse(200, {'access_token': 'acc-2', 'expires_in': 300}),
            FakeResponse(200, _token_body('acc-3', 'off-3', 300)),
        ])
        provider: KeycloakTokenProvider = _build_provider(transport)

        clock['now'] = 1000.0 + 300.0
        provider.authorization_metadata()  # refresh #1 → acc-2, no new offline token
        clock['now'] = 1000.0 + 600.0
        provider.authorization_metadata()  # refresh #2 → must still use off-1

        assert transport.calls[2]['refresh_token'] == 'off-1'


class TestTokenExpirationBound:
    """The `token_expiration_in_s` upper bound on how long auto-refresh keeps running."""

    def test_refresh_stops_after_token_expiration_in_s(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Refresh runs inside the window but stops (serving the stale token) once it elapses.

        Args:
            monkeypatch (pytest.MonkeyPatch):
                Fixture used to replace the module clock with a controllable fake.
        """
        clock: Dict[str, float] = {'now': 1000.0}
        monkeypatch.setattr(keycloak_module.time, 'monotonic', lambda: clock['now'])

        token_expiration_in_s: int = 600
        transport: FakeTransport = FakeTransport([
            FakeResponse(200, _token_body('acc-1', 'off-1', 300)),
            FakeResponse(200, _token_body('acc-2', 'off-2', 300)),
        ])
        provider: KeycloakTokenProvider = _build_provider(transport, token_expiration_in_s=token_expiration_in_s)

        # First refresh (at +300s) is still within the 600s window → happens.
        clock['now'] = 1000.0 + 300.0
        _, value_in_window = provider.authorization_metadata()
        assert value_in_window == 'Bearer acc-2'
        assert len(transport.calls) == 2

        # Past the 600s bound: refresh must stop; the stale token is returned, no HTTP call.
        clock['now'] = 1000.0 + token_expiration_in_s + 1.0
        _, value_after_bound = provider.authorization_metadata()
        assert value_after_bound == 'Bearer acc-2'
        assert len(transport.calls) == 2

    def test_unbounded_keeps_refreshing(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """With token_expiration_in_s=None the provider keeps refreshing on every expiry.

        Args:
            monkeypatch (pytest.MonkeyPatch):
                Fixture used to replace the module clock with a controllable fake.
        """
        clock: Dict[str, float] = {'now': 1000.0}
        monkeypatch.setattr(keycloak_module.time, 'monotonic', lambda: clock['now'])

        transport: FakeTransport = FakeTransport([
            FakeResponse(200, _token_body('acc-1', 'off-1', 300)),
            FakeResponse(200, _token_body('acc-2', 'off-2', 300)),
            FakeResponse(200, _token_body('acc-3', 'off-3', 300)),
        ])
        provider: KeycloakTokenProvider = _build_provider(transport, token_expiration_in_s=None)

        clock['now'] = 1000.0 + 300.0
        provider.authorization_metadata()
        clock['now'] = 1000.0 + 600.0
        _, value = provider.authorization_metadata()

        assert value == 'Bearer acc-3'
        assert len(transport.calls) == 3

    def test_refresh_failure_after_login_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A rejected refresh (after a successful login) raises `KeycloakAuthenticationError`.

        Args:
            monkeypatch (pytest.MonkeyPatch):
                Fixture used to replace the module clock with a controllable fake.
        """
        clock: Dict[str, float] = {'now': 1000.0}
        monkeypatch.setattr(keycloak_module.time, 'monotonic', lambda: clock['now'])

        transport: FakeTransport = FakeTransport([
            FakeResponse(200, _token_body('acc-1', 'off-1', 300)),
            FakeResponse(400, {'error': 'invalid_grant'}),
        ])
        provider: KeycloakTokenProvider = _build_provider(transport)

        clock['now'] = 1000.0 + 300.0
        with pytest.raises(KeycloakAuthenticationError):
            provider.authorization_metadata()


class TestSharedProviderRegistry:
    """The per-`ClientConfig` shared-provider factory `get_keycloak_token_provider`."""

    def test_same_config_returns_same_provider(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Two factory calls for one config return the same provider and log in only once.

        Args:
            monkeypatch (pytest.MonkeyPatch):
                Fixture used to patch `requests.post` so the default transport hits no network.
        """
        # Drive the default transport (requests) through a fake so no network is hit.
        post_calls: List[Dict[str, str]] = []

        def fake_post(url: str, data: Dict[str, str], timeout: float) -> FakeResponse:
            """Record the POST and return a canned successful login response.

            Args:
                url (str):
                    The token-endpoint URL.
                data (Dict[str, str]):
                    The form-encoded request parameters.
                timeout (float):
                    The request timeout (unused).

            Returns:
                FakeResponse:
                    A 200 response carrying access/refresh tokens.
            """
            post_calls.append({'url': url, **data})
            return FakeResponse(200, _token_body('acc-1', 'off-1', 300))

        monkeypatch.setattr(keycloak_module.requests, 'post', fake_post)

        config: ClientConfig = ClientConfig(
            host='localhost',
            port='50055',
            user_name=USERNAME,
            password=PASSWORD,
            keycloak_url=KEYCLOAK_URL,
            realm=REALM,
            client_id=CLIENT_ID,
        )
        first: KeycloakTokenProvider = get_keycloak_token_provider(config)
        second: KeycloakTokenProvider = get_keycloak_token_provider(config)

        assert first is second
        # Login happened exactly once despite two factory calls.
        assert len(post_calls) == 1

    def test_factory_forwards_token_expiration_in_s(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """The factory threads `token_expiration_in_s` from the config into the provider.

        Args:
            monkeypatch (pytest.MonkeyPatch):
                Fixture used to patch the module clock and `requests.post`.
        """
        # The factory must thread `token_expiration_in_s` from the config into the provider so
        # the auto-refresh bound is honoured; otherwise a refresh would run past the deadline.
        clock: Dict[str, float] = {'now': 1000.0}
        monkeypatch.setattr(keycloak_module.time, 'monotonic', lambda: clock['now'])

        token_expiration_in_s: int = 600

        def fake_post(url: str, data: Dict[str, str], timeout: float) -> FakeResponse:
            """Return a canned successful login response.

            Args:
                url (str):
                    The token-endpoint URL (unused).
                data (Dict[str, str]):
                    The form-encoded request parameters (unused).
                timeout (float):
                    The request timeout (unused).

            Returns:
                FakeResponse:
                    A 200 response carrying access/refresh tokens.
            """
            return FakeResponse(200, _token_body('acc-1', 'off-1', 300))

        monkeypatch.setattr(keycloak_module.requests, 'post', fake_post)

        config: ClientConfig = ClientConfig(
            host='localhost',
            port='50055',
            user_name=USERNAME,
            password=PASSWORD,
            keycloak_url=KEYCLOAK_URL,
            realm=REALM,
            client_id=CLIENT_ID,
            token_expiration_in_s=token_expiration_in_s,
        )
        provider: KeycloakTokenProvider = get_keycloak_token_provider(config)

        assert provider.token_expiration_in_s == token_expiration_in_s


class TestDefaultRequestsTransport:
    """The default `_RequestsTransport` used when no transport is injected (production path)."""

    def test_provider_uses_requests_transport_by_default(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """With no injected transport the provider falls back to the requests-backed transport.

        Args:
            monkeypatch (pytest.MonkeyPatch):
                Fixture used to patch `requests.post` so no network is touched.
        """
        # When no transport is injected the provider must fall back to the real requests-backed
        # transport (the production path); patch requests.post so no network is touched.
        post_calls: List[Dict[str, str]] = []

        def fake_post(url: str, data: Dict[str, str], timeout: float) -> FakeResponse:
            """Record the POST and return a canned successful login response.

            Args:
                url (str):
                    The token-endpoint URL.
                data (Dict[str, str]):
                    The form-encoded request parameters.
                timeout (float):
                    The request timeout (unused).

            Returns:
                FakeResponse:
                    A 200 response carrying access/refresh tokens.
            """
            post_calls.append({'url': url, **data})
            return FakeResponse(200, _token_body('acc-1', 'off-1', 300))

        monkeypatch.setattr(keycloak_module.requests, 'post', fake_post)

        provider: KeycloakTokenProvider = KeycloakTokenProvider(
            keycloak_url=KEYCLOAK_URL,
            realm=REALM,
            client_id=CLIENT_ID,
            username=USERNAME,
            password=PASSWORD,
        )

        assert isinstance(provider._transport, _RequestsTransport)
        assert provider.access_token == 'acc-1'
        assert len(post_calls) == 1
        assert post_calls[0]['url'] == EXPECTED_TOKEN_ENDPOINT

    def test_requests_transport_forwards_url_data_and_timeout(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """`_RequestsTransport.post` forwards url/data verbatim and the module HTTP timeout.

        Args:
            monkeypatch (pytest.MonkeyPatch):
                Fixture used to patch `requests.post` and capture its arguments.
        """
        # _RequestsTransport.post must pass through url/data verbatim and the module HTTP timeout.
        captured: Dict[str, Any] = {}

        def fake_post(url: str, data: Dict[str, str], timeout: float) -> FakeResponse:
            """Capture the forwarded arguments and return a canned response.

            Args:
                url (str):
                    The token-endpoint URL.
                data (Dict[str, str]):
                    The form-encoded request parameters.
                timeout (float):
                    The request timeout.

            Returns:
                FakeResponse:
                    A 200 response carrying access/refresh tokens.
            """
            captured['url'] = url
            captured['data'] = data
            captured['timeout'] = timeout
            return FakeResponse(200, _token_body('acc-1', 'off-1', 300))

        monkeypatch.setattr(keycloak_module.requests, 'post', fake_post)

        transport: _RequestsTransport = _RequestsTransport()
        form_data: Dict[str, str] = {'grant_type': 'password'}
        # `_RequestsTransport.post` is statically typed to return `requests.Response`; let mypy
        # infer that declared type rather than the fake the patched `requests.post` actually yields.
        response = transport.post(EXPECTED_TOKEN_ENDPOINT, data=form_data, timeout=_HTTP_TIMEOUT_S)

        assert response.status_code == 200
        assert captured['url'] == EXPECTED_TOKEN_ENDPOINT
        assert captured['data'] == form_data
        assert captured['timeout'] == _HTTP_TIMEOUT_S


class TestStoreTokensExpiry:
    """The `expires_in`-driven expiry bookkeeping in `_store_tokens`."""

    def test_missing_expires_in_defaults_to_zero_and_forces_refresh(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """A response without `expires_in` is treated as already expired, forcing the next refresh.

        Args:
            monkeypatch (pytest.MonkeyPatch):
                Fixture used to replace the module clock with a controllable fake.
        """
        # A token response without `expires_in` is treated as already at expiry (0s), so the very
        # next metadata read must refresh rather than serve a token with an unknown lifetime.
        clock: Dict[str, float] = {'now': 1000.0}
        monkeypatch.setattr(keycloak_module.time, 'monotonic', lambda: clock['now'])

        transport: FakeTransport = FakeTransport([
            FakeResponse(200, {'access_token': 'acc-1', 'refresh_token': 'off-1'}),
            FakeResponse(200, _token_body('acc-2', 'off-2', 300)),
        ])
        provider: KeycloakTokenProvider = _build_provider(transport)

        # Clock has not advanced, but expires_at == login time (expires_in defaulted to 0), so the
        # leeway check fires immediately and the next read refreshes.
        _, value = provider.authorization_metadata()

        assert value == 'Bearer acc-2'
        assert len(transport.calls) == 2


class ScriptedEvent:
    """A `threading.Event` stand-in that drives `_refresh_loop` deterministically.

    `wait(timeout)` records each requested delay and replays a queued list of return values
    (`True` = stop fired during the sleep, `False` = the sleep timed out → trigger a refresh).
    Once the script is exhausted it returns `True`, terminating the loop so a test never spins
    or sleeps for real. A `clock` and optional per-step advances let `wait` move the injected
    monotonic clock forward exactly as a real timed wait would.
    """

    def __init__(
        self,
        wait_returns: List[bool],
        clock: Dict[str, float],
        advance_by: Optional[List[float]] = None,
    ) -> None:
        """Queue the scripted `wait` results and bind the controllable clock.

        Args:
            wait_returns (List[bool]):
                Successive return values for `wait()`: `True` simulates `stop()` firing during
                the sleep, `False` simulates a timeout that should drive a refresh.
            clock (Dict[str, float]):
                The shared mutable clock (`{'now': <seconds>}`) the injected `time_fn` reads.
            advance_by (Optional[List[float]]):
                Optional per-`wait` clock advances (seconds); when shorter than the requested
                delay this models a `stop()` that interrupts the sleep early. Defaults to
                advancing by exactly the requested delay each call.
        """
        self._wait_returns: List[bool] = list(wait_returns)
        self._clock: Dict[str, float] = clock
        self._advance_by: Optional[List[float]] = list(advance_by) if advance_by is not None else None
        self._set: bool = False
        self.wait_delays: List[float] = []

    def is_set(self) -> bool:
        """Return whether the event has been set (mirrors `threading.Event.is_set`).

        Returns:
            bool:
                `True` once `set()` has been called.
        """
        return self._set

    def set(self) -> None:
        """Mark the event as set (mirrors `threading.Event.set`)."""
        self._set = True

    def wait(self, timeout: Optional[float] = None) -> bool:
        """Record the requested delay, advance the clock, and replay the next scripted result.

        Args:
            timeout (Optional[float]):
                The delay the loop asked to sleep for; recorded in `wait_delays`.

        Returns:
            bool:
                The next queued return value (`True` = stopped, `False` = timed out); `True`
                once the script is exhausted so the loop terminates.
        """
        self.wait_delays.append(float(timeout if timeout is not None else 0.0))
        if self._advance_by is not None and self._advance_by:
            self._clock['now'] += self._advance_by.pop(0)
        elif timeout is not None:
            self._clock['now'] += timeout
        if not self._wait_returns:
            self._set = True
            return True
        result: bool = self._wait_returns.pop(0)
        if result:
            self._set = True
        return result


def _weak(obj: KeycloakTokenProvider) -> 'Any':
    """Return a weak reference to a provider (a thin, typed wrapper around `weakref.ref`).

    Args:
        obj (KeycloakTokenProvider):
            The provider to weakly reference.

    Returns:
        Any:
            A weak reference whose deref yields the provider while it is alive, else `None`.
    """
    import weakref

    return weakref.ref(obj)


def _build_background_provider(
    transport: FakeTransport,
    clock: Dict[str, float],
    stop_event: ScriptedEvent,
    token_expiration_in_s: int | None = None,
) -> KeycloakTokenProvider:
    """Construct a provider wired to an injected clock + scripted event, background thread off.

    The background thread is not started here; tests call `_refresh_loop` directly with the
    scripted event so the loop body runs deterministically without a real thread or sleeps.

    Args:
        transport (FakeTransport):
            The fake token endpoint backing the provider.
        clock (Dict[str, float]):
            The shared mutable monotonic clock (`{'now': <seconds>}`).
        stop_event (ScriptedEvent):
            The scripted event driving `wait()`/`is_set()` in the loop.
        token_expiration_in_s (int | None):
            Optional upper bound on auto-refresh; `None` keeps refreshing unbounded.

    Returns:
        KeycloakTokenProvider:
            A logged-in provider with `start_background_refresh=False`.
    """
    return KeycloakTokenProvider(
        keycloak_url=KEYCLOAK_URL,
        realm=REALM,
        client_id=CLIENT_ID,
        username=USERNAME,
        password=PASSWORD,
        token_expiration_in_s=token_expiration_in_s,
        transport=transport,
        time_fn=lambda: clock['now'],
        stop_event=stop_event,  # type: ignore[arg-type]  # ScriptedEvent is a structural Event stand-in
        start_background_refresh=False,
    )


class TestBackgroundRefresh:
    """The proactive background-refresh loop (`_refresh_loop` + its scheduling/teardown)."""

    def test_refreshes_before_expiry_and_reschedules(self) -> None:
        """The loop wakes leeway-before-expiry, refreshes, and reschedules from the new expiry."""
        clock: Dict[str, float] = {'now': 1000.0}
        transport: FakeTransport = FakeTransport([
            FakeResponse(200, _token_body('acc-1', 'off-1', 300)),
            FakeResponse(200, _token_body('acc-2', 'off-2', 300)),
            FakeResponse(200, _token_body('acc-3', 'off-3', 300)),
        ])
        # Each wait advances the clock by exactly the requested delay (the default), landing the
        # clock at expiry-minus-leeway so the post-wait refresh guard fires. Two timeouts → two
        # refreshes; the third wait exhausts the script and stops the loop.
        event: ScriptedEvent = ScriptedEvent(wait_returns=[False, False], clock=clock)
        provider: KeycloakTokenProvider = _build_background_provider(transport, clock, event)

        _refresh_loop(_weak(provider), event, lambda: clock['now'])  # type: ignore[arg-type]

        # Login + two background refreshes.
        assert len(transport.calls) == 3
        assert transport.calls[1]['grant_type'] == 'refresh_token'
        assert transport.calls[1]['refresh_token'] == 'off-1'
        assert transport.calls[2]['refresh_token'] == 'off-2'
        assert provider.access_token == 'acc-3'
        # Each scheduled delay is (expires_in - leeway) = 300 - 30 = 270s, computed from the
        # then-current expiry — proving the loop reschedules off the *new* expiry each time.
        expected_delay: float = 300.0 - _EXPIRY_LEEWAY_S
        assert event.wait_delays[0] == expected_delay
        assert event.wait_delays[1] == expected_delay

    def test_min_delay_clamp_prevents_hot_loop(self) -> None:
        """A token whose lifetime is below the leeway clamps the wait to the minimum delay."""
        clock: Dict[str, float] = {'now': 1000.0}
        # expires_in=5 → desired delay 5 - 30 = -25 → must clamp to _MIN_REFRESH_DELAY_S.
        transport: FakeTransport = FakeTransport([
            FakeResponse(200, _token_body('acc-1', 'off-1', 5)),
            FakeResponse(200, _token_body('acc-2', 'off-2', 300)),
        ])
        event: ScriptedEvent = ScriptedEvent(wait_returns=[False], clock=clock, advance_by=[0.0, 0.0])
        provider: KeycloakTokenProvider = _build_background_provider(transport, clock, event)

        _refresh_loop(_weak(provider), event, lambda: clock['now'])  # type: ignore[arg-type]

        assert event.wait_delays[0] == _MIN_REFRESH_DELAY_S
        assert provider.access_token == 'acc-2'

    def test_stop_during_wait_halts_the_loop_without_refresh(self) -> None:
        """When `wait()` returns True (stop fired mid-sleep) the loop exits with no refresh."""
        clock: Dict[str, float] = {'now': 1000.0}
        transport: FakeTransport = FakeTransport([FakeResponse(200, _token_body('acc-1', 'off-1', 300))])
        # First wait reports stop() fired during the sleep → loop returns immediately.
        event: ScriptedEvent = ScriptedEvent(wait_returns=[True], clock=clock, advance_by=[0.0])
        provider: KeycloakTokenProvider = _build_background_provider(transport, clock, event)

        _refresh_loop(_weak(provider), event, lambda: clock['now'])  # type: ignore[arg-type]

        # Only the login call happened; no refresh after the stop.
        assert len(transport.calls) == 1
        assert event.wait_delays == [300.0 - _EXPIRY_LEEWAY_S]

    def test_already_set_event_exits_before_first_wait(self) -> None:
        """A pre-set stop event makes the loop exit at the top, before computing any delay."""
        clock: Dict[str, float] = {'now': 1000.0}
        transport: FakeTransport = FakeTransport([FakeResponse(200, _token_body('acc-1', 'off-1', 300))])
        event: ScriptedEvent = ScriptedEvent(wait_returns=[], clock=clock)
        provider: KeycloakTokenProvider = _build_background_provider(transport, clock, event)
        event.set()

        _refresh_loop(_weak(provider), event, lambda: clock['now'])  # type: ignore[arg-type]

        assert event.wait_delays == []
        assert len(transport.calls) == 1

    def test_bounded_deadline_stops_loop_at_top(self) -> None:
        """Once the login deadline has elapsed the loop sets the event and exits (no refresh)."""
        clock: Dict[str, float] = {'now': 1000.0}
        token_expiration_in_s: int = 100
        transport: FakeTransport = FakeTransport([FakeResponse(200, _token_body('acc-1', 'off-1', 300))])
        event: ScriptedEvent = ScriptedEvent(wait_returns=[], clock=clock)
        provider: KeycloakTokenProvider = _build_background_provider(
            transport, clock, event, token_expiration_in_s=token_expiration_in_s,
        )
        # Jump the clock past the login deadline (login was at 1000, deadline = 1100).
        clock['now'] = 1000.0 + token_expiration_in_s + 1.0

        _refresh_loop(_weak(provider), event, lambda: clock['now'])  # type: ignore[arg-type]

        # Deadline elapsed at the top of the loop → no wait, no refresh, and the event is set.
        assert event.wait_delays == []
        assert len(transport.calls) == 1
        assert event.is_set()

    def test_deadline_clamps_remaining_time_below_expiry_delay(self) -> None:
        """When the deadline is nearer than the expiry-leeway delay, the wait clamps to it."""
        clock: Dict[str, float] = {'now': 1000.0}
        # Deadline at +50s is nearer than the expiry-leeway delay (300 - 30 = 270), so the
        # remaining-to-deadline (50s) must clamp the wait; the post-wait refresh then sees the
        # clock at the deadline and the loop stops via _refresh_if_within_window.
        token_expiration_in_s: int = 50
        transport: FakeTransport = FakeTransport([FakeResponse(200, _token_body('acc-1', 'off-1', 300))])
        event: ScriptedEvent = ScriptedEvent(wait_returns=[False], clock=clock, advance_by=[50.0])
        provider: KeycloakTokenProvider = _build_background_provider(
            transport, clock, event, token_expiration_in_s=token_expiration_in_s,
        )

        _refresh_loop(_weak(provider), event, lambda: clock['now'])  # type: ignore[arg-type]

        assert event.wait_delays[0] == float(token_expiration_in_s)
        # The wait advanced the clock by 50s → now == deadline → the post-wait refresh is skipped.
        assert len(transport.calls) == 1

    def test_weakref_collected_provider_exits_loop(self) -> None:
        """A loop whose provider was already collected exits at the top without a refresh."""
        clock: Dict[str, float] = {'now': 1000.0}
        transport: FakeTransport = FakeTransport([FakeResponse(200, _token_body('acc-1', 'off-1', 300))])
        provider: KeycloakTokenProvider = _build_background_provider(transport, clock, ScriptedEvent([], clock))
        ref: 'Any' = _weak(provider)

        del provider
        gc.collect()

        # Drive the loop with a *separate*, un-set event: collecting the provider runs its
        # `__del__` → `stop()`, which sets the provider's own internal stop event, but the loop
        # here is handed a fresh event so its `while not stop_event.is_set()` still enters once,
        # exercising the top-of-loop deref-to-None exit (the weakref-GC teardown path).
        loop_event: ScriptedEvent = ScriptedEvent(wait_returns=[False], clock=clock)
        _refresh_loop(ref, loop_event, lambda: clock['now'])  # type: ignore[arg-type]

        # The provider was collected before the loop ran, so its first top-of-loop deref is
        # already None → exits immediately with only the login call recorded.
        assert ref() is None
        assert len(transport.calls) == 1
        assert loop_event.wait_delays == []

    def test_post_wait_weakref_collected_provider_exits(self) -> None:
        """If the provider is collected during the wait, the post-wait deref exits the loop.

        Drives the branch where the *top-of-loop* deref succeeds (provider still alive), the
        loop arms a wait, and the provider is collected *during* that wait so the second deref
        returns None.
        """
        clock: Dict[str, float] = {'now': 1000.0}
        transport: FakeTransport = FakeTransport([FakeResponse(200, _token_body('acc-1', 'off-1', 300))])
        holder: Dict[str, Optional[KeycloakTokenProvider]] = {
            'provider': _build_background_provider(transport, clock, ScriptedEvent([], clock)),
        }
        ref: 'Any' = _weak(holder['provider'])

        class CollectingEvent(ScriptedEvent):
            """A scripted event whose single `wait` collects the provider before returning."""

            def wait(self, timeout: Optional[float] = None) -> bool:
                """Drop the provider strong-ref, force a GC, then report a timeout once.

                Args:
                    timeout (Optional[float]):
                        The requested delay (recorded for assertion).

                Returns:
                    bool:
                        `False` exactly once (a timeout) so the loop proceeds to the
                        now-None post-wait deref.
                """
                self.wait_delays.append(float(timeout if timeout is not None else 0.0))
                holder['provider'] = None
                gc.collect()
                return False

        event: CollectingEvent = CollectingEvent(wait_returns=[], clock=clock)

        _refresh_loop(ref, event, lambda: clock['now'])  # type: ignore[arg-type]

        assert ref() is None
        # Top-of-loop deref armed exactly one wait; the post-wait deref found None and exited.
        assert len(event.wait_delays) == 1
        assert len(transport.calls) == 1

    def test_start_background_refresh_spawns_daemon_thread(self) -> None:
        """`start_background_refresh=True` spawns a named daemon thread that `stop()` joins."""
        clock: Dict[str, float] = {'now': 1000.0}
        transport: FakeTransport = FakeTransport([FakeResponse(200, _token_body('acc-1', 'off-1', 300))])
        # A real Event + a frozen clock keep the first computed delay large (270s), so the thread
        # parks in wait() until stop() releases it — no refresh fires, no real sleep elapses.
        provider: KeycloakTokenProvider = KeycloakTokenProvider(
            keycloak_url=KEYCLOAK_URL,
            realm=REALM,
            client_id=CLIENT_ID,
            username=USERNAME,
            password=PASSWORD,
            transport=transport,
            time_fn=lambda: clock['now'],
            start_background_refresh=True,
        )
        thread: Optional[threading.Thread] = provider._refresh_thread
        assert thread is not None
        assert thread.daemon is True
        assert thread.name == f'keycloak-token-refresh-{CLIENT_ID}'
        assert thread.is_alive()

        provider.stop()

        # stop() set the event (interrupting the wait) and joined the thread.
        assert not thread.is_alive()
        # Only the login call happened: the thread parked in wait() and never refreshed.
        assert len(transport.calls) == 1

    def test_stop_is_idempotent(self) -> None:
        """Calling `stop()` twice is safe and leaves the thread joined."""
        clock: Dict[str, float] = {'now': 1000.0}
        transport: FakeTransport = FakeTransport([FakeResponse(200, _token_body('acc-1', 'off-1', 300))])
        provider: KeycloakTokenProvider = KeycloakTokenProvider(
            keycloak_url=KEYCLOAK_URL,
            realm=REALM,
            client_id=CLIENT_ID,
            username=USERNAME,
            password=PASSWORD,
            transport=transport,
            time_fn=lambda: clock['now'],
            start_background_refresh=True,
        )

        provider.stop()
        provider.stop()  # second call must be a no-op, not an error

        assert provider._refresh_thread is not None
        assert not provider._refresh_thread.is_alive()

    def test_close_alias_stops_thread(self) -> None:
        """The `close` alias performs the same teardown as `stop`."""
        clock: Dict[str, float] = {'now': 1000.0}
        transport: FakeTransport = FakeTransport([FakeResponse(200, _token_body('acc-1', 'off-1', 300))])
        provider: KeycloakTokenProvider = KeycloakTokenProvider(
            keycloak_url=KEYCLOAK_URL,
            realm=REALM,
            client_id=CLIENT_ID,
            username=USERNAME,
            password=PASSWORD,
            transport=transport,
            time_fn=lambda: clock['now'],
            start_background_refresh=True,
        )
        thread: Optional[threading.Thread] = provider._refresh_thread
        assert thread is not None

        provider.close()

        assert not thread.is_alive()

    def test_context_manager_stops_thread_on_exit(self) -> None:
        """Using the provider as a context manager stops its background thread on block exit."""
        clock: Dict[str, float] = {'now': 1000.0}
        transport: FakeTransport = FakeTransport([FakeResponse(200, _token_body('acc-1', 'off-1', 300))])
        with KeycloakTokenProvider(
            keycloak_url=KEYCLOAK_URL,
            realm=REALM,
            client_id=CLIENT_ID,
            username=USERNAME,
            password=PASSWORD,
            transport=transport,
            time_fn=lambda: clock['now'],
            start_background_refresh=True,
        ) as provider:
            thread: Optional[threading.Thread] = provider._refresh_thread
            assert thread is not None
            assert thread.is_alive()
            assert provider.access_token == 'acc-1'

        assert thread is not None
        assert not thread.is_alive()

    def test_del_stops_thread(self) -> None:
        """Garbage-collecting the provider triggers `__del__`, which stops the background thread."""
        clock: Dict[str, float] = {'now': 1000.0}
        transport: FakeTransport = FakeTransport([FakeResponse(200, _token_body('acc-1', 'off-1', 300))])
        provider: KeycloakTokenProvider = KeycloakTokenProvider(
            keycloak_url=KEYCLOAK_URL,
            realm=REALM,
            client_id=CLIENT_ID,
            username=USERNAME,
            password=PASSWORD,
            transport=transport,
            time_fn=lambda: clock['now'],
            start_background_refresh=True,
        )
        thread: Optional[threading.Thread] = provider._refresh_thread
        assert thread is not None
        assert thread.is_alive()

        del provider
        gc.collect()
        # __del__ set the stop event; the daemon thread (holding only a weakref) then exits.
        thread.join(timeout=5.0)
        assert not thread.is_alive()

    def test_stop_from_within_refresh_thread_skips_self_join(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """`stop()` invoked as the refresh thread must skip the self-join (would deadlock).

        Drives the `thread is threading.current_thread()` guard by patching `current_thread` to
        return the provider's refresh thread, so `stop()` sees itself and must not call `join`.

        Args:
            monkeypatch (pytest.MonkeyPatch):
                Fixture used to patch `threading.current_thread` for the guard.
        """
        clock: Dict[str, float] = {'now': 1000.0}
        transport: FakeTransport = FakeTransport([FakeResponse(200, _token_body('acc-1', 'off-1', 300))])
        provider: KeycloakTokenProvider = KeycloakTokenProvider(
            keycloak_url=KEYCLOAK_URL,
            realm=REALM,
            client_id=CLIENT_ID,
            username=USERNAME,
            password=PASSWORD,
            transport=transport,
            time_fn=lambda: clock['now'],
            start_background_refresh=True,
        )
        refresh_thread: Optional[threading.Thread] = provider._refresh_thread
        assert refresh_thread is not None

        joined: List[bool] = []
        original_join = refresh_thread.join

        def _tracking_join(timeout: Optional[float] = None) -> None:
            """Record a join attempt, then delegate to the real `Thread.join`.

            Args:
                timeout (Optional[float]):
                    The join timeout forwarded to the real `Thread.join`.
            """
            joined.append(True)
            original_join(timeout=timeout)

        refresh_thread.join = _tracking_join  # type: ignore[method-assign]

        monkeypatch.setattr(keycloak_module.threading, 'current_thread', lambda: refresh_thread)
        provider.stop()
        # The self-join guard skipped join() entirely.
        assert joined == []

        # Restore real current_thread so a normal external stop joins and tears the thread down.
        monkeypatch.undo()
        provider.stop()
        assert joined == [True]
        assert not refresh_thread.is_alive()
