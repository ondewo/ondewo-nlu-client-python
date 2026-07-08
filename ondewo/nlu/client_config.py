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
from typing import Optional

from dataclasses_json import dataclass_json
from ondewo.utils.base_client_config import BaseClientConfig


@dataclass_json
@dataclass(frozen=True)
class ClientConfig(BaseClientConfig):
    """
    Configuration for the ONDEWO Python client.

    This class extends `BaseClientConfig` with the authentication details required for
    connecting to ONDEWO NLU services. Authentication is **Keycloak bearer only**:

    * **Keycloak headless offline-token auth (D18)** — set `keycloak_url`, `realm`,
      `client_id`, `user_name`, and `password` (and optionally `token_expiration_in_s`).
      The client performs an ROPC login with `scope=offline_access` against the *public*
      Keycloak SDK client (no `client_secret`), then auto-refreshes the short-lived access
      token and attaches it as `Authorization: Bearer` on every gRPC call.

    When the Keycloak fields are omitted the client sends no auth metadata at all, so the
    connection travels unauthenticated (e.g. against a plaintext server or an Envoy ingress
    that injects the bearer token).

    Attributes:
        user_name (str):
            The user name for authenticating with ONDEWO NLU services.
            Example: 'testuser@ondewo.com'.
        password (str):
            The password associated with the ONDEWO NLU services user.
        keycloak_url (str):
            Base URL of the Keycloak server (the part before `/realms/<realm>`),
            e.g. 'https://my-host/auth'. Required for the Keycloak offline-token path.
        realm (str):
            Keycloak realm name, e.g. 'ondewo-ccai-platform'. Required for the Keycloak path.
        client_id (str):
            The public Keycloak SDK client id, e.g. 'ondewo-nlu-cai-sdk-public'
            (public client, no `client_secret`). Required for the Keycloak path.
        token_expiration_in_s (Optional[int]):
            Bounds how long the auto-refresh loop runs (seconds since login). `None`
            keeps refreshing until the offline session itself expires.
        keycloak_verify_ssl (bool):
            Whether to verify the Keycloak server's TLS certificate on the token-endpoint
            call. Defaults to `True` (secure). Set `False` only for a self-signed/local
            Envoy at `https://localhost:12001/auth`.
    """

    user_name: str = ""
    password: str = ""
    keycloak_url: str = ""
    realm: str = ""
    client_id: str = ""
    token_expiration_in_s: Optional[int] = None
    keycloak_verify_ssl: bool = True

    @property
    def use_keycloak(self) -> bool:
        """
        Whether the Keycloak headless offline-token path (D18) is configured.

        Returns:
            bool: True when `keycloak_url`, `realm`, and `client_id` are all set.
        """
        return bool(self.keycloak_url and self.realm and self.client_id)

    def __post_init__(self) -> None:
        """
        Post-initialization hook to validate the configured authentication path.

        Envoy validates the Bearer JWT, so no separate proxy credential is required. The
        check requires `user_name` and `password`, and additionally requires the full
        Keycloak triple (`keycloak_url`, `realm`, `client_id`) to be all-or-nothing.

        Raises:
            ValueError:
                If `user_name` or `password` is empty, or if the Keycloak fields are only
                partially provided.
        """
        super(ClientConfig, self).__post_init__()

        if not self.user_name:
            raise ValueError(f"The field `user_name` is mandatory in {self.__class__.__name__}.")
        if not self.password:
            raise ValueError(f"The field `password` is mandatory in {self.__class__.__name__}.")

        keycloak_fields: tuple[str, str, str] = (self.keycloak_url, self.realm, self.client_id)
        if any(keycloak_fields) and not all(keycloak_fields):
            raise ValueError(
                "The Keycloak fields `keycloak_url`, `realm`, and `client_id` must be provided "
                f"together in {self.__class__.__name__}."
            )
