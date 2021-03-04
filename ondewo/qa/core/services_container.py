from dataclasses import dataclass

from ondewo.qa.services.qa import QA
from ondewo.utils.base_service_container import BaseServicesContainer


@dataclass
class ServicesContainer(BaseServicesContainer):
    qa: QA
