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
Minimal detect-intent example using the current Keycloak bearer auth (D18).

The legacy `Login` RPC / `cai-token` / `Authorization: Basic http_token` path has been
removed from the platform. Authentication now uses the headless Keycloak offline-token
flow: configure `keycloak_url`, `realm`, and `client_id` (the public SDK client, no
secret) together with the technical-user `user_name` / `password`. The `Client` then
attaches a freshly auto-refreshed `Authorization: Bearer <token>` to every gRPC call.

The request-building and response-formatting logic is factored into small functions so it
can be unit-tested with the gRPC client mocked (see
`tests/unit/examples/test_detect_intent_keycloak.py`) — no live server required.
"""
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.session_pb2 import (
    DetectIntentRequest,
    DetectIntentResponse,
    QueryInput,
    TextInput,
)


def build_detect_intent_request(
    session: str,
    text: str,
    language_code: str = 'en',
) -> DetectIntentRequest:
    """
    Build a `DetectIntentRequest` for a single text turn in a session.

    Args:
        session (str):
            Fully qualified session name, e.g.
            `projects/<project-uuid>/agent/sessions/<session-uuid>`.
        text (str):
            The user utterance to send to the NLU server.
        language_code (str):
            The language of the utterance, e.g. `en`.

    Returns:
        DetectIntentRequest:
            The request carrying the text query for the given session.
    """
    return DetectIntentRequest(
        session=session,
        query_input=QueryInput(
            text=TextInput(text=text, language_code=language_code),
        ),
    )


def detect_intent(
    client: Client,
    session: str,
    text: str,
    language_code: str = 'en',
) -> DetectIntentResponse:
    """
    Send a single text turn to the NLU server and return the response.

    Args:
        client (Client):
            An authenticated ONDEWO NLU client (Keycloak bearer auth).
        session (str):
            Fully qualified session name.
        text (str):
            The user utterance to send.
        language_code (str):
            The language of the utterance.

    Returns:
        DetectIntentResponse:
            The server response with the detected intent and fulfillment.
    """
    request: DetectIntentRequest = build_detect_intent_request(
        session=session,
        text=text,
        language_code=language_code,
    )
    return client.services.sessions.detect_intent(request=request)


def format_response(response: DetectIntentResponse) -> str:
    """
    Render a short, human-readable summary of a detect-intent response.

    Args:
        response (DetectIntentResponse):
            The response returned by `detect_intent`.

    Returns:
        str:
            A one-line summary with the recognised query text and detected intent.
    """
    query_result = response.query_result
    return f'query_text={query_result.query_text!r} intent={query_result.intent.display_name!r}'


if __name__ == '__main__':
    # Current auth (D18): Keycloak headless offline-token flow — no http_token / cai-token.
    config: ClientConfig = ClientConfig(
        host='localhost',
        port='50055',
        user_name='<technical-user-email>',
        password='<technical-user-password>',
        keycloak_url='https://<host>/auth',
        realm='ondewo-ccai-platform',
        client_id='ondewo-nlu-cai-sdk-public',
    )
    client: Client = Client(config=config, use_secure_channel=True)

    parent: str = 'projects/<project-uuid>/agent'
    session_id: str = f'{parent}/sessions/<session-uuid>'

    response: DetectIntentResponse = detect_intent(
        client=client,
        session=session_id,
        text='Hello',
    )
    print(format_response(response))
