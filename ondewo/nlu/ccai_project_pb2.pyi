"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright 2020-2023 ONDEWO GmbH

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.field_mask_pb2
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.timestamp_pb2
import ondewo.nlu.common_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _CcaiProjectStatus:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _CcaiProjectStatusEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_CcaiProjectStatus.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    UNSPECIFIED: _CcaiProjectStatus.ValueType  # 0
    """No status specified"""
    UNDEPLOYED: _CcaiProjectStatus.ValueType  # 1
    """Project successfully created and undeployed"""
    UPDATING: _CcaiProjectStatus.ValueType  # 2
    """Project configuration is updating"""
    DEPLOYING: _CcaiProjectStatus.ValueType  # 3
    """Project is deploying"""
    DEPLOYED: _CcaiProjectStatus.ValueType  # 4
    """Project is deployed"""
    UNDEPLOYING: _CcaiProjectStatus.ValueType  # 5
    """Project is un-deploying"""
    DELETING: _CcaiProjectStatus.ValueType  # 6
    """Project is currently deleting"""
    DELETED: _CcaiProjectStatus.ValueType  # 7
    """Project is deleted"""

class CcaiProjectStatus(_CcaiProjectStatus, metaclass=_CcaiProjectStatusEnumTypeWrapper):
    """Status of a VtsiProject."""

UNSPECIFIED: CcaiProjectStatus.ValueType  # 0
"""No status specified"""
UNDEPLOYED: CcaiProjectStatus.ValueType  # 1
"""Project successfully created and undeployed"""
UPDATING: CcaiProjectStatus.ValueType  # 2
"""Project configuration is updating"""
DEPLOYING: CcaiProjectStatus.ValueType  # 3
"""Project is deploying"""
DEPLOYED: CcaiProjectStatus.ValueType  # 4
"""Project is deployed"""
UNDEPLOYING: CcaiProjectStatus.ValueType  # 5
"""Project is un-deploying"""
DELETING: CcaiProjectStatus.ValueType  # 6
"""Project is currently deleting"""
DELETED: CcaiProjectStatus.ValueType  # 7
"""Project is deleted"""
global___CcaiProjectStatus = CcaiProjectStatus

class _CcaiServiceType:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _CcaiServiceTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_CcaiServiceType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    CCAI_SERVICE_TYPE_UNSPECIFIED: _CcaiServiceType.ValueType  # 0
    """unspecified"""
    CCAI_SERVICE_TYPE_ONDEWO_AIM: _CcaiServiceType.ValueType  # 1
    """ondewo-aim service"""
    CCAI_SERVICE_TYPE_ONDEWO_BPI: _CcaiServiceType.ValueType  # 2
    """ondewo-bpi service"""
    CCAI_SERVICE_TYPE_ONDEWO_CSI: _CcaiServiceType.ValueType  # 3
    """ondewo-csi service"""
    CCAI_SERVICE_TYPE_ONDEWO_NLU: _CcaiServiceType.ValueType  # 4
    """ondewo-nlu service"""
    CCAI_SERVICE_TYPE_ONDEWO_S2T: _CcaiServiceType.ValueType  # 5
    """ondewo-s2t service"""
    CCAI_SERVICE_TYPE_ONDEWO_SIP: _CcaiServiceType.ValueType  # 6
    """ondewo-sip service"""
    CCAI_SERVICE_TYPE_ONDEWO_T2S: _CcaiServiceType.ValueType  # 7
    """ondewo-t2s service"""
    CCAI_SERVICE_TYPE_ONDEWO_VTSI: _CcaiServiceType.ValueType  # 8
    """ondewo-vtsi service"""
    CCAI_SERVICE_TYPE_VTSI_RABBITMQ: _CcaiServiceType.ValueType  # 9
    """ondewo-vtsi service"""
    CCAI_SERVICE_TYPE_ONDEWO_NLU_QA: _CcaiServiceType.ValueType  # 10
    """ondewo-nlu-qa service"""
    CCAI_SERVICE_TYPE_ONDEWO_NLU_WEBHOOK: _CcaiServiceType.ValueType  # 11
    """ondewo-nlu-webhook service"""
    CCAI_SERVICE_TYPE_ONDEWO_SURVEY: _CcaiServiceType.ValueType  # 12
    """ondewo-survey service"""

