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
