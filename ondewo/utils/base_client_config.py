from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class BaseClientConfig:
    """
    Configuration for the ONDEWO python client.

    Attributes:
        host: str ... IP address of the ONDEWO QA services host (e.g. 'localhost', '127.22.444.11', etc)
        port: str ... port of the ONDEWO QA services host (e.g. '50444', etc)
        grpc_cert: Optional[str] = None ... the certificate required for setting up a secure grpc channel;
            this field must be set unless the client is instantiated using `use_secure_channel=False`
            (not recommended)

    """
    host: str
    port: str
    grpc_cert: Optional[str] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, 'grpc_cert', self.grpc_cert.encode() if self.grpc_cert else self.grpc_cert)

    @property
    def host_and_port(self) -> str:
        return f'{self.host}:{self.port}'