class CcaiServiceType(_CcaiServiceType, metaclass=_CcaiServiceTypeEnumTypeWrapper): ...

CCAI_SERVICE_TYPE_UNSPECIFIED: CcaiServiceType.ValueType  # 0
"""unspecified"""
CCAI_SERVICE_TYPE_ONDEWO_AIM: CcaiServiceType.ValueType  # 1
"""ondewo-aim service"""
CCAI_SERVICE_TYPE_ONDEWO_BPI: CcaiServiceType.ValueType  # 2
"""ondewo-bpi service"""
CCAI_SERVICE_TYPE_ONDEWO_CSI: CcaiServiceType.ValueType  # 3
"""ondewo-csi service"""
CCAI_SERVICE_TYPE_ONDEWO_NLU: CcaiServiceType.ValueType  # 4
"""ondewo-nlu service"""
CCAI_SERVICE_TYPE_ONDEWO_S2T: CcaiServiceType.ValueType  # 5
"""ondewo-s2t service"""
CCAI_SERVICE_TYPE_ONDEWO_SIP: CcaiServiceType.ValueType  # 6
"""ondewo-sip service"""
CCAI_SERVICE_TYPE_ONDEWO_T2S: CcaiServiceType.ValueType  # 7
"""ondewo-t2s service"""
CCAI_SERVICE_TYPE_ONDEWO_VTSI: CcaiServiceType.ValueType  # 8
"""ondewo-vtsi service"""
CCAI_SERVICE_TYPE_VTSI_RABBITMQ: CcaiServiceType.ValueType  # 9
"""ondewo-vtsi service"""
CCAI_SERVICE_TYPE_ONDEWO_NLU_QA: CcaiServiceType.ValueType  # 10
"""ondewo-nlu-qa service"""
CCAI_SERVICE_TYPE_ONDEWO_NLU_WEBHOOK: CcaiServiceType.ValueType  # 11
"""ondewo-nlu-webhook service"""
CCAI_SERVICE_TYPE_ONDEWO_SURVEY: CcaiServiceType.ValueType  # 12
"""ondewo-survey service"""
global___CcaiServiceType = CcaiServiceType

class _CcaiProjectView:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _CcaiProjectViewEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_CcaiProjectView.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    CCAI_PROJECT_VIEW_UNSPECIFIED: _CcaiProjectView.ValueType  # 0
    """Unspecified CCAI_PROJECT view: the view is defined by the call:"""
    CCAI_PROJECT_VIEW_FULL: _CcaiProjectView.ValueType  # 1
    """Full CCAI_PROJECT view: populate all the fields of the CCAI_PROJECT message including configs."""
    CCAI_PROJECT_VIEW_SHALLOW: _CcaiProjectView.ValueType  # 2
    """Shallow CCAI_PROJECT view: populates all the fields except configs."""
    CCAI_PROJECT_VIEW_MINIMUM: _CcaiProjectView.ValueType  # 3
    """Minimum view including only CCAI_PROJECT UUID and CCAI_PROJECT display name"""

class CcaiProjectView(_CcaiProjectView, metaclass=_CcaiProjectViewEnumTypeWrapper):
    """Structure of CCAI_PROJECT view
    - CreateCCAI_PROJECT: CCAI_PROJECT_VIEW_SHALLOW
    - UpdateCCAI_PROJECT: CCAI_PROJECT_VIEW_SHALLOW
    - GetCCAI_PROJECT: CCAI_PROJECT_VIEW_FULL
    - ListCCAI_PROJECTs: CCAI_PROJECT_VIEW_SHALLOW
    """

