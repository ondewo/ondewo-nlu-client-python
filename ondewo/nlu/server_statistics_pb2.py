# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ondewo/nlu/server_statistics.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from ondewo.nlu import common_pb2 as ondewo_dot_nlu_dot_common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"ondewo/nlu/server_statistics.proto\x12\nondewo.nlu\x1a\x1cgoogle/api/annotations.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x17ondewo/nlu/common.proto\"-\n\x1aGetUserProjectCountRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t2\xd5\x02\n\x10ServerStatistics\x12\\\n\x0fGetProjectCount\x12\x16.google.protobuf.Empty\x1a\x18.ondewo.nlu.StatResponse\"\x17\x82\xd3\xe4\x93\x02\x11\x12\x0f/projects:count\x12\x8a\x01\n\x13GetUserProjectCount\x12&.ondewo.nlu.GetUserProjectCountRequest\x1a\x18.ondewo.nlu.StatResponse\"1\x82\xd3\xe4\x93\x02+\x12)/users/{user_identifier=*}/projects:count\x12V\n\x0cGetUserCount\x12\x16.google.protobuf.Empty\x1a\x18.ondewo.nlu.StatResponse\"\x14\x82\xd3\xe4\x93\x02\x0e\x12\x0c/users:countb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ondewo.nlu.server_statistics_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SERVERSTATISTICS'].methods_by_name['GetProjectCount']._loaded_options = None
  _globals['_SERVERSTATISTICS'].methods_by_name['GetProjectCount']._serialized_options = b'\202\323\344\223\002\021\022\017/projects:count'
  _globals['_SERVERSTATISTICS'].methods_by_name['GetUserProjectCount']._loaded_options = None
  _globals['_SERVERSTATISTICS'].methods_by_name['GetUserProjectCount']._serialized_options = b'\202\323\344\223\002+\022)/users/{user_identifier=*}/projects:count'
  _globals['_SERVERSTATISTICS'].methods_by_name['GetUserCount']._loaded_options = None
  _globals['_SERVERSTATISTICS'].methods_by_name['GetUserCount']._serialized_options = b'\202\323\344\223\002\016\022\014/users:count'
  _globals['_GETUSERPROJECTCOUNTREQUEST']._serialized_start=134
  _globals['_GETUSERPROJECTCOUNTREQUEST']._serialized_end=179
  _globals['_SERVERSTATISTICS']._serialized_start=182
  _globals['_SERVERSTATISTICS']._serialized_end=523
# @@protoc_insertion_point(module_scope)
