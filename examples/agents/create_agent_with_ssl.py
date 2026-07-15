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
"""
Create an agent over a TLS-encrypted gRPC channel, with the CA certificate taken from the environment.

The point of this example is the *channel*, not the agent: `create_agent.py` does the same work over
plaintext gRPC. Everything TLS-specific is in `build_tls_client()` below.

Two ingredients are needed for a TLS channel, and BOTH are required:

  1. `Client(..., use_secure_channel=True)`
  2. `ClientConfig(grpc_cert=<the CA certificate>)`

`grpc_cert` is the PEM **contents**, not a path — the SDK does `grpc_cert.encode()` and passes the
bytes to `grpc.ssl_channel_credentials(root_certificates=...)`. Handing it a filename would silently
produce a garbage trust root. The SDK does NOT fall back to the system trust store: a secure channel
without `grpc_cert` raises `ValueError: No grpc certificate found on config`.

    ⚠️ THE CERTIFICATE HERE COMES FROM AN ENVIRONMENT VARIABLE, NOT A FILE.

`ONDEWO_NLU_CAI_GRPC_CERT_BASE64` carries the base64 of the CA PEM. That is the shape a deployment
actually has: a container, a CI job or a Kubernetes Secret injects the certificate into the process
environment, and there is no file on disk to point at. It is base64 because a PEM is multi-line and
an env var in a `.env` file is a single line — the raw text cannot survive a `KEY=VALUE` round trip.
(ondewo-cai uses the same `*_BASE64` convention for a PEM in `ONDEWO_NLU_CAI_RAGFLOW_PUBLIC_KEY_BASE64`.)

Produce the value from the CA that signed the server's certificate:

    base64 -w0 < <path-to>/ondewo-cai/certs/ca-cert.pem

Only the CA is needed. It is public material — the server's private key never leaves the server, and
because the gRPC hop is server-auth TLS (not mutual TLS) the client presents no certificate of its own.
Do NOT put a private key in this variable.

Server side — the cai server must actually be serving TLS on the port you point at:

    make generate_ssl_certificates                                  # in the ondewo-cai repo
    export ONDEWO_NLU_CAI_GRPC_SERVER_USE_INSECURE_CHANNEL=False
    export ONDEWO_NLU_CAI_GRPC_SERVER_KEY_FILE=$(pwd)/certs/server-key.pem
    export ONDEWO_NLU_CAI_GRPC_SERVER_CHAIN_FILE=$(pwd)/certs/server-cert.pem
    python -m ondewo_cai.ondewo_cdls.services.server                # logs "using secure gRPC channel"

The hostname you connect to must appear in the server certificate's SANs, or verification fails with
"Hostname mismatch" even though the CA is correct.
"""

import sys
import uuid
from pathlib import Path

from ondewo.nlu.agent_pb2 import (
    Agent,
    CreateAgentRequest,
)
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from example_env import (  # noqa: E402
    env,
    get_grpc_cert_from_env,
)


def build_tls_client() -> Client:
    """
    Build a client whose gRPC channel is TLS-encrypted, trusting the CA held in the environment.

    Returns:
        Client:
            A client that talks TLS to the server and attaches a Keycloak bearer token to every call.

    Raises:
        ValueError:
            If `ONDEWO_NLU_CAI_GRPC_CERT_BASE64` is not valid base64 of a PEM certificate.
        KeyError:
            If `ONDEWO_NLU_CAI_GRPC_CERT_BASE64` is not set at all.
    """
    # The CA certificate, straight from the environment — no file is read.
    ca_certificate: str = get_grpc_cert_from_env()

    config: ClientConfig = ClientConfig(
        host=env("ONDEWO_NLU_CAI_HOST"),
        port=env("ONDEWO_NLU_CAI_PORT"),
        grpc_cert=ca_certificate,  # PEM CONTENTS, not a path.
        keycloak_url=env("ONDEWO_KEYCLOAK_URL"),
        realm=env("ONDEWO_KEYCLOAK_REALM"),
        client_id=env("ONDEWO_KEYCLOAK_SDK_PUBLIC_CLIENT_ID"),
        user_name=env("ONDEWO_NLU_CAI_USER_NAME"),
        password=env("ONDEWO_NLU_CAI_PASSWORD"),
    )
    return Client(config=config, use_secure_channel=True)


if __name__ == "__main__":
    client: Client = build_tls_client()

    # A unique display name keeps the example re-runnable: the server rejects a duplicate.
    display_name: str = f"tls-example-agent-{uuid.uuid4().hex[:8]}"

    # `default_language_code` must be a FULL code from the LanguageCode enum — a bare "en" is
    # rejected with "Expected a value compatible with enum class 'LanguageCode'".
    agent: Agent = client.services.agents.create_agent(
        CreateAgentRequest(
            agent=Agent(
                display_name=display_name,
                default_language_code=env("ONDEWO_NLU_CAI_LANGUAGE_CODE"),
                supported_language_codes=[env("ONDEWO_NLU_CAI_LANGUAGE_CODE")],
                time_zone="Europe/Vienna",
                nlu_platform="ONDEWO",
            ),
        ),
    )
    project_id: str = agent.parent.split("/")[1]

    print("Created an agent over a TLS gRPC channel:")
    print(f"  display_name : {agent.display_name}")
    print(f"  parent       : {agent.parent}")
    print(f"  project_id   : {project_id}")
    print("The CA certificate came from ONDEWO_NLU_CAI_GRPC_CERT_BASE64 — no certificate file was read.")
