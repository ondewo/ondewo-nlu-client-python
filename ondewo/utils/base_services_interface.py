from abc import abstractmethod, ABC
from logging import warning
from typing import Tuple, List, Any, Optional, Set, Dict

import grpc

from ondewo.utils.base_client_config import BaseClientConfig

MAX_MESSAGE_LENGTH = 20 * 1024 * 1024  # 20MB


def get_secure_channel(host: str,
                       cert: str,
                       options: Optional[List[Tuple[str, Any]]] = None, ) -> grpc.Channel:
    credentials = grpc.ssl_channel_credentials(root_certificates=cert)
    return grpc.secure_channel(host, credentials, options=options)


def _get_grpc_channel(config: BaseClientConfig,
                      use_secure_channel: bool,
                      options: Optional[List[Tuple[str, Any]]] = None, ) -> grpc.Channel:
    if not use_secure_channel:
        warning('Using insecure grpc channel.')
        return grpc.insecure_channel(target=config.host_and_port, options=options)

    if not config.grpc_cert:
        raise ValueError(f'No grpc certificate found on config {config}.')

    return get_secure_channel(
        host=config.host_and_port,
        cert=config.grpc_cert,
        options=options,
    )


class BaseServicesInterface(ABC):
    def __init__(
            self,
            config: BaseClientConfig,
            use_secure_channel: bool,
            options: Optional[Set[Tuple[str, Any]]] = None,
    ) -> None:
        default_options: Dict[str, Any] = {
            'grpc.max_send_message_length': MAX_MESSAGE_LENGTH,
            'grpc.max_receive_message_length': MAX_MESSAGE_LENGTH,
        }

        if options:
            default_options = {**default_options, **options}

        opt: List[Tuple[str, Any]] = [(k, default_options[k]) for k in default_options.keys()]

        self.grpc_channel: grpc.Channel = _get_grpc_channel(
            config,
            use_secure_channel=use_secure_channel,
            options=opt
        )

    @property
    @abstractmethod
    def stub(self) -> Any:
        pass
