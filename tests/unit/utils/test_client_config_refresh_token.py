"""``ClientConfig.refresh_token``: a handed-off Keycloak offline token instead of a password.

Shared by every ondewo python client SDK (only the imports, the user-name keyword and the name of the
"Keycloak configured" property differ). A token-only config must construct, must count as Keycloak
auth, must reach the token provider, and must never print the token.
"""

import dataclasses
import weakref
from typing import Any, Dict, List

import pytest

from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.utils import keycloak as km

KEYCLOAK: Dict[str, Any] = {
    "host": "localhost",
    "port": "50051",
    "keycloak_url": "https://keycloak.example/auth",
    "realm": "ondewo-test-realm",
    "client_id": "ondewo-test-sdk-public",
    "user_name": "technical-user@example.com",
}
OFFLINE_TOKEN: str = "off-handed-secret-31"


def config(**overrides: Any) -> ClientConfig:
    fields: Dict[str, Any] = dict(KEYCLOAK)
    fields.update(overrides)
    return ClientConfig(**fields)


def test_refresh_token_is_the_last_field_so_positional_callers_keep_their_meaning() -> None:
    assert [field.name for field in dataclasses.fields(ClientConfig)][-1] == "refresh_token"


def test_a_token_only_config_constructs_and_counts_as_keycloak_auth() -> None:
    token_only: ClientConfig = config(refresh_token=OFFLINE_TOKEN)
    assert token_only.refresh_token == OFFLINE_TOKEN
    assert token_only.use_keycloak


def test_a_config_with_neither_credential_is_refused_at_construction() -> None:
    with pytest.raises(ValueError, match="refresh_token"):
        config()


def test_a_password_config_is_unchanged() -> None:
    assert config(password="pw").use_keycloak


def test_the_refresh_token_is_redacted_in_the_repr() -> None:
    rendered: str = repr(config(refresh_token=OFFLINE_TOKEN))
    assert OFFLINE_TOKEN not in rendered
    assert "refresh_token='***REDACTED***'" in rendered


def test_a_token_only_config_reaches_the_provider_with_the_token_and_no_password(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    constructed: List[Dict[str, Any]] = []

    class Recorder:
        def __init__(self, **kwargs: Any) -> None:
            constructed.append(kwargs)

    monkeypatch.setattr(km, "KeycloakTokenProvider", Recorder)
    monkeypatch.setattr(km, "_PROVIDER_REGISTRY", weakref.WeakValueDictionary())

    provider: Any = km.get_keycloak_token_provider(config(refresh_token=OFFLINE_TOKEN))

    assert isinstance(provider, Recorder)
    assert constructed[0]["refresh_token"] == OFFLINE_TOKEN
    assert not constructed[0]["password"]
