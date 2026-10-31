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
Descriptor guards on the nlu-api 7.5.0 turn-control wire contract (OND236-120).

Field numbers, field types, oneof membership and enum value names are the wire contract with ondewo-csi
(client) and ondewo-cai (server); a renumbered field or a field that slips into a oneof makes the two disagree
without any error. These tests read the generated descriptors, so they fail when the vendored ``session.proto``
and the generated ``session_pb2`` drift, as well as when the contract itself changes.

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
from google.protobuf import descriptor_pb2
from google.protobuf.descriptor import (
    Descriptor,
    EnumDescriptor,
    FieldDescriptor,
)

from ondewo.nlu import session_pb2

# (field name, field number, cpp type, message or enum full name or None) per message.
FieldSpec = Tuple[str, int, int, Optional[str]]

_STRING: int = FieldDescriptor.CPPTYPE_STRING
_MESSAGE: int = FieldDescriptor.CPPTYPE_MESSAGE
_ENUM: int = FieldDescriptor.CPPTYPE_ENUM
_INT32: int = FieldDescriptor.CPPTYPE_INT32
_FLOAT: int = FieldDescriptor.CPPTYPE_FLOAT
_BOOL: int = FieldDescriptor.CPPTYPE_BOOL

EXPECTED_FIELDS: Dict[str, List[FieldSpec]] = {
    "TurnControl": [
        ("cancel_turn", 1, _MESSAGE, "ondewo.nlu.CancelTurn"),
        ("heard_report", 2, _MESSAGE, "ondewo.nlu.HeardReport"),
        ("discard_draft", 3, _MESSAGE, "ondewo.nlu.DiscardDraft"),
    ],
    "CancelTurn": [
        ("response_id", 1, _STRING, None),
        ("client_turn_id", 2, _STRING, None),
        ("turn_interruption_reason", 3, _ENUM, "ondewo.nlu.TurnInterruptionReason"),
        ("decided_at", 4, _MESSAGE, "google.protobuf.Timestamp"),
        ("background_work_policy", 5, _ENUM, "ondewo.nlu.BackgroundWorkPolicy"),
    ],
    "HeardMessage": [
        ("fulfillment_message_index", 1, _INT32, None),
        ("platform", 2, _ENUM, "ondewo.nlu.Intent.Message.Platform"),
        ("full_text", 3, _STRING, None),
        ("heard_text", 4, _STRING, None),
        ("heard_char_count", 5, _INT32, None),
        ("heard_audio_duration_in_s", 6, _FLOAT, None),
        ("total_audio_duration_in_s", 7, _FLOAT, None),
        ("completed", 8, _BOOL, None),
        ("never_started", 9, _BOOL, None),
        ("skipped_sip_trigger", 10, _BOOL, None),
        ("filler_id", 11, _STRING, None),
    ],
    "HeardReport": [
        ("response_id", 1, _STRING, None),
        ("client_turn_id", 2, _STRING, None),
        ("revision", 3, _INT32, None),
        ("turn_interruption_reason", 4, _ENUM, "ondewo.nlu.TurnInterruptionReason"),
        ("heard_messages", 5, _MESSAGE, "ondewo.nlu.HeardMessage"),
        ("heard_text_precision", 6, _ENUM, "ondewo.nlu.HeardTextPrecision"),
        ("caller_overlap_duration_in_s", 7, _FLOAT, None),
    ],
    "DiscardDraft": [
        ("response_id", 1, _STRING, None),
    ],
    "TurnControlAck": [
        ("response_id", 1, _STRING, None),
        ("client_turn_id", 2, _STRING, None),
        ("turn_control_ack_status", 3, _ENUM, "ondewo.nlu.TurnControlAckStatus"),
        ("server_cancel_duration_in_s", 4, _FLOAT, None),
    ],
    "InterruptTurnRequest": [
        ("session", 1, _STRING, None),
        ("turn_control", 2, _MESSAGE, "ondewo.nlu.TurnControl"),
    ],
    "InterruptTurnResponse": [
        ("turn_control_ack", 1, _MESSAGE, "ondewo.nlu.TurnControlAck"),
    ],
}

