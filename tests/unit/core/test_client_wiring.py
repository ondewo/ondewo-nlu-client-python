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
"""Hermetic unit tests for `Client` / `AsyncClient` and their services containers.

All four modules under test are AUTO-GENERATED (`ondewo/nlu/scripts/generate_services.py`
plus the perl rewrites in `Makefile:157-163`), which shapes what is worth asserting here.
The async half is produced by regex-substituting the sync half:

    cp ondewo/nlu/client.py ondewo/nlu/async_client.py
    perl -i -pe 's/from ondewo\\.nlu\\.services\\.([a-z_]+) import/…async_$1 import/g; …'

That makes one specific failure mode both plausible and invisible to the type checker: if a
substitution misses a service, `AsyncClient` silently wires the **synchronous** implementation
(the classes share their names — `async_agents.Agents` vs `agents.Agents`), and because
`async_services_container.py` is rewritten by the *same* kind of regex, a consistent miss in
both leaves mypy green while every call on that service blocks the event loop. Hence
`TestClientServiceWiring` asserts on the concrete `__module__` of each *live* wired instance
rather than on types alone.

Nothing here touches the network: gRPC channels are lazy, the client is built with
`use_secure_channel=False`, and no RPC is ever issued.
"""

import asyncio
import re
from typing import (
    Any,
    Dict,
    Optional,
    Tuple,
    Type,
    get_type_hints,
)

import grpc
import pytest
from ondewo.utils.base_client_config import BaseClientConfig

from ondewo.nlu.async_client import AsyncClient
from ondewo.nlu.client import Client
from ondewo.nlu.core.async_services_container import AsyncServicesContainer
from ondewo.nlu.core.services_container import ServicesContainer
from tests.unit.core.conftest import (
    HOST,
    PORT,
    non_keycloak_config,
)

# The public service surface of the SDK, spelled out once as a golden list. Deriving it from
# `ServicesContainer.__annotations__` would make every assertion below tautological; hardcoding
# it means dropping or renaming a service — a breaking change for SDK users — has to be a
# deliberate edit here too.
EXPECTED_SERVICE_NAMES: Tuple[str, ...] = (
    "agents",
    "aiservices",
    "ccai_projects",
    "contexts",
    "entity_types",
    "intents",
    "llm_evaluations",
    "operations",
    "project_roles",
    "project_statistics",
    "rags",
    "server_statistics",
    "sessions",
    "users",
    "utilities",
    "webhooks",
)

SYNC_SERVICE_MODULE_PREFIX: str = "ondewo.nlu.services."
ASYNC_SERVICE_MODULE_PREFIX: str = "ondewo.nlu.services.async_"

# The guard both `client.py` and `async_client.py` carry, verbatim.
CONFIG_TYPE_ERROR_MESSAGE: str = "The provided config must be of type `ondewo.nlu.client_config.ClientConfig`"


class _ChannelCloseSpy:
    """Records `close()` calls on a `grpc.Channel` and delegates to the real one.

    Delegating (rather than swallowing) keeps the test honest: the real channel opened at
    construction is still torn down, so the spy adds an assertion without leaking a channel.
    """

    def __init__(self, wrapped: grpc.Channel) -> None:
        self._wrapped: grpc.Channel = wrapped
        self.close_calls: int = 0

    def close(self) -> None:
        """Count the call and close the wrapped channel."""
        self.close_calls += 1
        self._wrapped.close()


class _AsyncChannelCloseSpy:
    """Async counterpart of `_ChannelCloseSpy` for `grpc.aio.Channel`."""

    def __init__(self, wrapped: grpc.aio.Channel) -> None:
        self._wrapped: grpc.aio.Channel = wrapped
        self.close_calls: int = 0

    async def close(self, grace: Optional[float] = None) -> None:
        """Count the call and close the wrapped channel."""
        self.close_calls += 1
        await self._wrapped.close(grace=grace)


def _service_modules(container: Any) -> Dict[str, str]:
    """Map each declared service name to the `__module__` of its wired instance's class."""
    return {name: type(getattr(container, name)).__module__ for name in EXPECTED_SERVICE_NAMES}


def _wired_types(container: Any) -> Dict[str, Type[Any]]:
    """Map each declared service name to the exact class of its wired instance."""
    return {name: type(getattr(container, name)) for name in EXPECTED_SERVICE_NAMES}


