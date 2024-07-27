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
from faker import Faker

from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.session_pb2 import (
    DetectIntentRequest,
    DetectIntentResponse,
    QueryInput,
    TextInput,
)

if __name__ == '__main__':
    parent: str = '<PUT_YOUR_AGENT_PARENT_HERE>'
    config: ClientConfig = ClientConfig(
        host='localhost',
        port='1234',
        http_token='<http/root token>',
        user_name='<e-mail of user>',
        password='<password of user>'
    )
    client: Client = Client(config=config, use_secure_channel=False)
    f: Faker = Faker()
    session_name: str = f.name()

    request: DetectIntentRequest = DetectIntentRequest(
        session=f'{parent}/sessions/{session_name}',
        query_input=QueryInput(
            text=TextInput(text='<Some text>')
        )
    )

    response: DetectIntentResponse = client.services.sessions.detect_intent(request=request)

    print(f'Text received by the server: {response.query_result.query_text}')
    print(f'Intent detected: {response.query_result.intent.display_name}')
    print(f'Text response: {response.query_result.fulfillment_messages[0].text.text[0]}')
