# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ondewo/nlu/session.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.rpc import status_pb2 as google_dot_rpc_dot_status__pb2
from google.type import latlng_pb2 as google_dot_type_dot_latlng__pb2
from ondewo.nlu import context_pb2 as ondewo_dot_nlu_dot_context__pb2
from ondewo.nlu import intent_pb2 as ondewo_dot_nlu_dot_intent__pb2
from ondewo.nlu import entity_type_pb2 as ondewo_dot_nlu_dot_entity__type__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18ondewo/nlu/session.proto\x12\nondewo.nlu\x1a\x1cgoogle/api/annotations.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a google/protobuf/field_mask.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x17google/rpc/status.proto\x1a\x18google/type/latlng.proto\x1a\x18ondewo/nlu/context.proto\x1a\x17ondewo/nlu/intent.proto\x1a\x1condewo/nlu/entity_type.proto\"\x9b\x01\n\x13\x44\x65tectIntentRequest\x12\x0f\n\x07session\x18\x01 \x01(\t\x12\x31\n\x0cquery_params\x18\x02 \x01(\x0b\x32\x1b.ondewo.nlu.QueryParameters\x12+\n\x0bquery_input\x18\x03 \x01(\x0b\x32\x16.ondewo.nlu.QueryInput\x12\x13\n\x0binput_audio\x18\x05 \x01(\x0c\"\x86\x01\n\x14\x44\x65tectIntentResponse\x12\x13\n\x0bresponse_id\x18\x01 \x01(\t\x12-\n\x0cquery_result\x18\x02 \x01(\x0b\x32\x17.ondewo.nlu.QueryResult\x12*\n\x0ewebhook_status\x18\x03 \x01(\x0b\x32\x12.google.rpc.Status\"\xc8\x01\n\x0fQueryParameters\x12\x11\n\ttime_zone\x18\x01 \x01(\t\x12)\n\x0cgeo_location\x18\x02 \x01(\x0b\x32\x13.google.type.LatLng\x12%\n\x08\x63ontexts\x18\x03 \x03(\x0b\x32\x13.ondewo.nlu.Context\x12\x16\n\x0ereset_contexts\x18\x04 \x01(\x08\x12(\n\x07payload\x18\x06 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x0e\n\x06labels\x18\x07 \x03(\t\"\x9b\x01\n\nQueryInput\x12\x34\n\x0c\x61udio_config\x18\x01 \x01(\x0b\x32\x1c.ondewo.nlu.InputAudioConfigH\x00\x12%\n\x04text\x18\x02 \x01(\x0b\x32\x15.ondewo.nlu.TextInputH\x00\x12\'\n\x05\x65vent\x18\x03 \x01(\x0b\x32\x16.ondewo.nlu.EventInputH\x00\x42\x07\n\x05input\"\x88\x04\n\x0bQueryResult\x12\x12\n\nquery_text\x18\x01 \x01(\t\x12\x15\n\rlanguage_code\x18\x0f \x01(\t\x12%\n\x1dspeech_recognition_confidence\x18\x02 \x01(\x02\x12\x0e\n\x06\x61\x63tion\x18\x03 \x01(\t\x12+\n\nparameters\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\x12#\n\x1b\x61ll_required_params_present\x18\x05 \x01(\x08\x12\x18\n\x10\x66ulfillment_text\x18\x06 \x01(\t\x12\x38\n\x14\x66ulfillment_messages\x18\x07 \x03(\x0b\x32\x1a.ondewo.nlu.Intent.Message\x12\x16\n\x0ewebhook_source\x18\x08 \x01(\t\x12\x30\n\x0fwebhook_payload\x18\t \x01(\x0b\x32\x17.google.protobuf.Struct\x12,\n\x0foutput_contexts\x18\n \x03(\x0b\x32\x13.ondewo.nlu.Context\x12\"\n\x06intent\x18\x0b \x01(\x0b\x32\x12.ondewo.nlu.Intent\x12#\n\x1bintent_detection_confidence\x18\x0c \x01(\x02\x12\x30\n\x0f\x64iagnostic_info\x18\x0e \x01(\x0b\x32\x17.google.protobuf.Struct\"\xbe\x01\n\x1cStreamingDetectIntentRequest\x12\x0f\n\x07session\x18\x01 \x01(\t\x12\x31\n\x0cquery_params\x18\x02 \x01(\x0b\x32\x1b.ondewo.nlu.QueryParameters\x12+\n\x0bquery_input\x18\x03 \x01(\x0b\x32\x16.ondewo.nlu.QueryInput\x12\x18\n\x10single_utterance\x18\x04 \x01(\x08\x12\x13\n\x0binput_audio\x18\x06 \x01(\x0c\"\xd3\x01\n\x1dStreamingDetectIntentResponse\x12\x13\n\x0bresponse_id\x18\x01 \x01(\t\x12\x42\n\x12recognition_result\x18\x02 \x01(\x0b\x32&.ondewo.nlu.StreamingRecognitionResult\x12-\n\x0cquery_result\x18\x03 \x01(\x0b\x32\x17.ondewo.nlu.QueryResult\x12*\n\x0ewebhook_status\x18\x04 \x01(\x0b\x32\x12.google.rpc.Status\"\xfa\x01\n\x1aStreamingRecognitionResult\x12H\n\x0cmessage_type\x18\x01 \x01(\x0e\x32\x32.ondewo.nlu.StreamingRecognitionResult.MessageType\x12\x12\n\ntranscript\x18\x02 \x01(\t\x12\x10\n\x08is_final\x18\x03 \x01(\x08\x12\x12\n\nconfidence\x18\x04 \x01(\x02\"X\n\x0bMessageType\x12\x1c\n\x18MESSAGE_TYPE_UNSPECIFIED\x10\x00\x12\x0e\n\nTRANSCRIPT\x10\x01\x12\x1b\n\x17\x45ND_OF_SINGLE_UTTERANCE\x10\x02\"\x8d\x01\n\x10InputAudioConfig\x12\x31\n\x0e\x61udio_encoding\x18\x01 \x01(\x0e\x32\x19.ondewo.nlu.AudioEncoding\x12\x19\n\x11sample_rate_hertz\x18\x02 \x01(\x05\x12\x15\n\rlanguage_code\x18\x03 \x01(\t\x12\x14\n\x0cphrase_hints\x18\x04 \x03(\t\"0\n\tTextInput\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x15\n\rlanguage_code\x18\x02 \x01(\t\"^\n\nEventInput\x12\x0c\n\x04name\x18\x01 \x01(\t\x12+\n\nparameters\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\x15\n\rlanguage_code\x18\x03 \x01(\t\"\xba\x01\n\x07Session\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12.\n\rsession_steps\x18\x02 \x03(\x0b\x32\x17.ondewo.nlu.SessionStep\x12-\n\x0csession_info\x18\x03 \x01(\x0b\x32\x17.ondewo.nlu.SessionInfo\"<\n\x04View\x12\x14\n\x10VIEW_UNSPECIFIED\x10\x00\x12\r\n\tVIEW_FULL\x10\x01\x12\x0f\n\x0bVIEW_SPARSE\x10\x02\"\xb6\x01\n\x0bSessionStep\x12>\n\x15\x64\x65tect_intent_request\x18\x01 \x01(\x0b\x32\x1f.ondewo.nlu.DetectIntentRequest\x12@\n\x16\x64\x65tect_intent_response\x18\x02 \x01(\x0b\x32 .ondewo.nlu.DetectIntentResponse\x12%\n\x08\x63ontexts\x18\x03 \x03(\x0b\x32\x13.ondewo.nlu.Context\"\x8c\x01\n\x17TrackSessionStepRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12-\n\x0csession_step\x18\x02 \x01(\x0b\x32\x17.ondewo.nlu.SessionStep\x12.\n\x0csession_view\x18\x03 \x01(\x0e\x32\x18.ondewo.nlu.Session.View\"\xcc\x01\n\x13ListSessionsRequest\x12\x0e\n\x06parent\x18\x01 \x01(\t\x12.\n\x0csession_view\x18\x02 \x01(\x0e\x32\x18.ondewo.nlu.Session.View\x12\x12\n\npage_token\x18\x04 \x01(\t\x12\x31\n\x0esession_filter\x18\x05 \x01(\x0b\x32\x19.ondewo.nlu.SessionFilter\x12.\n\nfield_mask\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\"\xd3\x0b\n\rSessionFilter\x12\x16\n\x0elanguage_codes\x18\x01 \x03(\t\x12+\n\x0fmatched_intents\x18\x02 \x03(\x0b\x32\x12.ondewo.nlu.Intent\x12\x34\n\x14matched_entity_types\x18\x03 \x03(\x0b\x32\x16.ondewo.nlu.EntityType\x12\"\n\x1amin_intents_confidence_min\x18\x04 \x01(\x02\x12\"\n\x1amin_intents_confidence_max\x18\x05 \x01(\x02\x12\'\n\x1fmin_entity_types_confidence_min\x18\x06 \x01(\x02\x12\'\n\x1fmin_entity_types_confidence_max\x18\x07 \x01(\x02\x12\x10\n\x08\x65\x61rliest\x18\x08 \x01(\x02\x12\x0e\n\x06latest\x18\t \x01(\x02\x12\x18\n\x10min_number_turns\x18\n \x01(\x05\x12\x18\n\x10max_number_turns\x18\x0b \x01(\x05\x12\x0e\n\x06labels\x18\x0c \x03(\t\x12\x10\n\x08user_ids\x18\r \x03(\t\x12\x13\n\x0bintent_tags\x18\x0e \x03(\t\x12\x13\n\x0bsession_ids\x18\x0f \x03(\t\x12+\n\x0einput_contexts\x18\x10 \x03(\x0b\x32\x13.ondewo.nlu.Context\x12,\n\x0foutput_contexts\x18\x11 \x03(\x0b\x32\x13.ondewo.nlu.Context\x12\x19\n\x11\x64uration_in_s_min\x18\x12 \x01(\x02\x12\x19\n\x11\x64uration_in_s_max\x18\x13 \x01(\x02\x12\x19\n\x11\x64uration_in_m_min\x18\x14 \x01(\x02\x12\x19\n\x11\x64uration_in_m_max\x18\x15 \x01(\x02\x12!\n\x19\x64uration_in_m_rounded_min\x18\x16 \x01(\x02\x12!\n\x19\x64uration_in_m_rounded_max\x18\x17 \x01(\x02\x12)\n!duration_interval_15s_rounded_min\x18\x18 \x01(\x02\x12)\n!duration_interval_15s_rounded_max\x18\x19 \x01(\x02\x12)\n!duration_interval_30s_rounded_min\x18\x1a \x01(\x02\x12)\n!duration_interval_30s_rounded_max\x18\x1b \x01(\x02\x12)\n!duration_interval_45s_rounded_min\x18\x1c \x01(\x02\x12)\n!duration_interval_45s_rounded_max\x18\x1d \x01(\x02\x12&\n\x1estarted_time_slot_per_hour_min\x18\x1e \x01(\t\x12&\n\x1estarted_time_slot_per_hour_max\x18\x1f \x01(\t\x12.\n&started_time_slot_per_quarter_hour_min\x18  \x01(\t\x12.\n&started_time_slot_per_quarter_hour_max\x18! \x01(\t\x12+\n#started_time_slot_per_half_hour_min\x18\" \x01(\t\x12+\n#started_time_slot_per_half_hour_max\x18# \x01(\t\x12+\n#started_time_slot_per_day_phase_min\x18$ \x01(\t\x12+\n#started_time_slot_per_day_phase_max\x18% \x01(\t\x12(\n started_time_slot_per_minute_min\x18& \x01(\t\x12(\n started_time_slot_per_minute_max\x18\' \x01(\t\x12!\n\x19\x64uration_in_s_rounded_min\x18( \x01(\x02\x12!\n\x19\x64uration_in_s_rounded_max\x18) \x01(\x02\"\xa7\x07\n\x0bSessionInfo\x12\x16\n\x0elanguage_codes\x18\x01 \x03(\t\x12+\n\x0fmatched_intents\x18\x02 \x03(\x0b\x32\x12.ondewo.nlu.Intent\x12\x34\n\x14matched_entity_types\x18\x03 \x03(\x0b\x32\x16.ondewo.nlu.EntityType\x12\x1e\n\x16min_intents_confidence\x18\x04 \x01(\x02\x12#\n\x1bmin_entity_types_confidence\x18\x05 \x01(\x02\x12\x10\n\x08\x65\x61rliest\x18\x06 \x01(\x02\x12\x0e\n\x06latest\x18\x07 \x01(\x02\x12\x14\n\x0cnumber_turns\x18\x08 \x01(\x05\x12\x0e\n\x06labels\x18\t \x03(\t\x12\x10\n\x08user_ids\x18\n \x03(\t\x12\x13\n\x0bintent_tags\x18\x0b \x03(\t\x12\x41\n\x13input_context_steps\x18\x0c \x03(\x0b\x32$.ondewo.nlu.SessionInfo.ContextSteps\x12\x42\n\x14output_context_steps\x18\r \x03(\x0b\x32$.ondewo.nlu.SessionInfo.ContextSteps\x12\x15\n\rduration_in_s\x18\x0e \x01(\x02\x12\x15\n\rduration_in_m\x18\x0f \x01(\x02\x12\x1d\n\x15\x64uration_in_m_rounded\x18\x10 \x01(\x02\x12%\n\x1d\x64uration_interval_15s_rounded\x18\x11 \x01(\x02\x12%\n\x1d\x64uration_interval_30s_rounded\x18\x12 \x01(\x02\x12%\n\x1d\x64uration_interval_45s_rounded\x18\x13 \x01(\x02\x12\"\n\x1astarted_time_slot_per_hour\x18\x14 \x01(\t\x12*\n\"started_time_slot_per_quarter_hour\x18\x15 \x01(\t\x12\'\n\x1fstarted_time_slot_per_half_hour\x18\x16 \x01(\t\x12\'\n\x1fstarted_time_slot_per_day_phase\x18\x17 \x01(\t\x12$\n\x1cstarted_time_slot_per_minute\x18\x18 \x01(\t\x12!\n\x19\x64uration_in_s_rounded_max\x18\x19 \x01(\x02\x1a\x35\n\x0c\x43ontextSteps\x12%\n\x08\x63ontexts\x18\x01 \x03(\x0b\x32\x13.ondewo.nlu.Context\"V\n\x14ListSessionsResponse\x12%\n\x08sessions\x18\x01 \x03(\x0b\x32\x13.ondewo.nlu.Session\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\x87\x01\n\x11GetSessionRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12.\n\x0csession_view\x18\x02 \x01(\x0e\x32\x18.ondewo.nlu.Session.View\x12.\n\nfield_mask\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\"L\n\x14\x43reateSessionRequest\x12\x0e\n\x06parent\x18\x01 \x01(\t\x12\x14\n\x0csession_uuid\x18\x02 \x01(\t\x12\x0e\n\x06labels\x18\x03 \x03(\t\"*\n\x14\x44\x65leteSessionRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\"\xba\x01\n\x1a\x43reateSessionReviewRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12\x18\n\x10parent_review_id\x18\x02 \x01(\t\x12\x31\n\x0esession_review\x18\x03 \x01(\x0b\x32\x19.ondewo.nlu.SessionReview\x12;\n\x13session_review_view\x18\x04 \x01(\x0e\x32\x1e.ondewo.nlu.SessionReview.View\"\xa5\x01\n\rSessionReview\x12\x19\n\x11session_review_id\x18\x01 \x01(\t\x12;\n\x14session_review_steps\x18\x02 \x03(\x0b\x32\x1d.ondewo.nlu.SessionReviewStep\"<\n\x04View\x12\x14\n\x10VIEW_UNSPECIFIED\x10\x00\x12\r\n\tVIEW_FULL\x10\x01\x12\x0f\n\x0bVIEW_SPARSE\x10\x02\"\xf1\x01\n\x11SessionReviewStep\x12=\n\x12\x61nnotated_usersays\x18\x01 \x01(\x0b\x32!.ondewo.nlu.Intent.TrainingPhrase\x12\x15\n\rlanguage_code\x18\x02 \x01(\t\x12\x34\n\x10\x64\x65tected_intents\x18\x03 \x03(\x0b\x32\x1a.ondewo.nlu.DetectedIntent\x12%\n\x08\x63ontexts\x18\x04 \x03(\x0b\x32\x13.ondewo.nlu.Context\x12)\n\x0c\x63ontexts_out\x18\x05 \x03(\x0b\x32\x13.ondewo.nlu.Context\"\xb0\x01\n\x0e\x44\x65tectedIntent\x12\"\n\x06intent\x18\x01 \x01(\x0b\x32\x12.ondewo.nlu.Intent\x12\r\n\x05score\x18\x02 \x01(\x02\x12\x11\n\talgorithm\x18\x03 \x01(\t\x12\x38\n\x14\x66ulfillment_messages\x18\x04 \x03(\x0b\x32\x1a.ondewo.nlu.Intent.Message\x12\x1e\n\x16required_param_missing\x18\x05 \x01(\x08\".\n\x18ListSessionLabelsRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\"7\n%ListSessionLabelsOfAllSessionsRequest\x12\x0e\n\x06parent\x18\x01 \x01(\t\"+\n\x19ListSessionLabelsResponse\x12\x0e\n\x06labels\x18\x01 \x03(\t\"=\n\x17\x41\x64\x64SessionLabelsRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12\x0e\n\x06labels\x18\x02 \x03(\t\"@\n\x1a\x44\x65leteSessionLabelsRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12\x0e\n\x06labels\x18\x02 \x03(\t\"\x80\x01\n\x19ListSessionReviewsRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12;\n\x13session_review_view\x18\x02 \x01(\x0e\x32\x1e.ondewo.nlu.SessionReview.View\x12\x12\n\npage_token\x18\x04 \x01(\t\"i\n\x1aListSessionReviewsResponse\x12\x32\n\x0fsession_reviews\x18\x01 \x03(\x0b\x32\x19.ondewo.nlu.SessionReview\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"q\n\x17GetSessionReviewRequest\x12\x19\n\x11session_review_id\x18\x01 \x01(\t\x12;\n\x13session_review_view\x18\x02 \x01(\x0e\x32\x1e.ondewo.nlu.SessionReview.View\"p\n\x1dGetLatestSessionReviewRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12;\n\x13session_review_view\x18\x02 \x01(\x0e\x32\x1e.ondewo.nlu.SessionReview.View*\xfb\x01\n\rAudioEncoding\x12\x1e\n\x1a\x41UDIO_ENCODING_UNSPECIFIED\x10\x00\x12\x1c\n\x18\x41UDIO_ENCODING_LINEAR_16\x10\x01\x12\x17\n\x13\x41UDIO_ENCODING_FLAC\x10\x02\x12\x18\n\x14\x41UDIO_ENCODING_MULAW\x10\x03\x12\x16\n\x12\x41UDIO_ENCODING_AMR\x10\x04\x12\x19\n\x15\x41UDIO_ENCODING_AMR_WB\x10\x05\x12\x1b\n\x17\x41UDIO_ENCODING_OGG_OPUS\x10\x06\x12)\n%AUDIO_ENCODING_SPEEX_WITH_HEADER_BYTE\x10\x07\x32\xc5\x11\n\x08Sessions\x12\x94\x01\n\x0c\x44\x65tectIntent\x12\x1f.ondewo.nlu.DetectIntentRequest\x1a .ondewo.nlu.DetectIntentResponse\"A\x82\xd3\xe4\x93\x02;\"6/v2/{session=projects/*/agent/sessions/*}:detectIntent:\x01*\x12p\n\x15StreamingDetectIntent\x12(.ondewo.nlu.StreamingDetectIntentRequest\x1a).ondewo.nlu.StreamingDetectIntentResponse(\x01\x30\x01\x12\x81\x01\n\x0cListSessions\x12\x1f.ondewo.nlu.ListSessionsRequest\x1a .ondewo.nlu.ListSessionsResponse\".\x82\xd3\xe4\x93\x02(\x12&/v2/{parent=projects/*/agent}/sessions\x12v\n\nGetSession\x12\x1d.ondewo.nlu.GetSessionRequest\x1a\x13.ondewo.nlu.Session\"4\x82\xd3\xe4\x93\x02.\x12,/v2/{session_id=projects/*/agent/sessions/*}\x12y\n\rCreateSession\x12 .ondewo.nlu.CreateSessionRequest\x1a\x13.ondewo.nlu.Session\"1\x82\xd3\xe4\x93\x02+\"&/v2/{parent=projects/*/agent}/sessions:\x01*\x12\x96\x01\n\x10TrackSessionStep\x12#.ondewo.nlu.TrackSessionStepRequest\x1a\x13.ondewo.nlu.Session\"H\x82\xd3\xe4\x93\x02\x42\"=/v2/{session_id=projects/*/agent/sessions/*}:trackSessionStep:\x01*\x12\x7f\n\rDeleteSession\x12 .ondewo.nlu.DeleteSessionRequest\x1a\x16.google.protobuf.Empty\"4\x82\xd3\xe4\x93\x02.*,/v2/{session_id=projects/*/agent/sessions/*}\x12\x9d\x01\n\x11ListSessionLabels\x12$.ondewo.nlu.ListSessionLabelsRequest\x1a%.ondewo.nlu.ListSessionLabelsResponse\";\x82\xd3\xe4\x93\x02\x35\x12\x33/v2/{session_id=projects/*/agent/sessions/*}/labels\x12\xb1\x01\n\x1eListSessionLabelsOfAllSessions\x12\x31.ondewo.nlu.ListSessionLabelsOfAllSessionsRequest\x1a%.ondewo.nlu.ListSessionLabelsResponse\"5\x82\xd3\xe4\x93\x02/\x12-/v2/{parent=projects/*/agent}/sessions/labels\x12\x90\x01\n\x10\x41\x64\x64SessionLabels\x12#.ondewo.nlu.AddSessionLabelsRequest\x1a\x13.ondewo.nlu.Session\"B\x82\xd3\xe4\x93\x02<\"7/v2/{session_id=projects/*/agent/sessions/*}/labels:add:\x01*\x12\x99\x01\n\x13\x44\x65leteSessionLabels\x12&.ondewo.nlu.DeleteSessionLabelsRequest\x1a\x13.ondewo.nlu.Session\"E\x82\xd3\xe4\x93\x02?\":/v2/{session_id=projects/*/agent/sessions/*}/labels:delete:\x01*\x12\xa1\x01\n\x12ListSessionReviews\x12%.ondewo.nlu.ListSessionReviewsRequest\x1a&.ondewo.nlu.ListSessionReviewsResponse\"<\x82\xd3\xe4\x93\x02\x36\x12\x34/v2/{session_id=projects/*/agent/sessions/*}/reviews\x12\x99\x01\n\x10GetSessionReview\x12#.ondewo.nlu.GetSessionReviewRequest\x1a\x19.ondewo.nlu.SessionReview\"E\x82\xd3\xe4\x93\x02?\x12=/v2/{session_review_id=projects/*/agent/sessions/*/reviews/*}\x12\xb3\x01\n\x16GetLatestSessionReview\x12).ondewo.nlu.GetLatestSessionReviewRequest\x1a\x19.ondewo.nlu.SessionReview\"S\x82\xd3\xe4\x93\x02M\x12K/v2/{session_id=projects/*/agent/sessions/*}/reviews:getLatestSessionReview\x12\xa5\x01\n\x13\x43reateSessionReview\x12&.ondewo.nlu.CreateSessionReviewRequest\x1a\x19.ondewo.nlu.SessionReview\"K\x82\xd3\xe4\x93\x02\x45\"@/v2/{session_id=projects/*/agent/sessions/*}:createSessionReview:\x01*B\x9b\x01\n\x1e\x63om.google.cloud.dialogflow.v2B\x0cSessionProtoP\x01ZDgoogle.golang.org/genproto/googleapis/cloud/dialogflow/v2;dialogflow\xf8\x01\x01\xa2\x02\x02\x44\x46\xaa\x02\x1aGoogle.Cloud.Dialogflow.V2b\x06proto3')

_AUDIOENCODING = DESCRIPTOR.enum_types_by_name['AudioEncoding']
AudioEncoding = enum_type_wrapper.EnumTypeWrapper(_AUDIOENCODING)
AUDIO_ENCODING_UNSPECIFIED = 0
AUDIO_ENCODING_LINEAR_16 = 1
AUDIO_ENCODING_FLAC = 2
AUDIO_ENCODING_MULAW = 3
AUDIO_ENCODING_AMR = 4
AUDIO_ENCODING_AMR_WB = 5
AUDIO_ENCODING_OGG_OPUS = 6
AUDIO_ENCODING_SPEEX_WITH_HEADER_BYTE = 7


_DETECTINTENTREQUEST = DESCRIPTOR.message_types_by_name['DetectIntentRequest']
_DETECTINTENTRESPONSE = DESCRIPTOR.message_types_by_name['DetectIntentResponse']
_QUERYPARAMETERS = DESCRIPTOR.message_types_by_name['QueryParameters']
_QUERYINPUT = DESCRIPTOR.message_types_by_name['QueryInput']
_QUERYRESULT = DESCRIPTOR.message_types_by_name['QueryResult']
_STREAMINGDETECTINTENTREQUEST = DESCRIPTOR.message_types_by_name['StreamingDetectIntentRequest']
_STREAMINGDETECTINTENTRESPONSE = DESCRIPTOR.message_types_by_name['StreamingDetectIntentResponse']
_STREAMINGRECOGNITIONRESULT = DESCRIPTOR.message_types_by_name['StreamingRecognitionResult']
_INPUTAUDIOCONFIG = DESCRIPTOR.message_types_by_name['InputAudioConfig']
_TEXTINPUT = DESCRIPTOR.message_types_by_name['TextInput']
_EVENTINPUT = DESCRIPTOR.message_types_by_name['EventInput']
_SESSION = DESCRIPTOR.message_types_by_name['Session']
_SESSIONSTEP = DESCRIPTOR.message_types_by_name['SessionStep']
_TRACKSESSIONSTEPREQUEST = DESCRIPTOR.message_types_by_name['TrackSessionStepRequest']
_LISTSESSIONSREQUEST = DESCRIPTOR.message_types_by_name['ListSessionsRequest']
_SESSIONFILTER = DESCRIPTOR.message_types_by_name['SessionFilter']
_SESSIONINFO = DESCRIPTOR.message_types_by_name['SessionInfo']
_SESSIONINFO_CONTEXTSTEPS = _SESSIONINFO.nested_types_by_name['ContextSteps']
_LISTSESSIONSRESPONSE = DESCRIPTOR.message_types_by_name['ListSessionsResponse']
_GETSESSIONREQUEST = DESCRIPTOR.message_types_by_name['GetSessionRequest']
_CREATESESSIONREQUEST = DESCRIPTOR.message_types_by_name['CreateSessionRequest']
_DELETESESSIONREQUEST = DESCRIPTOR.message_types_by_name['DeleteSessionRequest']
_CREATESESSIONREVIEWREQUEST = DESCRIPTOR.message_types_by_name['CreateSessionReviewRequest']
_SESSIONREVIEW = DESCRIPTOR.message_types_by_name['SessionReview']
_SESSIONREVIEWSTEP = DESCRIPTOR.message_types_by_name['SessionReviewStep']
_DETECTEDINTENT = DESCRIPTOR.message_types_by_name['DetectedIntent']
_LISTSESSIONLABELSREQUEST = DESCRIPTOR.message_types_by_name['ListSessionLabelsRequest']
_LISTSESSIONLABELSOFALLSESSIONSREQUEST = DESCRIPTOR.message_types_by_name['ListSessionLabelsOfAllSessionsRequest']
_LISTSESSIONLABELSRESPONSE = DESCRIPTOR.message_types_by_name['ListSessionLabelsResponse']
_ADDSESSIONLABELSREQUEST = DESCRIPTOR.message_types_by_name['AddSessionLabelsRequest']
_DELETESESSIONLABELSREQUEST = DESCRIPTOR.message_types_by_name['DeleteSessionLabelsRequest']
_LISTSESSIONREVIEWSREQUEST = DESCRIPTOR.message_types_by_name['ListSessionReviewsRequest']
_LISTSESSIONREVIEWSRESPONSE = DESCRIPTOR.message_types_by_name['ListSessionReviewsResponse']
_GETSESSIONREVIEWREQUEST = DESCRIPTOR.message_types_by_name['GetSessionReviewRequest']
_GETLATESTSESSIONREVIEWREQUEST = DESCRIPTOR.message_types_by_name['GetLatestSessionReviewRequest']
_STREAMINGRECOGNITIONRESULT_MESSAGETYPE = _STREAMINGRECOGNITIONRESULT.enum_types_by_name['MessageType']
_SESSION_VIEW = _SESSION.enum_types_by_name['View']
_SESSIONREVIEW_VIEW = _SESSIONREVIEW.enum_types_by_name['View']
DetectIntentRequest = _reflection.GeneratedProtocolMessageType('DetectIntentRequest', (_message.Message,), {
  'DESCRIPTOR' : _DETECTINTENTREQUEST,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.DetectIntentRequest)
  })
_sym_db.RegisterMessage(DetectIntentRequest)

DetectIntentResponse = _reflection.GeneratedProtocolMessageType('DetectIntentResponse', (_message.Message,), {
  'DESCRIPTOR' : _DETECTINTENTRESPONSE,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.DetectIntentResponse)
  })
