# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ondewo/nlu/ccai_project.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import field_mask_pb2 as google_dot_protobuf_dot_field__mask__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from ondewo.nlu import common_pb2 as ondewo_dot_nlu_dot_common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dondewo/nlu/ccai_project.proto\x12\nondewo.nlu\x1a google/protobuf/field_mask.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x17ondewo/nlu/common.proto\"\xc6\x02\n\x0b\x43\x63\x61iProject\x12\x0c\n\x04name\x18\x01 \x01(\t\x12I\n\x12\x63\x63\x61i_service_lists\x18\x02 \x03(\x0b\x32-.ondewo.nlu.CcaiProject.CcaiServiceListsEntry\x12.\n\ncreated_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0bmodified_at\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x12\n\ncreated_by\x18\x05 \x01(\t\x12\x13\n\x0bmodified_by\x18\x06 \x01(\t\x1aT\n\x15\x43\x63\x61iServiceListsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12*\n\x05value\x18\x02 \x01(\x0b\x32\x1b.ondewo.nlu.CcaiServiceList:\x02\x38\x01\"A\n\x0f\x43\x63\x61iServiceList\x12.\n\rccai_services\x18\x01 \x03(\x0b\x32\x17.ondewo.nlu.CcaiService\"\xbc\x03\n\x0b\x43\x63\x61iService\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x14\n\x0c\x64isplay_name\x18\x02 \x01(\t\x12\x11\n\tgrpc_host\x18\x03 \x01(\t\x12\x11\n\tgrpc_port\x18\x04 \x01(\x05\x12\x14\n\x0cwebgrpc_host\x18\x05 \x01(\t\x12\x14\n\x0cwebgrpc_port\x18\x06 \x01(\x05\x12\x11\n\tgrpc_cert\x18\x07 \x01(\t\x12\x0c\n\x04host\x18\x08 \x01(\t\x12\x0c\n\x04port\x18\t \x01(\x05\x12\r\n\x05port2\x18\n \x01(\x05\x12\x14\n\x0c\x61\x63\x63ount_name\x18\x0b \x01(\t\x12\x10\n\x08password\x18\x0c \x01(\t\x12\x0f\n\x07\x61pi_key\x18\r \x01(\t\x12\x36\n\x11\x63\x63\x61i_service_type\x18\x0e \x01(\x0e\x32\x1b.ondewo.nlu.CcaiServiceType\x12.\n\ncreated_at\x18\x0f \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0bmodified_at\x18\x10 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x12\n\ncreated_by\x18\x11 \x01(\t\x12\x13\n\x0bmodified_by\x18\x12 \x01(\t\"I\n\x18\x43reateCcaiProjectRequest\x12-\n\x0c\x63\x63\x61i_project\x18\x01 \x01(\x0b\x32\x17.ondewo.nlu.CcaiProject\"a\n\x19\x43reateCcaiProjectResponse\x12-\n\x0c\x63\x63\x61i_project\x18\x01 \x01(\x0b\x32\x17.ondewo.nlu.CcaiProject\x12\x15\n\rerror_message\x18\x02 \x01(\t\"\x99\x01\n\x15GetCcaiProjectRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x36\n\x11\x63\x63\x61i_project_view\x18\x02 \x01(\x0e\x32\x1b.ondewo.nlu.CcaiProjectView\x12:\n\x13\x63\x63\x61i_project_filter\x18\x03 \x01(\x0b\x32\x1d.ondewo.nlu.CcaiProjectFilter\"\xee\x01\n\x17ListCcaiProjectsRequest\x12\x36\n\x11\x63\x63\x61i_project_view\x18\x01 \x01(\x0e\x32\x1b.ondewo.nlu.CcaiProjectView\x12\x17\n\npage_token\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x41\n\x14\x63\x63\x61i_project_sorting\x18\x03 \x01(\x0b\x32\x1e.ondewo.nlu.CcaiProjectSortingH\x01\x88\x01\x01\x12\x17\n\x0fnlu_agent_names\x18\x04 \x03(\tB\r\n\x0b_page_tokenB\x17\n\x15_ccai_project_sorting\"c\n\x18ListCcaiProjectsResponse\x12.\n\rccai_projects\x18\x01 \x03(\x0b\x32\x17.ondewo.nlu.CcaiProject\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\x8e\x03\n\x12\x43\x63\x61iProjectSorting\x12R\n\rsorting_field\x18\x01 \x01(\x0e\x32\x36.ondewo.nlu.CcaiProjectSorting.CcaiProjectSortingFieldH\x00\x88\x01\x01\x12\x32\n\x0csorting_mode\x18\x02 \x01(\x0e\x32\x17.ondewo.nlu.SortingModeH\x01\x88\x01\x01\"\xcc\x01\n\x17\x43\x63\x61iProjectSortingField\x12\x1b\n\x17NO_CCAI_PROJECT_SORTING\x10\x00\x12\x1d\n\x19SORT_CCAI_PROJECT_BY_NAME\x10\x01\x12%\n!SORT_CCAI_PROJECT_BY_DISPLAY_NAME\x10\x02\x12&\n\"SORT_CCAI_PROJECT_BY_CREATION_DATE\x10\x03\x12&\n\"SORT_CCAI_PROJECT_BY_LAST_MODIFIED\x10\x04\x42\x10\n\x0e_sorting_fieldB\x0f\n\r_sorting_mode\"c\n\x11\x43\x63\x61iProjectFilter\x12\x16\n\x0elanguage_codes\x18\x01 \x03(\t\x12\x36\n\x11\x63\x63\x61i_service_type\x18\x0e \x03(\x0e\x32\x1b.ondewo.nlu.CcaiServiceType\"z\n\x18UpdateCcaiProjectRequest\x12-\n\x0c\x63\x63\x61i_project\x18\x01 \x01(\x0b\x32\x17.ondewo.nlu.CcaiProject\x12/\n\x0bupdate_mask\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\"@\n\x19UpdateCcaiProjectResponse\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x15\n\rerror_message\x18\x02 \x01(\t\"(\n\x18\x44\x65leteCcaiProjectRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"@\n\x19\x44\x65leteCcaiProjectResponse\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x15\n\rerror_message\x18\x02 \x01(\t*\xde\x03\n\x0f\x43\x63\x61iServiceType\x12!\n\x1d\x43\x43\x41I_SERVICE_TYPE_UNSPECIFIED\x10\x00\x12 \n\x1c\x43\x43\x41I_SERVICE_TYPE_ONDEWO_AIM\x10\x01\x12 \n\x1c\x43\x43\x41I_SERVICE_TYPE_ONDEWO_BPI\x10\x02\x12 \n\x1c\x43\x43\x41I_SERVICE_TYPE_ONDEWO_CSI\x10\x03\x12 \n\x1c\x43\x43\x41I_SERVICE_TYPE_ONDEWO_NLU\x10\x04\x12 \n\x1c\x43\x43\x41I_SERVICE_TYPE_ONDEWO_S2T\x10\x05\x12 \n\x1c\x43\x43\x41I_SERVICE_TYPE_ONDEWO_SIP\x10\x06\x12 \n\x1c\x43\x43\x41I_SERVICE_TYPE_ONDEWO_T2S\x10\x07\x12!\n\x1d\x43\x43\x41I_SERVICE_TYPE_ONDEWO_VTSI\x10\x08\x12#\n\x1f\x43\x43\x41I_SERVICE_TYPE_VTSI_RABBITMQ\x10\t\x12#\n\x1f\x43\x43\x41I_SERVICE_TYPE_ONDEWO_NLU_QA\x10\n\x12(\n$CCAI_SERVICE_TYPE_ONDEWO_NLU_WEBHOOK\x10\x0b\x12#\n\x1f\x43\x43\x41I_SERVICE_TYPE_ONDEWO_SURVEY\x10\x0c*\x8e\x01\n\x0f\x43\x63\x61iProjectView\x12!\n\x1d\x43\x43\x41I_PROJECT_VIEW_UNSPECIFIED\x10\x00\x12\x1a\n\x16\x43\x43\x41I_PROJECT_VIEW_FULL\x10\x01\x12\x1d\n\x19\x43\x43\x41I_PROJECT_VIEW_SHALLOW\x10\x02\x12\x1d\n\x19\x43\x43\x41I_PROJECT_VIEW_MINIMUM\x10\x03\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ondewo.nlu.ccai_project_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _CCAIPROJECT_CCAISERVICELISTSENTRY._options = None
  _CCAIPROJECT_CCAISERVICELISTSENTRY._serialized_options = b'8\001'
  _globals['_CCAISERVICETYPE']._serialized_start=2453
  _globals['_CCAISERVICETYPE']._serialized_end=2931
  _globals['_CCAIPROJECTVIEW']._serialized_start=2934
  _globals['_CCAIPROJECTVIEW']._serialized_end=3076
  _globals['_CCAIPROJECT']._serialized_start=138
  _globals['_CCAIPROJECT']._serialized_end=464
  _globals['_CCAIPROJECT_CCAISERVICELISTSENTRY']._serialized_start=380
  _globals['_CCAIPROJECT_CCAISERVICELISTSENTRY']._serialized_end=464
  _globals['_CCAISERVICELIST']._serialized_start=466
  _globals['_CCAISERVICELIST']._serialized_end=531
  _globals['_CCAISERVICE']._serialized_start=534
  _globals['_CCAISERVICE']._serialized_end=978
  _globals['_CREATECCAIPROJECTREQUEST']._serialized_start=980
  _globals['_CREATECCAIPROJECTREQUEST']._serialized_end=1053
  _globals['_CREATECCAIPROJECTRESPONSE']._serialized_start=1055
  _globals['_CREATECCAIPROJECTRESPONSE']._serialized_end=1152
  _globals['_GETCCAIPROJECTREQUEST']._serialized_start=1155
  _globals['_GETCCAIPROJECTREQUEST']._serialized_end=1308
  _globals['_LISTCCAIPROJECTSREQUEST']._serialized_start=1311
  _globals['_LISTCCAIPROJECTSREQUEST']._serialized_end=1549
  _globals['_LISTCCAIPROJECTSRESPONSE']._serialized_start=1551
  _globals['_LISTCCAIPROJECTSRESPONSE']._serialized_end=1650
  _globals['_CCAIPROJECTSORTING']._serialized_start=1653
  _globals['_CCAIPROJECTSORTING']._serialized_end=2051
  _globals['_CCAIPROJECTSORTING_CCAIPROJECTSORTINGFIELD']._serialized_start=1812
  _globals['_CCAIPROJECTSORTING_CCAIPROJECTSORTINGFIELD']._serialized_end=2016
  _globals['_CCAIPROJECTFILTER']._serialized_start=2053
  _globals['_CCAIPROJECTFILTER']._serialized_end=2152
  _globals['_UPDATECCAIPROJECTREQUEST']._serialized_start=2154
  _globals['_UPDATECCAIPROJECTREQUEST']._serialized_end=2276
  _globals['_UPDATECCAIPROJECTRESPONSE']._serialized_start=2278
  _globals['_UPDATECCAIPROJECTRESPONSE']._serialized_end=2342
  _globals['_DELETECCAIPROJECTREQUEST']._serialized_start=2344
  _globals['_DELETECCAIPROJECTREQUEST']._serialized_end=2384
  _globals['_DELETECCAIPROJECTRESPONSE']._serialized_start=2386
  _globals['_DELETECCAIPROJECTRESPONSE']._serialized_end=2450
# @@protoc_insertion_point(module_scope)
