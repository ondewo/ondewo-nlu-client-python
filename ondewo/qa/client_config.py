from dataclasses import dataclass

from dataclasses_json import dataclass_json

from ondewo.utils.base_client_config import BaseClientConfig


@dataclass_json
@dataclass(frozen=True)
class ClientConfig(BaseClientConfig):
    # Note: this empty dataclass sets the config for extendability and future forward-compatible changes
    pass
