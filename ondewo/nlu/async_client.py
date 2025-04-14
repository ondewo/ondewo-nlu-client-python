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

from ondewo.utils.async_base_client import AsyncBaseClient

from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.core.async_services_container import AsyncServicesContainer
from ondewo.nlu.services.async_agents import Agents
from ondewo.nlu.services.async_aiservices import AIServices
from ondewo.nlu.services.async_ccai_projects import CcaiProjects
from ondewo.nlu.services.async_contexts import Contexts
from ondewo.nlu.services.async_entity_types import EntityTypes
from ondewo.nlu.services.async_intents import Intents
from ondewo.nlu.services.async_operations import Operations
from ondewo.nlu.services.async_project_roles import ProjectRoles
from ondewo.nlu.services.async_project_statistics import ProjectStatistics
from ondewo.nlu.services.async_server_statistics import ServerStatistics
from ondewo.nlu.services.async_sessions import Sessions
from ondewo.nlu.services.async_users import Users
from ondewo.nlu.services.async_utilities import Utilities
from ondewo.nlu.utils.login import login


class AsyncClient(AsyncBaseClient):
    """
    The core asynchronous Python client for interacting with ONDEWO NLU services.
    """

    def _initialize_services(
        self,
        config: ClientConfig,
        use_secure_channel: bool,
        options: Optional[Set[Tuple[str, Any]]] = None,
    ) -> None:
        """
        Initialize the asynchronous service clients, login with the current config,
        and set up the services in self.services.

        Args:
            config (ClientConfig): Configuration for the client.
            use_secure_channel (bool): Whether to use a secure gRPC channel.
            options (Optional[Set[Tuple[str, Any]]]): Additional options for the gRPC channel.
        """
        if not isinstance(config, ClientConfig):
            raise ValueError('The provided config must be of type `ondewo.nlu.client_config.ClientConfig`')

        nlu_token: str = login(config=config, use_secure_channel=use_secure_channel, options=options)
        kwargs: Dict[str, Any] = {
            'config': config,
            'nlu_token': nlu_token,
            'use_secure_channel': use_secure_channel,
            'options': options,
        }
        self.services: AsyncServicesContainer = AsyncServicesContainer(
            agents=Agents(**kwargs),
            aiservices=AIServices(**kwargs),
            ccai_projects=CcaiProjects(**kwargs),
            contexts=Contexts(**kwargs),
            entity_types=EntityTypes(**kwargs),
            intents=Intents(**kwargs),
            operations=Operations(**kwargs),
            project_roles=ProjectRoles(**kwargs),
            project_statistics=ProjectStatistics(**kwargs),
            server_statistics=ServerStatistics(**kwargs),
            sessions=Sessions(**kwargs),
            users=Users(**kwargs),
            utilities=Utilities(**kwargs),
        )
