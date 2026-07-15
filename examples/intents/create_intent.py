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
from ondewo.nlu import intent_pb2
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from example_env import (  # noqa: E402
    env,
    get_client_config,
    use_secure_channel,
)

if __name__ == "__main__":
    # CONFIGURING THE CLIENT
    config: ClientConfig = get_client_config()
    client: Client = Client(config=config, use_secure_channel=use_secure_channel())

    # CONFIGURING THE AGENT
    parent: str = env("ONDEWO_NLU_CAI_AGENT_PARENT")
    language_code: str = env("ONDEWO_NLU_CAI_LANGUAGE_CODE")

    r = intent_pb2.CreateIntentRequest(
        intent=intent_pb2.Intent(
            display_name="i.pepper.dance",
            webhook_state=intent_pb2.Intent.WEBHOOK_STATE_UNSPECIFIED,
            priority=250000,
            is_fallback=False,
            input_context_names=[],
            messages=[
                intent_pb2.Intent.Message(
                    text=intent_pb2.Intent.Message.Text(
                        text=[
                            "Hast du nicht die Fotos vom letzten Wochenende gesehen? ",
                            "Pass mal auf.  $onStartBehavior=ht_entertainment/dance",
                        ]
                    )
                ),
                intent_pb2.Intent.Message(
                    platform=intent_pb2.Intent.Message.Platform.FACEBOOK,
                    text=intent_pb2.Intent.Message.Text(
                        text=[
                            "FACEBOOK",
                            "FACEBOOK ffuscd",
                        ]
                    ),
                ),
                intent_pb2.Intent.Message(
                    platform=intent_pb2.Intent.Message.Platform.KIK,
                    text=intent_pb2.Intent.Message.Text(
                        text=[
                            "PLATFORM 12 rocks!",
                        ]
                    ),
                ),
            ],
            training_phrases=[
                intent_pb2.Intent.TrainingPhrase(
                    text="@pepper:pepper kannst du tanzen?",
                    type=intent_pb2.Intent.TrainingPhrase.TEMPLATE,
                ),
                intent_pb2.Intent.TrainingPhrase(
                    text="@pepper:pepper kannst du essen?", type=intent_pb2.Intent.TrainingPhrase.TEMPLATE
                ),
            ],
        ),
        parent=parent,
        language_code=env("ONDEWO_NLU_CAI_LANGUAGE_CODE"),
    )

    response = client.services.intents.create_intent(r)
    print(response)
    print(
        client.services.intents.get_intent(
            intent_pb2.GetIntentRequest(name=response.name, language_code=env("ONDEWO_NLU_CAI_LANGUAGE_CODE"))
        )
    )
