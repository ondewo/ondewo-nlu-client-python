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
