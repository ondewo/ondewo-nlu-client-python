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
"""Hermetic unit tests for the `ondewo.qa` client surface.

The QA half of this SDK is the neglected one: it has no generator behind it (unlike
`ondewo/nlu/services`, which `generate_services.py` emits) and, until recently, no tests at
all — which is exactly how `services/async_qa.py` came to ship to PyPI raising
`ModuleNotFoundError` on import. These tests pin the parts that can actually break:

* the config type guard and the service wiring in `client.py`,
* `disconnect()` closing the channel it opened,
* and the plain importability of `services/async_qa.py` (see `TestAsyncQaModuleImports`).

Nothing here touches the network: gRPC channels are lazy, the client is built with
`use_secure_channel=False`, and no RPC is ever issued.
"""

import importlib
import re
from types import ModuleType
from typing import (
    Optional,
    Tuple,
)

import grpc
import pytest
from ondewo.utils.base_client_config import BaseClientConfig

from ondewo.qa.client import Client
from ondewo.qa.client_config import ClientConfig
from ondewo.qa.core.services_container import ServicesContainer

# Bound once so a refactor that changes only an input or only an expectation cannot silently
# make an assertion tautological.
HOST: str = "localhost"
PORT: str = "50055"

# The public service surface of the QA client, spelled out as a golden list rather than derived
# from `ServicesContainer.__annotations__` (which would make the assertion tautological).
EXPECTED_SERVICE_NAMES: Tuple[str, ...] = ("qa",)

SYNC_QA_SERVICE_MODULE: str = "ondewo.qa.services.qa"
ASYNC_QA_SERVICE_MODULE: str = "ondewo.qa.services.async_qa"
QA_SERVICE_CLASS_NAME: str = "QA"

# The guard `client.py` carries, verbatim.
CONFIG_TYPE_ERROR_MESSAGE: str = "The provided config must be of type `ondewo.qa.client_config.ClientConfig`"


def qa_config() -> ClientConfig:
    """Build a QA client config (host/port only — the QA config has no auth fields)."""
    return ClientConfig(host=HOST, port=PORT)


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


class TestServicesContainerSurface:
    """The QA container declares the agreed service fields."""

    def test_container_declares_the_expected_services(self) -> None:
        """`ServicesContainer` exposes exactly the golden service list — no more, no less."""
        assert tuple(ServicesContainer.__annotations__.keys()) == EXPECTED_SERVICE_NAMES


class TestQaClientWiring:
    """`_initialize_services` populates the container with the right implementation."""

    def test_client_wires_the_synchronous_qa_service(self) -> None:
        """The client wires the `QA` class from the synchronous service module.

        Asserted via `__module__`/`__name__` rather than `isinstance`: the sync and async QA
        implementations share the class name `QA`, so an import that reached into
        `services/async_qa.py` would satisfy a type check while blocking on every call.
        """
        client: Client = Client(config=qa_config(), use_secure_channel=False)
        try:
            container: Optional[ServicesContainer] = client.services
            assert container is not None

            assert type(container.qa).__module__ == SYNC_QA_SERVICE_MODULE
            assert type(container.qa).__name__ == QA_SERVICE_CLASS_NAME
        finally:
            client.disconnect()

    def test_client_opens_a_channel_for_the_qa_service(self) -> None:
        """The wired service gets a live gRPC channel (lazy — no connection is attempted)."""
        client: Client = Client(config=qa_config(), use_secure_channel=False)
        try:
            container: Optional[ServicesContainer] = client.services
            assert container is not None

            assert container.qa.grpc_channel is not None
        finally:
            client.disconnect()


class TestConfigTypeGuard:
    """The client rejects a config that is not an `ondewo.qa` `ClientConfig`."""

    def test_client_rejects_a_non_qa_config(self) -> None:
        """Passing the generic `BaseClientConfig` to `Client` raises `ValueError`.

        The QA client shares its host/port fields with `BaseClientConfig`, so without this
        guard an `ondewo.nlu` config would wire up and fail much later at call time.
        """
        base_config: BaseClientConfig = BaseClientConfig(host=HOST, port=PORT)

        with pytest.raises(ValueError, match=re.escape(CONFIG_TYPE_ERROR_MESSAGE)):
            Client(config=base_config, use_secure_channel=False)  # type: ignore[arg-type]


class TestDisconnect:
    """`disconnect()` tears down every channel the container declares and clears `services`."""

    def test_disconnect_closes_the_qa_channel_and_clears_services(self) -> None:
        """The QA service's channel is closed exactly once and the container is dropped."""
        client: Client = Client(config=qa_config(), use_secure_channel=False)
        container: Optional[ServicesContainer] = client.services
        assert container is not None

        spy: _ChannelCloseSpy = _ChannelCloseSpy(container.qa.grpc_channel)
        container.qa.grpc_channel = spy

        client.disconnect()

        assert spy.close_calls == 1
        assert client.services is None


class TestAsyncQaModuleImports:
    """`ondewo.qa.services.async_qa` must import cleanly.

    Regression guard for a bug that shipped to PyPI: the module raised
    `ModuleNotFoundError: No module named 'ondewo.qa.core.async_services_interface'` at import
    time, so `from ondewo.qa.services.async_qa import QA` was broken for every installed user.
    Nothing else reaches this module — the QA `Client` wires only the synchronous service and
    there is no `AsyncClient` for QA — so without this test the module's importability is
    unguarded and the same breakage could ship again unnoticed.
    """

    def test_async_qa_module_imports_and_exposes_the_qa_service(self) -> None:
        """Importing the async QA module succeeds and yields its `QA` service class."""
        module: ModuleType = importlib.import_module(ASYNC_QA_SERVICE_MODULE)

        assert module.QA.__module__ == ASYNC_QA_SERVICE_MODULE
