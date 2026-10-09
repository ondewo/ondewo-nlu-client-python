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
"""`Client(use_shared_channel=True)` / `AsyncClient(use_shared_channel=True)`: one channel for all services.

The default (one channel per service) is pinned too, so the opt-in cannot silently become the
default. The RPC tests run against a real in-process server on 127.0.0.1 and check that the
Keycloak bearer metadata, which is per call and not a channel interceptor, still reaches it.
"""

import asyncio
import dataclasses
from concurrent import futures
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    get_type_hints,
)

import grpc
import pytest
from google.protobuf.empty_pb2 import Empty

from ondewo.nlu.agent_pb2 import GetPlatformInfoResponse
from ondewo.nlu.agent_pb2_grpc import (
    AgentsServicer,
    add_AgentsServicer_to_server,
)
from ondewo.nlu.async_client import AsyncClient
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.common_pb2 import StatResponse
from ondewo.nlu.core.services_container import ServicesContainer
from ondewo.nlu.server_statistics_pb2_grpc import (
    ServerStatisticsServicer,
    add_ServerStatisticsServicer_to_server,
)
from tests.unit.core.conftest import (
    keycloak_config,
    non_keycloak_config,
)
from tests.unit.core.test_client_wiring import EXPECTED_SERVICE_NAMES

BEARER: Tuple[str, str] = ("authorization", "Bearer acc-1")
PLATFORM_VERSION: str = "9.9.9"
PROJECT_COUNT: int = 42


class _FakeKeycloakProvider:
    """Stand-in for `KeycloakTokenProvider` returning a fixed bearer tuple."""

    def bearer_metadata(self) -> List[Tuple[str, str]]:
        """Return the canned bearer metadata without any network call."""
        return [BEARER]


def _authorization(context: Any) -> Optional[str]:
    """Return the `authorization` metadata value the server received, if any."""
    return dict(context.invocation_metadata()).get("authorization")


class _Agents(AgentsServicer):
    def __init__(self, seen: List[Optional[str]]) -> None:
        self.seen: List[Optional[str]] = seen

    def GetPlatformInfo(self, request: Empty, context: Any) -> GetPlatformInfoResponse:
        self.seen.append(_authorization(context))
        return GetPlatformInfoResponse(version=PLATFORM_VERSION)


class _ServerStatistics(ServerStatisticsServicer):
    def __init__(self, seen: List[Optional[str]]) -> None:
        self.seen: List[Optional[str]] = seen

    def GetProjectCount(self, request: Empty, context: Any) -> StatResponse:
        self.seen.append(_authorization(context))
        return StatResponse(value=PROJECT_COUNT)


class _AsyncAgents(AgentsServicer):
    def __init__(self, seen: List[Optional[str]]) -> None:
        self.seen: List[Optional[str]] = seen

    async def GetPlatformInfo(self, request: Empty, context: Any) -> GetPlatformInfoResponse:  # type: ignore[override]
        self.seen.append(_authorization(context))
        return GetPlatformInfoResponse(version=PLATFORM_VERSION)


class _AsyncServerStatistics(ServerStatisticsServicer):
    def __init__(self, seen: List[Optional[str]]) -> None:
        self.seen: List[Optional[str]] = seen

    async def GetProjectCount(self, request: Empty, context: Any) -> StatResponse:  # type: ignore[override]
        self.seen.append(_authorization(context))
        return StatResponse(value=PROJECT_COUNT)


def _config(port: int, use_keycloak: bool = False) -> ClientConfig:
    """Point a conftest config at the in-process server."""
    config: ClientConfig = keycloak_config() if use_keycloak else non_keycloak_config()
    return dataclasses.replace(config, host="127.0.0.1", port=str(port))


def _channels(client: Any) -> List[Any]:
    """The channel object of every declared service, in container order."""
    return [getattr(client.services, name).grpc_channel for name in EXPECTED_SERVICE_NAMES]


class _CloseSpy:
    """Counts `close()` calls and delegates to the real channel (sync or `grpc.aio`)."""

    def __init__(self, wrapped: Any) -> None:
        self.wrapped: Any = wrapped
        self.close_calls: int = 0

    def close(self, grace: Optional[float] = None) -> Any:
        self.close_calls += 1
        return self.wrapped.close() if grace is None else self.wrapped.close(grace)


@pytest.fixture
def sync_server() -> Iterator[Tuple[int, List[Optional[str]]]]:
    """A sync in-process server for Agents and ServerStatistics; yields its port and the auth it saw."""
    seen: List[Optional[str]] = []
    server: grpc.Server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    add_AgentsServicer_to_server(_Agents(seen), server)
    add_ServerStatisticsServicer_to_server(_ServerStatistics(seen), server)
    port: int = server.add_insecure_port("127.0.0.1:0")
    server.start()
    try:
        yield port, seen
    finally:
        server.stop(grace=None)


class TestDefaultIsOneChannelPerService:
    def test_sync_default_opens_a_distinct_channel_per_service(self) -> None:
        client: Client = Client(config=non_keycloak_config(), use_secure_channel=False)
        try:
            assert client.use_shared_channel is False
            assert len({id(channel) for channel in _channels(client)}) == len(EXPECTED_SERVICE_NAMES)
        finally:
            client.disconnect()

    def test_async_default_opens_a_distinct_channel_per_service(self) -> None:
        async def scenario() -> Set[int]:
            client: AsyncClient = AsyncClient(config=non_keycloak_config(), use_secure_channel=False)
            try:
                return {id(channel) for channel in _channels(client)}
            finally:
                await client.disconnect()

        assert len(asyncio.run(scenario())) == len(EXPECTED_SERVICE_NAMES)


