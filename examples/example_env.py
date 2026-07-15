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
"""Shared configuration loader for the examples.

Every example reads its settings from ``examples/environment.env`` instead of carrying hard-coded
placeholders, so a single file configures the whole tree. Copy the template and edit it once::

    cp examples/environment.env.template examples/environment.env
    # then fill in host/port, the Keycloak settings and your credentials

Usage from any example::

    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from example_env import env, get_client_config

    config = get_client_config()

The parsing is deliberately stdlib-only: the examples are meant to be copy-pasteable and the
client library must not grow a runtime dependency (e.g. ``python-dotenv``) just to run them.

Real environment variables always win over the file, so a CI job or a shell ``export`` can
override any value without editing it.
"""

import base64
import binascii
import os
from pathlib import Path
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)

from google.protobuf.message import Message

from ondewo.nlu.client_config import ClientConfig

#: Location of the env file: ``examples/environment.env``, next to this module.
ENVIRONMENT_FILE: Path = Path(__file__).resolve().parent / "environment.env"

_TRUE_VALUES: frozenset = frozenset({"1", "true", "t", "yes", "y", "on"})

_loaded: bool = False


def load_environment(path: Optional[Path] = None, override: bool = False) -> Dict[str, str]:
    """
    Parse an ``.env``-style file and merge it into ``os.environ``.

    Supports ``KEY=VALUE`` lines, ``#`` comments, blank lines, an optional ``export `` prefix, and
    optional single/double quotes around the value.

    Args:
        path (Optional[Path]):
            The file to read. Defaults to :data:`ENVIRONMENT_FILE`.
        override (bool):
            When ``False`` (the default) an existing real environment variable wins over the file,
            so a shell ``export`` or a CI setting can override it without editing the file.

    Returns:
        Dict[str, str]:
            The key/value pairs found in the file (whether or not they were applied to
            ``os.environ``).

    Raises:
        FileNotFoundError:
            If the env file does not exist, with a hint to copy the template.
    """
    env_path: Path = path or ENVIRONMENT_FILE
    if not env_path.is_file():
        raise FileNotFoundError(
            f"{env_path} not found. Copy the template and fill it in:\n"
            f"    cp {env_path.with_suffix('.env.template').name} {env_path.name}",
        )

    values: Dict[str, str] = {}
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line: str = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[len("export ") :]
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        values[key] = value
        if override or key not in os.environ:
            os.environ[key] = value

    global _loaded
    _loaded = True
    return values


def env(key: str, default: Optional[str] = None) -> str:
    """
    Read a setting, loading ``environment.env`` on first use.

    Args:
        key (str):
            The variable name.
        default (Optional[str]):
            Value to return when the variable is absent. When ``None`` the variable is required.

    Returns:
        str:
            The value.

    Raises:
        KeyError:
            If the variable is not set and no default was given.
    """
    if not _loaded:
        load_environment()
    value: Optional[str] = os.environ.get(key, default)
    if value is None:
        raise KeyError(f"{key} is not set — add it to {ENVIRONMENT_FILE}")
    return value


def env_bool(key: str, default: bool = False) -> bool:
    """
    Read a boolean setting (``true/1/yes/on`` are true, case-insensitive).

    Args:
        key (str):
            The variable name.
        default (bool):
            Value to return when the variable is absent.

    Returns:
        bool:
            The parsed value.
    """
    raw: str = env(key, str(default))
    return raw.strip().lower() in _TRUE_VALUES


def get_client_config() -> ClientConfig:
    """
    Build a :class:`ClientConfig` for the headless Keycloak auth flow (D18) from the env file.

    The SDK performs a one-time ROPC grant (``grant_type=password``, ``scope=offline_access``)
    against the **public** SDK client — so no client secret — then auto-refreshes the access token
    and attaches ``Authorization: Bearer`` to every call. No ondewo-aim involved.

    ⚠️ ``ONDEWO_NLU_CAI_USER_NAME`` must be a **2FA-exempt** identity. ROPC cannot perform an
    interactive TOTP step, so a normal human user is rejected by Keycloak with
    ``400 invalid_grant: "Account is not fully set up"``. Use a project technical user's
    *username* (see ``examples/agents/create_and_use_project_technical_user.py``).

    When ``ONDEWO_NLU_CAI_SECURE`` is true the config also carries ``grpc_cert``, taken from
    ``ONDEWO_NLU_CAI_GRPC_CERT_BASE64``. The SDK requires it for a TLS channel: it does NOT fall back
    to the system trust store, it raises ``ValueError: No grpc certificate found``.

    Returns:
        ClientConfig:
            The configuration for :class:`ondewo.nlu.client.Client`.

    Raises:
        KeyError:
            If a TLS channel is requested but ``ONDEWO_NLU_CAI_GRPC_CERT_BASE64`` is not set.
        ValueError:
            If that value is not valid base64 of a PEM certificate.
    """
    return ClientConfig(
        host=env("ONDEWO_NLU_CAI_HOST"),
        port=env("ONDEWO_NLU_CAI_PORT"),
        grpc_cert=get_grpc_cert(),
        keycloak_url=env("ONDEWO_KEYCLOAK_URL"),
        realm=env("ONDEWO_KEYCLOAK_REALM"),
        client_id=env("ONDEWO_KEYCLOAK_SDK_PUBLIC_CLIENT_ID"),
        user_name=env("ONDEWO_NLU_CAI_USER_NAME"),
        password=env("ONDEWO_NLU_CAI_PASSWORD"),
    )


