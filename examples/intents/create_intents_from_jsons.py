# Copyright 2021-2024 ONDEWO GmbH
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
from pathlib import Path

from google.protobuf.json_format import Parse

from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.intent_pb2 import (
    CreateIntentRequest,
    Intent,
)

if __name__ == '__main__':
    # CONFIGURING THE CLIENT
    config: ClientConfig = ClientConfig(
        host='localhost',
        port='1234',
        http_token='<http/root token>',
        user_name='<e-mail of user>',
        password='<password of user>'
    )
    client: Client = Client(config=config, use_secure_channel=False)

    # CONFIGURING THE AGENT
    parent: str = '<PUT_YOUR_AGENT_PARENT_HERE>'
    language_code: str = '<acronym of he language of choice, i.e "en">'

    # CREATE INTENTS BASED ON JSON-FILES
    import_dir: Path = Path('<lookup folder>') / language_code
    for json_file in import_dir.glob('*.json'):
        with json_file.open('r') as f:
            intent_json: str = f.read()
        intent: Intent = Parse(text=intent_json, message=Intent())
        client.services.intents.create_intent(
            CreateIntentRequest(
                parent=parent,
                language_code=language_code,
                intent=intent,
            )
        )