CCAI_PROJECT_VIEW_UNSPECIFIED: CcaiProjectView.ValueType  # 0
"""Unspecified CCAI_PROJECT view: the view is defined by the call:"""
CCAI_PROJECT_VIEW_FULL: CcaiProjectView.ValueType  # 1
"""Full CCAI_PROJECT view: populate all the fields of the CCAI_PROJECT message including configs."""
CCAI_PROJECT_VIEW_SHALLOW: CcaiProjectView.ValueType  # 2
"""Shallow CCAI_PROJECT view: populates all the fields except configs."""
CCAI_PROJECT_VIEW_MINIMUM: CcaiProjectView.ValueType  # 3
"""Minimum view including only CCAI_PROJECT UUID and CCAI_PROJECT display name"""
global___CcaiProjectView = CcaiProjectView

@typing_extensions.final
class CcaiProject(google.protobuf.message.Message):
    """Message representing a CCAI project"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class CcaiServiceListsEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        @property
        def value(self) -> global___CcaiServiceList: ...
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: global___CcaiServiceList | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value", b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key", b"key", "value", b"value"]) -> None: ...

    NAME_FIELD_NUMBER: builtins.int
    DISPLAY_NAME_FIELD_NUMBER: builtins.int
    OWNER_NAME_FIELD_NUMBER: builtins.int
    CCAI_SERVICE_LISTS_FIELD_NUMBER: builtins.int
    CCAI_PROJECT_STATUS_FIELD_NUMBER: builtins.int
    CREATED_AT_FIELD_NUMBER: builtins.int
    MODIFIED_AT_FIELD_NUMBER: builtins.int
    CREATED_BY_FIELD_NUMBER: builtins.int
    MODIFIED_BY_FIELD_NUMBER: builtins.int
    name: builtins.str
    """Resource name of the CCAI project"""
    display_name: builtins.str
    """Required. The display name of this ccai project."""
    owner_name: builtins.str
    """Optional. Resource name of the user who is the owner of the project."""
    @property
    def ccai_service_lists(self) -> google.protobuf.internal.containers.MessageMap[builtins.str, global___CcaiServiceList]:
        """Map of two letter language codes to lists of CcaiServiceList
        Two-letter language codes following ISO 639-1 (see https://en.wikipedia.org/wiki/ISO_639-1)
        """
    ccai_project_status: global___CcaiProjectStatus.ValueType
    """The status of the ccai project."""
    @property
    def created_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Creation date and time. Read-only field."""
    @property
    def modified_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Modification date and time. Read-only field."""
    created_by: builtins.str
    """User id in the form of a valid UUID."""
    modified_by: builtins.str
    """User id in the form of a valid UUID."""
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        display_name: builtins.str = ...,
        owner_name: builtins.str = ...,
        ccai_service_lists: collections.abc.Mapping[builtins.str, global___CcaiServiceList] | None = ...,
        ccai_project_status: global___CcaiProjectStatus.ValueType = ...,
        created_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        modified_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        created_by: builtins.str = ...,
        modified_by: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["created_at", b"created_at", "modified_at", b"modified_at"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["ccai_project_status", b"ccai_project_status", "ccai_service_lists", b"ccai_service_lists", "created_at", b"created_at", "created_by", b"created_by", "display_name", b"display_name", "modified_at", b"modified_at", "modified_by", b"modified_by", "name", b"name", "owner_name", b"owner_name"]) -> None: ...

global___CcaiProject = CcaiProject

@typing_extensions.final
class CcaiServiceList(google.protobuf.message.Message):
    """Message representing a list of CCAI services"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CCAI_SERVICES_FIELD_NUMBER: builtins.int
    @property
    def ccai_services(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___CcaiService]:
        """CCAI services"""
    def __init__(
        self,
        *,
        ccai_services: collections.abc.Iterable[global___CcaiService] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["ccai_services", b"ccai_services"]) -> None: ...

global___CcaiServiceList = CcaiServiceList

@typing_extensions.final
class CcaiService(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    DISPLAY_NAME_FIELD_NUMBER: builtins.int
    GRPC_HOST_FIELD_NUMBER: builtins.int
    GRPC_PORT_FIELD_NUMBER: builtins.int
    WEBGRPC_HOST_FIELD_NUMBER: builtins.int
    WEBGRPC_PORT_FIELD_NUMBER: builtins.int
    GRPC_CERT_FIELD_NUMBER: builtins.int
    HOST_FIELD_NUMBER: builtins.int
    PORT_FIELD_NUMBER: builtins.int
    PORT2_FIELD_NUMBER: builtins.int
    ACCOUNT_NAME_FIELD_NUMBER: builtins.int
    PASSWORD_FIELD_NUMBER: builtins.int
    API_KEY_FIELD_NUMBER: builtins.int
    CCAI_SERVICE_TYPE_FIELD_NUMBER: builtins.int
    CREATED_AT_FIELD_NUMBER: builtins.int
    MODIFIED_AT_FIELD_NUMBER: builtins.int
    CREATED_BY_FIELD_NUMBER: builtins.int
    MODIFIED_BY_FIELD_NUMBER: builtins.int
    name: builtins.str
    """Resource name of the service"""
    display_name: builtins.str
    """Display name"""
    grpc_host: builtins.str
    """gRPC host and port"""
    grpc_port: builtins.int
    webgrpc_host: builtins.str
    """Web gRPC host and port"""
    webgrpc_port: builtins.int
    grpc_cert: builtins.str
    """Path to the gRPC certificate"""
    host: builtins.str
    """Additional host and ports"""
    port: builtins.int
    port2: builtins.int
    account_name: builtins.str
    """Account information"""
    password: builtins.str
    api_key: builtins.str
    """API key for the service"""
    ccai_service_type: global___CcaiServiceType.ValueType
    """Type of CCAI service"""
    @property
    def created_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Creation date and time. Read-only field."""
    @property
    def modified_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Modification date and time. Read-only field."""
    created_by: builtins.str
    """User id in the form of a valid UUID."""
    modified_by: builtins.str
    """User id in the form of a valid UUID."""
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        display_name: builtins.str = ...,
        grpc_host: builtins.str = ...,
        grpc_port: builtins.int = ...,
        webgrpc_host: builtins.str = ...,
        webgrpc_port: builtins.int = ...,
        grpc_cert: builtins.str = ...,
        host: builtins.str = ...,
        port: builtins.int = ...,
        port2: builtins.int = ...,
        account_name: builtins.str = ...,
        password: builtins.str = ...,
        api_key: builtins.str = ...,
        ccai_service_type: global___CcaiServiceType.ValueType = ...,
        created_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        modified_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        created_by: builtins.str = ...,
        modified_by: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["created_at", b"created_at", "modified_at", b"modified_at"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["account_name", b"account_name", "api_key", b"api_key", "ccai_service_type", b"ccai_service_type", "created_at", b"created_at", "created_by", b"created_by", "display_name", b"display_name", "grpc_cert", b"grpc_cert", "grpc_host", b"grpc_host", "grpc_port", b"grpc_port", "host", b"host", "modified_at", b"modified_at", "modified_by", b"modified_by", "name", b"name", "password", b"password", "port", b"port", "port2", b"port2", "webgrpc_host", b"webgrpc_host", "webgrpc_port", b"webgrpc_port"]) -> None: ...

global___CcaiService = CcaiService

@typing_extensions.final
class CreateCcaiProjectRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CCAI_PROJECT_FIELD_NUMBER: builtins.int
    @property
    def ccai_project(self) -> global___CcaiProject: ...
    def __init__(
        self,
        *,
        ccai_project: global___CcaiProject | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["ccai_project", b"ccai_project"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["ccai_project", b"ccai_project"]) -> None: ...

global___CreateCcaiProjectRequest = CreateCcaiProjectRequest

@typing_extensions.final
class CreateCcaiProjectResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CCAI_PROJECT_FIELD_NUMBER: builtins.int
    ERROR_MESSAGE_FIELD_NUMBER: builtins.int
    @property
    def ccai_project(self) -> global___CcaiProject: ...
    error_message: builtins.str
    """error message if there are any."""
    def __init__(
        self,
        *,
        ccai_project: global___CcaiProject | None = ...,
        error_message: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["ccai_project", b"ccai_project"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["ccai_project", b"ccai_project", "error_message", b"error_message"]) -> None: ...

global___CreateCcaiProjectResponse = CreateCcaiProjectResponse

@typing_extensions.final
class GetCcaiProjectRequest(google.protobuf.message.Message):
    """Request to retrieve a CCAI project"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    CCAI_PROJECT_VIEW_FIELD_NUMBER: builtins.int
    CCAI_PROJECT_FILTER_FIELD_NUMBER: builtins.int
    name: builtins.str
    """CCAI project name with which to perform the call of the form <pre><code>projects/&lt;project_uuid&gt;/project</code></pre>"""
    ccai_project_view: global___CcaiProjectView.ValueType
    """Optional. Specify the view of the returned CcaiProject (full view by default)"""
    @property
    def ccai_project_filter(self) -> global___CcaiProjectFilter: ...
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        ccai_project_view: global___CcaiProjectView.ValueType = ...,
        ccai_project_filter: global___CcaiProjectFilter | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["ccai_project_filter", b"ccai_project_filter"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["ccai_project_filter", b"ccai_project_filter", "ccai_project_view", b"ccai_project_view", "name", b"name"]) -> None: ...

global___GetCcaiProjectRequest = GetCcaiProjectRequest

@typing_extensions.final
class ListCcaiProjectsRequest(google.protobuf.message.Message):
    """Request to get the list of agents"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CCAI_PROJECT_VIEW_FIELD_NUMBER: builtins.int
    PAGE_TOKEN_FIELD_NUMBER: builtins.int
    CCAI_PROJECT_SORTING_FIELD_NUMBER: builtins.int
    NLU_AGENT_NAMES_FIELD_NUMBER: builtins.int
    ccai_project_view: global___CcaiProjectView.ValueType
    """Optional. Specify the view of the returned CcaiProject (full view by default)"""
    page_token: builtins.str
    """Optional. The next_page_token value returned from a previous list request.
    Example: "current_index-1--page_size-20"
    The page token to support pagination.
    Pagination allows you to retrieve a large result set in smaller, more manageable portions.
    The page token is a string representing the current index and page size.

    Valid page token strings:
    * "" (empty string) - Retrieves the first page.
    * "current_index-0--page_size-20" - Retrieves the first page with a page size of 20.
    * "current_index-1--page_size-20" - Retrieves the second page with a page size of 20.

    Index starts at 0.

    Examples of valid page token strings:
    * ""
    * "current_index-0--page_size-20"
    * "current_index-1--page_size-20"
    * "current_index-10--page_size-20"

    Examples of invalid page token strings:
    * "1"
    * "current_index-0--page_size-20"
    * "current_index--1--page_size-20"
    * "current_index1--page_size-20"
    * "current_index-1--page_size--20"
    """
    @property
    def ccai_project_sorting(self) -> global___CcaiProjectSorting:
        """Optional. Field to define the sorting of the list of CCAI projects in the response.
        If not specified, the default behavior is to have no sorting.
        """
    @property
    def nlu_agent_names(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Optional. Filter based on associated NLU agents
        Format: `projects/<Project ID>/agent`.
        """
    def __init__(
        self,
        *,
        ccai_project_view: global___CcaiProjectView.ValueType = ...,
        page_token: builtins.str | None = ...,
        ccai_project_sorting: global___CcaiProjectSorting | None = ...,
        nlu_agent_names: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_ccai_project_sorting", b"_ccai_project_sorting", "_page_token", b"_page_token", "ccai_project_sorting", b"ccai_project_sorting", "page_token", b"page_token"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_ccai_project_sorting", b"_ccai_project_sorting", "_page_token", b"_page_token", "ccai_project_sorting", b"ccai_project_sorting", "ccai_project_view", b"ccai_project_view", "nlu_agent_names", b"nlu_agent_names", "page_token", b"page_token"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_ccai_project_sorting", b"_ccai_project_sorting"]) -> typing_extensions.Literal["ccai_project_sorting"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_page_token", b"_page_token"]) -> typing_extensions.Literal["page_token"] | None: ...

global___ListCcaiProjectsRequest = ListCcaiProjectsRequest

@typing_extensions.final
class ListCcaiProjectsResponse(google.protobuf.message.Message):
    """This is a protobuf message definition for the response of getting a list of CCAI projects."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CCAI_PROJECTS_FIELD_NUMBER: builtins.int
    NEXT_PAGE_TOKEN_FIELD_NUMBER: builtins.int
    @property
    def ccai_projects(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___CcaiProject]:
        """The list of CCAI projects returned in the response.
        Use the 'repeated' keyword to indicate that this field can contain multiple instances of CcaiProject.
        """
    next_page_token: builtins.str
    """Token to retrieve the next page of results.
    This field is a string that holds a token for fetching the next page of results.
    If there are no more results in the list, this field will be empty.
    """
    def __init__(
        self,
        *,
        ccai_projects: collections.abc.Iterable[global___CcaiProject] | None = ...,
        next_page_token: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["ccai_projects", b"ccai_projects", "next_page_token", b"next_page_token"]) -> None: ...

global___ListCcaiProjectsResponse = ListCcaiProjectsResponse

@typing_extensions.final
class CcaiProjectSorting(google.protobuf.message.Message):
    """This protobuf message defines the sorting order for CCAI (Virtual Test System Infrastructure) projects."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _CcaiProjectSortingField:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _CcaiProjectSortingFieldEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[CcaiProjectSorting._CcaiProjectSortingField.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        NO_CCAI_PROJECT_SORTING: CcaiProjectSorting._CcaiProjectSortingField.ValueType  # 0
        """No sorting"""
        SORT_CCAI_PROJECT_BY_NAME: CcaiProjectSorting._CcaiProjectSortingField.ValueType  # 1
        """Sort by project name such as <pre><code>projects/&lt;project_uuid&gt;/project</code></pre>."""
        SORT_CCAI_PROJECT_BY_DISPLAY_NAME: CcaiProjectSorting._CcaiProjectSortingField.ValueType  # 2
        """Sort by display name"""
        SORT_CCAI_PROJECT_BY_CREATION_DATE: CcaiProjectSorting._CcaiProjectSortingField.ValueType  # 3
        """Sort by creation date"""
        SORT_CCAI_PROJECT_BY_LAST_MODIFIED: CcaiProjectSorting._CcaiProjectSortingField.ValueType  # 4
        """Sort by last modified date"""

    class CcaiProjectSortingField(_CcaiProjectSortingField, metaclass=_CcaiProjectSortingFieldEnumTypeWrapper):
        """Enum to specify the sorting field for CCAI projects."""

    NO_CCAI_PROJECT_SORTING: CcaiProjectSorting.CcaiProjectSortingField.ValueType  # 0
    """No sorting"""
    SORT_CCAI_PROJECT_BY_NAME: CcaiProjectSorting.CcaiProjectSortingField.ValueType  # 1
    """Sort by project name such as <pre><code>projects/&lt;project_uuid&gt;/project</code></pre>."""
    SORT_CCAI_PROJECT_BY_DISPLAY_NAME: CcaiProjectSorting.CcaiProjectSortingField.ValueType  # 2
    """Sort by display name"""
    SORT_CCAI_PROJECT_BY_CREATION_DATE: CcaiProjectSorting.CcaiProjectSortingField.ValueType  # 3
    """Sort by creation date"""
    SORT_CCAI_PROJECT_BY_LAST_MODIFIED: CcaiProjectSorting.CcaiProjectSortingField.ValueType  # 4
    """Sort by last modified date"""

    SORTING_FIELD_FIELD_NUMBER: builtins.int
    SORTING_MODE_FIELD_NUMBER: builtins.int
    sorting_field: global___CcaiProjectSorting.CcaiProjectSortingField.ValueType
    """sorting field for ccai projects sorting"""
    sorting_mode: ondewo.nlu.common_pb2.SortingMode.ValueType
    """Sorting mode"""
    def __init__(
        self,
        *,
        sorting_field: global___CcaiProjectSorting.CcaiProjectSortingField.ValueType | None = ...,
        sorting_mode: ondewo.nlu.common_pb2.SortingMode.ValueType | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_sorting_field", b"_sorting_field", "_sorting_mode", b"_sorting_mode", "sorting_field", b"sorting_field", "sorting_mode", b"sorting_mode"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_sorting_field", b"_sorting_field", "_sorting_mode", b"_sorting_mode", "sorting_field", b"sorting_field", "sorting_mode", b"sorting_mode"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_sorting_field", b"_sorting_field"]) -> typing_extensions.Literal["sorting_field"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_sorting_mode", b"_sorting_mode"]) -> typing_extensions.Literal["sorting_mode"] | None: ...

global___CcaiProjectSorting = CcaiProjectSorting

@typing_extensions.final
class CcaiProjectFilter(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    LANGUAGE_CODES_FIELD_NUMBER: builtins.int
    CCAI_SERVICE_TYPE_FIELD_NUMBER: builtins.int
    @property
    def language_codes(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """Language codes of the projects for which services are filtered."""
    @property
    def ccai_service_type(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[global___CcaiServiceType.ValueType]:
        """Type of CCAI service"""
    def __init__(
        self,
        *,
        language_codes: collections.abc.Iterable[builtins.str] | None = ...,
        ccai_service_type: collections.abc.Iterable[global___CcaiServiceType.ValueType] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["ccai_service_type", b"ccai_service_type", "language_codes", b"language_codes"]) -> None: ...

global___CcaiProjectFilter = CcaiProjectFilter

@typing_extensions.final
class UpdateCcaiProjectRequest(google.protobuf.message.Message):
    """Request to updated CCAI project"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CCAI_PROJECT_FIELD_NUMBER: builtins.int
    UPDATE_MASK_FIELD_NUMBER: builtins.int
    @property
    def ccai_project(self) -> global___CcaiProject:
        """Project Configs."""
    @property
    def update_mask(self) -> google.protobuf.field_mask_pb2.FieldMask:
        """Optional. The mask to control which fields get updated."""
    def __init__(
        self,
        *,
        ccai_project: global___CcaiProject | None = ...,
        update_mask: google.protobuf.field_mask_pb2.FieldMask | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["ccai_project", b"ccai_project", "update_mask", b"update_mask"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["ccai_project", b"ccai_project", "update_mask", b"update_mask"]) -> None: ...

global___UpdateCcaiProjectRequest = UpdateCcaiProjectRequest

@typing_extensions.final
class UpdateCcaiProjectResponse(google.protobuf.message.Message):
    """Request to updated CCAI project"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    ERROR_MESSAGE_FIELD_NUMBER: builtins.int
    name: builtins.str
    """CCAI project name with which to perform the call of the form <pre><code>projects/&lt;project_uuid&gt;/project</code></pre>"""
    error_message: builtins.str
    """error message if there are any."""
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        error_message: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["error_message", b"error_message", "name", b"name"]) -> None: ...

global___UpdateCcaiProjectResponse = UpdateCcaiProjectResponse

@typing_extensions.final
class DeleteCcaiProjectRequest(google.protobuf.message.Message):
    """Request to delete a CCAI project
    If a deployed CCAI project was deleted then it was undeployed beforehand automatically
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    name: builtins.str
    """CCAI project name with which to perform the call of the form <pre><code>projects/&lt;project_uuid&gt;/project</code></pre>"""
    def __init__(
        self,
        *,
        name: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["name", b"name"]) -> None: ...

global___DeleteCcaiProjectRequest = DeleteCcaiProjectRequest

@typing_extensions.final
class DeleteCcaiProjectResponse(google.protobuf.message.Message):
    """Response to delete a CCAI project
    If a deployed CCAI project was deleted then it was undeployed beforehand automatically
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAME_FIELD_NUMBER: builtins.int
    ERROR_MESSAGE_FIELD_NUMBER: builtins.int
    name: builtins.str
    """CCAI project name with which to perform the call of the form <pre><code>projects/&lt;project_uuid&gt;/project</code></pre>"""
    error_message: builtins.str
    """error message if there are any."""
    def __init__(
        self,
        *,
        name: builtins.str = ...,
        error_message: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["error_message", b"error_message", "name", b"name"]) -> None: ...

global___DeleteCcaiProjectResponse = DeleteCcaiProjectResponse