class TestServicesContainerSurface:
    """The generated containers declare the agreed service fields, sync and async in parity."""

    def test_sync_container_declares_the_expected_services(self) -> None:
        """`ServicesContainer` exposes exactly the golden service list — no more, no less."""
        assert tuple(ServicesContainer.__annotations__.keys()) == EXPECTED_SERVICE_NAMES

    def test_async_container_declares_the_expected_services(self) -> None:
        """`AsyncServicesContainer` exposes the same surface, so both clients stay swappable."""
        assert tuple(AsyncServicesContainer.__annotations__.keys()) == EXPECTED_SERVICE_NAMES

    def test_async_container_is_typed_with_async_service_classes(self) -> None:
        """Every `AsyncServicesContainer` field is typed with a class from an `async_*` module.

        Guards the `Makefile` perl rewrite of `async_services_container.py`: sync and async
        service classes share their names, so a missed substitution is otherwise silent.
        """
        hints: Dict[str, Any] = get_type_hints(AsyncServicesContainer)

        non_async: Dict[str, str] = {
            name: hints[name].__module__
            for name in EXPECTED_SERVICE_NAMES
            if not hints[name].__module__.startswith(ASYNC_SERVICE_MODULE_PREFIX)
        }
        assert non_async == {}

    def test_sync_container_is_typed_with_sync_service_classes(self) -> None:
        """No `ServicesContainer` field leaks an `async_*` class into the synchronous surface."""
        hints: Dict[str, Any] = get_type_hints(ServicesContainer)

        leaked_async: Dict[str, str] = {
            name: hints[name].__module__
            for name in EXPECTED_SERVICE_NAMES
            if hints[name].__module__.startswith(ASYNC_SERVICE_MODULE_PREFIX)
        }
        assert leaked_async == {}


class TestClientServiceWiring:
    """`_initialize_services` populates the container with the right implementations."""

    def test_client_wires_every_service_with_its_declared_type(self) -> None:
        """Each service the sync client constructs is exactly the class its container declares."""
        client: Client = Client(config=non_keycloak_config(), use_secure_channel=False)
        try:
            container: Optional[ServicesContainer] = client.services
            assert container is not None

            assert _wired_types(container) == {
                name: get_type_hints(ServicesContainer)[name] for name in EXPECTED_SERVICE_NAMES
            }
        finally:
            client.disconnect()

    def test_client_wires_only_synchronous_implementations(self) -> None:
        """The sync client never reaches into an `async_*` service module."""
        client: Client = Client(config=non_keycloak_config(), use_secure_channel=False)
        try:
            container: Optional[ServicesContainer] = client.services
            assert container is not None

            leaked_async: Dict[str, str] = {
                name: module
                for name, module in _service_modules(container).items()
                if module.startswith(ASYNC_SERVICE_MODULE_PREFIX)
            }
            assert leaked_async == {}
        finally:
            client.disconnect()

    def test_async_client_wires_every_service_with_its_declared_type(self) -> None:
        """Each service the async client constructs is exactly the class its container declares."""

        async def scenario() -> Dict[str, Type[Any]]:
            client: AsyncClient = AsyncClient(config=non_keycloak_config(), use_secure_channel=False)
            try:
                container: Optional[AsyncServicesContainer] = client.services
                assert container is not None
                return _wired_types(container)
            finally:
                await client.disconnect()

        assert asyncio.run(scenario()) == {
            name: get_type_hints(AsyncServicesContainer)[name] for name in EXPECTED_SERVICE_NAMES
        }

    def test_async_client_wires_only_asynchronous_implementations(self) -> None:
        """Every service the async client constructs comes from an `async_*` module.

        This is the assertion the type checker cannot make: a perl rewrite that misses a
        service in both `async_client.py` and `async_services_container.py` leaves mypy green
        while the client silently blocks the event loop on a synchronous stub.
        """

        async def scenario() -> Dict[str, str]:
            client: AsyncClient = AsyncClient(config=non_keycloak_config(), use_secure_channel=False)
            try:
                container: Optional[AsyncServicesContainer] = client.services
                assert container is not None
                return _service_modules(container)
            finally:
                await client.disconnect()

        modules: Dict[str, str] = asyncio.run(scenario())

        non_async: Dict[str, str] = {
            name: module for name, module in modules.items() if not module.startswith(ASYNC_SERVICE_MODULE_PREFIX)
        }
        assert non_async == {}

    def test_sync_and_async_services_are_distinct_modules(self) -> None:
        """The two clients wire genuinely different implementations for the same service names.

        A regex rewrite that produced a byte-identical async client would satisfy the module
        prefix checks above only by accident; pinning the pairing makes the divergence explicit.
        """
        sync_client: Client = Client(config=non_keycloak_config(), use_secure_channel=False)
        try:
            sync_container: Optional[ServicesContainer] = sync_client.services
            assert sync_container is not None
            sync_modules: Dict[str, str] = _service_modules(sync_container)
        finally:
            sync_client.disconnect()

        async def scenario() -> Dict[str, str]:
            client: AsyncClient = AsyncClient(config=non_keycloak_config(), use_secure_channel=False)
            try:
                container: Optional[AsyncServicesContainer] = client.services
                assert container is not None
                return _service_modules(container)
            finally:
                await client.disconnect()

        async_modules: Dict[str, str] = asyncio.run(scenario())

        # `agents` -> `ondewo.nlu.services.agents` pairs with `ondewo.nlu.services.async_agents`.
        assert async_modules == {
            name: module.replace(SYNC_SERVICE_MODULE_PREFIX, ASYNC_SERVICE_MODULE_PREFIX, 1)
            for name, module in sync_modules.items()
        }