class TestSharedChannel:
    def test_sync_every_service_holds_the_identical_channel(self) -> None:
        client: Client = Client(config=non_keycloak_config(), use_secure_channel=False, use_shared_channel=True)
        try:
            channels: List[Any] = _channels(client)
            assert isinstance(channels[0], grpc.Channel)
            assert all(channel is channels[0] for channel in channels)
        finally:
            client.disconnect()

    def test_async_every_service_holds_the_identical_channel(self) -> None:
        async def scenario() -> List[Any]:
            client: AsyncClient = AsyncClient(
                config=non_keycloak_config(), use_secure_channel=False, use_shared_channel=True
            )
            try:
                return _channels(client)
            finally:
                await client.disconnect()

        channels: List[Any] = asyncio.run(scenario())
        assert isinstance(channels[0], grpc.aio.Channel)
        assert all(channel is channels[0] for channel in channels)

    def test_sync_disconnect_closes_the_shared_channel_once(self) -> None:
        client: Client = Client(config=non_keycloak_config(), use_secure_channel=False, use_shared_channel=True)
        spy: _CloseSpy = _CloseSpy(_channels(client)[0])
        for name in EXPECTED_SERVICE_NAMES:
            getattr(client.services, name).grpc_channel = spy

        client.disconnect()

        assert spy.close_calls == 1
        assert client.services is None

    def test_async_disconnect_closes_the_shared_channel_once(self) -> None:
        async def scenario() -> int:
            client: AsyncClient = AsyncClient(
                config=non_keycloak_config(), use_secure_channel=False, use_shared_channel=True
            )
            spy: _CloseSpy = _CloseSpy(_channels(client)[0])
            for name in EXPECTED_SERVICE_NAMES:
                getattr(client.services, name).grpc_channel = spy
            await client.disconnect()
            return spy.close_calls

        assert asyncio.run(scenario()) == 1

    def test_connect_after_disconnect_keeps_sharing(self) -> None:
        client: Client = Client(config=non_keycloak_config(), use_secure_channel=False, use_shared_channel=True)
        first: Any = _channels(client)[0]
        client.disconnect()

        client.connect(config=non_keycloak_config(), use_secure_channel=False)
        try:
            channels: List[Any] = _channels(client)
            assert channels[0] is not first
            assert all(channel is channels[0] for channel in channels)
        finally:
            client.disconnect()

    def test_options_reach_the_shared_channel(self, monkeypatch: pytest.MonkeyPatch) -> None:
        captured: Dict[str, Any] = {}

        def fake_build(**kwargs: Any) -> grpc.Channel:
            captured.update(kwargs)
            return grpc.insecure_channel("127.0.0.1:1")

        monkeypatch.setattr("ondewo.utils.base_services_interface.build_shared_channel", fake_build)
        options: Set[Tuple[str, Any]] = {("grpc.primary_user_agent", "shared-test")}
        client: Client = Client(
            config=non_keycloak_config(), use_secure_channel=False, options=options, use_shared_channel=True
        )
        client.disconnect()

        assert captured["options"] == options
        assert captured["use_secure_channel"] is False
        # The union retry policy covers exactly the services the client wires.
        hints: Dict[str, Any] = get_type_hints(ServicesContainer)
        assert captured["service_classes"] == tuple(hints[name] for name in EXPECTED_SERVICE_NAMES)


class TestSharedChannelRpc:
    def test_sync_rpcs_of_two_services_reach_the_server_with_auth(
        self,
        sync_server: Tuple[int, List[Optional[str]]],
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(
            "ondewo.nlu.core.services_interface.get_keycloak_token_provider",
            lambda config: _FakeKeycloakProvider(),
        )
        port, seen = sync_server
        client: Client = Client(
            config=_config(port, use_keycloak=True), use_secure_channel=False, use_shared_channel=True
        )
        try:
            assert client.services is not None
            assert client.services.agents.get_platform_info().version == PLATFORM_VERSION
            assert client.services.server_statistics.get_project_count().value == PROJECT_COUNT
        finally:
            client.disconnect()

        assert seen == [BEARER[1], BEARER[1]]

    def test_async_rpcs_of_two_services_reach_the_server_with_auth(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(
            "ondewo.nlu.core.async_services_interface.get_keycloak_token_provider",
            lambda config: _FakeKeycloakProvider(),
        )
        seen: List[Optional[str]] = []

        async def scenario() -> Tuple[str, int]:
            server: grpc.aio.Server = grpc.aio.server()
            add_AgentsServicer_to_server(_AsyncAgents(seen), server)
            add_ServerStatisticsServicer_to_server(_AsyncServerStatistics(seen), server)
            port: int = server.add_insecure_port("127.0.0.1:0")
            await server.start()
            client: AsyncClient = AsyncClient(
                config=_config(port, use_keycloak=True), use_secure_channel=False, use_shared_channel=True
            )
            try:
                assert client.services is not None
                info: GetPlatformInfoResponse = await client.services.agents.get_platform_info()
                count: StatResponse = await client.services.server_statistics.get_project_count()
                return info.version, count.value
            finally:
                await client.disconnect()
                await server.stop(grace=None)

        assert asyncio.run(scenario()) == (PLATFORM_VERSION, PROJECT_COUNT)
        assert seen == [BEARER[1], BEARER[1]]
