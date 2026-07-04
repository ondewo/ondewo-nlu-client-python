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

from ondewo.utils.base_services_interface import BaseServicesInterface

from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.utils.keycloak import (
    KeycloakTokenProvider,
    get_keycloak_token_provider,
)


class ServicesInterface(BaseServicesInterface, ABC):
    def __init__(
        self,
        config: ClientConfig,
        nlu_token: str,
        use_secure_channel: bool,
        options: Optional[Set[Tuple[str, Any]]] = None,
    ) -> None:
        super(ServicesInterface, self).__init__(config=config, use_secure_channel=use_secure_channel, options=options)
        # When Keycloak headless auth (D18) is configured, every call carries a freshly
        # auto-refreshed `Authorization: Bearer` token; the provider is shared per config so
        # the offline-token ROPC login happens once for all services on the client.
        self._keycloak_provider: Optional[KeycloakTokenProvider] = (
            get_keycloak_token_provider(config) if config.use_keycloak else None
        )
        # Legacy dual-mode metadata: the `cai-token` from the `Login` RPC plus the optional
        # legacy `Authorization: Basic` http_token.
        self._legacy_metadata: List[Tuple[str, str]] = [
            ('cai-token', nlu_token if nlu_token else 'null'),
            ('authorization', config.http_token),
        ]

    @property
    def metadata(self) -> List[Tuple[str, str]]:
        """
        The gRPC metadata attached to every outgoing call.

        With Keycloak auth this rebuilds (and auto-refreshes) the `Authorization: Bearer`
        token on each access; otherwise it returns the legacy `cai-token` metadata.

        Returns:
            List[Tuple[str, str]]: The metadata tuples for the next gRPC call.
        """
        if self._keycloak_provider is not None:
            return self._keycloak_provider.bearer_metadata()
        return self._legacy_metadata

    @metadata.setter
    def metadata(self, value: List[Tuple[str, str]]) -> None:
        """Allow the base class / callers to override the legacy metadata list."""
        self._legacy_metadata = value
