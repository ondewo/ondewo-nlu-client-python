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
import uuid
from typing import (
    Dict,
    List,
    Optional,
)

from ondewo.nlu import context_pb2
from ondewo.nlu.client import Client as NluClient
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.session_pb2 import (
    DetectIntentRequest,
    DetectIntentResponse,
    QueryInput,
    QueryParameters,
    TextInput,
)


def make_context() -> context_pb2.Context:
    # Enter intent name .. Example would be i.order.pizza
    intent_name: str = "<intent_name>"
    context_parameter: context_pb2.Context.Parameter = context_pb2.Context.Parameter(
        display_name='intent_name',
        value=intent_name
    )

    # intent_name in display_name and parameter "dictionary" are hardcoded. So don't change them
    parameter: Dict[str, context_pb2.Context.Parameter] = {'intent_name': context_parameter}

    # Don't change the name, just change the lifespan_count, which
    # defines how many interactions this context is going to stay active
    context = context_pb2.Context(
        name=f"{session}/contexts/exact_intent",
        lifespan_count=20,
        parameters=parameter
    )

    return context


def create_session_nlu(project_id: str) -> str:
    session_id: str = str(uuid.uuid4())
    project_parent: str = f'projects/{project_id}/agent'
    return f'{project_parent}/sessions/{session_id}'


if __name__ == '__main__':
    # Pass in your project id and a session will be created for the nlu client
    project_id: str = '<project id>'
    session: str = create_session_nlu(project_id)

    # Client configuration
    config: ClientConfig = ClientConfig(
        host='localhost',
        port='1234',
        http_token='<http/root token>',
        user_name='<e-mail of user>',
        password='<password of user>'
    )
    nlu_client: NluClient = NluClient(config=config, use_secure_channel=False)
    # You have to go to the function and set the context you want
    context: Optional[List[context_pb2.Context]] = [make_context()]
    print(f"The context here is: {context}")

    # Nlu request and response
    # You can have context set to None if you don't want to use this functionality
    context = context or None
    nlu_request: DetectIntentRequest = DetectIntentRequest(
        session=session,
        query_input=QueryInput(
            text=TextInput(
                text="<enter your text here>",
                language_code='de',
            )
        ),
        query_params=QueryParameters(
            contexts=context
        )
    )
    nlu_response: DetectIntentResponse = nlu_client.services.sessions.detect_intent(
        request=nlu_request,
    )

    print(f'Text received by the server: {nlu_response.query_result.query_text}')
    print(f'Intent detected: {nlu_response.query_result.intent.display_name}')
    print('Text response:')
    for message in nlu_response.query_result.fulfillment_messages:
        print(message.text.text[0])
