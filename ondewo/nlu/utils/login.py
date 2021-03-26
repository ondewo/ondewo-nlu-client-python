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


from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.services.users import Users
from ondewo.nlu.user_pb2 import LoginRequest, LoginResponse


def login(config: ClientConfig, use_secure_channel: bool) -> str:
    """Log in using the user and password in the client config and return the auth token"""
    request: LoginRequest = LoginRequest(
        user_email=config.user_name,
        password=config.password,
    )
    user_service: Users = Users(config=config, nlu_token='', use_secure_channel=use_secure_channel)
    response: LoginResponse = user_service.login(request)
    nlu_token: str = response.auth_token
    user_service.grpc_channel.close()
    return nlu_token
