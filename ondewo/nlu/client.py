# Copyright 2021 ONDEWO GmbH
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


from typing import Dict, Any

from ondewo.utils.base_client import BaseClient
from ondewo.utils.base_client_config import BaseClientConfig

from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.core.services_container import ServicesContainer
from ondewo.nlu.services.agents import Agents
from ondewo.nlu.services.aiservices import AIServices
from ondewo.nlu.services.contexts import Contexts
from ondewo.nlu.services.entity_types import EntityTypes
from ondewo.nlu.services.intents import Intents
from ondewo.nlu.services.operations import Operations
from ondewo.nlu.services.project_roles import ProjectRoles
from ondewo.nlu.services.project_statistics import ProjectStatistics
from ondewo.nlu.services.server_statistics import ServerStatistics
from ondewo.nlu.services.sessions import Sessions
from ondewo.nlu.services.users import Users
from ondewo.nlu.services.utilities import Utilities
from ondewo.nlu.utils.login import login


class Client(BaseClient):
    """
    The core python client for interacting with ONDEWO NLU services.
    """

    def _initialize_services(self, config: BaseClientConfig, use_secure_channel: bool) -> None:
        """
        Login with the current config and setup the services in self.services

        Returns:
            None
        """
        if not isinstance(config, ClientConfig):
            raise ValueError('The provided config must be of type `ondewo.nlu.client_config.ClientConfig`')

        nlu_token: str = login(config=config, use_secure_channel=use_secure_channel)
        kwargs: Dict[str, Any] = {
            'config': config,
            'nlu_token': nlu_token,
            'use_secure_channel': use_secure_channel,
        }
        self.services: ServicesContainer = ServicesContainer(
            agents=Agents(**kwargs),
            aiservices=AIServices(**kwargs),
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