_sym_db.RegisterMessage(DetectIntentResponse)

QueryParameters = _reflection.GeneratedProtocolMessageType('QueryParameters', (_message.Message,), {
  'DESCRIPTOR' : _QUERYPARAMETERS,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.QueryParameters)
  })
_sym_db.RegisterMessage(QueryParameters)

QueryInput = _reflection.GeneratedProtocolMessageType('QueryInput', (_message.Message,), {
  'DESCRIPTOR' : _QUERYINPUT,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.QueryInput)
  })
_sym_db.RegisterMessage(QueryInput)

QueryResult = _reflection.GeneratedProtocolMessageType('QueryResult', (_message.Message,), {
  'DESCRIPTOR' : _QUERYRESULT,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.QueryResult)
  })
_sym_db.RegisterMessage(QueryResult)

StreamingDetectIntentRequest = _reflection.GeneratedProtocolMessageType('StreamingDetectIntentRequest', (_message.Message,), {
  'DESCRIPTOR' : _STREAMINGDETECTINTENTREQUEST,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.StreamingDetectIntentRequest)
  })
_sym_db.RegisterMessage(StreamingDetectIntentRequest)

StreamingDetectIntentResponse = _reflection.GeneratedProtocolMessageType('StreamingDetectIntentResponse', (_message.Message,), {
  'DESCRIPTOR' : _STREAMINGDETECTINTENTRESPONSE,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.StreamingDetectIntentResponse)
  })
