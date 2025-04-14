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
from dataclasses import dataclass

from ondewo.utils.base_service_container import BaseServicesContainer

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


@dataclass
class AsyncServicesContainer(BaseServicesContainer):
    agents: Agents
    aiservices: AIServices
    ccai_projects: CcaiProjects
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
