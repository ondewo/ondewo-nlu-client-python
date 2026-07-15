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
"""Hermetic tests for how the examples decide between a TLS and a plaintext channel.

TLS needs BOTH halves — `ONDEWO_NLU_CAI_SECURE` asking for it and a CA in
`ONDEWO_NLU_CAI_GRPC_CERT_BASE64` to verify the server with — because the SDK does not fall back to
the system trust store. These tests pin the four combinations and the base64 validation, with no
network and no certificate files.
"""

import base64
import sys
from pathlib import Path
from typing import (
    Iterator,
    Optional,
)

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "examples"))
import example_env  # noqa: E402

_CERT_ENV_VAR: str = "ONDEWO_NLU_CAI_GRPC_CERT_BASE64"
_SECURE_ENV_VAR: str = "ONDEWO_NLU_CAI_SECURE"

# A syntactically valid PEM certificate is all these tests need: nothing here opens a socket, and
# grpc only parses the bytes when a channel is actually dialled.
_CERT_PEM: str = "-----BEGIN CERTIFICATE-----\nMIIBkTCB+w==\n-----END CERTIFICATE-----\n"


@pytest.fixture(autouse=True)
def loaded_environment(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """
    Pretend `environment.env` was already loaded, so the tests never read the developer's real file.

    `example_env` lazily loads the env file on first access, which would make these tests depend on a
    gitignored file that does not exist in CI.

    Yields:
        None
    """
    monkeypatch.setattr(example_env, "_loaded", True)
    yield


def _set_channel_env(
    monkeypatch: pytest.MonkeyPatch,
    secure: str,
    cert_base64: Optional[str],
) -> None:
    """
    Set the two variables that decide the channel type.

    Args:
        monkeypatch (pytest.MonkeyPatch):
            Used to scope the changes to one test.
        secure (str):
            Value for `ONDEWO_NLU_CAI_SECURE`.
        cert_base64 (Optional[str]):
            Value for `ONDEWO_NLU_CAI_GRPC_CERT_BASE64`, or None to leave it unset.

    Returns:
        None
    """
    monkeypatch.setenv(_SECURE_ENV_VAR, secure)
    if cert_base64 is None:
        monkeypatch.delenv(_CERT_ENV_VAR, raising=False)
    else:
        monkeypatch.setenv(_CERT_ENV_VAR, cert_base64)


class TestChannelSelection:
    @staticmethod
    @pytest.mark.parametrize(
        "secure, cert_base64, expected_secure",
        [
            # TLS asked for and a CA to verify with: the only combination that yields a TLS channel.
            ("true", base64.b64encode(_CERT_PEM.encode()).decode(), True),
            # TLS asked for but no CA. The SDK would raise ValueError("No grpc certificate found"),
            # so the examples fall back to plaintext instead of dying on a config error.
            ("true", None, False),
            # An empty value counts as absent, not as a certificate.
            ("true", "   ", False),
            # TLS not asked for: the certificate being available must not silently enable it.
            ("false", base64.b64encode(_CERT_PEM.encode()).decode(), False),
            ("false", None, False),
        ],
    )
    def test_tls_requires_both_the_flag_and_a_certificate(
        monkeypatch: pytest.MonkeyPatch,
        secure: str,
        cert_base64: Optional[str],
        expected_secure: bool,
    ) -> None:
        _set_channel_env(monkeypatch=monkeypatch, secure=secure, cert_base64=cert_base64)

        assert example_env.use_secure_channel() is expected_secure

    @staticmethod
    def test_falling_back_to_plaintext_is_reported_on_stderr(
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """A silent downgrade to plaintext would be the dangerous outcome — it must be visible."""
        _set_channel_env(monkeypatch=monkeypatch, secure="true", cert_base64=None)

        example_env.use_secure_channel()

        stderr: str = capsys.readouterr().err
        assert _CERT_ENV_VAR in stderr
        assert "INSECURE" in stderr

    @staticmethod
    def test_no_warning_when_plaintext_was_what_was_asked_for(
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        _set_channel_env(monkeypatch=monkeypatch, secure="false", cert_base64=None)

        example_env.use_secure_channel()

        assert capsys.readouterr().err == ""


class TestGrpcCert:
    @staticmethod
    def test_certificate_is_decoded_from_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
        _set_channel_env(
            monkeypatch=monkeypatch,
            secure="true",
            cert_base64=base64.b64encode(_CERT_PEM.encode()).decode(),
        )

        assert example_env.get_grpc_cert() == _CERT_PEM

    @staticmethod
    def test_no_certificate_is_supplied_for_a_plaintext_channel(monkeypatch: pytest.MonkeyPatch) -> None:
        """`grpc_cert` must stay None for a plaintext channel, including the fallback case."""
        _set_channel_env(monkeypatch=monkeypatch, secure="true", cert_base64=None)

        assert example_env.get_grpc_cert() is None

    @staticmethod
    @pytest.mark.parametrize(
        "bad_value, expected_message_fragment",
        [
            ("!!! not base64 !!!", "not valid base64"),
            (base64.b64encode(b"this is not a certificate").decode(), "not a PEM certificate"),
        ],
    )
    def test_a_bad_certificate_value_fails_with_an_actionable_message(
        monkeypatch: pytest.MonkeyPatch,
        bad_value: str,
        expected_message_fragment: str,
    ) -> None:
        """Catching this here beats letting it surface later as an opaque TLS handshake failure."""
        _set_channel_env(monkeypatch=monkeypatch, secure="true", cert_base64=bad_value)

        with pytest.raises(ValueError) as exception_info:
            example_env.get_grpc_cert()

        assert expected_message_fragment in str(exception_info.value)
