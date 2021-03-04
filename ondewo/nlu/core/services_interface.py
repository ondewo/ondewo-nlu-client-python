from abc import ABC
from typing import Tuple, List

from ondewo.nlu.client_config import ClientConfig
from ondewo.utils.base_services_interface import BaseServicesInterface


class ServicesInterface(BaseServicesInterface, ABC):
    def __init__(
            self,
            config: ClientConfig,
            nlu_token: str,
            use_secure_channel: bool,
    ) -> None:
        super(ServicesInterface, self).__init__(config=config, use_secure_channel=use_secure_channel)
        self.metadata: List[Tuple[str, str]] = [
            ('cai-token', nlu_token if nlu_token else 'null'),
            ('authorization', config.http_token),
        ]
