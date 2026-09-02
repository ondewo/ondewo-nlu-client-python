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
from dataclasses import dataclass, fields
from typing import Any, ClassVar, FrozenSet, List, Optional

from ondewo.utils.base_client_config import BaseClientConfig


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
    * **Handed-off offline token** — set `refresh_token` instead of `password`. The client
      then never sends a password grant at all: it exchanges the handed-off offline token
      for an access token and auto-refreshes exactly as above. This exists because Keycloak's
      brute-force detection counts failed *logins*, so N processes booting at once with the
      same technical user are a burst the realm penalises, while N concurrent refresh grants
      are not.

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
        refresh_token (str):
            A Keycloak *offline* refresh token handed to this client instead of a password.
            When set, the client skips the ROPC password grant entirely and bootstraps from
            this token. At least one of `password` and `refresh_token` must be provided; when
            BOTH are set the refresh token wins and no password grant is ever sent. There is
            deliberately no fallback to the password if the offline token is rejected -- a
            silent fallback would reintroduce exactly the login burst this field exists to
            avoid, at the least predictable moment.
    """

    user_name: str = ""
    password: str = ""
    keycloak_url: str = ""
    realm: str = ""
    client_id: str = ""
    token_expiration_in_s: Optional[int] = None
    keycloak_verify_ssl: bool = True
    # APPENDED LAST, deliberately. The dataclass is frozen and `host`/`port` are positional, so an
    # external caller may be passing fields positionally; inserting mid-list would silently rebind
    # their arguments. No test in this repository could see that, because every construction site
    # here uses keyword arguments.
    refresh_token: str = ""

    #: Fields whose value must never be rendered. ``grpc_cert`` is PEM material, ``password`` is the
    #: ROPC login secret and ``refresh_token`` is a long-lived offline bearer credential; all three
    #: are printed verbatim by the ``__repr__`` ``@dataclass`` generates. Matching here is by EXACT
    #: field name -- unlike ondewo-vtsi's substring-matching ``SECRET_NAME_TOKENS`` -- so a new
    #: secret field is rendered in full until it is named on this line.
    SECRET_FIELD_NAMES: ClassVar[FrozenSet[str]] = frozenset({"password", "grpc_cert", "refresh_token"})

    def __repr__(self) -> str:
        """
        Render the config without its credential material.

        ``@dataclass`` generates a ``__repr__`` that prints every field, so any caller doing
        ``log.debug(f"...{config}")`` -- or a bare traceback carrying locals -- writes the ROPC
        password and the gRPC certificate to its logs in clear text. Downstream services do exactly
        that: a repository-wide sweep in ondewo-vtsi found this class among its leaking dataclasses.

        An EMPTY secret still renders as ``''`` rather than as ``***REDACTED***``. The distinction is
        deliberate: the marker reads as "this is set and sensitive", which is actively misleading
        when the real problem is that nobody set it -- usually the very thing being debugged.

        Returns:
            str:
                ``ClientConfig(host=..., password=***REDACTED***, ...)``.
        """
        rendered: List[str] = []
        for field in fields(self):
            value: Any = getattr(self, field.name, None)
            if field.name in self.SECRET_FIELD_NAMES and value:
                rendered.append(f"{field.name}='***REDACTED***'")
            else:
                rendered.append(f"{field.name}={value!r}")
        return f"{type(self).__name__}({', '.join(rendered)})"

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
        check requires `user_name` and AT LEAST ONE credential -- `password` (ROPC login) or
        `refresh_token` (a handed-off offline token) -- and additionally requires the full
        Keycloak triple (`keycloak_url`, `realm`, `client_id`) to be all-or-nothing. Supplying
        both credentials is allowed and is the normal shape mid-migration; the refresh token is
        the one that gets used.

        The credential check is WIDENED rather than removed. Dropping it would let a
        credential-less config construct successfully and fail later at the token endpoint,
        which turns a constructor precondition into a runtime failure far from its cause.

        Raises:
            ValueError:
                If `user_name` is empty, if NEITHER `password` nor `refresh_token` is set, or
                if the Keycloak fields are only partially provided.
        """
        super(ClientConfig, self).__post_init__()

        if not self.user_name:
            raise ValueError(f"The field `user_name` is mandatory in {self.__class__.__name__}.")
        if not self.password and not self.refresh_token:
            raise ValueError(
                f"Either the field `password` or the field `refresh_token` is mandatory in {self.__class__.__name__}."
            )

        keycloak_fields: tuple[str, str, str] = (self.keycloak_url, self.realm, self.client_id)
        if any(keycloak_fields) and not all(keycloak_fields):
            raise ValueError(
                "The Keycloak fields `keycloak_url`, `realm`, and `client_id` must be provided "
                f"together in {self.__class__.__name__}."
            )
