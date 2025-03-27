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
from dataclasses import dataclass

from dataclasses_json import dataclass_json
from ondewo.utils.base_client_config import BaseClientConfig


@dataclass_json
@dataclass(frozen=True)
class ClientConfig(BaseClientConfig):
    """
    Configuration for the ONDEWO Python client.

    This class extends `BaseClientConfig` to include additional authentication
    details required for connecting to ONDEWO NLU services.

    Attributes:
        http_token (str): The token required for bypassing nginx or other proxies.
        user_name (str): The user name for authenticating with ONDEWO NLU services.
                         Example: 'testuser@ondewo.com'.
        password (str): The password associated with the ONDEWO NLU services user.
    """
    http_token: str = ''
    user_name: str = ''
    password: str = ''

    def __post_init__(self) -> None:
        """
        Post-initialization hook to validate mandatory fields.

        This method is called automatically after the dataclass is initialized.
        It checks if `http_token`, `user_name`, and `password` are provided.
        Raises:
            ValueError: If any of the mandatory fields (`http_token`, `user_name`, or `password`)
                        are empty or not provided.
        """
        super(ClientConfig, self).__post_init__()

        if not self.http_token:
            raise ValueError(f'The field `http_token` is mandatory in {self.__class__.__name__}.')
        if not self.user_name:
            raise ValueError(f'The field `user_name` is mandatory in {self.__class__.__name__}.')
        if not self.password:
            raise ValueError(f'The field `password` is mandatory in {self.__class__.__name__}.')