_sym_db.RegisterMessage(StreamingDetectIntentResponse)

StreamingRecognitionResult = _reflection.GeneratedProtocolMessageType('StreamingRecognitionResult', (_message.Message,), {
  'DESCRIPTOR' : _STREAMINGRECOGNITIONRESULT,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.StreamingRecognitionResult)
  })
_sym_db.RegisterMessage(StreamingRecognitionResult)

InputAudioConfig = _reflection.GeneratedProtocolMessageType('InputAudioConfig', (_message.Message,), {
  'DESCRIPTOR' : _INPUTAUDIOCONFIG,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.InputAudioConfig)
  })
_sym_db.RegisterMessage(InputAudioConfig)

TextInput = _reflection.GeneratedProtocolMessageType('TextInput', (_message.Message,), {
  'DESCRIPTOR' : _TEXTINPUT,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.TextInput)
  })
_sym_db.RegisterMessage(TextInput)

EventInput = _reflection.GeneratedProtocolMessageType('EventInput', (_message.Message,), {
  'DESCRIPTOR' : _EVENTINPUT,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.EventInput)
  })
_sym_db.RegisterMessage(EventInput)

Session = _reflection.GeneratedProtocolMessageType('Session', (_message.Message,), {
  'DESCRIPTOR' : _SESSION,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.Session)
  })
