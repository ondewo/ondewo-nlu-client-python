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
"""Hermetic unit tests for `SharedRequestData`.

Nothing here touches the network: `SharedRequestData` is a pure dataclass that derives
resource-name strings and copies protobuf requests, so every test is a plain in-memory call.

The expected resource names are pinned as explicit literals rather than re-derived with the
same f-string the implementation uses — mirroring the implementation would make the format
assertions unable to fail. Each literal is bound exactly once at module level.
"""

from typing import (
    Any,
    Dict,
    Optional,
    Type,
)
from uuid import UUID

import pytest
from google.protobuf.message import Message

from ondewo.nlu.agent_pb2 import GetAgentRequest
from ondewo.nlu.context_pb2 import (
    CreateContextRequest,
    DeleteAllContextsRequest,
    DeleteContextRequest,
    GetContextRequest,
    ListContextsRequest,
    UpdateContextRequest,
)
from ondewo.nlu.convenience.shared_request_data import SharedRequestData
from ondewo.nlu.intent_pb2 import (
    BatchDeleteIntentsRequest,
    BatchUpdateIntentsRequest,
    CreateIntentRequest,
    DeleteIntentRequest,
    GetIntentRequest,
    ListIntentsRequest,
    UpdateIntentRequest,
)
from ondewo.nlu.session_pb2 import (
    CreateSessionReviewRequest,
    DetectIntentRequest,
    GetLatestSessionReviewRequest,
    GetSessionRequest,
    GetSessionReviewRequest,
    ListSessionReviewsRequest,
    ListSessionsRequest,
)

# --- Inputs: bound exactly once ---------------------------------------------------------
PROJECT_PARENT: str = "projects/my-project/agent"
LANGUAGE_CODE: str = "de"
SESSION_UUID: str = "sess-1"
SESSION_REVIEW_UUID: str = "rev-1"
INTENT_UUID: str = "intent-1"

# --- Expected resource names: the API contract, pinned literally -------------------------
EXPECTED_SESSION_ID: str = "projects/my-project/agent/sessions/sess-1"
EXPECTED_SESSION_REVIEW_ID: str = "projects/my-project/agent/sessions/sess-1/reviews/rev-1"
EXPECTED_INTENT_ID: str = "projects/my-project/agent/intents/intent-1"

# A resource name that differs from every derived value above, used to prove that a value
# already present on a request is never overwritten by the shared data.
PRESET_SESSION_ID: str = "projects/other-project/agent/sessions/preset-session"


def _full() -> SharedRequestData:
    """Return a `SharedRequestData` with every field populated."""
    return SharedRequestData(
        project_parent=PROJECT_PARENT,
        language_code=LANGUAGE_CODE,
        intent_uuid=INTENT_UUID,
        session_uuid=SESSION_UUID,
        session_review_uuid=SESSION_REVIEW_UUID,
    )


class TestSetFreshSessionUuid:
    """`set_fresh_session_uuid` stores the uuid on the instance and returns it."""

    def test_explicit_uuid_is_stored_and_returned(self) -> None:
        data: SharedRequestData = SharedRequestData()

        returned: str = data.set_fresh_session_uuid(uuid=SESSION_UUID)

        assert returned == SESSION_UUID
        assert data.session_uuid == SESSION_UUID

    def test_explicit_uuid_overwrites_a_previous_session_uuid(self) -> None:
        data: SharedRequestData = SharedRequestData(session_uuid="stale-session")

        returned: str = data.set_fresh_session_uuid(uuid=SESSION_UUID)

        assert returned == SESSION_UUID
        assert data.session_uuid == SESSION_UUID

    def test_omitted_uuid_generates_a_uuid4(self) -> None:
        data: SharedRequestData = SharedRequestData()

        returned: str = data.set_fresh_session_uuid()

        assert data.session_uuid == returned
        # Raises ValueError if `returned` is not a well-formed uuid4 string.
        assert str(UUID(returned, version=4)) == returned

    def test_empty_string_uuid_falls_back_to_a_generated_uuid4(self) -> None:
        """An empty string is falsy, so the `uuid or str(uuid4())` fallback must kick in."""
        data: SharedRequestData = SharedRequestData()

        returned: str = data.set_fresh_session_uuid(uuid="")

        assert returned != ""
        assert data.session_uuid == returned
        assert str(UUID(returned, version=4)) == returned

    def test_successive_generated_uuids_differ(self) -> None:
        data: SharedRequestData = SharedRequestData()

        first: str = data.set_fresh_session_uuid()
        second: str = data.set_fresh_session_uuid()

        assert first != second
        assert data.session_uuid == second


