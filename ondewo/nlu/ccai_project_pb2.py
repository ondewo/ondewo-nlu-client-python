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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dondewo/nlu/ccai_project.proto\x12\nondewo.nlu\x1a google/protobuf/field_mask.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x17ondewo/nlu/common.proto\"\xc3\x03\n\x0b\x43\x63\x61iProject\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x14\n\x0c\x64isplay_name\x18\x02 \x01(\t\x12\x12\n\nowner_name\x18\x03 \x01(\t\x12G\n\x11\x63\x63\x61i_services_map\x18\x04 \x03(\x0b\x32,.ondewo.nlu.CcaiProject.CcaiServicesMapEntry\x12:\n\x13\x63\x63\x61i_project_status\x18\x05 \x01(\x0e\x32\x1d.ondewo.nlu.CcaiProjectStatus\x12.\n\ncreated_at\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0bmodified_at\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x12\n\ncreated_by\x18\x08 \x01(\t\x12\x13\n\x0bmodified_by\x18\t \x01(\t\x12\x18\n\x10nlu_project_name\x18\n \x01(\t\x1aS\n\x14\x43\x63\x61iServicesMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12*\n\x05value\x18\x02 \x01(\x0b\x32\x1b.ondewo.nlu.CcaiServiceList:\x02\x38\x01\"A\n\x0f\x43\x63\x61iServiceList\x12.\n\rccai_services\x18\x01 \x03(\x0b\x32\x17.ondewo.nlu.CcaiService\"\x95\x04\n\x0b\x43\x63\x61iService\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x14\n\x0c\x64isplay_name\x18\x02 \x01(\t\x12\x15\n\rlanguage_code\x18\x03 \x01(\t\x12\x11\n\tgrpc_host\x18\x04 \x01(\t\x12\x11\n\tgrpc_port\x18\x05 \x01(\x05\x12\x14\n\x0cwebgrpc_host\x18\x06 \x01(\t\x12\x14\n\x0cwebgrpc_port\x18\x07 \x01(\x05\x12\x11\n\tgrpc_cert\x18\x08 \x01(\t\x12\x0c\n\x04host\x18\t \x01(\t\x12\x0c\n\x04port\x18\n \x01(\x05\x12\r\n\x05port2\x18\x0b \x01(\x05\x12\x1d\n\x15http_basic_auth_token\x18\x0c \x01(\t\x12\x14\n\x0c\x61\x63\x63ount_name\x18\r \x01(\t\x12\x18\n\x10\x61\x63\x63ount_password\x18\x0e \x01(\t\x12\x0f\n\x07\x61pi_key\x18\x0f \x01(\t\x12\x36\n\x11\x63\x63\x61i_service_type\x18\x10 \x01(\x0e\x32\x1b.ondewo.nlu.CcaiServiceType\x12\x19\n\x11\x63\x63\x61i_project_name\x18\x11 \x01(\t\x12.\n\ncreated_at\x18\x12 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0bmodified_at\x18\x13 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x12\n\ncreated_by\x18\x14 \x01(\t\x12\x13\n\x0bmodified_by\x18\x15 \x01(\t\"c\n\x18\x43reateCcaiProjectRequest\x12-\n\x0c\x63\x63\x61i_project\x18\x01 \x01(\x0b\x32\x17.ondewo.nlu.CcaiProject\x12\x18\n\x10nlu_project_name\x18\x04 \x01(\t\"a\n\x19\x43reateCcaiProjectResponse\x12-\n\x0c\x63\x63\x61i_project\x18\x01 \x01(\x0b\x32\x17.ondewo.nlu.CcaiProject\x12\x15\n\rerror_message\x18\x02 \x01(\t\"\xeb\x01\n\x15GetCcaiProjectRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12;\n\x11\x63\x63\x61i_project_view\x18\x02 \x01(\x0e\x32\x1b.ondewo.nlu.CcaiProjectViewH\x00\x88\x01\x01\x12?\n\x13\x63\x63\x61i_service_filter\x18\x03 \x01(\x0b\x32\x1d.ondewo.nlu.CcaiServiceFilterH\x01\x88\x01\x01\x12\x18\n\x10nlu_project_name\x18\x04 \x01(\tB\x14\n\x12_ccai_project_viewB\x16\n\x14_ccai_service_filter\"\xef\x01\n\x17ListCcaiProjectsRequest\x12\x36\n\x11\x63\x63\x61i_project_view\x18\x01 \x01(\x0e\x32\x1b.ondewo.nlu.CcaiProjectView\x12\x17\n\npage_token\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x41\n\x14\x63\x63\x61i_project_sorting\x18\x03 \x01(\x0b\x32\x1e.ondewo.nlu.CcaiProjectSortingH\x01\x88\x01\x01\x12\x18\n\x10nlu_project_name\x18\x04 \x01(\tB\r\n\x0b_page_tokenB\x17\n\x15_ccai_project_sorting\"c\n\x18ListCcaiProjectsResponse\x12.\n\rccai_projects\x18\x01 \x03(\x0b\x32\x17.ondewo.nlu.CcaiProject\x12\x17\n\x0fnext_page_token\x18\x02 \x01(\t\"\x8e\x03\n\x12\x43\x63\x61iProjectSorting\x12R\n\rsorting_field\x18\x01 \x01(\x0e\x32\x36.ondewo.nlu.CcaiProjectSorting.CcaiProjectSortingFieldH\x00\x88\x01\x01\x12\x32\n\x0csorting_mode\x18\x02 \x01(\x0e\x32\x17.ondewo.nlu.SortingModeH\x01\x88\x01\x01\"\xcc\x01\n\x17\x43\x63\x61iProjectSortingField\x12\x1b\n\x17NO_CCAI_PROJECT_SORTING\x10\x00\x12\x1d\n\x19SORT_CCAI_PROJECT_BY_NAME\x10\x01\x12%\n!SORT_CCAI_PROJECT_BY_DISPLAY_NAME\x10\x02\x12&\n\"SORT_CCAI_PROJECT_BY_CREATION_DATE\x10\x03\x12&\n\"SORT_CCAI_PROJECT_BY_LAST_MODIFIED\x10\x04\x42\x10\n\x0e_sorting_fieldB\x0f\n\r_sorting_mode\"d\n\x11\x43\x63\x61iServiceFilter\x12\x16\n\x0elanguage_codes\x18\x01 \x03(\t\x12\x37\n\x12\x63\x63\x61i_service_types\x18\x02 \x03(\x0e\x32\x1b.ondewo.nlu.CcaiServiceType\"\xed\x01\n\x18UpdateCcaiProjectRequest\x12-\n\x0c\x63\x63\x61i_project\x18\x01 \x01(\x0b\x32\x17.ondewo.nlu.CcaiProject\x12?\n\x13\x63\x63\x61i_service_filter\x18\x02 \x01(\x0b\x32\x1d.ondewo.nlu.CcaiServiceFilterH\x00\x88\x01\x01\x12/\n\x0bupdate_mask\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.FieldMask\x12\x18\n\x10nlu_project_name\x18\x04 \x01(\tB\x16\n\x14_ccai_service_filter\"@\n\x19UpdateCcaiProjectResponse\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x15\n\rerror_message\x18\x02 \x01(\t\"B\n\x18\x44\x65leteCcaiProjectRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x18\n\x10nlu_project_name\x18\x04 \x01(\t\"Z\n\x19\x44\x65leteCcaiProjectResponse\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x15\n\rerror_message\x18\x02 \x01(\t\x12\x18\n\x10nlu_project_name\x18\x04 \x01(\t*\xab\x02\n\x11\x43\x63\x61iProjectStatus\x12#\n\x1f\x43\x43\x41I_PROJECT_STATUS_UNSPECIFIED\x10\x00\x12\"\n\x1e\x43\x43\x41I_PROJECT_STATUS_UNDEPLOYED\x10\x01\x12 \n\x1c\x43\x43\x41I_PROJECT_STATUS_UPDATING\x10\x02\x12!\n\x1d\x43\x43\x41I_PROJECT_STATUS_DEPLOYING\x10\x03\x12 \n\x1c\x43\x43\x41I_PROJECT_STATUS_DEPLOYED\x10\x04\x12#\n\x1f\x43\x43\x41I_PROJECT_STATUS_UNDEPLOYING\x10\x05\x12 \n\x1c\x43\x43\x41I_PROJECT_STATUS_DELETING\x10\x06\x12\x1f\n\x1b\x43\x43\x41I_PROJECT_STATUS_DELETED\x10\x07*\xde\x03\n\x0f\x43\x63\x61iServiceType\x12!\n\x1d\x43\x43\x41I_SERVICE_TYPE_UNSPECIFIED\x10\x00\x12 \n\x1c\x43\x43\x41I_SERVICE_TYPE_ONDEWO_AIM\x10\x01\x12 \n\x1c\x43\x43\x41I_SERVICE_TYPE_ONDEWO_BPI\x10\x02\x12 \n\x1c\x43\x43\x41I_SERVICE_TYPE_ONDEWO_CSI\x10\x03\x12 \n\x1c\x43\x43\x41I_SERVICE_TYPE_ONDEWO_NLU\x10\x04\x12 \n\x1c\x43\x43\x41I_SERVICE_TYPE_ONDEWO_S2T\x10\x05\x12 \n\x1c\x43\x43\x41I_SERVICE_TYPE_ONDEWO_SIP\x10\x06\x12 \n\x1c\x43\x43\x41I_SERVICE_TYPE_ONDEWO_T2S\x10\x07\x12!\n\x1d\x43\x43\x41I_SERVICE_TYPE_ONDEWO_VTSI\x10\x08\x12#\n\x1f\x43\x43\x41I_SERVICE_TYPE_VTSI_RABBITMQ\x10\t\x12#\n\x1f\x43\x43\x41I_SERVICE_TYPE_ONDEWO_NLU_QA\x10\n\x12(\n$CCAI_SERVICE_TYPE_ONDEWO_NLU_WEBHOOK\x10\x0b\x12#\n\x1f\x43\x43\x41I_SERVICE_TYPE_ONDEWO_SURVEY\x10\x0c*\x8e\x01\n\x0f\x43\x63\x61iProjectView\x12!\n\x1d\x43\x43\x41I_PROJECT_VIEW_UNSPECIFIED\x10\x00\x12\x1a\n\x16\x43\x43\x41I_PROJECT_VIEW_FULL\x10\x01\x12\x1d\n\x19\x43\x43\x41I_PROJECT_VIEW_SHALLOW\x10\x02\x12\x1d\n\x19\x43\x43\x41I_PROJECT_VIEW_MINIMUM\x10\x03\x32\xe1\x03\n\x0c\x43\x63\x61iProjects\x12L\n\x0eGetCcaiProject\x12!.ondewo.nlu.GetCcaiProjectRequest\x1a\x17.ondewo.nlu.CcaiProject\x12`\n\x11\x43reateCcaiProject\x12$.ondewo.nlu.CreateCcaiProjectRequest\x1a%.ondewo.nlu.CreateCcaiProjectResponse\x12`\n\x11\x44\x65leteCcaiProject\x12$.ondewo.nlu.DeleteCcaiProjectRequest\x1a%.ondewo.nlu.DeleteCcaiProjectResponse\x12]\n\x10ListCcaiProjects\x12#.ondewo.nlu.ListCcaiProjectsRequest\x1a$.ondewo.nlu.ListCcaiProjectsResponse\x12`\n\x11UpdateCcaiProject\x12$.ondewo.nlu.UpdateCcaiProjectRequest\x1a%.ondewo.nlu.UpdateCcaiProjectResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ondewo.nlu.ccai_project_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _CCAIPROJECT_CCAISERVICESMAPENTRY._options = None
  _CCAIPROJECT_CCAISERVICESMAPENTRY._serialized_options = b'8\001'
  _globals['_CCAIPROJECTSTATUS']._serialized_start=2945
  _globals['_CCAIPROJECTSTATUS']._serialized_end=3244
  _globals['_CCAISERVICETYPE']._serialized_start=3247
  _globals['_CCAISERVICETYPE']._serialized_end=3725
  _globals['_CCAIPROJECTVIEW']._serialized_start=3728
  _globals['_CCAIPROJECTVIEW']._serialized_end=3870
  _globals['_CCAIPROJECT']._serialized_start=138
  _globals['_CCAIPROJECT']._serialized_end=589
  _globals['_CCAIPROJECT_CCAISERVICESMAPENTRY']._serialized_start=506
  _globals['_CCAIPROJECT_CCAISERVICESMAPENTRY']._serialized_end=589
  _globals['_CCAISERVICELIST']._serialized_start=591
  _globals['_CCAISERVICELIST']._serialized_end=656
  _globals['_CCAISERVICE']._serialized_start=659
  _globals['_CCAISERVICE']._serialized_end=1192
  _globals['_CREATECCAIPROJECTREQUEST']._serialized_start=1194
  _globals['_CREATECCAIPROJECTREQUEST']._serialized_end=1293
  _globals['_CREATECCAIPROJECTRESPONSE']._serialized_start=1295
  _globals['_CREATECCAIPROJECTRESPONSE']._serialized_end=1392
  _globals['_GETCCAIPROJECTREQUEST']._serialized_start=1395
  _globals['_GETCCAIPROJECTREQUEST']._serialized_end=1630
  _globals['_LISTCCAIPROJECTSREQUEST']._serialized_start=1633
  _globals['_LISTCCAIPROJECTSREQUEST']._serialized_end=1872
  _globals['_LISTCCAIPROJECTSRESPONSE']._serialized_start=1874
  _globals['_LISTCCAIPROJECTSRESPONSE']._serialized_end=1973
  _globals['_CCAIPROJECTSORTING']._serialized_start=1976
  _globals['_CCAIPROJECTSORTING']._serialized_end=2374
  _globals['_CCAIPROJECTSORTING_CCAIPROJECTSORTINGFIELD']._serialized_start=2135
  _globals['_CCAIPROJECTSORTING_CCAIPROJECTSORTINGFIELD']._serialized_end=2339
  _globals['_CCAISERVICEFILTER']._serialized_start=2376
  _globals['_CCAISERVICEFILTER']._serialized_end=2476
  _globals['_UPDATECCAIPROJECTREQUEST']._serialized_start=2479
  _globals['_UPDATECCAIPROJECTREQUEST']._serialized_end=2716
  _globals['_UPDATECCAIPROJECTRESPONSE']._serialized_start=2718
  _globals['_UPDATECCAIPROJECTRESPONSE']._serialized_end=2782
  _globals['_DELETECCAIPROJECTREQUEST']._serialized_start=2784
  _globals['_DELETECCAIPROJECTREQUEST']._serialized_end=2850
  _globals['_DELETECCAIPROJECTRESPONSE']._serialized_start=2852
  _globals['_DELETECCAIPROJECTRESPONSE']._serialized_end=2942
  _globals['_CCAIPROJECTS']._serialized_start=3873
  _globals['_CCAIPROJECTS']._serialized_end=4354
# @@protoc_insertion_point(module_scope)
