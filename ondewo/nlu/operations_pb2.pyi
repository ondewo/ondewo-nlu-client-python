"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.any_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import google.protobuf.timestamp_pb2
import google.rpc.status_pb2
import ondewo.nlu.operation_metadata_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class Operation(google.protobuf.message.Message):
    """This resource represents a long-running operation that is the result of a
    network API call.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    METADATA_FIELD_NUMBER: builtins.int
    DONE_FIELD_NUMBER: builtins.int
    ERROR_FIELD_NUMBER: builtins.int
    RESPONSE_FIELD_NUMBER: builtins.int
    name: typing.Text
    """The server-assigned name, which is only unique within the same service that
    originally returns it. If you use the default HTTP mapping, the
    `name` should have the format of `operations/some/unique/name`.
    """

    @property
    def metadata(self) -> ondewo.nlu.operation_metadata_pb2.OperationMetadata:
        """Service-specific metadata associated with the operation.  It typically
        contains progress information and common metadata such as create time.
        Some services might not provide such metadata.  Any method that returns a
        long-running operation should document the metadata type, if any.
        """
        pass
    done: builtins.bool
    """If the value is `false`, it means the operation is still in progress.
    If true, the operation is completed, and either `error` or `response` is
    available.
    """

    @property
    def error(self) -> google.rpc.status_pb2.Status:
        """The error result of the operation in case of failure or cancellation."""
        pass
    @property
    def response(self) -> google.protobuf.any_pb2.Any:
        """The normal response of the operation in case of success.  If the original
        method returns no data on success, such as `Delete`, the response is
        `google.protobuf.Empty`.  If the original method is standard
        `Get`/`Create`/`Update`, the response should be the resource.  For other
        methods, the response should have the type `XxxResponse`, where `Xxx`
        is the original method name.  For example, if the original method name
        is `TakeSnapshot()`, the inferred response type is
        `TakeSnapshotResponse`.
        """
        pass
    def __init__(self,
        *,
        name: typing.Text = ...,
        metadata: typing.Optional[ondewo.nlu.operation_metadata_pb2.OperationMetadata] = ...,
        done: builtins.bool = ...,
        error: typing.Optional[google.rpc.status_pb2.Status] = ...,
        response: typing.Optional[google.protobuf.any_pb2.Any] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["error",b"error","metadata",b"metadata","response",b"response","result",b"result"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["done",b"done","error",b"error","metadata",b"metadata","name",b"name","response",b"response","result",b"result"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["result",b"result"]) -> typing.Optional[typing_extensions.Literal["error","response"]]: ...
global___Operation = Operation

class GetOperationRequest(google.protobuf.message.Message):
    """The request message for [Operations.GetOperation][ondewo.nlu.Operations.GetOperation]."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    name: typing.Text
    """The name of the operation resource."""

    def __init__(self,
        *,
        name: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["name",b"name"]) -> None: ...
global___GetOperationRequest = GetOperationRequest

