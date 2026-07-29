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

Authentication uses the headless Keycloak offline-token flow: configure `keycloak_url`,
`realm`, and `client_id` (the public SDK client, no secret) together with the
technical-user `user_name` / `password`. The `Client` then attaches a freshly
auto-refreshed `Authorization: Bearer <token>` to every gRPC call.

The request-building and response-formatting logic is factored into small functions so it
can be unit-tested with the gRPC client mocked (see
`tests/unit/examples/test_detect_intent_keycloak.py`) — no live server required.
"""

import sys
from pathlib import Path
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


def build_detect_intent_request(
    session: str,
    text: str,
    language_code: str = "en-US",
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
            The language of the utterance, e.g. `en-US`. Must be a full code from the
            `LanguageCode` enum — a bare `en` is rejected.

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
    language_code: str = "en-US",
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
    return f"query_text={query_result.query_text!r} intent={query_result.intent.display_name!r}"


if __name__ == "__main__":
    # Auth (D18): Keycloak headless offline-token flow — bearer token attached automatically.
    # NOTE: a technical user logs in with its *username* (as returned by
    # `CreateProjectTechnicalUser`), never with the synthetic `tech-<hash>@…` e-mail the server
    # derives for it. That e-mail exists only to satisfy Keycloak's unique-email requirement.
    config: ClientConfig = get_client_config()
    client: Client = Client(config=config, use_secure_channel=use_secure_channel())

    parent: str = env("ONDEWO_NLU_CAI_AGENT_PARENT")
    session_id: str = f"{parent}/sessions/{env('ONDEWO_NLU_CAI_SESSION_ID')}"

    response: DetectIntentResponse = detect_intent(
        client=client,
        session=session_id,
        text=env("ONDEWO_NLU_CAI_TEXT"),
        language_code=env("ONDEWO_NLU_CAI_LANGUAGE_CODE"),
    )
    print(format_response(response))
