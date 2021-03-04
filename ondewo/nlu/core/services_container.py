from dataclasses import dataclass

from ondewo.nlu.services.agents import Agents
from ondewo.nlu.services.aiservices import AIServices
from ondewo.nlu.services.contexts import Contexts
from ondewo.nlu.services.entity_types import EntityTypes
from ondewo.nlu.services.intents import Intents
from ondewo.nlu.services.operations import Operations
from ondewo.nlu.services.project_roles import ProjectRoles
from ondewo.nlu.services.sessions import Sessions
from ondewo.nlu.services.users import Users
from ondewo.utils.base_service_container import BaseServicesContainer


@dataclass
class ServicesContainer(BaseServicesContainer):
    agents: Agents
    aiservices: AIServices
    contexts: Contexts
    entity_types: EntityTypes
    intents: Intents
    operations: Operations
    project_roles: ProjectRoles
    sessions: Sessions
    users: Users
