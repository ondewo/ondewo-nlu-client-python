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
import sys
from pathlib import Path
import json
from typing import (
    Any,
    Optional,
    Set,
    Tuple,
)

import grpc
import polling

from ondewo.nlu.agent_pb2 import (
    Agent,
    CreateAgentRequest,
    ExportAgentRequest,
    ExportAgentResponse,
    GetAgentRequest,
    ListAgentsRequest,
)
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.intent_pb2 import (
    CreateIntentRequest,
    Intent,
    ListIntentsRequest,
)
from ondewo.nlu.operations_pb2 import (
    GetOperationRequest,
    Operation,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from example_env import (  # noqa: E402
    env,
    get_client_config,
    use_secure_channel,
)

if __name__ == "__main__":
    # The client authenticates directly against Keycloak — no ondewo-aim involved. On construction the SDK
    # performs a one-time ROPC grant (grant_type=password, scope=offline_access) against the *public*
    # `ondewo-nlu-cai-sdk-public` client (so there is no client_secret), then auto-refreshes the short-lived
    # access token in a background thread and sends `Authorization: Bearer` on every call.
    #
    # IMPORTANT — `user_name` must be a 2FA-EXEMPT identity.
    # ROPC is non-interactive and cannot perform a TOTP step, so a normal human user (for whom the realm
    # enforces 2FA) is rejected by Keycloak with:
    #     400 {"error":"invalid_grant","error_description":"Account is not fully set up"}
    # Use a *project technical user* instead: an admin/developer calls `CreateProjectTechnicalUser`, which
    # returns a `username` (NOT an e-mail) plus a one-time password, and is exempt from 2FA. Pass that
    # username here. A human e-mail only works on deployments where 2FA is relaxed (e.g. local dev), so
    # scripts written against one will pass locally and fail in production.
    config: ClientConfig = get_client_config()

    # https://github.com/grpc/grpc-proto/blob/master/grpc/service_config/service_config.proto
    service_config_json: str = json.dumps(
        {
            "methodConfig": [
                {
                    "name": [
                        # To apply retry to all methods, put [{}] as a value in the "name" field
                        # {}
                        # List single  rpc method call
                        {"service": "ondewo.nlu.Users", "method": "CreateUser"},
                        # NOTE: no entry for `ondewo.nlu.Users/Login` — authentication is Keycloak-bearer
                        # only and the client never calls that RPC, so a retry policy for it would never fire.
                    ],
                    "retryPolicy": {
                        "maxAttempts": 10,
                        "initialBackoff": "1.1s",
                        "maxBackoff": "3000s",
                        "backoffMultiplier": 2,
                        "retryableStatusCodes": [
                            grpc.StatusCode.CANCELLED.name,
                            grpc.StatusCode.UNKNOWN.name,
                            grpc.StatusCode.DEADLINE_EXCEEDED.name,
                            grpc.StatusCode.NOT_FOUND.name,
                            grpc.StatusCode.RESOURCE_EXHAUSTED.name,
                            grpc.StatusCode.ABORTED.name,
                            grpc.StatusCode.INTERNAL.name,
                            grpc.StatusCode.UNAVAILABLE.name,
                            grpc.StatusCode.DATA_LOSS.name,
                        ],
                    },
                }
            ]
        }
    )

    options: Set[Tuple[str, Any]] = {
        # Define custom max message sizes: 1MB here is an arbitrary example.
        ("grpc.max_send_message_length", 1024 * 1024),
        ("grpc.max_receive_message_length", 1024 * 1024),
        # Example of setting KeepAlive options through generic channel_args
        ("grpc.keepalive_time_ms", 2**31 - 1),
        ("grpc.keepalive_timeout_ms", 20000),
        ("grpc.keepalive_permit_without_calls", False),
        ("grpc.http2.max_pings_without_data", 2),
        # Example arg requested for the feature
        ("grpc.dns_enable_srv_queries", 1),
        ("grpc.enable_retries", 1),
        ("grpc.service_config", service_config_json),
    }

    client: Client = Client(config=config, use_secure_channel=use_secure_channel(), options=options)

    created_agent: Agent = client.services.agents.create_agent(
        request=CreateAgentRequest(
            agent=Agent(
                display_name="my python agent",
                default_language_code=env("ONDEWO_NLU_CAI_LANGUAGE_CODE"),
                supported_language_codes=[env("ONDEWO_NLU_CAI_LANGUAGE_CODE")],
                time_zone="Europe/Vienna",
                nlu_platform="ONDEWO",
                description="This is an agent created through the python client",
            )
        )
    )

    print(client.services.agents.list_agents(ListAgentsRequest()))
    print(client.services.agents.get_agent(GetAgentRequest(parent=created_agent.parent)))

    created_intent: Intent = client.services.intents.create_intent(
        CreateIntentRequest(
            parent=created_agent.parent,
            language_code=env("ONDEWO_NLU_CAI_LANGUAGE_CODE"),
            intent=Intent(
                display_name="i.my_python_intent",
                training_phrases=[
                    Intent.TrainingPhrase(
                        type=Intent.TrainingPhrase.Type.EXAMPLE,
                        text="This is a training phrase",
                    )
                ],
            ),
        )
    )

    print(
        client.services.intents.list_intents(
            ListIntentsRequest(parent=created_agent.parent, language_code=env("ONDEWO_NLU_CAI_LANGUAGE_CODE"))
        )
    )

    export_operation: Operation = client.services.agents.export_agent(ExportAgentRequest(parent=created_agent.parent))

    polling.poll(
        target=client.services.operations.get_operation,
        step=1,
        args=(GetOperationRequest(name=export_operation.name),),
        check_success=lambda op: op.done,
        timeout=600,  # wait 10 minutes until training is finished
    )

    export_operation_update: Optional[Operation] = client.services.operations.get_operation(
        GetOperationRequest(name=export_operation.name)
    )
    export_response: ExportAgentResponse = ExportAgentResponse()
    if export_operation_update is not None:
        export_operation_update.response.Unpack(export_response)
    assert export_response.agent_content

    with open(env("ONDEWO_NLU_CAI_AGENT_ZIP_PATH"), mode="wb") as zf:
        zf.write(export_response.agent_content)
