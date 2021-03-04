from dataclasses import dataclass

from dataclasses_json import dataclass_json

from ondewo.utils.base_client_config import BaseClientConfig


@dataclass_json
@dataclass(frozen=True)
class ClientConfig(BaseClientConfig):
    """
    Configuration for the ONDEWO python client.

    Attributes:
        http_token: str ... the token required for getting past nginx
        user_name: str ... the user name for ONDEWO NLU services (e.g., testuser@ondewo.com)
        passwort: str ... the password for ONDEWO NLU services

    """
    http_token: str = ''
    user_name: str = ''
    password: str = ''

    def __post_init__(self) -> None:
        super(ClientConfig, self).__post_init__()

        if not self.http_token:
            raise ValueError(f'The field `http_token` is mandatory in {self.__class__.__name__}.')
        if not self.user_name:
            raise ValueError(f'The field `user_name` is mandatory in {self.__class__.__name__}.')
        if not self.password:
            raise ValueError(f'The field `password` is mandatory in {self.__class__.__name__}.')
