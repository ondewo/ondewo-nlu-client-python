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
from typing import (
    Any,
    Optional,
    Set,
    Tuple,
)

from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.services.users import Users
from ondewo.nlu.user_pb2 import (
    LoginRequest,
    LoginResponse,
)


def login(
    config: ClientConfig,
    use_secure_channel: bool,
    options: Optional[Set[Tuple[str, Any]]] = None,
) -> str:
    """
    Log in using the user and password in the client config and returns the auth token, i.e. "cai-token".

    Args:
        config (BaseClientConfig):
            Configuration for the client.
        use_secure_channel (bool):
            Whether to use a secure gRPC channel.
        options (Optional[Set[Tuple[str, Any]]]):
            Additional options for the gRPC channel.

    Returns
        str: returns the auth token, i.e. "cai-token"
    """
    request: LoginRequest = LoginRequest(
        user_email=config.user_name,
        password=config.password,
    )

    user_service: Users = Users(
        config=config,
        nlu_token='',
        use_secure_channel=use_secure_channel,
        options=options,
    )
    response: LoginResponse = user_service.login(request)
    # retrieve the "cai-token"
    nlu_token: str = response.auth_token
    user_service.grpc_channel.close()

    return nlu_token