# Enum full name -> (required value prefix, expected value names in number order).
EXPECTED_ENUMS: Dict[str, Tuple[str, List[str]]] = {
    "TurnInterruptionReason": (
        "TURN_INTERRUPTION_REASON_",
        [
            "TURN_INTERRUPTION_REASON_UNSPECIFIED",
            "TURN_INTERRUPTION_REASON_BARGE_IN",
            "TURN_INTERRUPTION_REASON_CALLER_SPOKE_WHILE_THINKING",
            "TURN_INTERRUPTION_REASON_CALL_ENDED",
            "TURN_INTERRUPTION_REASON_FILLER_CUT",
            "TURN_INTERRUPTION_REASON_NO_FINAL_TIMEOUT",
            "TURN_INTERRUPTION_REASON_OPERATOR_TAKEOVER",
            "TURN_INTERRUPTION_REASON_BOT_MUTED",
        ],
    ),
    "BackgroundWorkPolicy": (
        "BACKGROUND_WORK_POLICY_",
        ["BACKGROUND_WORK_POLICY_KEEP", "BACKGROUND_WORK_POLICY_CANCEL_PENDING"],
    ),
    "HeardTextPrecision": (
        "HEARD_TEXT_PRECISION_",
        [
            "HEARD_TEXT_PRECISION_UNSPECIFIED",
            "HEARD_TEXT_PRECISION_NONE_HEARD",
            "HEARD_TEXT_PRECISION_FULL",
            "HEARD_TEXT_PRECISION_ESTIMATED_SERVER",
            "HEARD_TEXT_PRECISION_PROPORTIONAL",
        ],
    ),
    "TurnControlAckStatus": (
        "TURN_CONTROL_ACK_STATUS_",
        [
            "TURN_CONTROL_ACK_STATUS_UNSPECIFIED",
            "TURN_CONTROL_ACK_STATUS_CANCELLED",
            "TURN_CONTROL_ACK_STATUS_CANCELLED_QUEUED",
            "TURN_CONTROL_ACK_STATUS_ALREADY_FINISHED",
            "TURN_CONTROL_ACK_STATUS_UNKNOWN_TURN",
            "TURN_CONTROL_ACK_STATUS_HEARD_APPLIED",
            "TURN_CONTROL_ACK_STATUS_HEARD_STALE",
            "TURN_CONTROL_ACK_STATUS_DRAFT_DISCARDED",
        ],
    ),
}

REQUEST: Descriptor = session_pb2.StreamingDetectIntentRequest.DESCRIPTOR
RESPONSE: Descriptor = session_pb2.StreamingDetectIntentResponse.DESCRIPTOR
TELEMETRY_ONEOF: str = "telemetry_event"


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


class TestStreamingDetectIntentRequest:
    """The request gains ``turn_control`` (7) and ``client_turn_id`` (8)."""

    def test_turn_control_is_field_7(self) -> None:
        """``turn_control`` is the ``TurnControl`` message at field 7."""
        field: FieldDescriptor = REQUEST.fields_by_name["turn_control"]
        assert (field.number, _type_name(field)) == (7, "ondewo.nlu.TurnControl")

    def test_client_turn_id_is_string_field_8(self) -> None:
        """``client_turn_id`` is a string at field 8."""
        field: FieldDescriptor = REQUEST.fields_by_name["client_turn_id"]
        assert (field.number, field.cpp_type) == (8, _STRING)

    def test_field_5_stays_undeclared(self) -> None:
        """Field 5 is neither declared nor reserved (review NLU-9: no ``reserved 5``)."""
        assert 5 not in REQUEST.fields_by_number
        assert not any(start <= 5 < end for start, end in _reserved_ranges(REQUEST))

    def test_existing_fields_keep_their_numbers(self) -> None:
        """The pre-7.5.0 fields are untouched."""
        numbers: Dict[str, int] = {f.name: f.number for f in REQUEST.fields}
        expected: Dict[str, int] = {
            "session": 1,
            "query_params": 2,
            "query_input": 3,
            "single_utterance": 4,
            "input_audio": 6,
        }
        assert {name: numbers[name] for name in expected} == expected

    def test_new_request_fields_are_in_no_oneof(self) -> None:
        """Neither new field is part of a oneof, so they combine freely with every other field."""
        assert REQUEST.fields_by_name["turn_control"].containing_oneof is None
        assert REQUEST.fields_by_name["client_turn_id"].containing_oneof is None

    def test_a_control_only_request_round_trips(self) -> None:
        """A request carrying only a ``CancelTurn`` serializes and parses back unchanged."""
        request = session_pb2.StreamingDetectIntentRequest(
            turn_control=session_pb2.TurnControl(
                cancel_turn=session_pb2.CancelTurn(
                    client_turn_id="abc",
                    turn_interruption_reason=session_pb2.TURN_INTERRUPTION_REASON_BARGE_IN,
                )
            )
        )
        parsed = session_pb2.StreamingDetectIntentRequest.FromString(request.SerializeToString())
        assert parsed == request
        assert not parsed.HasField("query_input")
        assert parsed.turn_control.WhichOneof("turn_control") == "cancel_turn"


