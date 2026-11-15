# Copyright 2021-2026 ONDEWO GmbH
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
Descriptor guards on the nlu-api 7.6.0 warm transfer intro wire contract (OND236-120).

Field numbers, field types, field presence, enum value names and the HTTP bindings are the wire contract between
ondewo-vtsi (client) and ondewo-cai (server). Two fields are ``optional`` on purpose, because an unset value means
"take the next configuration level": ``WarmTransferIntroConfig.confirm_human_before_intro`` and
``decline_reason_question``, and the agent level's ``enabled`` and ``decline_reason_question``. A regenerated stub that
lost that presence would make ``HasField`` raise, so the presence is pinned here too.

No network is touched.
"""

from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)

import pytest
from google.api import (
    annotations_pb2,
    http_pb2,
)
from google.protobuf.descriptor import (
    Descriptor,
    EnumDescriptor,
    FieldDescriptor,
    FileDescriptor,
    MethodDescriptor,
)

from ondewo.nlu import (
    agent_pb2,
    session_pb2,
)

# (field name, field number, cpp type, message or enum full name or None).
FieldSpec = Tuple[str, int, int, Optional[str]]

_STRING: int = FieldDescriptor.CPPTYPE_STRING
_MESSAGE: int = FieldDescriptor.CPPTYPE_MESSAGE
_ENUM: int = FieldDescriptor.CPPTYPE_ENUM
_INT32: int = FieldDescriptor.CPPTYPE_INT32
_BOOL: int = FieldDescriptor.CPPTYPE_BOOL

_TEXT_SOURCE: str = "ondewo.nlu.WarmTransferIntroTextSource"

EXPECTED_SESSION_FIELDS: Dict[str, List[FieldSpec]] = {
    "WarmTransferIntroConfig": [
        ("intro_prompt", 1, _STRING, None),
        ("text_source", 2, _ENUM, _TEXT_SOURCE),
        ("ready_question", 3, _STRING, None),
        ("confirm_human_before_intro", 4, _BOOL, None),
        ("accept_question", 5, _STRING, None),
        ("decline_reason_question", 6, _STRING, None),
        ("caller_declined_message", 7, _STRING, None),
        ("caller_unreachable_message", 8, _STRING, None),
        ("accept_dtmf", 9, _STRING, None),
        ("decline_dtmf", 10, _STRING, None),
        ("callee_display_name", 11, _STRING, None),
        ("callee_description", 12, _STRING, None),
        ("llm_ccai_service_name", 13, _STRING, None),
        ("max_history_steps", 14, _INT32, None),
        ("decision_timeout_s", 15, _INT32, None),
        ("project_display_name", 16, _STRING, None),
    ],
    "PrepareWarmTransferIntroRequest": [
        ("intro_session", 1, _STRING, None),
        ("source_session", 2, _STRING, None),
        ("config", 3, _MESSAGE, "ondewo.nlu.WarmTransferIntroConfig"),
        ("language_code", 4, _STRING, None),
        ("transfer_request_id", 5, _STRING, None),
    ],
    "PrepareWarmTransferIntroResponse": [
        ("text_source_used", 1, _ENUM, _TEXT_SOURCE),
        ("text_fell_back", 2, _BOOL, None),
        ("intro_text_chars", 3, _INT32, None),
        ("prompt_digest", 4, _STRING, None),
    ],
    "GetWarmTransferIntroOutcomeRequest": [
        ("intro_session", 1, _STRING, None),
    ],
    "WarmTransferIntroOutcome": [
        ("decision", 1, _ENUM, "ondewo.nlu.WarmTransferIntroDecision"),
        ("decided_by", 2, _ENUM, "ondewo.nlu.WarmTransferIntroDecidedBy"),
        ("decline_reason_present", 3, _BOOL, None),
        ("stage", 4, _ENUM, "ondewo.nlu.WarmTransferIntroStage"),
        ("cause", 5, _STRING, None),
    ],
}

EXPECTED_AGENT_FIELDS: Dict[str, List[FieldSpec]] = {
    "WarmTransferAgentSettings": [
        ("enabled", 1, _BOOL, None),
        ("llm_ccai_service_name", 2, _STRING, None),
        ("default_texts", 3, _MESSAGE, "ondewo.nlu.WarmTransferAgentSettings.DefaultTextsEntry"),
        ("extra_lexicon", 4, _MESSAGE, "ondewo.nlu.WarmTransferAgentSettings.ExtraLexiconEntry"),
    ],
    "WarmTransferAgentTexts": [
        ("ready_question", 1, _STRING, None),
        ("accept_question", 2, _STRING, None),
        ("decline_reason_question", 3, _STRING, None),
        ("caller_declined_message", 4, _STRING, None),
        ("caller_unreachable_message", 5, _STRING, None),
    ],
    "WarmTransferAgentLexicon": [
        ("accept_phrases", 1, _STRING, None),
        ("decline_phrases", 2, _STRING, None),
    ],
}

# Fields that carry presence (proto3 ``optional``): unset means "the next configuration level decides".
OPTIONAL_FIELDS: List[Tuple[Descriptor, str]] = [
    (session_pb2.WarmTransferIntroConfig.DESCRIPTOR, "confirm_human_before_intro"),
    (session_pb2.WarmTransferIntroConfig.DESCRIPTOR, "decline_reason_question"),
    (agent_pb2.WarmTransferAgentSettings.DESCRIPTOR, "enabled"),
    (agent_pb2.WarmTransferAgentTexts.DESCRIPTOR, "decline_reason_question"),
]

EXPECTED_ENUMS: Dict[str, List[str]] = {
    "WarmTransferIntroTextSource": [
        "WARM_TRANSFER_INTRO_TEXT_SOURCE_UNSPECIFIED",
        "WARM_TRANSFER_INTRO_TEXT_SOURCE_TEMPLATE",
        "WARM_TRANSFER_INTRO_TEXT_SOURCE_LLM_SUMMARY",
    ],
    "WarmTransferIntroDecision": [
        "WARM_TRANSFER_INTRO_DECISION_UNSPECIFIED",
        "WARM_TRANSFER_INTRO_DECISION_PENDING",
        "WARM_TRANSFER_INTRO_DECISION_ACCEPTED",
        "WARM_TRANSFER_INTRO_DECISION_DECLINED",
        "WARM_TRANSFER_INTRO_DECISION_NO_DECISION",
    ],
    "WarmTransferIntroDecidedBy": [
        "WARM_TRANSFER_INTRO_DECIDED_BY_UNSPECIFIED",
        "WARM_TRANSFER_INTRO_DECIDED_BY_DTMF",
        "WARM_TRANSFER_INTRO_DECIDED_BY_SPEECH",
        "WARM_TRANSFER_INTRO_DECIDED_BY_TIMEOUT",
    ],
    "WarmTransferIntroStage": [
        "WARM_TRANSFER_INTRO_STAGE_UNSPECIFIED",
        "WARM_TRANSFER_INTRO_STAGE_PREPARED",
        "WARM_TRANSFER_INTRO_STAGE_READY_ASKED",
        "WARM_TRANSFER_INTRO_STAGE_INTRO_SPOKEN",
        "WARM_TRANSFER_INTRO_STAGE_REASON_ASKED",
        "WARM_TRANSFER_INTRO_STAGE_CLOSED",
    ],
}


def _type_name(field: FieldDescriptor) -> Optional[str]:
    """
    Return the full name of a field's message or enum type.

    Args:
        field (FieldDescriptor):
            The field.

    Returns:
        Optional[str]:
            The message or enum full name, or None for a scalar field.
    """
    if field.message_type is not None:
        return str(field.message_type.full_name)
    if field.enum_type is not None:
        return str(field.enum_type.full_name)
    return None


def _spec_of(descriptor: Descriptor) -> List[FieldSpec]:
    """
    Render a message's fields as ``FieldSpec`` tuples in field-number order.

    Args:
        descriptor (Descriptor):
            The message descriptor.

    Returns:
        List[FieldSpec]:
            One tuple per declared field.
    """
    return [(f.name, f.number, f.cpp_type, _type_name(f)) for f in sorted(descriptor.fields, key=lambda f: f.number)]


def _sessions_method(name: str) -> MethodDescriptor:
    """
    Look up an RPC of the ``Sessions`` service.

    Args:
        name (str):
            The RPC name.

    Returns:
        MethodDescriptor:
            Its descriptor.
    """
    file_descriptor: FileDescriptor = session_pb2.DESCRIPTOR
    method: MethodDescriptor = file_descriptor.services_by_name["Sessions"].methods_by_name[name]
    return method


class TestSessionMessages:
    """Every new session message has exactly the fields, numbers and types of the 7.6.0 contract."""

    @pytest.mark.parametrize("message_name", sorted(EXPECTED_SESSION_FIELDS))
    def test_fields_numbers_and_types(self, message_name: str) -> None:
        """The message declares exactly the expected fields."""
        descriptor: Descriptor = session_pb2.DESCRIPTOR.message_types_by_name[message_name]
        assert _spec_of(descriptor) == EXPECTED_SESSION_FIELDS[message_name]

    def test_the_request_is_exposed_as_a_class(self) -> None:
        """``session_pb2.PrepareWarmTransferIntroRequest`` builds and round-trips."""
        request = session_pb2.PrepareWarmTransferIntroRequest(
            intro_session="projects/p/agent/sessions/intro",
            source_session="projects/p/agent/sessions/source",
            config=session_pb2.WarmTransferIntroConfig(
                text_source=session_pb2.WARM_TRANSFER_INTRO_TEXT_SOURCE_LLM_SUMMARY,
                confirm_human_before_intro=False,
            ),
            language_code="de",
            transfer_request_id="t-1",
        )
        assert session_pb2.PrepareWarmTransferIntroRequest.FromString(request.SerializeToString()) == request


class TestAgentMessages:
    """``Agent.warm_transfer_settings`` (15) and the three messages it is built from."""

    @pytest.mark.parametrize("message_name", sorted(EXPECTED_AGENT_FIELDS))
    def test_fields_numbers_and_types(self, message_name: str) -> None:
        """The message declares exactly the expected fields."""
        descriptor: Descriptor = agent_pb2.DESCRIPTOR.message_types_by_name[message_name]
        assert _spec_of(descriptor) == EXPECTED_AGENT_FIELDS[message_name]

    def test_agent_carries_the_settings_at_field_15(self) -> None:
        """``Agent.warm_transfer_settings`` is the ``WarmTransferAgentSettings`` message at field 15."""
        field: FieldDescriptor = agent_pb2.Agent.DESCRIPTOR.fields_by_name["warm_transfer_settings"]
        assert (field.number, _type_name(field)) == (15, "ondewo.nlu.WarmTransferAgentSettings")

    def test_the_maps_are_keyed_by_language_code(self) -> None:
        """``default_texts`` and ``extra_lexicon`` are ``map<string, …>``."""
        settings = agent_pb2.WarmTransferAgentSettings()
        settings.default_texts["de"].ready_question = "Sind Sie bereit?"
        settings.extra_lexicon["de"].accept_phrases.append("passt")
        assert settings.default_texts["de"].ready_question == "Sind Sie bereit?"
        assert list(settings.extra_lexicon["de"].accept_phrases) == ["passt"]

    def test_the_phrases_are_repeated(self) -> None:
        """Both lexicon lists are repeated strings."""
        descriptor: Descriptor = agent_pb2.WarmTransferAgentLexicon.DESCRIPTOR
        assert all(f.is_repeated for f in descriptor.fields)


class TestPresence:
    """The ``optional`` fields keep their presence: unset is distinguishable from the default value."""

    @pytest.mark.parametrize(("descriptor", "field_name"), OPTIONAL_FIELDS)
    def test_field_has_presence(self, descriptor: Descriptor, field_name: str) -> None:
        """The field tracks presence and sits in its synthetic oneof."""
        field: FieldDescriptor = descriptor.fields_by_name[field_name]
        assert field.has_presence
        assert field.containing_oneof is not None
        assert field.containing_oneof.name == f"_{field_name}"

    def test_unset_and_default_are_different(self) -> None:
        """An explicit ``False`` / ``""`` is set; an untouched field is not."""
        config = session_pb2.WarmTransferIntroConfig()
        assert not config.HasField("confirm_human_before_intro")
        assert not config.HasField("decline_reason_question")
        config.confirm_human_before_intro = False
        config.decline_reason_question = ""
        assert config.HasField("confirm_human_before_intro")
        assert config.HasField("decline_reason_question")

    def test_no_other_new_field_has_presence(self) -> None:
        """Every other scalar of the new messages is plain: empty means "agent default, then built-in"."""
        optional_names: List[Tuple[str, str]] = [(d.name, name) for d, name in OPTIONAL_FIELDS]
        descriptors: List[Descriptor] = [
            *(session_pb2.DESCRIPTOR.message_types_by_name[n] for n in EXPECTED_SESSION_FIELDS),
            *(agent_pb2.DESCRIPTOR.message_types_by_name[n] for n in EXPECTED_AGENT_FIELDS),
        ]
        with_presence: List[Tuple[str, str]] = [
            (d.name, f.name)
            for d in descriptors
            for f in d.fields
            if f.cpp_type != _MESSAGE and not f.is_repeated and f.has_presence
        ]
        assert sorted(with_presence) == sorted(optional_names)


class TestEnums:
    """Every new enum value carries the full ``WARM_TRANSFER_INTRO_*`` prefix."""

    @pytest.mark.parametrize("enum_name", sorted(EXPECTED_ENUMS))
    def test_values_in_number_order(self, enum_name: str) -> None:
        """The enum declares exactly the expected values, numbered from 0 without gaps."""
        descriptor: EnumDescriptor = session_pb2.DESCRIPTOR.enum_types_by_name[enum_name]
        expected: List[str] = EXPECTED_ENUMS[enum_name]
        assert [v.name for v in sorted(descriptor.values, key=lambda v: v.number)] == expected
        assert sorted(v.number for v in descriptor.values) == list(range(len(expected)))


class TestRpcs:
    """The two unary ``Sessions`` RPCs and their HTTP bindings."""

    def test_prepare_signature(self) -> None:
        """``PrepareWarmTransferIntro`` is unary both ways."""
        method: MethodDescriptor = _sessions_method("PrepareWarmTransferIntro")
        assert method.input_type.full_name == "ondewo.nlu.PrepareWarmTransferIntroRequest"
        assert method.output_type.full_name == "ondewo.nlu.PrepareWarmTransferIntroResponse"
        assert not method.client_streaming
        assert not method.server_streaming

    def test_prepare_http_binding(self) -> None:
        """``POST /v2/{intro_session=projects/*/agent/sessions/*}:prepareWarmTransferIntro``."""
        rule: http_pb2.HttpRule = (
            _sessions_method("PrepareWarmTransferIntro").GetOptions().Extensions[annotations_pb2.http]
        )
        assert (rule.post, rule.body) == (
            "/v2/{intro_session=projects/*/agent/sessions/*}:prepareWarmTransferIntro",
            "*",
        )

    def test_get_outcome_signature(self) -> None:
        """``GetWarmTransferIntroOutcome`` is unary both ways and answers the outcome message itself."""
        method: MethodDescriptor = _sessions_method("GetWarmTransferIntroOutcome")
        assert method.input_type.full_name == "ondewo.nlu.GetWarmTransferIntroOutcomeRequest"
        assert method.output_type.full_name == "ondewo.nlu.WarmTransferIntroOutcome"
        assert not method.client_streaming
        assert not method.server_streaming

    def test_get_outcome_http_binding(self) -> None:
        """``GET /v2/{intro_session=projects/*/agent/sessions/*}/warmTransferIntroOutcome``."""
        rule: http_pb2.HttpRule = (
            _sessions_method("GetWarmTransferIntroOutcome").GetOptions().Extensions[annotations_pb2.http]
        )
        assert rule.get == "/v2/{intro_session=projects/*/agent/sessions/*}/warmTransferIntroOutcome"
