# Copyright 2021-2026 ONDEWO GmbH
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
"""
``ClientConfig`` must not print its password or its certificate.

``@dataclass`` generates a ``__repr__`` that prints every field, so before this guard any caller
doing ``log.debug(f"...{config}")`` -- or any traceback carrying locals -- wrote the ROPC password
and the gRPC certificate to its logs in clear text. Downstream consumers really do log config
objects: a repository-wide sweep in ondewo-vtsi found this class among the leakers, alongside its
own.

The assertions are behavioural (build the object, read its ``repr``) rather than a source grep,
because a grep for ``__repr__`` passes just as well for a ``__repr__`` that prints the secret anyway.
"""

from typing import Any, Dict

from ondewo.nlu.client_config import ClientConfig

#: Distinctive, so a match cannot be a coincidence of a field name or a host.
PASSWORD: str = "PLANTED-password-6b21fa"
GRPC_CERT: str = "PLANTED-BEGIN-CERTIFICATE-91cd3e"
REFRESH_TOKEN: str = "PLANTED-offline-refresh-token-4f19ac"
HOST: str = "planted-host.invalid"
USER: str = "planted-user@invalid"


def _config(**overrides: Any) -> ClientConfig:
    kwargs: Dict[str, Any] = {
        "host": HOST,
        "port": 50055,
        "grpc_cert": GRPC_CERT,
        "user_name": USER,
        "password": PASSWORD,
        "refresh_token": REFRESH_TOKEN,
    }
    kwargs.update(overrides)
    return ClientConfig(**kwargs)


class TestClientConfigReprRedactsSecrets:
    def test_the_password_is_not_printed(self) -> None:
        config: ClientConfig = _config()
        # Read the ATTRIBUTE to prove the secret is really on the object. Using repr for this would
        # make the test unfalsifiable, since repr is the thing under test.
        assert config.password == PASSWORD
        assert PASSWORD not in repr(config)
        assert "***REDACTED***" in repr(config)

    def test_the_grpc_certificate_is_not_printed(self) -> None:
        config: ClientConfig = _config()
        # BaseClientConfig.__post_init__ ENCODES the certificate, so the stored value is bytes.
        # Compared against the str here, this "is it really planted" check would fail while the
        # redaction it guards was working perfectly -- a red test that says nothing about the code.
        assert config.grpc_cert == GRPC_CERT.encode()
        assert GRPC_CERT not in repr(config)

    def test_the_offline_refresh_token_is_not_printed(self) -> None:
        # A handed-off Keycloak offline token is a long-lived bearer credential: anyone holding it
        # mints access tokens for the life of the offline session, with no password policy and no
        # realm login in the way. SECRET_FIELD_NAMES matches by EXACT field name -- unlike
        # ondewo-vtsi's substring-matching SECRET_NAME_TOKENS, which already covers "token" -- so
        # checking the downstream list and inferring this one leaves the token printed in full.
        config: ClientConfig = _config()
        # Read the ATTRIBUTE to prove the secret is really on the object; using repr for this would
        # make the test unfalsifiable, since repr is the thing under test.
        assert config.refresh_token == REFRESH_TOKEN
        assert REFRESH_TOKEN not in repr(config)

    def test_an_unset_offline_refresh_token_is_not_reported_as_present(self) -> None:
        # The common case is a password config, which carries no token at all. Rendering that as
        # ***REDACTED*** would read as "a token is set", hiding the very state being debugged.
        assert "refresh_token=''" in repr(_config(refresh_token=""))

    def test_str_is_redacted_too(self) -> None:
        # `str()` falls back to `__repr__` unless `__str__` is defined; assert it explicitly so a
        # later `__str__` cannot reopen the hole while this file still passes.
        assert PASSWORD not in str(_config())

    def test_the_non_secret_fields_survive(self) -> None:
        # Redaction must not be satisfied by printing nothing: host and user are what make the line
        # diagnosable, and neither is a secret.
        rendered: str = repr(_config())
        assert HOST in rendered
        assert USER in rendered

    def test_an_unset_secret_is_not_reported_as_present(self) -> None:
        # An empty secret renders as '' and NOT as ***REDACTED***. The marker reads as "set and
        # sensitive", which is actively misleading when the real fault is that nobody set it.
        rendered: str = repr(_config(grpc_cert=""))
        assert "grpc_cert=''" in rendered