_sym_db.RegisterMessage(Session)

SessionStep = _reflection.GeneratedProtocolMessageType('SessionStep', (_message.Message,), {
  'DESCRIPTOR' : _SESSIONSTEP,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.SessionStep)
  })
_sym_db.RegisterMessage(SessionStep)

TrackSessionStepRequest = _reflection.GeneratedProtocolMessageType('TrackSessionStepRequest', (_message.Message,), {
  'DESCRIPTOR' : _TRACKSESSIONSTEPREQUEST,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.TrackSessionStepRequest)
  })
_sym_db.RegisterMessage(TrackSessionStepRequest)

ListSessionsRequest = _reflection.GeneratedProtocolMessageType('ListSessionsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTSESSIONSREQUEST,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.ListSessionsRequest)
  })
_sym_db.RegisterMessage(ListSessionsRequest)

SessionFilter = _reflection.GeneratedProtocolMessageType('SessionFilter', (_message.Message,), {
  'DESCRIPTOR' : _SESSIONFILTER,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.SessionFilter)
  })
_sym_db.RegisterMessage(SessionFilter)

SessionInfo = _reflection.GeneratedProtocolMessageType('SessionInfo', (_message.Message,), {

  'ContextSteps' : _reflection.GeneratedProtocolMessageType('ContextSteps', (_message.Message,), {
    'DESCRIPTOR' : _SESSIONINFO_CONTEXTSTEPS,
    '__module__' : 'ondewo.nlu.session_pb2'
    # @@protoc_insertion_point(class_scope:ondewo.nlu.SessionInfo.ContextSteps)
    })
  ,
  'DESCRIPTOR' : _SESSIONINFO,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.SessionInfo)
  })
