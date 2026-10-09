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
from typing import (
    Any,
    Dict,
    Optional,
    Set,
    Tuple,
)

from ondewo.utils.base_client import BaseClient
from ondewo.utils.base_client_config import BaseClientConfig

from ondewo.qa.client_config import ClientConfig
from ondewo.qa.core.services_container import ServicesContainer
from ondewo.qa.services.qa import QA


class Client(BaseClient):
    """
    The core python client for interacting with ONDEWO QA services.
    """

    def __init__(
        self,
        config: BaseClientConfig,
        use_secure_channel: bool = True,
        options: Optional[Set[Tuple[str, Any]]] = None,
        *,
        use_shared_channel: bool = False,
    ) -> None:
        """
        Initialize the client and its service clients.

        Args:
            config (BaseClientConfig):
                Configuration for the client; must be an ``ondewo.qa.client_config.ClientConfig``.
            use_secure_channel (bool):
                Whether to use a secure gRPC channel. Defaults to ``True``.
            options (Optional[Set[Tuple[str, Any]]]):
                Additional options for the gRPC channel. Defaults to ``None``.
            use_shared_channel (bool):
                Build the channel with ``build_shared_channel``, as ``ondewo.nlu.client.Client`` does. The QA
                client has one service, so it opens one channel either way; the flag exists for parity with the
                NLU client. Kept by ``connect`` after a ``disconnect``. Needs Python >= 3.12
                (ondewo-client-utils >= 4.0.0). Defaults to ``False``.
        """
        self.use_shared_channel: bool = use_shared_channel
        super().__init__(config=config, use_secure_channel=use_secure_channel, options=options)

    def _initialize_services(
        self,
        config: BaseClientConfig,
        use_secure_channel: bool,
        options: Optional[Set[Tuple[str, Any]]] = None,
    ) -> None:
        """

        Initialize the service clients and lLogin with the current config and set up the services in self.services

        Args:
            config (BaseClientConfig):
                Configuration for the client.
            use_secure_channel (bool):
                Whether to use a secure gRPC channel.
            options (Optional[Set[Tuple[str, Any]]]):
                Additional options for the gRPC channel.
        """
        if not isinstance(config, ClientConfig):
            raise ValueError("The provided config must be of type `ondewo.qa.client_config.ClientConfig`")

        kwargs: Dict[str, Any] = {
            "config": config,
            "use_secure_channel": use_secure_channel,
            "options": options,
        }
        if self.use_shared_channel:
            # Imported here: ondewo-client-utils < 4.0.0 (Python < 3.12) has no build_shared_channel.
            from ondewo.utils.base_services_interface import build_shared_channel

            kwargs["grpc_channel"] = build_shared_channel(
                config=config,
                use_secure_channel=use_secure_channel,
                service_classes=(QA,),
                options=options,
            )
        self.services: ServicesContainer = ServicesContainer(
            qa=QA(**kwargs),
        )
