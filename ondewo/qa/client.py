from ondewo.nlu.session_pb2 import TextInput
from ondewo.qa.client_config import ClientConfig
from ondewo.qa.core.services_container import ServicesContainer
from ondewo.qa.qa_pb2 import GetAnswerRequest
from ondewo.qa.services.qa import QA
from ondewo.utils.base_client import BaseClient
from ondewo.utils.base_client_config import BaseClientConfig


class Client(BaseClient):
    """
    The core python client for interacting with Question & Answering services.
    """

    def __init__(self, config: ClientConfig, use_secure_channel: bool = True) -> None:
        super(Client, self).__init__(config=config, use_secure_channel=use_secure_channel)
        self._connection_trial()

    def _initialize_services(self, config: BaseClientConfig, use_secure_channel: bool) -> None:
        """
        Setup the services in self.services

        Returns:
            None
        """
        if not isinstance(config, ClientConfig):
            raise ValueError('The provided config must be of type `ondewo.qa.client_config.ClientConfig`')

        self.services: ServicesContainer = ServicesContainer(
            qa=QA(config=config, use_secure_channel=use_secure_channel),
        )

    def _connection_trial(self) -> None:
        self.services.qa.get_answer(GetAnswerRequest(text=TextInput(text='test'), max_num_answers=1))
