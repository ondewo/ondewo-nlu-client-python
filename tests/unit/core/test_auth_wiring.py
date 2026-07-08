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
"""Hermetic unit tests for the client's bearer-only auth wiring.

These cover the two seams that decide *how* a call authenticates, independent of the
Keycloak token helper itself (covered by `test_keycloak.py`):

* `login()` / async `login()` are neutralized no-ops — authentication is Keycloak bearer
  only, so they never call the legacy `Login` RPC and always return an empty string.
* `ServicesInterface.metadata` / `AsyncServicesInterface.metadata` selection — the Keycloak
  path must attach the **lowercase** `authorization` bearer tuple (grpc-python rejects a
  capital metadata key client-side), and the non-Keycloak path must attach an empty list so
  the call travels unauthenticated (no legacy `cai-token` metadata).

No network is touched: the Keycloak token provider is replaced with a fake, and the gRPC
channels created at construction are insecure and are never used to issue a call.
"""

import asyncio
from typing import (
    List,
    Tuple,
)

import pytest

from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.core.async_services_interface import AsyncServicesInterface
from ondewo.nlu.core.services_interface import ServicesInterface
from ondewo.nlu.utils.async_login import login as async_login
from ondewo.nlu.utils.login import login

# Bound once so a refactor that changes only an input or only an expectation cannot silently
# make an assertion tautological.
HOST: str = "localhost"
PORT: str = "50055"
USERNAME: str = "tech-user@example.com"
PASSWORD: str = "s3cr3t"
KEYCLOAK_URL: str = "https://kc.example.com/auth"
REALM: str = "ondewo-ccai-platform"
CLIENT_ID: str = "ondewo-nlu-cai-sdk-public"
BEARER_METADATA: List[Tuple[str, str]] = [("authorization", "Bearer acc-1")]


def _non_keycloak_config() -> ClientConfig:
    """Build a config with no Keycloak fields set (calls travel unauthenticated)."""
    return ClientConfig(
        host=HOST,
        port=PORT,
        user_name=USERNAME,
        password=PASSWORD,
    )


def _keycloak_config() -> ClientConfig:
    """Build a config for the Keycloak headless offline-token auth path (D18)."""
    return ClientConfig(
        host=HOST,
        port=PORT,
        user_name=USERNAME,
        password=PASSWORD,
        keycloak_url=KEYCLOAK_URL,
        realm=REALM,
        client_id=CLIENT_ID,
    )


class _FakeKeycloakProvider:
    """Stand-in for `KeycloakTokenProvider` returning a fixed bearer metadata list."""

    def bearer_metadata(self) -> List[Tuple[str, str]]:
        """Return the canned bearer metadata without any network call."""
        return list(BEARER_METADATA)


class _SyncService(ServicesInterface):
    """Minimal concrete `ServicesInterface` so `metadata` can be exercised in isolation."""

    @property
    def stub(self) -> None:
        """No stub is needed — the metadata wiring never issues a gRPC call."""
        return None


class _AsyncService(AsyncServicesInterface):
    """Minimal concrete `AsyncServicesInterface` so `metadata` can be exercised in isolation."""

    @property
    def stub(self) -> None:
        """No stub is needed — the metadata wiring never issues a gRPC call."""
        return None


async def _async_metadata(config: ClientConfig) -> List[Tuple[str, str]]:
    """Build an `_AsyncService` (needs a running loop for its `grpc.aio` channel) and read its metadata."""
    service: _AsyncService = _AsyncService(config=config, nlu_token="", use_secure_channel=False)
    try:
        return service.metadata
    finally:
        await service.grpc_channel.close()


class TestLoginIsNeutralizedNoOp:
    """`login()` never calls the legacy `Login` RPC and always returns an empty string."""

    def test_sync_login_returns_empty_for_keycloak(self) -> None:
        """The synchronous `login()` returns `''` for a Keycloak config without an RPC."""
        assert login(_keycloak_config(), use_secure_channel=False) == ""

    def test_sync_login_returns_empty_without_keycloak(self) -> None:
        """The synchronous `login()` returns `''` for a non-Keycloak config without an RPC."""
        assert login(_non_keycloak_config(), use_secure_channel=False) == ""

    def test_async_login_returns_empty_for_keycloak(self) -> None:
        """The asynchronous `login()` returns `''` for a Keycloak config without an RPC."""
        assert asyncio.run(async_login(_keycloak_config(), use_secure_channel=False)) == ""

    def test_async_login_returns_empty_without_keycloak(self) -> None:
        """The asynchronous `login()` returns `''` for a non-Keycloak config without an RPC."""
        assert asyncio.run(async_login(_non_keycloak_config(), use_secure_channel=False)) == ""


class TestMetadataSelection:
    """`metadata` picks the lowercase bearer tuple under Keycloak, an empty list otherwise."""

    def test_sync_metadata_is_lowercase_bearer_tuple_for_keycloak(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """With Keycloak configured the sync interface attaches the fake provider's bearer tuple."""
        monkeypatch.setattr(
            "ondewo.nlu.core.services_interface.get_keycloak_token_provider",
            lambda config: _FakeKeycloakProvider(),
        )

        service: _SyncService = _SyncService(config=_keycloak_config(), nlu_token="", use_secure_channel=False)

        assert service.metadata == BEARER_METADATA
        assert service.metadata[0][0] == "authorization"

    def test_sync_metadata_is_empty_without_keycloak(self) -> None:
        """Without Keycloak the sync interface attaches no metadata (unauthenticated call)."""
        service: _SyncService = _SyncService(config=_non_keycloak_config(), nlu_token="", use_secure_channel=False)

        assert service.metadata == []

    def test_async_metadata_is_lowercase_bearer_tuple_for_keycloak(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """With Keycloak configured the async interface attaches the fake provider's bearer tuple."""
        monkeypatch.setattr(
            "ondewo.nlu.core.async_services_interface.get_keycloak_token_provider",
            lambda config: _FakeKeycloakProvider(),
        )

        # The async interface builds a `grpc.aio` channel at construction, which needs a running
        # event loop; build it and read `metadata` (a sync property) inside `asyncio.run`.
        metadata: List[Tuple[str, str]] = asyncio.run(_async_metadata(_keycloak_config()))

        assert metadata == BEARER_METADATA
        assert metadata[0][0] == "authorization"

    def test_async_metadata_is_empty_without_keycloak(self) -> None:
        """Without Keycloak the async interface attaches no metadata (unauthenticated call)."""
        metadata: List[Tuple[str, str]] = asyncio.run(_async_metadata(_non_keycloak_config()))

        assert metadata == []
