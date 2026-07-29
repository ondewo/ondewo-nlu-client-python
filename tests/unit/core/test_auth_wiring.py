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

These cover the seam that decides *how* a call authenticates, independent of the Keycloak
token helper itself (covered by `test_keycloak.py`):

* `ServicesInterface.metadata` / `AsyncServicesInterface.metadata` selection — the Keycloak
  path must attach the **lowercase** `authorization` bearer tuple (grpc-python rejects a
  capital metadata key client-side), and the non-Keycloak path must attach an empty list so
  the call travels unauthenticated (no legacy `cai-token` metadata).

There is nothing else to cover: authentication is Keycloak bearer only. The client no longer
has a `login()` step at all — the neutralized no-op that used to return `""` (and the
`nlu_token` it threaded into every service, only to be discarded) has been removed.

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
from tests.unit.core.conftest import (
    keycloak_config as _keycloak_config,
    non_keycloak_config as _non_keycloak_config,
)

# Bound once so a refactor that changes only an input or only an expectation cannot silently
# make an assertion tautological.
BEARER_METADATA: List[Tuple[str, str]] = [("authorization", "Bearer acc-1")]


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
    service: _AsyncService = _AsyncService(config=config, use_secure_channel=False)
    try:
        return service.metadata
    finally:
        await service.grpc_channel.close()


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

        service: _SyncService = _SyncService(config=_keycloak_config(), use_secure_channel=False)

        assert service.metadata == BEARER_METADATA
        assert service.metadata[0][0] == "authorization"

    def test_sync_metadata_is_empty_without_keycloak(self) -> None:
        """Without Keycloak the sync interface attaches no metadata (unauthenticated call)."""
        service: _SyncService = _SyncService(config=_non_keycloak_config(), use_secure_channel=False)

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
