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
from typing import List

from google.protobuf.json_format import MessageToJson
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.intent_pb2 import Intent, ListIntentsRequest, IntentView

if __name__ == '__main__':
    # CONFIGURING THE CLIENT
    config: ClientConfig = ClientConfig(
        host='<host>',
        port='<port>',
        http_token='<http/root token>',
        user_name='<e-mail of user>',
        password='<password of user>'
    )
    client: Client = Client(config=config, use_secure_channel=False)

    # CONFIGURING THE AGENT
    parent: str = '<PUT_YOUR_AGENT_PARENT_HERE>'
    language_code: str = '<acronym of he language of choice, i.e "en">'

    # LOAD ALL INTENTS
    intents: List[Intent] = list(
        client.services.intents.list_intents(
            ListIntentsRequest(
                parent=parent,
                language_code=language_code,
                intent_view=IntentView.INTENT_VIEW_FULL,
                page_token='page_size-10000',
            )
        ).intents
    )

    # EXPORT ALL INTENTS AS JSON FILES
    export_dir: Path = Path('<destination folder>') / language_code
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
        export_path: Path = export_dir / f'{intent.display_name}.json'
        intent_json: str = MessageToJson(intent)
        with export_path.open('w') as f:
            f.write(intent_json)
