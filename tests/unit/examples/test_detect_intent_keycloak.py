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
Hermetic mock tests proving the `detect_intent_keycloak` example works without a server.

The example module is loaded by file path (the `examples/` tree is not an importable
package). Loading executes only module-level imports — the `if __name__ == '__main__':`
block never runs, so no `Client` is constructed and no Keycloak / gRPC network call is
made. The gRPC client is replaced with a `MagicMock`, so the tests assert exactly the
request the example builds and that it returns the server response unchanged.
"""

import importlib.util
from pathlib import Path
from types import ModuleType
from unittest.mock import MagicMock

from ondewo.nlu.session_pb2 import DetectIntentResponse

_EXAMPLE_PATH: Path = Path(__file__).parents[3] / "examples" / "sessions" / "detect_intent_keycloak.py"

# Bound once so a refactor that changes only an input or only an expectation cannot
# silently make an assertion tautological.
SESSION: str = "projects/11111111-1111-1111-1111-111111111111/agent/sessions/abc"
TEXT: str = "Hello there"
LANGUAGE_CODE: str = "de"
QUERY_TEXT: str = "Hello there"
INTENT_NAME: str = "i.greeting"


def _load_example() -> ModuleType:
    """
    Load the example module from its file path without executing its `__main__` block.

    Returns:
        ModuleType:
            The imported `detect_intent_keycloak` example module.
    """
    spec = importlib.util.spec_from_file_location("detect_intent_keycloak", _EXAMPLE_PATH)
    assert spec is not None and spec.loader is not None
    module: ModuleType = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestDetectIntentKeycloakExample:
    """The example's request-building, stub-call, and response-formatting logic."""

    def test_example_file_exists(self) -> None:
        """The example the tests drive is present at the expected path."""
        assert _EXAMPLE_PATH.exists(), f"Example not found at {_EXAMPLE_PATH}"

    def test_build_request_sets_session_text_and_language(self) -> None:
        """`build_detect_intent_request` maps its args onto the proto request fields."""
        module: ModuleType = _load_example()

        request = module.build_detect_intent_request(
            session=SESSION,
            text=TEXT,
            language_code=LANGUAGE_CODE,
        )

        assert request.session == SESSION
        assert request.query_input.text.text == TEXT
        assert request.query_input.text.language_code == LANGUAGE_CODE

    def test_detect_intent_calls_stub_with_built_request_and_returns_response(self) -> None:
        """`detect_intent` sends the built request to the sessions stub and returns its response."""
        module: ModuleType = _load_example()

        expected_response: DetectIntentResponse = DetectIntentResponse()
        expected_response.query_result.query_text = QUERY_TEXT
        expected_response.query_result.intent.display_name = INTENT_NAME

        client: MagicMock = MagicMock()
        client.services.sessions.detect_intent.return_value = expected_response

        result = module.detect_intent(
            client=client,
            session=SESSION,
            text=TEXT,
            language_code=LANGUAGE_CODE,
        )

        client.services.sessions.detect_intent.assert_called_once()
        sent_request = client.services.sessions.detect_intent.call_args.kwargs["request"]
        assert sent_request.session == SESSION
        assert sent_request.query_input.text.text == TEXT
        assert sent_request.query_input.text.language_code == LANGUAGE_CODE
        # The example returns the server response unchanged (no client-side rewriting).
        assert result is expected_response

    def test_format_response_summarises_query_text_and_intent(self) -> None:
        """`format_response` renders the recognised query text and detected intent name."""
        module: ModuleType = _load_example()

        response: DetectIntentResponse = DetectIntentResponse()
        response.query_result.query_text = QUERY_TEXT
        response.query_result.intent.display_name = INTENT_NAME

        summary: str = module.format_response(response)

        assert summary == f"query_text={QUERY_TEXT!r} intent={INTENT_NAME!r}"
