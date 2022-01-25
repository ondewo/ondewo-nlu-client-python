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


from dataclasses import dataclass

from ondewo.utils.base_service_container import BaseServicesContainer

from ondewo.nlu.project_statistics_pb2_grpc import ProjectStatistics
from ondewo.nlu.services.agents import Agents
from ondewo.nlu.services.aiservices import AIServices
from ondewo.nlu.services.contexts import Contexts
from ondewo.nlu.services.entity_types import EntityTypes
from ondewo.nlu.services.intents import Intents
from ondewo.nlu.services.operations import Operations
from ondewo.nlu.services.project_roles import ProjectRoles
from ondewo.nlu.services.server_statistics import ServerStatistics
from ondewo.nlu.services.sessions import Sessions
from ondewo.nlu.services.users import Users
from ondewo.nlu.services.utilities import Utilities


@dataclass
class ServicesContainer(BaseServicesContainer):
    agents: Agents
    aiservices: AIServices
    contexts: Contexts
    entity_types: EntityTypes
    intents: Intents
    operations: Operations
    project_roles: ProjectRoles
    project_statistics: ProjectStatistics
    server_statistics: ServerStatistics
    sessions: Sessions
    users: Users
    utilities: Utilities
