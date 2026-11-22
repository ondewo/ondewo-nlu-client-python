"""Pins the 7.7.0 ``SessionStep.interruption`` field and the aligned heard-text precisions in the generated stubs."""

from ondewo.nlu import session_pb2


def test_session_step_carries_the_typed_interruption_as_field_12() -> None:
    field = session_pb2.SessionStep.DESCRIPTOR.fields_by_name["interruption"]
    assert field.number == 12
    assert field.message_type is session_pb2.SessionStepInterruption.DESCRIPTOR


def test_the_aligned_precisions_exist() -> None:
    assert session_pb2.HeardTextPrecision.Value("HEARD_TEXT_PRECISION_SENTENCE_ALIGNED") == 5
    assert session_pb2.HeardTextPrecision.Value("HEARD_TEXT_PRECISION_WORD_TIMED") == 6


def test_session_step_interruption_fields() -> None:
    fields = session_pb2.SessionStepInterruption.DESCRIPTOR.fields_by_name
    assert [(name, fields[name].number) for name in fields] == [
        ("interrupted", 1),
        ("cancelled", 2),
        ("phase", 3),
        ("turn_interruption_reason", 4),
        ("heard_report_revision", 5),
        ("heard_text_precision", 6),
        ("heard_char_count", 7),
        ("total_char_count", 8),
        ("generated_text", 9),
        ("tools_in_flight", 10),
        ("skipped_sip_trigger_count", 11),
        ("caller_overlap_duration_in_s", 12),
    ]
    assert session_pb2.SessionStepInterruptionPhase.Value("SESSION_STEP_INTERRUPTION_PHASE_GENERATING") == 1
    assert session_pb2.SessionStepInterruptionPhase.Value("SESSION_STEP_INTERRUPTION_PHASE_FINISHED") == 2
    assert not session_pb2.SessionStep().HasField("interruption")
