"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.field_mask_pb2
import google.protobuf.internal.containers
import google.protobuf.message
import ondewo.nlu.common_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class Context(google.protobuf.message.Message):
    """Represents a context."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class Parameter(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        NAME_FIELD_NUMBER: builtins.int
        DISPLAY_NAME_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        VALUE_ORIGINAL_FIELD_NUMBER: builtins.int
        CREATED_MODIFIED_FIELD_NUMBER: builtins.int
        name: typing.Text
        """The name of the context parameter."""

        display_name: typing.Text
        """The display name of the context parameter."""

        value: typing.Text
        """The value(s) of the context parameter."""

        value_original: typing.Text
        """The original value(s) of the context parameter."""

        @property
        def created_modified(self) -> ondewo.nlu.common_pb2.CreatedModified:
            """created_at, created_by,modified_at, modified_by"""
            pass
        def __init__(self,
            *,
            name: typing.Text = ...,
            display_name: typing.Text = ...,
            value: typing.Text = ...,
            value_original: typing.Text = ...,
            created_modified: typing.Optional[ondewo.nlu.common_pb2.CreatedModified] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["created_modified",b"created_modified"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["created_modified",b"created_modified","display_name",b"display_name","name",b"name","value",b"value","value_original",b"value_original"]) -> None: ...

    class ParametersEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text
        @property
        def value(self) -> global___Context.Parameter: ...
        def __init__(self,
            *,
            key: typing.Text = ...,
            value: typing.Optional[global___Context.Parameter] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["value",b"value"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    NAME_FIELD_NUMBER: builtins.int
    LIFESPAN_COUNT_FIELD_NUMBER: builtins.int
    PARAMETERS_FIELD_NUMBER: builtins.int
    LIFESPAN_TIME_FIELD_NUMBER: builtins.int
    CREATED_MODIFIED_FIELD_NUMBER: builtins.int
    name: typing.Text
    """Required. The display name of the context (must be unique per session).

    Note: we are deviating from the dialogflow format `projects/<Project ID>/agent/sessions/<Session ID>/contexts/<Context ID>`.

    - DetectIntent only returns
       - the short display name in the "name" field in query_result.output_contexts
       - only expects the short display name in the "name" field in query_parameters.contexts
    - Also inside the persisted session object only the short display name is used.
       - SessionStep.contexts only contains the short display name
       - SessionReviewStep.contexts only contains the short display name
    """

    lifespan_count: builtins.int
    """Optional. The number of conversational query requests after which the
    context expires. If set to `0` (the default) the context expires
    immediately. Contexts expire automatically after 10 minutes even if there
    are no matching queries.
    """

    @property
    def parameters(self) -> google.protobuf.internal.containers.MessageMap[typing.Text, global___Context.Parameter]:
        """Optional. The collection of parameters associated with this context.
        Refer to [this doc](https://dialogflow.com/docs/actions-and-parameters) for
        syntax.
        Keys are the display names of context parameters.
        """
        pass
    lifespan_time: builtins.float
    """Optional. The time span in seconds after which the context expires. By default it does not expire."""

    @property
    def created_modified(self) -> ondewo.nlu.common_pb2.CreatedModified:
        """created_at, created_by,modified_at, modified_by"""
        pass
    def __init__(self,
        *,
        name: typing.Text = ...,
        lifespan_count: builtins.int = ...,
        parameters: typing.Optional[typing.Mapping[typing.Text, global___Context.Parameter]] = ...,
        lifespan_time: builtins.float = ...,
        created_modified: typing.Optional[ondewo.nlu.common_pb2.CreatedModified] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["created_modified",b"created_modified"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["created_modified",b"created_modified","lifespan_count",b"lifespan_count","lifespan_time",b"lifespan_time","name",b"name","parameters",b"parameters"]) -> None: ...
global___Context = Context

class ListContextsRequest(google.protobuf.message.Message):
    """The request message for [Contexts.ListContexts][google.cloud.dialogflow.v2.Contexts.ListContexts]."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    PARENT_FIELD_NUMBER: builtins.int
    PAGE_TOKEN_FIELD_NUMBER: builtins.int
    parent: typing.Text
    """Required. The session to list all contexts from.
    Format: `projects/<Project ID>/agent/sessions/<Session ID>`.
    """

    page_token: typing.Text
    """Optional. The next_page_token value returned from a previous list request."""

    def __init__(self,
        *,
        parent: typing.Text = ...,
        page_token: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["page_token",b"page_token","parent",b"parent"]) -> None: ...
global___ListContextsRequest = ListContextsRequest

class ListContextsResponse(google.protobuf.message.Message):
    """The response message for [Contexts.ListContexts][google.cloud.dialogflow.v2.Contexts.ListContexts]."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    CONTEXTS_FIELD_NUMBER: builtins.int
    NEXT_PAGE_TOKEN_FIELD_NUMBER: builtins.int
    @property
    def contexts(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Context]:
        """The list of contexts. There will be a maximum number of items
        returned based on the page_token field in the request.
        """
        pass
    next_page_token: typing.Text
    """Token to retrieve the next page of results, or empty if there are no
    more results in the list.
    """

    def __init__(self,
        *,
        contexts: typing.Optional[typing.Iterable[global___Context]] = ...,
        next_page_token: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["contexts",b"contexts","next_page_token",b"next_page_token"]) -> None: ...
global___ListContextsResponse = ListContextsResponse

class GetContextRequest(google.protobuf.message.Message):
    """The request message for [Contexts.GetContext][google.cloud.dialogflow.v2.Contexts.GetContext]."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    name: typing.Text
    """Required. The name of the context. Format:
    `projects/<Project ID>/agent/sessions/<Session ID>/contexts/<Context ID>`.
    """

    def __init__(self,
        *,
        name: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["name",b"name"]) -> None: ...
global___GetContextRequest = GetContextRequest

class CreateContextRequest(google.protobuf.message.Message):
    """The request message for [Contexts.CreateContext][google.cloud.dialogflow.v2.Contexts.CreateContext]."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    PARENT_FIELD_NUMBER: builtins.int
    CONTEXT_FIELD_NUMBER: builtins.int
    parent: typing.Text
    """Required. The session to create a context for.
    Format: `projects/<Project ID>/agent/sessions/<Session ID>`.
    """

    @property
    def context(self) -> global___Context:
        """Required. The context to create."""
        pass
    def __init__(self,
        *,
        parent: typing.Text = ...,
        context: typing.Optional[global___Context] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["context",b"context"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["context",b"context","parent",b"parent"]) -> None: ...
global___CreateContextRequest = CreateContextRequest

class UpdateContextRequest(google.protobuf.message.Message):
    """The request message for [Contexts.UpdateContext][google.cloud.dialogflow.v2.Contexts.UpdateContext]."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    CONTEXT_FIELD_NUMBER: builtins.int
    UPDATE_MASK_FIELD_NUMBER: builtins.int
    @property
    def context(self) -> global___Context:
        """Required. The context to update."""
        pass
    @property
    def update_mask(self) -> google.protobuf.field_mask_pb2.FieldMask:
        """Optional. The mask to control which fields get updated."""
        pass
    def __init__(self,
        *,
        context: typing.Optional[global___Context] = ...,
        update_mask: typing.Optional[google.protobuf.field_mask_pb2.FieldMask] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["context",b"context","update_mask",b"update_mask"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["context",b"context","update_mask",b"update_mask"]) -> None: ...
global___UpdateContextRequest = UpdateContextRequest

class DeleteContextRequest(google.protobuf.message.Message):
    """The request message for [Contexts.DeleteContext][google.cloud.dialogflow.v2.Contexts.DeleteContext]."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    name: typing.Text
    """Required. The name of the context to delete. Format:
    `projects/<Project ID>/agent/sessions/<Session ID>/contexts/<Context ID>`.
    """

    def __init__(self,
        *,
        name: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["name",b"name"]) -> None: ...
global___DeleteContextRequest = DeleteContextRequest

class DeleteAllContextsRequest(google.protobuf.message.Message):
    """The request message for [Contexts.DeleteAllContexts][google.cloud.dialogflow.v2.Contexts.DeleteAllContexts]."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    PARENT_FIELD_NUMBER: builtins.int
    parent: typing.Text
    """Required. The name of the session to delete all contexts from. Format:
    `projects/<Project ID>/agent/sessions/<Session ID>`.
    """

    def __init__(self,
        *,
        parent: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["parent",b"parent"]) -> None: ...
global___DeleteAllContextsRequest = DeleteAllContextsRequest
