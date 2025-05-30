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
            raise ValueError('The provided config must be of type `ondewo.qa.client_config.ClientConfig`')

        self.services: ServicesContainer = ServicesContainer(
            qa=QA(config=config, use_secure_channel=use_secure_channel, options=options),
        )
