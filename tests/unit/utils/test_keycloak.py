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
"""
from typing import (
    Any,
    Dict,
    List,
    Tuple,
)

import pytest

from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.utils import keycloak as keycloak_module
from ondewo.nlu.utils.keycloak import (
    _HTTP_TIMEOUT_S,
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
        self.status_code: int = status_code
        self._body: Dict[str, Any] = body

    def json(self) -> Dict[str, Any]:
        return self._body

    @property
    def text(self) -> str:
        return repr(self._body)


class FakeTransport:
    """Fake token endpoint: records every POST and replays queued responses in order."""

    def __init__(self, responses: List[FakeResponse]) -> None:
        self._responses: List[FakeResponse] = list(responses)
        self.calls: List[Dict[str, str]] = []

    def post(self, url: str, data: Dict[str, str], timeout: float) -> FakeResponse:
        self.calls.append({'url': url, **data})
        if not self._responses:
            raise AssertionError('FakeTransport received more POSTs than queued responses')
        return self._responses.pop(0)


def _token_body(access_token: str, refresh_token: str, expires_in: int) -> Dict[str, Any]:
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
    return KeycloakTokenProvider(
        keycloak_url=KEYCLOAK_URL,
        realm=REALM,
        client_id=CLIENT_ID,
        username=USERNAME,
        password=PASSWORD,
        token_expiration_in_s=token_expiration_in_s,
        transport=transport,
    )


class TestLogin:
    def test_ropc_login_sends_offline_access_scope_and_no_secret(self) -> None:
        transport = FakeTransport([FakeResponse(200, _token_body('acc-1', 'off-1', 300))])

        provider = _build_provider(transport)

        assert provider.access_token == 'acc-1'
        assert len(transport.calls) == 1
        login_call = transport.calls[0]
        assert login_call['url'] == EXPECTED_TOKEN_ENDPOINT
        assert login_call['grant_type'] == 'password'
        assert login_call['client_id'] == CLIENT_ID
        assert login_call['username'] == USERNAME
        assert login_call['password'] == PASSWORD
        assert login_call['scope'] == 'offline_access'
        # Q1: public client — never send a client_secret.
        assert 'client_secret' not in login_call

    def test_authorization_metadata_is_bearer(self) -> None:
        transport = FakeTransport([FakeResponse(200, _token_body('acc-1', 'off-1', 300))])

        provider = _build_provider(transport)

        key, value = provider.authorization_metadata()
        assert key == 'authorization'
        assert value == 'Bearer acc-1'

    def test_bearer_metadata_shape(self) -> None:
        transport = FakeTransport([FakeResponse(200, _token_body('acc-1', 'off-1', 300))])

        provider = _build_provider(transport)

        metadata: List[Tuple[str, str]] = provider.bearer_metadata()
        assert metadata == [('authorization', 'Bearer acc-1')]

    def test_login_failure_raises(self) -> None:
        transport = FakeTransport([FakeResponse(401, {'error': 'invalid_grant'})])

        with pytest.raises(KeycloakAuthenticationError):
            _build_provider(transport)

    def test_missing_access_token_raises(self) -> None:
        transport = FakeTransport([FakeResponse(200, {'refresh_token': 'off-1', 'expires_in': 300})])

        with pytest.raises(KeycloakAuthenticationError):
            _build_provider(transport)


class TestRefresh:
    def test_refresh_uses_offline_refresh_token(self, monkeypatch: pytest.MonkeyPatch) -> None:
        clock: Dict[str, float] = {'now': 1000.0}
        monkeypatch.setattr(keycloak_module.time, 'monotonic', lambda: clock['now'])

        transport = FakeTransport([
            FakeResponse(200, _token_body('acc-1', 'off-1', 300)),
            FakeResponse(200, _token_body('acc-2', 'off-2', 300)),
        ])
        provider = _build_provider(transport)

        # Advance the clock past the access-token lifetime so the next read refreshes.
        clock['now'] = 1000.0 + 300.0
        _, value = provider.authorization_metadata()

        assert value == 'Bearer acc-2'
        assert len(transport.calls) == 2
        refresh_call = transport.calls[1]
        assert refresh_call['grant_type'] == 'refresh_token'
        assert refresh_call['client_id'] == CLIENT_ID
        assert refresh_call['refresh_token'] == 'off-1'
        assert 'client_secret' not in refresh_call

    def test_no_refresh_while_token_still_valid(self, monkeypatch: pytest.MonkeyPatch) -> None:
        clock: Dict[str, float] = {'now': 1000.0}
        monkeypatch.setattr(keycloak_module.time, 'monotonic', lambda: clock['now'])

        transport = FakeTransport([FakeResponse(200, _token_body('acc-1', 'off-1', 300))])
        provider = _build_provider(transport)

        # Read several times well inside the validity window: still exactly one HTTP call.
        clock['now'] = 1000.0 + 100.0
        provider.authorization_metadata()
        provider.authorization_metadata()

        assert len(transport.calls) == 1

    def test_refresh_keeps_previous_offline_token_when_omitted(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        clock: Dict[str, float] = {'now': 1000.0}
        monkeypatch.setattr(keycloak_module.time, 'monotonic', lambda: clock['now'])

        transport = FakeTransport([
            FakeResponse(200, _token_body('acc-1', 'off-1', 300)),
            # A refresh response that omits refresh_token — provider keeps the old one.
            FakeResponse(200, {'access_token': 'acc-2', 'expires_in': 300}),
            FakeResponse(200, _token_body('acc-3', 'off-3', 300)),
        ])
        provider = _build_provider(transport)

        clock['now'] = 1000.0 + 300.0
        provider.authorization_metadata()  # refresh #1 → acc-2, no new offline token
        clock['now'] = 1000.0 + 600.0
        provider.authorization_metadata()  # refresh #2 → must still use off-1

        assert transport.calls[2]['refresh_token'] == 'off-1'


class TestTokenExpirationBound:
    def test_refresh_stops_after_token_expiration_in_s(self, monkeypatch: pytest.MonkeyPatch) -> None:
        clock: Dict[str, float] = {'now': 1000.0}
        monkeypatch.setattr(keycloak_module.time, 'monotonic', lambda: clock['now'])

        token_expiration_in_s: int = 600
        transport = FakeTransport([
            FakeResponse(200, _token_body('acc-1', 'off-1', 300)),
            FakeResponse(200, _token_body('acc-2', 'off-2', 300)),
        ])
        provider = _build_provider(transport, token_expiration_in_s=token_expiration_in_s)

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
        clock: Dict[str, float] = {'now': 1000.0}
        monkeypatch.setattr(keycloak_module.time, 'monotonic', lambda: clock['now'])

        transport = FakeTransport([
            FakeResponse(200, _token_body('acc-1', 'off-1', 300)),
            FakeResponse(200, _token_body('acc-2', 'off-2', 300)),
            FakeResponse(200, _token_body('acc-3', 'off-3', 300)),
        ])
        provider = _build_provider(transport, token_expiration_in_s=None)

        clock['now'] = 1000.0 + 300.0
        provider.authorization_metadata()
        clock['now'] = 1000.0 + 600.0
        _, value = provider.authorization_metadata()

        assert value == 'Bearer acc-3'
        assert len(transport.calls) == 3

    def test_refresh_failure_after_login_raises(self, monkeypatch: pytest.MonkeyPatch) -> None:
        clock: Dict[str, float] = {'now': 1000.0}
        monkeypatch.setattr(keycloak_module.time, 'monotonic', lambda: clock['now'])

        transport = FakeTransport([
            FakeResponse(200, _token_body('acc-1', 'off-1', 300)),
            FakeResponse(400, {'error': 'invalid_grant'}),
        ])
        provider = _build_provider(transport)

        clock['now'] = 1000.0 + 300.0
        with pytest.raises(KeycloakAuthenticationError):
            provider.authorization_metadata()


class TestSharedProviderRegistry:
    def test_same_config_returns_same_provider(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # Drive the default transport (requests) through a fake so no network is hit.
        post_calls: List[Dict[str, str]] = []

        def fake_post(url: str, data: Dict[str, str], timeout: float) -> FakeResponse:
            post_calls.append({'url': url, **data})
            return FakeResponse(200, _token_body('acc-1', 'off-1', 300))

        monkeypatch.setattr(keycloak_module.requests, 'post', fake_post)

        config = ClientConfig(
            host='localhost',
            port='50055',
            user_name=USERNAME,
            password=PASSWORD,
            keycloak_url=KEYCLOAK_URL,
            realm=REALM,
            client_id=CLIENT_ID,
        )
        first = get_keycloak_token_provider(config)
        second = get_keycloak_token_provider(config)

        assert first is second
        # Login happened exactly once despite two factory calls.
        assert len(post_calls) == 1

    def test_factory_forwards_token_expiration_in_s(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # The factory must thread `token_expiration_in_s` from the config into the provider so
        # the auto-refresh bound is honoured; otherwise a refresh would run past the deadline.
        clock: Dict[str, float] = {'now': 1000.0}
        monkeypatch.setattr(keycloak_module.time, 'monotonic', lambda: clock['now'])

        token_expiration_in_s: int = 600

        def fake_post(url: str, data: Dict[str, str], timeout: float) -> FakeResponse:
            return FakeResponse(200, _token_body('acc-1', 'off-1', 300))

        monkeypatch.setattr(keycloak_module.requests, 'post', fake_post)

        config = ClientConfig(
            host='localhost',
            port='50055',
            user_name=USERNAME,
            password=PASSWORD,
            keycloak_url=KEYCLOAK_URL,
            realm=REALM,
            client_id=CLIENT_ID,
            token_expiration_in_s=token_expiration_in_s,
        )
        provider = get_keycloak_token_provider(config)

        assert provider.token_expiration_in_s == token_expiration_in_s


class TestDefaultRequestsTransport:
    def test_provider_uses_requests_transport_by_default(self, monkeypatch: pytest.MonkeyPatch) -> None:
        # When no transport is injected the provider must fall back to the real requests-backed
        # transport (the production path); patch requests.post so no network is touched.
        post_calls: List[Dict[str, str]] = []

        def fake_post(url: str, data: Dict[str, str], timeout: float) -> FakeResponse:
            post_calls.append({'url': url, **data})
            return FakeResponse(200, _token_body('acc-1', 'off-1', 300))

        monkeypatch.setattr(keycloak_module.requests, 'post', fake_post)

        provider = KeycloakTokenProvider(
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
        # _RequestsTransport.post must pass through url/data verbatim and the module HTTP timeout.
        captured: Dict[str, Any] = {}

        def fake_post(url: str, data: Dict[str, str], timeout: float) -> FakeResponse:
            captured['url'] = url
            captured['data'] = data
            captured['timeout'] = timeout
            return FakeResponse(200, _token_body('acc-1', 'off-1', 300))

        monkeypatch.setattr(keycloak_module.requests, 'post', fake_post)

        transport = _RequestsTransport()
        form_data: Dict[str, str] = {'grant_type': 'password'}
        response = transport.post(EXPECTED_TOKEN_ENDPOINT, data=form_data, timeout=_HTTP_TIMEOUT_S)

        assert response.status_code == 200
        assert captured['url'] == EXPECTED_TOKEN_ENDPOINT
        assert captured['data'] == form_data
        assert captured['timeout'] == _HTTP_TIMEOUT_S


class TestStoreTokensExpiry:
    def test_missing_expires_in_defaults_to_zero_and_forces_refresh(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        # A token response without `expires_in` is treated as already at expiry (0s), so the very
        # next metadata read must refresh rather than serve a token with an unknown lifetime.
        clock: Dict[str, float] = {'now': 1000.0}
        monkeypatch.setattr(keycloak_module.time, 'monotonic', lambda: clock['now'])

        transport = FakeTransport([
            FakeResponse(200, {'access_token': 'acc-1', 'refresh_token': 'off-1'}),
            FakeResponse(200, _token_body('acc-2', 'off-2', 300)),
        ])
        provider = _build_provider(transport)

        # Clock has not advanced, but expires_at == login time (expires_in defaulted to 0), so the
        # leeway check fires immediately and the next read refreshes.
        _, value = provider.authorization_metadata()

        assert value == 'Bearer acc-2'
        assert len(transport.calls) == 2