class TestSessionId:
    """`session_id` composes the session resource name, or is None when an input is missing."""

    def test_returns_resource_name_when_inputs_are_set(self) -> None:
        assert _full().session_id == EXPECTED_SESSION_ID

    def test_returns_none_without_project_parent(self) -> None:
        data: SharedRequestData = SharedRequestData(session_uuid=SESSION_UUID)

        assert data.session_id is None

    def test_returns_none_without_session_uuid(self) -> None:
        data: SharedRequestData = SharedRequestData(project_parent=PROJECT_PARENT)

        assert data.session_id is None

    def test_returns_none_when_nothing_is_set(self) -> None:
        assert SharedRequestData().session_id is None


class TestSessionReviewId:
    """`session_review_id` composes the review resource name, or is None when an input is missing."""

    def test_returns_resource_name_when_inputs_are_set(self) -> None:
        assert _full().session_review_id == EXPECTED_SESSION_REVIEW_ID

    def test_returns_none_without_project_parent(self) -> None:
        data: SharedRequestData = SharedRequestData(
            session_uuid=SESSION_UUID,
            session_review_uuid=SESSION_REVIEW_UUID,
        )

        assert data.session_review_id is None

    def test_returns_none_without_session_uuid(self) -> None:
        data: SharedRequestData = SharedRequestData(
            project_parent=PROJECT_PARENT,
            session_review_uuid=SESSION_REVIEW_UUID,
        )

        assert data.session_review_id is None

    def test_returns_none_without_session_review_uuid(self) -> None:
        """Regression test: the guard must cover the uuid the f-string interpolates.

        The property previously guarded only on `project_parent`/`session_uuid` while
        interpolating `session_review_uuid`, so an unset review uuid produced the string
        '.../reviews/None' — a resource name the server can only reject — instead of None.
        """
        data: SharedRequestData = SharedRequestData(
            project_parent=PROJECT_PARENT,
            session_uuid=SESSION_UUID,
        )

        assert data.session_review_id is None


class TestIntentId:
    """`intent_id` composes the intent resource name, or is None when an input is missing."""

    def test_returns_resource_name_when_inputs_are_set(self) -> None:
        assert _full().intent_id == EXPECTED_INTENT_ID

    def test_returns_none_without_project_parent(self) -> None:
        data: SharedRequestData = SharedRequestData(intent_uuid=INTENT_UUID)

        assert data.intent_id is None

    def test_returns_none_without_intent_uuid(self) -> None:
        data: SharedRequestData = SharedRequestData(project_parent=PROJECT_PARENT)

        assert data.intent_id is None


