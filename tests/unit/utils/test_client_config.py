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
"""Unit tests for `ClientConfig` validation on the bearer-only auth model (D18)."""

import dataclasses
from typing import List

import pytest

from ondewo.nlu.client_config import ClientConfig

HOST: str = "localhost"
PORT: str = "50055"
USERNAME: str = "tech-user@example.com"
PASSWORD: str = "s3cr3t"
KEYCLOAK_URL: str = "https://kc.example.com/auth"
REALM: str = "ondewo-ccai-platform"
CLIENT_ID: str = "ondewo-nlu-cai-sdk-public"
# A fabricated stand-in for a Keycloak offline refresh token.
REFRESH_TOKEN: str = "PLANTED-offline-refresh-token-4f19ac"


class TestNonKeycloakPath:
    """Validation of a config with no Keycloak fields (calls travel unauthenticated)."""

    def test_config_without_keycloak_is_valid_and_not_keycloak(self) -> None:
        """A config with only user_name/password is valid and reports `use_keycloak is False`."""
        config: ClientConfig = ClientConfig(host=HOST, port=PORT, user_name=USERNAME, password=PASSWORD)

        assert config.use_keycloak is False

    def test_no_http_token_field_present(self) -> None:
        """The bearer-only config exposes no legacy `http_token` attribute."""
        config: ClientConfig = ClientConfig(host=HOST, port=PORT, user_name=USERNAME, password=PASSWORD)

        assert not hasattr(config, "http_token")

    def test_missing_user_name_raises(self) -> None:
        """An empty user_name fails `__post_init__` validation with `ValueError`."""
        with pytest.raises(ValueError):
            ClientConfig(host=HOST, port=PORT, password=PASSWORD)

    def test_missing_password_raises(self) -> None:
        """Neither a password nor a refresh token fails `__post_init__` validation."""
        with pytest.raises(ValueError):
            ClientConfig(host=HOST, port=PORT, user_name=USERNAME)


class TestKeycloakPath:
    """Validation of the Keycloak headless offline-token auth path (D18)."""

    def test_full_keycloak_config_is_valid_and_flagged(self) -> None:
        """A complete Keycloak triple plus token_expiration_in_s yields `use_keycloak is True`."""
        config: ClientConfig = ClientConfig(
            host=HOST,
            port=PORT,
            user_name=USERNAME,
            password=PASSWORD,
            keycloak_url=KEYCLOAK_URL,
            realm=REALM,
            client_id=CLIENT_ID,
            token_expiration_in_s=3600,
        )

        assert config.use_keycloak is True
        assert config.token_expiration_in_s == 3600
        assert config.client_id == CLIENT_ID

    def test_token_expiration_optional_defaults_none(self) -> None:
        """Omitting token_expiration_in_s leaves it `None` (unbounded auto-refresh)."""
        config: ClientConfig = ClientConfig(
            host=HOST,
            port=PORT,
            user_name=USERNAME,
            password=PASSWORD,
            keycloak_url=KEYCLOAK_URL,
            realm=REALM,
            client_id=CLIENT_ID,
        )

        assert config.token_expiration_in_s is None
        assert config.use_keycloak is True

    def test_partial_keycloak_config_raises(self) -> None:
        """A partial Keycloak triple (only keycloak_url set) fails the all-or-nothing check."""
        # realm + client_id missing while keycloak_url is set → all-or-nothing violation.
        with pytest.raises(ValueError):
            ClientConfig(
                host=HOST,
                port=PORT,
                user_name=USERNAME,
                password=PASSWORD,
                keycloak_url=KEYCLOAK_URL,
            )

    def test_token_only_config_is_valid_and_still_uses_keycloak(self) -> None:
        """A config carrying an offline token and NO password is valid and Keycloak-enabled.

        `use_keycloak` is computed from the Keycloak triple alone, so it is unaffected by which
        credential was supplied — but a silent `False` here would not fail anything, it would skip
        authentication entirely, so it is asserted rather than reasoned about.
        """
        config: ClientConfig = ClientConfig(
            host=HOST,
            port=PORT,
            user_name=USERNAME,
            keycloak_url=KEYCLOAK_URL,
            realm=REALM,
            client_id=CLIENT_ID,
            refresh_token=REFRESH_TOKEN,
        )

        assert config.password == ""
        assert config.refresh_token == REFRESH_TOKEN
        assert config.use_keycloak is True

    def test_refresh_token_is_the_last_field(self) -> None:
        """`refresh_token` must stay the LAST field of the dataclass.

        `ClientConfig` is frozen and `host`/`port` are positional, so an external caller may be
        constructing it positionally. Inserting the new field mid-list would silently rebind such a
        caller's arguments, and no construction site in this repository — all keyword-based — could
        see it. This guard is that missing signal.
        """
        field_names: List[str] = [field.name for field in dataclasses.fields(ClientConfig)]

        assert field_names[-1] == "refresh_token"

    def test_a_config_with_neither_credential_raises(self) -> None:
        """A config with no password AND no refresh token still fails at construction.

        The credential check is widened, never deleted: without it a credential-less config would
        construct happily and fail later at the token endpoint, far from its cause.
        """
        with pytest.raises(ValueError):
            ClientConfig(
                host=HOST,
                port=PORT,
                user_name=USERNAME,
                keycloak_url=KEYCLOAK_URL,
                realm=REALM,
                client_id=CLIENT_ID,
            )

    def test_no_client_secret_field_present(self) -> None:
        """The public SDK config exposes no client_secret attribute (Q1)."""
        # Q1: the public SDK client has no client_secret — the config must not expose one.
        config: ClientConfig = ClientConfig(
            host=HOST,
            port=PORT,
            user_name=USERNAME,
            password=PASSWORD,
            keycloak_url=KEYCLOAK_URL,
            realm=REALM,
            client_id=CLIENT_ID,
        )

        assert not hasattr(config, "client_secret")
