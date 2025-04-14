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

if __name__ == "__main__":
    config: ClientConfig = ClientConfig(
        host='localhost',
        port='1234',
        http_token='<http/root token>',
        user_name='<e-mail of user>',
        password='<password of user>',
    )

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
                        {"service": "ondewo.nlu.Users", "method": "Login"},
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
        ("grpc.keepalive_time_ms", 2 ** 31 - 1),
        ("grpc.keepalive_timeout_ms", 20000),
        ("grpc.keepalive_permit_without_calls", False),
        ("grpc.http2.max_pings_without_data", 2),
        # Example arg requested for the feature
        ("grpc.dns_enable_srv_queries", 1),
        ("grpc.enable_retries", 1),
        ("grpc.service_config", service_config_json)
    }

    client: Client = Client(config=config, use_secure_channel=False, options=options)

    created_agent: Agent = client.services.agents.create_agent(
        request=CreateAgentRequest(
            agent=Agent(
                display_name="my python agent",
                default_language_code="en",
                supported_language_codes=["en"],
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
            language_code="en",
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
            ListIntentsRequest(parent=created_agent.parent, language_code="en")
        )
    )

    export_operation: Operation = client.services.agents.export_agent(
        ExportAgentRequest(parent=created_agent.parent)
    )

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

    with open("my_backup.zip", mode="wb") as zf:
        zf.write(export_response.agent_content)
