# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ondewo/nlu/operation_metadata.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#ondewo/nlu/operation_metadata.proto\x12\nondewo.nlu\x1a\x1fgoogle/protobuf/timestamp.proto\"\xa9\x08\n\x11OperationMetadata\x12\x34\n\x06status\x18\x01 \x01(\x0e\x32$.ondewo.nlu.OperationMetadata.Status\x12\x1d\n\x15parent_operation_name\x18\x02 \x01(\t\x12\x1b\n\x13sub_operation_names\x18\x03 \x03(\t\x12/\n\x0b\x63reate_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nstart_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\x08\x65nd_time\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12!\n\x19is_cancellation_requested\x18\x07 \x01(\x08\x12\x16\n\x0e\x63\x61ncel_command\x18\x08 \x01(\t\x12\x17\n\x0fuser_id_created\x18\t \x01(\t\x12\x19\n\x11user_id_cancelled\x18\n \x01(\t\x12\x16\n\x0eproject_parent\x18\x0b \x01(\t\x12\x43\n\x0eoperation_type\x18\x0c \x01(\x0e\x32+.ondewo.nlu.OperationMetadata.OperationType\x12\x11\n\thost_name\x18\r \x01(\t\x12\x12\n\nnum_reruns\x18\x0e \x01(\x05\x12\x16\n\x0emax_num_reruns\x18\x0f \x01(\x05\x12\x13\n\x0b\x64\x65scription\x18\x10 \x01(\t\x12\x0b\n\x03log\x18\x11 \x03(\t\x12\x11\n\tlog_limit\x18\x12 \x01(\x05\x12.\n\ncreated_at\x18\x13 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0bmodified_at\x18\x14 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x12\n\ncreated_by\x18\x15 \x01(\t\x12\x13\n\x0bmodified_by\x18\x16 \x01(\t\"g\n\x06Status\x12\x16\n\x12STATUS_UNSPECIFIED\x10\x00\x12\x0f\n\x0bNOT_STARTED\x10\x01\x12\x0f\n\x0bIN_PROGRESS\x10\x02\x12\x08\n\x04\x44ONE\x10\x03\x12\r\n\tCANCELLED\x10\x04\x12\n\n\x06\x46\x41ILED\x10\x05\"\xdf\x01\n\rOperationType\x12\x1e\n\x1aOPERATION_TYPE_UNSPECIFIED\x10\x00\x12\x10\n\x0c\x43REATE_AGENT\x10\x01\x12\x10\n\x0cIMPORT_AGENT\x10\x02\x12\x10\n\x0c\x45XPORT_AGENT\x10\x03\x12\x10\n\x0c\x44\x45LETE_AGENT\x10\x04\x12\x11\n\rRESTORE_AGENT\x10\x05\x12\x15\n\x11\x42UILD_AGENT_CACHE\x10\x06\x12\x0f\n\x0bTRAIN_AGENT\x10\x07\x12\x1a\n\x16\x45XPORT_BENCHMARK_AGENT\x10\x08\x12\x0f\n\x0bINDEX_AGENT\x10\tb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ondewo.nlu.operation_metadata_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_OPERATIONMETADATA']._serialized_start=85
  _globals['_OPERATIONMETADATA']._serialized_end=1150
  _globals['_OPERATIONMETADATA_STATUS']._serialized_start=821
  _globals['_OPERATIONMETADATA_STATUS']._serialized_end=924
  _globals['_OPERATIONMETADATA_OPERATIONTYPE']._serialized_start=927
  _globals['_OPERATIONMETADATA_OPERATIONTYPE']._serialized_end=1150
# @@protoc_insertion_point(module_scope)
