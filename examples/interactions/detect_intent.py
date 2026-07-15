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
from faker import Faker

from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.session_pb2 import (
    DetectIntentRequest,
    DetectIntentResponse,
    QueryInput,
    TextInput,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from example_env import (  # noqa: E402
    env,
    get_client_config,
    use_secure_channel,
)

if __name__ == "__main__":
    parent: str = env("ONDEWO_NLU_CAI_AGENT_PARENT")
    config: ClientConfig = get_client_config()
    client: Client = Client(config=config, use_secure_channel=use_secure_channel())
    f: Faker = Faker()
    session_name: str = f.name()

    request: DetectIntentRequest = DetectIntentRequest(
        session=f"{parent}/sessions/{session_name}",
        query_input=QueryInput(
            text=TextInput(
                text=env("ONDEWO_NLU_CAI_TEXT"),
                language_code=env("ONDEWO_NLU_CAI_LANGUAGE_CODE"),
            ),
        ),
    )

    response: DetectIntentResponse = client.services.sessions.detect_intent(request=request)

    print(f"Text received by the server: {response.query_result.query_text}")
    print(f"Intent detected: {response.query_result.intent.display_name}")
    print(f"Text response: {response.query_result.fulfillment_messages[0].text.text[0]}")
