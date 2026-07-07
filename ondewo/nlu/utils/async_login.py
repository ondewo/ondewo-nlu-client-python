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


async def login(
    config: ClientConfig,
    use_secure_channel: bool,
    options: Optional[Set[Tuple[str, Any]]] = None,
) -> str:
    """
    No-op async login retained for backward compatibility with the generated client.

    Authentication is Keycloak bearer only: the access token is attached as
    `Authorization: Bearer` by the services interface. The legacy `Login` RPC is never
    called, so this always returns an empty string.

    Args:
        config (ClientConfig): Configuration for the client.
        use_secure_channel (bool): Whether to use a secure gRPC channel.
        options (Optional[Set[Tuple[str, Any]]]): Additional options for the gRPC channel.

    Returns:
        str: Always an empty string (no legacy token is issued).
    """
    return ''