_sym_db.RegisterMessage(SessionInfo)
_sym_db.RegisterMessage(SessionInfo.ContextSteps)

ListSessionsResponse = _reflection.GeneratedProtocolMessageType('ListSessionsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTSESSIONSRESPONSE,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.ListSessionsResponse)
  })
_sym_db.RegisterMessage(ListSessionsResponse)

GetSessionRequest = _reflection.GeneratedProtocolMessageType('GetSessionRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETSESSIONREQUEST,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.GetSessionRequest)
  })
_sym_db.RegisterMessage(GetSessionRequest)

CreateSessionRequest = _reflection.GeneratedProtocolMessageType('CreateSessionRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATESESSIONREQUEST,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.CreateSessionRequest)
  })
_sym_db.RegisterMessage(CreateSessionRequest)

DeleteSessionRequest = _reflection.GeneratedProtocolMessageType('DeleteSessionRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETESESSIONREQUEST,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.DeleteSessionRequest)
  })
_sym_db.RegisterMessage(DeleteSessionRequest)

CreateSessionReviewRequest = _reflection.GeneratedProtocolMessageType('CreateSessionReviewRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATESESSIONREVIEWREQUEST,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.CreateSessionReviewRequest)
  })
_sym_db.RegisterMessage(CreateSessionReviewRequest)