def _reserved_ranges(descriptor: Descriptor) -> List[Tuple[int, int]]:
    """
    Return the reserved field-number ranges of a message as half-open ``(start, end)`` pairs.

    Args:
        descriptor (Descriptor):
            The message descriptor.

    Returns:
        List[Tuple[int, int]]:
            The reserved ranges.
    """
    proto = descriptor_pb2.DescriptorProto()
    descriptor.CopyToProto(proto)
    return [(r.start, r.end) for r in proto.reserved_range]


class TestStreamingDetectIntentResponse:
    """The response gains ``turn_control_ack`` (12) and ``client_turn_id`` (13), both outside the oneof."""

    def test_turn_control_ack_is_field_12(self) -> None:
        """``turn_control_ack`` is the ``TurnControlAck`` message at field 12."""
        field: FieldDescriptor = RESPONSE.fields_by_name["turn_control_ack"]
        assert (field.number, _type_name(field)) == (12, "ondewo.nlu.TurnControlAck")

    def test_client_turn_id_is_string_field_13(self) -> None:
        """``client_turn_id`` (the echo) is a string at field 13."""
        field: FieldDescriptor = RESPONSE.fields_by_name["client_turn_id"]
        assert (field.number, field.cpp_type) == (13, _STRING)

    def test_ack_and_echo_are_not_in_the_telemetry_oneof(self) -> None:
        """The ack is top level: in the oneof it would clear (and be cleared by) a telemetry event."""
        assert RESPONSE.fields_by_name["turn_control_ack"].containing_oneof is None
        assert RESPONSE.fields_by_name["client_turn_id"].containing_oneof is None

    def test_the_telemetry_oneof_holds_only_its_7_4_0_members(self) -> None:
        """The oneof still holds exactly fields 5-11, so nothing new joined it."""
        oneof_numbers: List[int] = sorted(f.number for f in RESPONSE.oneofs_by_name[TELEMETRY_ONEOF].fields)
        assert oneof_numbers == list(range(5, 12))

    def test_an_ack_and_a_telemetry_event_coexist_on_the_wire(self) -> None:
        """Setting both keeps both after a round trip, which a shared oneof could not."""
        response = session_pb2.StreamingDetectIntentResponse(
            client_turn_id="abc",
            turn_control_ack=session_pb2.TurnControlAck(
                turn_control_ack_status=session_pb2.TURN_CONTROL_ACK_STATUS_CANCELLED,
            ),
            llm_token_usage_update=session_pb2.LlmTokenUsageUpdateEvent(llm_call_id="call-1"),
        )
        parsed = session_pb2.StreamingDetectIntentResponse.FromString(response.SerializeToString())
        assert parsed.HasField("turn_control_ack")
        assert parsed.WhichOneof("telemetry_event") == "llm_token_usage_update"
        assert parsed.client_turn_id == "abc"


class TestQueryParametersPreemptiveDraft:
    """``QueryParameters`` gains ``preemptive_draft`` (15), the mark ``DiscardDraft`` keys on."""

    def test_preemptive_draft_is_singular_bool_field_15(self) -> None:
        """``preemptive_draft`` is a singular bool at field 15."""
        field: FieldDescriptor = session_pb2.QueryParameters.DESCRIPTOR.fields_by_name["preemptive_draft"]
        assert (field.number, field.cpp_type) == (15, _BOOL)
        assert not field.is_repeated

    def test_preemptive_draft_is_in_no_oneof(self) -> None:
        """The mark combines freely with every other query parameter."""
        field: FieldDescriptor = session_pb2.QueryParameters.DESCRIPTOR.fields_by_name["preemptive_draft"]
        assert field.containing_oneof is None