def get_grpc_cert_from_env() -> str:
    """
    Read the CA certificate straight out of the environment, with no file involved.

    ``ONDEWO_NLU_CAI_GRPC_CERT_BASE64`` holds the base64 of the CA PEM. It is base64 rather than the
    raw PEM because a PEM is multi-line and an env file is line-based, so the raw text cannot survive
    a ``KEY=VALUE`` round trip. Encoding it keeps the whole certificate in a single value that a
    container runtime, a CI secret or a k8s Secret can inject directly — the deployment shape where
    there is no file to point at. ondewo-cai uses the same ``*_BASE64`` convention for the PEM in
    ``ONDEWO_NLU_CAI_RAGFLOW_PUBLIC_KEY_BASE64``.

    Produce the value with:
        base64 -w0 < ondewo-cai/certs/ca-cert.pem

    Returns:
        str:
            The CA PEM contents, ready to hand to ``ClientConfig.grpc_cert``.

    Raises:
        KeyError:
            If ``ONDEWO_NLU_CAI_GRPC_CERT_BASE64`` is not set.
        ValueError:
            If the value is not valid base64, or does not decode to a PEM certificate — caught here
            rather than surfacing later as an opaque TLS handshake failure.
    """
    raw: str = env("ONDEWO_NLU_CAI_GRPC_CERT_BASE64")
    try:
        pem: str = base64.b64decode(raw, validate=True).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError) as error:
        raise ValueError(
            "ONDEWO_NLU_CAI_GRPC_CERT_BASE64 is not valid base64 of a PEM certificate. Regenerate it "
            "with: base64 -w0 < <path-to>/ondewo-cai/certs/ca-cert.pem",
        ) from error
    if "BEGIN CERTIFICATE" not in pem:
        raise ValueError(
            "ONDEWO_NLU_CAI_GRPC_CERT_BASE64 decodes to something that is not a PEM certificate "
            f"(it starts with {pem[:32]!r}). It must be the base64 of the CA certificate that SIGNED "
            "the server's certificate, i.e. ondewo-cai/certs/ca-cert.pem — not the server cert, and "
            "not a private key.",
        )
    return pem


def get_grpc_cert() -> Optional[str]:
    """
    Return the CA certificate that signs the server's gRPC certificate, when TLS is in use.

    The certificate always comes from the environment — there is deliberately no file-path option.
    See :func:`get_grpc_cert_from_env` for why it is base64.

    Returns:
        Optional[str]:
            The CA PEM contents, or ``None`` when running against a plaintext server.

    Raises:
        KeyError:
            If TLS is requested but ``ONDEWO_NLU_CAI_GRPC_CERT_BASE64`` is not set.
        ValueError:
            If the value is not valid base64 of a PEM certificate.
    """
    if not use_secure_channel():
        return None
    return get_grpc_cert_from_env()


def use_secure_channel() -> bool:
    """
    Whether the gRPC channel should be TLS-secured.

    Returns:
        bool:
            ``ONDEWO_NLU_CAI_SECURE`` as a boolean; ``False`` by default (plaintext local server).
    """
    return env_bool("ONDEWO_NLU_CAI_SECURE", default=False)


# The server owns these fields and stamps them itself. It returns them on every read, but *rejects*
# them on Create/Update with "Expected field to be unset", so anything read back from the server has
# to be stripped before it can be written again. They sit not only on the top-level resource but
# also on its nested messages (an intent's training phrases, an entity type's entities, ...), which
# is why `clear_server_owned_fields` recurses.
SERVER_OWNED_FIELDS: Tuple[str, ...] = (
    "created_at",
    "created_by",
    "modified_at",
    "modified_by",
)


def clear_server_owned_fields(message: Message, clear_resource_names: bool = False) -> None:
    """
    Strip the server-owned fields from a message and everything nested inside it, in place.

    Use this for the read-modify-write pattern: take a resource returned by a Get/List call, change
    it, and send it back in an Update — without this the server rejects the write.

    Args:
        message (Message):
            The protobuf message to clean. Modified in place.
        clear_resource_names (bool):
            Whether to also drop the server-assigned ``name`` of the resource and of every message
            nested in it. Set this when *re-creating* a resource somewhere else, so the target server
            assigns fresh ids — keeping the old ones makes the create collide with the rows they
            already identify. Leave it ``False`` for an Update, which needs the resource name to know
            what it is updating.

    Returns:
        None
    """
    if clear_resource_names and "name" in {field.name for field in message.DESCRIPTOR.fields}:
        message.ClearField("name")

    for field, value in message.ListFields():
        if field.name in SERVER_OWNED_FIELDS:
            message.ClearField(field.name)
        elif field.message_type is not None and not field.message_type.GetOptions().map_entry:
            # `message_type` is set for message fields and None for scalar ones, so this both selects
            # the fields worth recursing into and skips map entries (whose values are not messages).
            # A singular message field hands back the message itself, a repeated one a container of
            # them. Telling them apart by the value's type keeps this working across protobuf
            # versions, which have moved the descriptor's repeated-ness flag around.
            nested: List[Message] = [value] if isinstance(value, Message) else list(value)
            for item in nested:
                clear_server_owned_fields(message=item, clear_resource_names=clear_resource_names)
