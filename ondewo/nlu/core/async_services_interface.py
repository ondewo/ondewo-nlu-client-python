# Copyright 2021-2025 ONDEWO GmbH
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
from typing import (
    Any,
    List,
    Optional,
    Set,
    Tuple,
)

from ondewo.utils.async_base_services_interface import AsyncBaseServicesInterface

from ondewo.nlu.client_config import ClientConfig


class AsyncServicesInterface(AsyncBaseServicesInterface, ABC):
    def __init__(
        self,
        config: ClientConfig,
        nlu_token: str,
        use_secure_channel: bool,
        options: Optional[Set[Tuple[str, Any]]] = None,
    ) -> None:
        super(AsyncServicesInterface, self).__init__(
            config=config,
            use_secure_channel=use_secure_channel,
            options=options,
        )
        self.metadata: List[Tuple[str, str]] = [
            ('cai-token', nlu_token if nlu_token else 'null'),
            ('authorization', config.http_token),
        ]