class TestTurnControlMessages:
    """Every new message has exactly the fields, numbers and types of the 7.5.0 contract."""

    @pytest.mark.parametrize("message_name", sorted(EXPECTED_FIELDS))
    def test_fields_numbers_and_types(self, message_name: str) -> None:
        """The message declares exactly the expected fields."""
        descriptor: Descriptor = session_pb2.DESCRIPTOR.message_types_by_name[message_name]
        assert _spec_of(descriptor) == EXPECTED_FIELDS[message_name]

    def test_turn_control_oneof_holds_exactly_the_three_controls(self) -> None:
        """``cancel_turn``, ``heard_report`` and ``discard_draft`` are the oneof; nothing is outside it."""
        descriptor: Descriptor = session_pb2.TurnControl.DESCRIPTOR
        assert [o.name for o in descriptor.oneofs] == ["turn_control"]
        assert sorted(f.name for f in descriptor.oneofs_by_name["turn_control"].fields) == [
            "cancel_turn",
            "discard_draft",
            "heard_report",
        ]
        assert all(f.containing_oneof is not None for f in descriptor.fields)

    def test_the_ack_is_not_a_turn_control(self) -> None:
        """A ``TurnControlAck`` is an answer, never something a client sends: it is not in the oneof."""
        type_names: List[Optional[str]] = [_type_name(f) for f in session_pb2.TurnControl.DESCRIPTOR.fields]
        assert "ondewo.nlu.TurnControlAck" not in type_names

    def test_cancel_turn_carries_no_provisional_heard_report(self) -> None:
        """Review B6 / D8: the heard report travels separately, behind the cancel."""
        assert not any(_type_name(f) == "ondewo.nlu.HeardReport" for f in session_pb2.CancelTurn.DESCRIPTOR.fields)

    def test_heard_messages_is_repeated(self) -> None:
        """A report carries one entry per spoken, queued or skipped message."""
        field: FieldDescriptor = session_pb2.HeardReport.DESCRIPTOR.fields_by_name["heard_messages"]
        assert field.is_repeated

    def test_setting_one_control_clears_another(self) -> None:
        """The oneof makes the three controls mutually exclusive."""
        control = session_pb2.TurnControl(heard_report=session_pb2.HeardReport(revision=1))
        control.discard_draft.response_id = "r-1"
        assert control.WhichOneof("turn_control") == "discard_draft"
        assert not control.HasField("heard_report")


class TestEnums:
    """Every new enum value carries its enum's prefix (C-style flat enum namespace)."""

    @pytest.mark.parametrize("enum_name", sorted(EXPECTED_ENUMS))
    def test_values_in_number_order(self, enum_name: str) -> None:
        """The enum declares exactly the expected values, numbered from 0 without gaps."""
        descriptor: EnumDescriptor = session_pb2.DESCRIPTOR.enum_types_by_name[enum_name]
        _, expected = EXPECTED_ENUMS[enum_name]
        assert [v.name for v in sorted(descriptor.values, key=lambda v: v.number)] == expected
        assert sorted(v.number for v in descriptor.values) == list(range(len(expected)))

    @pytest.mark.parametrize("enum_name", sorted(EXPECTED_ENUMS))
    def test_every_value_is_prefixed(self, enum_name: str) -> None:
        """No value name is generic (e.g. a bare ``CANCELLED``)."""
        descriptor: EnumDescriptor = session_pb2.DESCRIPTOR.enum_types_by_name[enum_name]
        prefix, _ = EXPECTED_ENUMS[enum_name]
        assert [v.name for v in descriptor.values if not v.name.startswith(prefix)] == []

    def test_the_ack_status_enum_is_top_level(self) -> None:
        """``TurnControlAckStatus`` is a top-level enum, not nested in ``TurnControlAck``."""
        assert session_pb2.TurnControlAck.DESCRIPTOR.enum_types == []


class TestInterruptTurnRpc:
    """``Sessions.InterruptTurn`` is a unary Request/Response RPC with an HTTP binding."""

    def test_signature(self) -> None:
        """It takes an ``InterruptTurnRequest`` and returns an ``InterruptTurnResponse``, unary both ways."""
        method = session_pb2.DESCRIPTOR.services_by_name["Sessions"].methods_by_name["InterruptTurn"]
        assert method.input_type.full_name == "ondewo.nlu.InterruptTurnRequest"
        assert method.output_type.full_name == "ondewo.nlu.InterruptTurnResponse"
        assert not method.client_streaming
        assert not method.server_streaming

    def test_http_binding(self) -> None:
        """It is reachable as ``POST /v2/{session=projects/*/agent/sessions/*}:interruptTurn``."""
        method = session_pb2.DESCRIPTOR.services_by_name["Sessions"].methods_by_name["InterruptTurn"]
        rule: http_pb2.HttpRule = method.GetOptions().Extensions[annotations_pb2.http]
        assert (rule.post, rule.body) == ("/v2/{session=projects/*/agent/sessions/*}:interruptTurn", "*")