class TestFillMissingFields:
    """`fill_missing_fields` returns a copy with unset mapped fields filled in from self."""

    def test_fills_flat_and_nested_fields_on_a_detect_intent_request(self) -> None:
        filled: DetectIntentRequest = _full().fill_missing_fields(request=DetectIntentRequest())

        assert filled.session == EXPECTED_SESSION_ID
        assert filled.query_input.text.language_code == LANGUAGE_CODE

    def test_does_not_mutate_the_original_request(self) -> None:
        """The docstring promises a copy: the caller's request must come back untouched."""
        request: DetectIntentRequest = DetectIntentRequest()

        filled: DetectIntentRequest = _full().fill_missing_fields(request=request)

        assert filled is not request
        assert request.session == ""
        assert request.query_input.text.language_code == ""

    def test_preserves_a_value_already_set_on_the_request(self) -> None:
        request: GetSessionRequest = GetSessionRequest(session_id=PRESET_SESSION_ID)

        filled: GetSessionRequest = _full().fill_missing_fields(request=request)

        assert filled.session_id == PRESET_SESSION_ID

    def test_fills_only_the_unset_field_of_a_partially_populated_request(self) -> None:
        request: DetectIntentRequest = DetectIntentRequest(session=PRESET_SESSION_ID)

        filled: DetectIntentRequest = _full().fill_missing_fields(request=request)

        assert filled.session == PRESET_SESSION_ID
        assert filled.query_input.text.language_code == LANGUAGE_CODE

    def test_uses_session_review_id_for_a_get_session_review_request(self) -> None:
        filled: GetSessionReviewRequest = _full().fill_missing_fields(request=GetSessionReviewRequest())

        assert filled.session_review_id == EXPECTED_SESSION_REVIEW_ID

    def test_fills_a_nested_message_field_on_a_create_intent_request(self) -> None:
        filled: CreateIntentRequest = _full().fill_missing_fields(request=CreateIntentRequest())

        assert filled.parent == PROJECT_PARENT
        assert filled.language_code == LANGUAGE_CODE
        assert filled.intent.name == EXPECTED_INTENT_ID

    @pytest.mark.parametrize(
        "request_type",
        [CreateContextRequest, ListContextsRequest, DeleteAllContextsRequest],
    )
    def test_session_scoped_context_request_is_filled_with_the_full_session_name(
        self,
        request_type: Type[Message],
    ) -> None:
        """Regression test: context requests take a session name, not a project parent.

        context.proto documents `session_id` on all three as
        "Format: projects/<project_uuid>/agent/sessions/<session_uuid>". Asserting the exact
        value — not merely that the field is non-empty — is what distinguishes the correct
        `session_id` mapping from a `project_parent` one, which would silently send
        "projects/my-project/agent" where the server expects a session.
        """
        filled: Message = _full().fill_missing_fields(request=request_type())

        assert _get_nested(filled, "session_id") == EXPECTED_SESSION_ID

    def test_request_type_with_an_empty_mapping_is_returned_as_an_equal_copy(self) -> None:
        request: GetContextRequest = GetContextRequest(name="projects/p/agent/sessions/s/contexts/c")

        filled: GetContextRequest = _full().fill_missing_fields(request=request)

        assert filled is not request
        assert filled == request

    def test_unmapped_request_type_raises_not_implemented_error(self) -> None:
        with pytest.raises(NotImplementedError) as exc_info:
            _full().fill_missing_fields(request=GetAgentRequest())

        assert "mapping not defined for request type" in str(exc_info.value)

    def test_missing_value_on_self_raises_value_error_naming_the_field(self) -> None:
        with pytest.raises(ValueError) as exc_info:
            SharedRequestData().fill_missing_fields(request=GetSessionRequest())

        assert "Could not get session_id" in str(exc_info.value)

    def test_missing_language_code_on_self_raises_value_error(self) -> None:
        """`project_parent` resolves but `language_code` does not — the second field must still raise."""
        data: SharedRequestData = SharedRequestData(project_parent=PROJECT_PARENT)

        with pytest.raises(ValueError) as exc_info:
            data.fill_missing_fields(request=ListIntentsRequest())

        assert "Could not get language_code" in str(exc_info.value)


class TestRequestFieldMapping:
    """The mapping table itself must stay consistent with `SharedRequestData`'s attributes."""

    def test_every_mapped_source_field_exists_on_shared_request_data(self) -> None:
        """Guards against a typo'd source field, which would only surface as a runtime ValueError.

        `get_attr_recursive` swallows a misspelled attribute into None, which `fill_missing_fields`
        then reports as the generic "Could not get <field>" — indistinguishable from a genuinely
        unset value. Checking the table against the real attributes catches it up front.
        """
        data: SharedRequestData = _full()
        mapping: Dict[Any, Dict[str, str]] = data._request_field__to__field__per__request_type

        for request_type, request_field__to__field in mapping.items():
            for field_name in request_field__to__field.values():
                assert hasattr(data, field_name), f"{request_type.__name__} maps to unknown field {field_name!r}"

    @pytest.mark.parametrize(
        "request_type",
        [
            DetectIntentRequest,
            ListSessionsRequest,
            GetSessionRequest,
            ListSessionReviewsRequest,
            GetSessionReviewRequest,
            GetLatestSessionReviewRequest,
            CreateSessionReviewRequest,
            CreateContextRequest,
            ListContextsRequest,
            GetContextRequest,
            UpdateContextRequest,
            DeleteContextRequest,
            DeleteAllContextsRequest,
            GetIntentRequest,
            ListIntentsRequest,
            CreateIntentRequest,
            UpdateIntentRequest,
            DeleteIntentRequest,
            BatchUpdateIntentsRequest,
            BatchDeleteIntentsRequest,
        ],
    )
    def test_every_mapped_request_type_fills_from_fully_populated_data(
        self,
        request_type: Type[Message],
    ) -> None:
        """A fully populated `SharedRequestData` must satisfy every mapped request type.

        Any mapped field that cannot be resolved raises ValueError, so reaching the asserts
        proves the whole table is wired to resolvable properties.
        """
        data: SharedRequestData = _full()

        filled: Message = data.fill_missing_fields(request=request_type())

        for request_field_name in data._request_field__to__field__per__request_type[request_type]:
            value: Optional[Any] = _get_nested(filled, request_field_name)
            assert value, f"{request_type.__name__}.{request_field_name} was not filled"


def _get_nested(message: Message, dotted_field: str) -> Any:
    """Read a possibly dotted protobuf field path off `message`."""
    value: Any = message
    for part in dotted_field.split("."):
        value = getattr(value, part)
    return value