class ListOperationsRequest(google.protobuf.message.Message):
    """The request message for [Operations.ListOperations][ondewo.nlu.Operations.ListOperations]."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    FILTER_FIELD_NUMBER: builtins.int
    PAGE_SIZE_FIELD_NUMBER: builtins.int
    PAGE_TOKEN_FIELD_NUMBER: builtins.int
    OPERATION_FILTER_FIELD_NUMBER: builtins.int
    name: typing.Text
    """The name of the operation collection."""

    filter: typing.Text
    """The standard list filter."""

    page_size: builtins.int
    """The standard list page size."""

    page_token: typing.Text
    """The standard list page token."""

    @property
    def operation_filter(self) -> global___OperationFilter:
        """Optional. A filter to narrow the response down to operations of interest."""
        pass
    def __init__(self,
        *,
        name: typing.Text = ...,
        filter: typing.Text = ...,
        page_size: builtins.int = ...,
        page_token: typing.Text = ...,
        operation_filter: typing.Optional[global___OperationFilter] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["operation_filter",b"operation_filter"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["filter",b"filter","name",b"name","operation_filter",b"operation_filter","page_size",b"page_size","page_token",b"page_token"]) -> None: ...
global___ListOperationsRequest = ListOperationsRequest

class OperationFilter(google.protobuf.message.Message):
    """An operationFilter can be used in some requests to return only operations matching certain filter conditions.

    All fields below are  optional. Multiple fields specified at the same time are chained via OR.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    PROJECT_PARENTS_FIELD_NUMBER: builtins.int
    STATUSES_FIELD_NUMBER: builtins.int
    TYPES_FIELD_NUMBER: builtins.int
    START_TIME_FIELD_NUMBER: builtins.int
    END_TIME_FIELD_NUMBER: builtins.int
    USER_IDS_FIELD_NUMBER: builtins.int
    @property
    def project_parents(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
        """Match operations with any of the following project parents."""
        pass
    @property
    def statuses(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[ondewo.nlu.operation_metadata_pb2.OperationMetadata.Status.ValueType]:
        """Match operation which had any of the following operation statuses."""
        pass
    @property
    def types(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[ondewo.nlu.operation_metadata_pb2.OperationMetadata.OperationType.ValueType]:
        """Match operation which had any of the following operation types."""
        pass
    @property
    def start_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """The time operation processing started."""
        pass
    @property
    def end_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """The time operation processing completed."""
        pass
    @property
    def user_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
        """Match operation which had any of the following user_ids."""
        pass
    def __init__(self,
        *,
        project_parents: typing.Optional[typing.Iterable[typing.Text]] = ...,
        statuses: typing.Optional[typing.Iterable[ondewo.nlu.operation_metadata_pb2.OperationMetadata.Status.ValueType]] = ...,
        types: typing.Optional[typing.Iterable[ondewo.nlu.operation_metadata_pb2.OperationMetadata.OperationType.ValueType]] = ...,
        start_time: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
        end_time: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
        user_ids: typing.Optional[typing.Iterable[typing.Text]] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["end_time",b"end_time","end_time_oneof",b"end_time_oneof","start_time",b"start_time","start_time_oneof",b"start_time_oneof"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["end_time",b"end_time","end_time_oneof",b"end_time_oneof","project_parents",b"project_parents","start_time",b"start_time","start_time_oneof",b"start_time_oneof","statuses",b"statuses","types",b"types","user_ids",b"user_ids"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["end_time_oneof",b"end_time_oneof"]) -> typing.Optional[typing_extensions.Literal["end_time"]]: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["start_time_oneof",b"start_time_oneof"]) -> typing.Optional[typing_extensions.Literal["start_time"]]: ...
global___OperationFilter = OperationFilter

class ListOperationsResponse(google.protobuf.message.Message):
    """The response message for [Operations.ListOperations][ondewo.nlu.Operations.ListOperations]."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    OPERATIONS_FIELD_NUMBER: builtins.int
    NEXT_PAGE_TOKEN_FIELD_NUMBER: builtins.int
    @property
    def operations(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Operation]:
        """A list of operations that matches the specified filter in the request."""
        pass
    next_page_token: typing.Text
    """The standard List next-page token."""

    def __init__(self,
        *,
        operations: typing.Optional[typing.Iterable[global___Operation]] = ...,
        next_page_token: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["next_page_token",b"next_page_token","operations",b"operations"]) -> None: ...
global___ListOperationsResponse = ListOperationsResponse

class CancelOperationRequest(google.protobuf.message.Message):
    """The request message for [Operations.CancelOperation][ondewo.nlu.Operations.CancelOperation]."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    name: typing.Text
    """The name of the operation resource to be cancelled."""

    def __init__(self,
        *,
        name: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["name",b"name"]) -> None: ...
global___CancelOperationRequest = CancelOperationRequest

class DeleteOperationRequest(google.protobuf.message.Message):
    """The request message for [Operations.DeleteOperation][ondewo.nlu.Operations.DeleteOperation]."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    name: typing.Text
    """The name of the operation resource to be deleted."""

    def __init__(self,
        *,
        name: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["name",b"name"]) -> None: ...
global___DeleteOperationRequest = DeleteOperationRequest