SessionReview = _reflection.GeneratedProtocolMessageType('SessionReview', (_message.Message,), {
  'DESCRIPTOR' : _SESSIONREVIEW,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.SessionReview)
  })
_sym_db.RegisterMessage(SessionReview)

SessionReviewStep = _reflection.GeneratedProtocolMessageType('SessionReviewStep', (_message.Message,), {
  'DESCRIPTOR' : _SESSIONREVIEWSTEP,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.SessionReviewStep)
  })
_sym_db.RegisterMessage(SessionReviewStep)

DetectedIntent = _reflection.GeneratedProtocolMessageType('DetectedIntent', (_message.Message,), {
  'DESCRIPTOR' : _DETECTEDINTENT,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.DetectedIntent)
  })
_sym_db.RegisterMessage(DetectedIntent)

ListSessionLabelsRequest = _reflection.GeneratedProtocolMessageType('ListSessionLabelsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTSESSIONLABELSREQUEST,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.ListSessionLabelsRequest)
  })
_sym_db.RegisterMessage(ListSessionLabelsRequest)

ListSessionLabelsOfAllSessionsRequest = _reflection.GeneratedProtocolMessageType('ListSessionLabelsOfAllSessionsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTSESSIONLABELSOFALLSESSIONSREQUEST,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.ListSessionLabelsOfAllSessionsRequest)
  })
