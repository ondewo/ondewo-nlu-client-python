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

import grpc

from ondewo.nlu.client import Client as NluClient
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.session_pb2 import (
    DeleteSessionRequest,
    DetectIntentRequest,
    DetectIntentResponse,
    QueryInput,
    QueryParameters,
    TextInput,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from example_env import (  # noqa: E402
    env,
    get_client_config,
    use_secure_channel,
)

if __name__ == "__main__":
    # Pass in your project id and a session will be created for the nlu client
    project_id: str = env("ONDEWO_NLU_CAI_PROJECT_ID")
    project_parent: str = f"projects/{project_id}/agent"
    session_id = env("ONDEWO_NLU_CAI_SESSION_ID")
    session_path: str = f"{project_parent}/sessions/{session_id}"

    # Client configuration
    config: ClientConfig = get_client_config()
    nlu_client: NluClient = NluClient(config=config, use_secure_channel=use_secure_channel())

    # DELETE the session first, so the interaction below starts from a clean slate. On a first run the
    # session does not exist yet and the server answers NOT_FOUND — that is expected, not an error.
    try:
        nlu_client.services.sessions.delete_session(DeleteSessionRequest(session_id=session_path))
    except grpc.RpcError as rpc_error:
        if rpc_error.code() is not grpc.StatusCode.NOT_FOUND:
            raise

    # Nlu request and response
    nlu_request: DetectIntentRequest = DetectIntentRequest(
        session=session_path,
        query_input=QueryInput(
            text=TextInput(
                text=env("ONDEWO_NLU_CAI_TEXT"),
                language_code=env("ONDEWO_NLU_CAI_LANGUAGE_CODE"),
            )
        ),
        query_params=QueryParameters(),
    )
    nlu_response: DetectIntentResponse = nlu_client.services.sessions.detect_intent(
        request=nlu_request,
    )

    print(f"Text received by the server: {nlu_response.query_result.query_text}")
    print(f"Intent detected: {nlu_response.query_result.intent.display_name}")
    print("Text response:")
    for message in nlu_response.query_result.fulfillment_messages:
        print(message.text.text[0])
