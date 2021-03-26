# Copyright 2021 ONDEWO GmbH
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
This script presents some examples for how to interact with the ONDEWO python client.
"""

import json
from typing import Any
from uuid import uuid4

from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.context_pb2 import ListContextsRequest, CreateContextRequest
from ondewo.nlu.convenience.shared_request_data import SharedRequestData
from ondewo.nlu.intent_pb2 import ListIntentsRequest
from ondewo.nlu.session_pb2 import DetectIntentRequest, GetLatestSessionReviewRequest, GetSessionRequest


# TODO: this is deprecated
if __name__ == '__main__':
    # 1. define the client configuration...
    # put your host, port, user_name, password, grpc_cert and http_token into the config_file json
    # format as follows:
    # {
    #     "host": "<host_ip>",
    #     "port": "<host_port>",
    #     "user_name": "<user_email>",
    #     "password": "<user_password>",
    #     "http_token": "<http_token>",
    #     "grpc_cert": "-----BEGIN CERTIFICATE-----\n<certificate_string>\n-----END CERTIFICATE-----\n",
    #     "project_parent": "projects/<project_id>/agent",
    #     "session_uuid": "<some_uuid>"
    # }
    config_file = "ondewo_client/python/.env.production.json"

    with open(config_file) as f:
        config_ = json.load(f)

    host: str = config_["host"]
    port: str = config_["port"]
    user_name: str = config_["user_name"]
    password: str = config_["password"]
    http_token: str = config_["http_token"]
    grpc_cert: bytes = str(config_.get("grpc_cert", '')).encode()

    config = ClientConfig(
        host=host,
        port=port,
        user_name=user_name,
        password=password,
        http_token=http_token,
        grpc_cert=grpc_cert,  # type: ignore
    )

    # 2. instantiate the client...
    client = Client(config=config)

    # 3. play...
    project_parent: str = config_["project_parent"]
    session_uuid: str = config_["session_uuid"]
    session_id: str = f'{project_parent}/sessions/{session_uuid}'

    # detect an intent
    request: Any = DetectIntentRequest()
    request.query_input.text.text = 'Hi'
    request.query_input.text.language_code = 'en'
    request.session = session_id
    response: Any = client.services.sessions.detect_intent(request)
    print(response.query_result.fulfillment_messages[0].text)

    # list all intents
    request = ListIntentsRequest()
    request.parent = project_parent
    request.language_code = 'en'
    response = client.services.intents.list_intents(request)
    print(response)

    # set a context
    request = CreateContextRequest()
    request.parent = project_parent
    request.context.name = f'{session_id}/contexts/{uuid4()}'
    request.context.lifespan_count = 2
    response = client.services.contexts.create_context(request)
    print(response)

    # list the contexts in this session
    request = ListContextsRequest()
    request.parent = session_id
    response = client.services.contexts.list_contexts(request)
    print(response)

    # get the current session
    request = GetSessionRequest()
    request.session_id = session_id
    response = client.services.sessions.get_session(request)
    print(response)

    # get the latest session review for the current session
    request = GetLatestSessionReviewRequest()
    request.session_id = session_id
    response = client.services.sessions.get_latest_session_review(request)
    print(response)

    # CONVENIENCE: share request data among different request types
    # 4. use a SharedRequestData to store commonly used information
    shared_request_data = SharedRequestData(
        project_parent=project_parent,
        session_uuid=session_uuid,
        language_code='en',
    )

    # try intent detection
    # fill request with data from shared_request_data to avoid needing to fill all fields explicitly
    request = DetectIntentRequest()
    request = shared_request_data.fill_missing_fields(request)
    request.query_input.text.text = 'Hi'
    response = client.services.sessions.detect_intent(request)
    print(response.query_result.fulfillment_messages[0].text)

    # again for a different language
    shared_request_data.language_code = 'de'
    request = DetectIntentRequest()
    request = shared_request_data.fill_missing_fields(request)
    request.query_input.text.text = 'Hallo'
    response = client.services.sessions.detect_intent(shared_request_data.fill_missing_fields(request))
    print(response.query_result.fulfillment_messages[0].text)

    # set a context
    request = CreateContextRequest()
    request = shared_request_data.fill_missing_fields(request)
    request.context.name = f'{shared_request_data.session_id}/contexts/{uuid4()}'
    request.context.lifespan_count = 2
    response = client.services.contexts.create_context(request)
    print(response)

    # list the contexts in this session
    request = ListContextsRequest()
    request = shared_request_data.fill_missing_fields(request)
    response = client.services.contexts.list_contexts(request)
    print(response)

    # get the current session
    request = GetSessionRequest()
    request = shared_request_data.fill_missing_fields(request)
    response = client.services.sessions.get_session(request)
    print(response)

    # get the latest session review for the current session
    request = GetLatestSessionReviewRequest()
    request = shared_request_data.fill_missing_fields(request)
    response = client.services.sessions.get_latest_session_review(request)
    print(response)