_sym_db.RegisterMessage(ListSessionLabelsOfAllSessionsRequest)

ListSessionLabelsResponse = _reflection.GeneratedProtocolMessageType('ListSessionLabelsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTSESSIONLABELSRESPONSE,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.ListSessionLabelsResponse)
  })
_sym_db.RegisterMessage(ListSessionLabelsResponse)

AddSessionLabelsRequest = _reflection.GeneratedProtocolMessageType('AddSessionLabelsRequest', (_message.Message,), {
  'DESCRIPTOR' : _ADDSESSIONLABELSREQUEST,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.AddSessionLabelsRequest)
  })
_sym_db.RegisterMessage(AddSessionLabelsRequest)

DeleteSessionLabelsRequest = _reflection.GeneratedProtocolMessageType('DeleteSessionLabelsRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETESESSIONLABELSREQUEST,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.DeleteSessionLabelsRequest)
  })
_sym_db.RegisterMessage(DeleteSessionLabelsRequest)

ListSessionReviewsRequest = _reflection.GeneratedProtocolMessageType('ListSessionReviewsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTSESSIONREVIEWSREQUEST,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.ListSessionReviewsRequest)
  })
_sym_db.RegisterMessage(ListSessionReviewsRequest)

ListSessionReviewsResponse = _reflection.GeneratedProtocolMessageType('ListSessionReviewsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTSESSIONREVIEWSRESPONSE,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.ListSessionReviewsResponse)
  })
_sym_db.RegisterMessage(ListSessionReviewsResponse)

GetSessionReviewRequest = _reflection.GeneratedProtocolMessageType('GetSessionReviewRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETSESSIONREVIEWREQUEST,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.GetSessionReviewRequest)
  })
_sym_db.RegisterMessage(GetSessionReviewRequest)

GetLatestSessionReviewRequest = _reflection.GeneratedProtocolMessageType('GetLatestSessionReviewRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETLATESTSESSIONREVIEWREQUEST,
  '__module__' : 'ondewo.nlu.session_pb2'
  # @@protoc_insertion_point(class_scope:ondewo.nlu.GetLatestSessionReviewRequest)
  })
_sym_db.RegisterMessage(GetLatestSessionReviewRequest)

