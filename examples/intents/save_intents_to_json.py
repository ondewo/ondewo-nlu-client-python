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
The pair of scripts create_intents_from_jsons.py and save_intents_to_jsons.py
allows to use AIM as an editor for intents or intent templates.

1) using create_intents_from_jsons.py:
 create intents in an existing agent (usually empty) from json-files in an input folder
2) using AIM: edit the new intents
3) using save_intents_to_jsons.py:
 save all intents of a given agent to json-files in an output folder
"""

import sys
from pathlib import Path
from typing import List

from google.protobuf.json_format import MessageToJson

from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.intent_pb2 import (
    Intent,
    IntentView,
    ListIntentsRequest,
)

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

    # LOAD ALL INTENTS
    intents: List[Intent] = list(
        client.services.intents.list_intents(
            ListIntentsRequest(
                parent=parent,
                language_code=language_code,
                intent_view=IntentView.INTENT_VIEW_FULL,
                page_token="page_size-10000",
            )
        ).intents
    )

    # EXPORT ALL INTENTS AS JSON FILES
    export_dir: Path = Path(env("ONDEWO_NLU_CAI_INTENTS_DIR")) / language_code
    # The per-language sub-directory does not exist on a first run; the example used to assume it did.
    export_dir.mkdir(parents=True, exist_ok=True)
    for intent in intents:
        if intent.display_name in [
            "Default Exit Intent",
            "Default Fallback Intent",
            "Default Reset Intent",
        ]:
            continue
        intent.ClearField("name")
        intent.ClearField("training_phrase_count")
        for training_phrase in intent.training_phrases:
            training_phrase.ClearField("name")
        export_path: Path = export_dir / f"{intent.display_name}.json"
        intent_json: str = MessageToJson(intent)
        with export_path.open("w") as f:
            f.write(intent_json)