class TestConfigTypeGuard:
    """Both clients reject a config that is not an `ondewo.nlu` `ClientConfig`.

    `client.py` and `async_client.py` carry independent copies of the guard (the async file is a
    rewritten copy of the sync one), so each needs its own test — neither covers the other.
    """

    def test_client_rejects_a_non_nlu_config(self) -> None:
        """Passing the generic `BaseClientConfig` to `Client` raises `ValueError`."""
        base_config: BaseClientConfig = BaseClientConfig(host=HOST, port=PORT)

        with pytest.raises(ValueError, match=re.escape(CONFIG_TYPE_ERROR_MESSAGE)):
            Client(config=base_config, use_secure_channel=False)  # type: ignore[arg-type]

    def test_async_client_rejects_a_non_nlu_config(self) -> None:
        """Passing the generic `BaseClientConfig` to `AsyncClient` raises `ValueError`.

        No event loop is needed: the guard fires before any `grpc.aio` channel is built.
        """
        base_config: BaseClientConfig = BaseClientConfig(host=HOST, port=PORT)

        with pytest.raises(ValueError, match=re.escape(CONFIG_TYPE_ERROR_MESSAGE)):
            AsyncClient(config=base_config, use_secure_channel=False)  # type: ignore[arg-type]


class TestDisconnect:
    """`disconnect()` tears down every channel the container declares and clears `services`.

    `BaseClient.disconnect` walks `self.services.__annotations__`, so these tests pin the
    contract between the generated container's field list and the teardown loop: a service the
    container forgets to declare would leak its channel forever.
    """

    def test_disconnect_closes_every_service_channel_and_clears_services(self) -> None:
        """Every sync service's channel is closed exactly once and the container is dropped."""
        client: Client = Client(config=non_keycloak_config(), use_secure_channel=False)
        container: Optional[ServicesContainer] = client.services
        assert container is not None

        spies: Dict[str, _ChannelCloseSpy] = {}
        for name in EXPECTED_SERVICE_NAMES:
            service: Any = getattr(container, name)
            spies[name] = _ChannelCloseSpy(service.grpc_channel)
            service.grpc_channel = spies[name]

        client.disconnect()

        assert {name: spy.close_calls for name, spy in spies.items()} == dict.fromkeys(EXPECTED_SERVICE_NAMES, 1)
        assert client.services is None

    def test_async_disconnect_closes_every_service_channel_and_clears_services(self) -> None:
        """Every async service's channel is awaited closed exactly once and the container dropped."""

        async def scenario() -> Tuple[Dict[str, int], Optional[AsyncServicesContainer]]:
            client: AsyncClient = AsyncClient(config=non_keycloak_config(), use_secure_channel=False)
            container: Optional[AsyncServicesContainer] = client.services
            assert container is not None

            spies: Dict[str, _AsyncChannelCloseSpy] = {}
            for name in EXPECTED_SERVICE_NAMES:
                service: Any = getattr(container, name)
                spies[name] = _AsyncChannelCloseSpy(service.grpc_channel)
                service.grpc_channel = spies[name]

            await client.disconnect()

            return {name: spy.close_calls for name, spy in spies.items()}, client.services

        close_calls, services_after = asyncio.run(scenario())

        assert close_calls == dict.fromkeys(EXPECTED_SERVICE_NAMES, 1)
        assert services_after is None