_SESSIONS = DESCRIPTOR.services_by_name['Sessions']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\036com.google.cloud.dialogflow.v2B\014SessionProtoP\001ZDgoogle.golang.org/genproto/googleapis/cloud/dialogflow/v2;dialogflow\370\001\001\242\002\002DF\252\002\032Google.Cloud.Dialogflow.V2'
  _SESSIONS.methods_by_name['DetectIntent']._options = None
  _SESSIONS.methods_by_name['DetectIntent']._serialized_options = b'\202\323\344\223\002;\"6/v2/{session=projects/*/agent/sessions/*}:detectIntent:\001*'
  _SESSIONS.methods_by_name['ListSessions']._options = None
  _SESSIONS.methods_by_name['ListSessions']._serialized_options = b'\202\323\344\223\002(\022&/v2/{parent=projects/*/agent}/sessions'
  _SESSIONS.methods_by_name['GetSession']._options = None
  _SESSIONS.methods_by_name['GetSession']._serialized_options = b'\202\323\344\223\002.\022,/v2/{session_id=projects/*/agent/sessions/*}'
  _SESSIONS.methods_by_name['CreateSession']._options = None
  _SESSIONS.methods_by_name['CreateSession']._serialized_options = b'\202\323\344\223\002+\"&/v2/{parent=projects/*/agent}/sessions:\001*'
  _SESSIONS.methods_by_name['TrackSessionStep']._options = None
  _SESSIONS.methods_by_name['TrackSessionStep']._serialized_options = b'\202\323\344\223\002B\"=/v2/{session_id=projects/*/agent/sessions/*}:trackSessionStep:\001*'
  _SESSIONS.methods_by_name['DeleteSession']._options = None
  _SESSIONS.methods_by_name['DeleteSession']._serialized_options = b'\202\323\344\223\002.*,/v2/{session_id=projects/*/agent/sessions/*}'
  _SESSIONS.methods_by_name['ListSessionLabels']._options = None
  _SESSIONS.methods_by_name['ListSessionLabels']._serialized_options = b'\202\323\344\223\0025\0223/v2/{session_id=projects/*/agent/sessions/*}/labels'
  _SESSIONS.methods_by_name['ListSessionLabelsOfAllSessions']._options = None
  _SESSIONS.methods_by_name['ListSessionLabelsOfAllSessions']._serialized_options = b'\202\323\344\223\002/\022-/v2/{parent=projects/*/agent}/sessions/labels'
  _SESSIONS.methods_by_name['AddSessionLabels']._options = None
  _SESSIONS.methods_by_name['AddSessionLabels']._serialized_options = b'\202\323\344\223\002<\"7/v2/{session_id=projects/*/agent/sessions/*}/labels:add:\001*'
  _SESSIONS.methods_by_name['DeleteSessionLabels']._options = None
  _SESSIONS.methods_by_name['DeleteSessionLabels']._serialized_options = b'\202\323\344\223\002?\":/v2/{session_id=projects/*/agent/sessions/*}/labels:delete:\001*'
  _SESSIONS.methods_by_name['ListSessionReviews']._options = None
  _SESSIONS.methods_by_name['ListSessionReviews']._serialized_options = b'\202\323\344\223\0026\0224/v2/{session_id=projects/*/agent/sessions/*}/reviews'
  _SESSIONS.methods_by_name['GetSessionReview']._options = None
  _SESSIONS.methods_by_name['GetSessionReview']._serialized_options = b'\202\323\344\223\002?\022=/v2/{session_review_id=projects/*/agent/sessions/*/reviews/*}'
  _SESSIONS.methods_by_name['GetLatestSessionReview']._options = None
  _SESSIONS.methods_by_name['GetLatestSessionReview']._serialized_options = b'\202\323\344\223\002M\022K/v2/{session_id=projects/*/agent/sessions/*}/reviews:getLatestSessionReview'
  _SESSIONS.methods_by_name['CreateSessionReview']._options = None
  _SESSIONS.methods_by_name['CreateSessionReview']._serialized_options = b'\202\323\344\223\002E\"@/v2/{session_id=projects/*/agent/sessions/*}:createSessionReview:\001*'
  _AUDIOENCODING._serialized_start=7455
  _AUDIOENCODING._serialized_end=7706
  _DETECTINTENTREQUEST._serialized_start=296
  _DETECTINTENTREQUEST._serialized_end=451
  _DETECTINTENTRESPONSE._serialized_start=454
  _DETECTINTENTRESPONSE._serialized_end=588
  _QUERYPARAMETERS._serialized_start=591
  _QUERYPARAMETERS._serialized_end=791
  _QUERYINPUT._serialized_start=794
  _QUERYINPUT._serialized_end=949
  _QUERYRESULT._serialized_start=952
  _QUERYRESULT._serialized_end=1472
  _STREAMINGDETECTINTENTREQUEST._serialized_start=1475
  _STREAMINGDETECTINTENTREQUEST._serialized_end=1665
  _STREAMINGDETECTINTENTRESPONSE._serialized_start=1668
  _STREAMINGDETECTINTENTRESPONSE._serialized_end=1879
  _STREAMINGRECOGNITIONRESULT._serialized_start=1882
  _STREAMINGRECOGNITIONRESULT._serialized_end=2132
  _STREAMINGRECOGNITIONRESULT_MESSAGETYPE._serialized_start=2044
  _STREAMINGRECOGNITIONRESULT_MESSAGETYPE._serialized_end=2132
  _INPUTAUDIOCONFIG._serialized_start=2135
  _INPUTAUDIOCONFIG._serialized_end=2276
  _TEXTINPUT._serialized_start=2278
  _TEXTINPUT._serialized_end=2326
  _EVENTINPUT._serialized_start=2328
  _EVENTINPUT._serialized_end=2422
  _SESSION._serialized_start=2425
  _SESSION._serialized_end=2611
  _SESSION_VIEW._serialized_start=2551
  _SESSION_VIEW._serialized_end=2611
  _SESSIONSTEP._serialized_start=2614
  _SESSIONSTEP._serialized_end=2796
  _TRACKSESSIONSTEPREQUEST._serialized_start=2799
  _TRACKSESSIONSTEPREQUEST._serialized_end=2939
  _LISTSESSIONSREQUEST._serialized_start=2942
  _LISTSESSIONSREQUEST._serialized_end=3146
  _SESSIONFILTER._serialized_start=3149
  _SESSIONFILTER._serialized_end=4640
  _SESSIONINFO._serialized_start=4643
  _SESSIONINFO._serialized_end=5578
  _SESSIONINFO_CONTEXTSTEPS._serialized_start=5525
  _SESSIONINFO_CONTEXTSTEPS._serialized_end=5578
  _LISTSESSIONSRESPONSE._serialized_start=5580
  _LISTSESSIONSRESPONSE._serialized_end=5666
  _GETSESSIONREQUEST._serialized_start=5669
  _GETSESSIONREQUEST._serialized_end=5804
  _CREATESESSIONREQUEST._serialized_start=5806
  _CREATESESSIONREQUEST._serialized_end=5882
  _DELETESESSIONREQUEST._serialized_start=5884
  _DELETESESSIONREQUEST._serialized_end=5926
  _CREATESESSIONREVIEWREQUEST._serialized_start=5929
  _CREATESESSIONREVIEWREQUEST._serialized_end=6115
  _SESSIONREVIEW._serialized_start=6118
  _SESSIONREVIEW._serialized_end=6283
  _SESSIONREVIEW_VIEW._serialized_start=2551
  _SESSIONREVIEW_VIEW._serialized_end=2611
  _SESSIONREVIEWSTEP._serialized_start=6286
  _SESSIONREVIEWSTEP._serialized_end=6527
  _DETECTEDINTENT._serialized_start=6530
  _DETECTEDINTENT._serialized_end=6706
  _LISTSESSIONLABELSREQUEST._serialized_start=6708
  _LISTSESSIONLABELSREQUEST._serialized_end=6754
  _LISTSESSIONLABELSOFALLSESSIONSREQUEST._serialized_start=6756
  _LISTSESSIONLABELSOFALLSESSIONSREQUEST._serialized_end=6811
  _LISTSESSIONLABELSRESPONSE._serialized_start=6813
  _LISTSESSIONLABELSRESPONSE._serialized_end=6856
  _ADDSESSIONLABELSREQUEST._serialized_start=6858
  _ADDSESSIONLABELSREQUEST._serialized_end=6919
  _DELETESESSIONLABELSREQUEST._serialized_start=6921
  _DELETESESSIONLABELSREQUEST._serialized_end=6985
  _LISTSESSIONREVIEWSREQUEST._serialized_start=6988
  _LISTSESSIONREVIEWSREQUEST._serialized_end=7116
  _LISTSESSIONREVIEWSRESPONSE._serialized_start=7118
  _LISTSESSIONREVIEWSRESPONSE._serialized_end=7223
  _GETSESSIONREVIEWREQUEST._serialized_start=7225
  _GETSESSIONREVIEWREQUEST._serialized_end=7338
  _GETLATESTSESSIONREVIEWREQUEST._serialized_start=7340
  _GETLATESTSESSIONREVIEWREQUEST._serialized_end=7452
  _SESSIONS._serialized_start=7709
  _SESSIONS._serialized_end=9954
# @@protoc_insertion_point(module_scope)
