"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import ondewo.nlu.session_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class GetAnswerRequest(google.protobuf.message.Message):
    """///// Messages ///////

    The request message
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    SESSION_ID_FIELD_NUMBER: builtins.int
    TEXT_FIELD_NUMBER: builtins.int
    MAX_NUM_ANSWERS_FIELD_NUMBER: builtins.int
    THRESHOLD_READER_FIELD_NUMBER: builtins.int
    THRESHOLD_RETRIEVER_FIELD_NUMBER: builtins.int
    THRESHOLD_OVERALL_FIELD_NUMBER: builtins.int
    READER_MODEL_NAME_FIELD_NUMBER: builtins.int
    URL_FILTER_FIELD_NUMBER: builtins.int
    session_id: typing.Text
    """Required. The name of the session this query is sent to. Format:
    `projects/<Project ID>/agent/sessions/<Session ID>`. It's up to the API
    caller to choose an appropriate session ID. It can be a random number or
    some type of user identifier (preferably hashed). The length of the session
    ID must not exceed 36 bytes.
    """

    @property
    def text(self) -> ondewo.nlu.session_pb2.TextInput:
        """Required. The context of the request. A message containing a string (in the form of a sentence) and a
        language code.
        """
        pass
    max_num_answers: builtins.int
    """Maximal number of answers returned"""

    threshold_reader: builtins.float
    """Threshold (minimal score) to give back reader result"""

    threshold_retriever: builtins.float
    """Threshold (minimal score) to give back retriever result"""

    threshold_overall: builtins.float
    """Threshold (minimal score) overall probability"""

    reader_model_name: typing.Text
    """Reader model name"""

    @property
    def url_filter(self) -> global___UrlFilter:
        """Optional. Filters applied to the urls, to restrict the retrieved documents."""
        pass
    def __init__(self,
        *,
        session_id: typing.Text = ...,
        text: typing.Optional[ondewo.nlu.session_pb2.TextInput] = ...,
        max_num_answers: builtins.int = ...,
        threshold_reader: builtins.float = ...,
        threshold_retriever: builtins.float = ...,
        threshold_overall: builtins.float = ...,
        reader_model_name: typing.Text = ...,
        url_filter: typing.Optional[global___UrlFilter] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["text",b"text","url_filter",b"url_filter"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["max_num_answers",b"max_num_answers","reader_model_name",b"reader_model_name","session_id",b"session_id","text",b"text","threshold_overall",b"threshold_overall","threshold_reader",b"threshold_reader","threshold_retriever",b"threshold_retriever","url_filter",b"url_filter"]) -> None: ...
global___GetAnswerRequest = GetAnswerRequest

class GetAnswerResponse(google.protobuf.message.Message):
    """The response message containing the greetings"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    QUERY_RESULT_FIELD_NUMBER: builtins.int
    @property
    def query_result(self) -> ondewo.nlu.session_pb2.DetectIntentResponse:
        """The results of the conversational query or event processing."""
        pass
    def __init__(self,
        *,
        query_result: typing.Optional[ondewo.nlu.session_pb2.DetectIntentResponse] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["query_result",b"query_result"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["query_result",b"query_result"]) -> None: ...
global___GetAnswerResponse = GetAnswerResponse

class RunScraperRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    PROJECT_IDS_FIELD_NUMBER: builtins.int
    @property
    def project_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
        """List of project_ids"""
        pass
    def __init__(self,
        *,
        project_ids: typing.Optional[typing.Iterable[typing.Text]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["project_ids",b"project_ids"]) -> None: ...
global___RunScraperRequest = RunScraperRequest

class RunScraperResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class ScraperContainer(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        CONTAINER_NAME_FIELD_NUMBER: builtins.int
        CONTAINER_ID_FIELD_NUMBER: builtins.int
        container_name: typing.Text
        """Name of the docker container that is running the job"""

        container_id: typing.Text
        """ID of the docker container that is running the scraping job"""

        def __init__(self,
            *,
            container_name: typing.Text = ...,
            container_id: typing.Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["container_id",b"container_id","container_name",b"container_name"]) -> None: ...

    SCRAPER_CONTAINERS_FIELD_NUMBER: builtins.int
    @property
    def scraper_containers(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___RunScraperResponse.ScraperContainer]: ...
    def __init__(self,
        *,
        scraper_containers: typing.Optional[typing.Iterable[global___RunScraperResponse.ScraperContainer]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["scraper_containers",b"scraper_containers"]) -> None: ...
global___RunScraperResponse = RunScraperResponse

class RunTrainingResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    F1_FIELD_NUMBER: builtins.int
    ACCURACY_FIELD_NUMBER: builtins.int
    f1: builtins.float
    """Response message of training"""

    accuracy: builtins.float
    """accuracy"""

    def __init__(self,
        *,
        f1: builtins.float = ...,
        accuracy: builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["accuracy",b"accuracy","f1",b"f1"]) -> None: ...
global___RunTrainingResponse = RunTrainingResponse

class UrlFilter(google.protobuf.message.Message):
    """Filters with URLs should be included and excluded from the scraping process"""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ALLOWED_VALUES_FIELD_NUMBER: builtins.int
    REGEX_FILTER_INCLUDE_FIELD_NUMBER: builtins.int
    REGEX_FILTER_EXCLUDE_FIELD_NUMBER: builtins.int
    @property
    def allowed_values(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
        """Optional. List of values that the metadata_field 'url' is allowed to take."""
        pass
    regex_filter_include: typing.Text
    """Optional. Regular expression which must be matched by the meta data."""

    regex_filter_exclude: typing.Text
    """Optional. Regular expression which must not be matched by the meta data."""

    def __init__(self,
        *,
        allowed_values: typing.Optional[typing.Iterable[typing.Text]] = ...,
        regex_filter_include: typing.Text = ...,
        regex_filter_exclude: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["allowed_values",b"allowed_values","regex_filter_exclude",b"regex_filter_exclude","regex_filter_include",b"regex_filter_include"]) -> None: ...
global___UrlFilter = UrlFilter

class GetServerStateResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    SERVER_IS_READY_FIELD_NUMBER: builtins.int
    server_is_ready: builtins.bool
    """Whether or not the server is ready to accept requests"""

    def __init__(self,
        *,
        server_is_ready: builtins.bool = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["server_is_ready",b"server_is_ready"]) -> None: ...
global___GetServerStateResponse = GetServerStateResponse

class ListProjectIdsResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    PROJECT_IDS_FIELD_NUMBER: builtins.int
    @property
    def project_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]: ...
    def __init__(self,
        *,
        project_ids: typing.Optional[typing.Iterable[typing.Text]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["project_ids",b"project_ids"]) -> None: ...
global___ListProjectIdsResponse = ListProjectIdsResponse

class GetProjectConfigRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    PROJECT_ID_FIELD_NUMBER: builtins.int
    project_id: typing.Text
    def __init__(self,
        *,
        project_id: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["project_id",b"project_id"]) -> None: ...
global___GetProjectConfigRequest = GetProjectConfigRequest

class GetProjectConfigResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    CONFIG_SERIALIZED_FIELD_NUMBER: builtins.int
    config_serialized: typing.Text
    def __init__(self,
        *,
        config_serialized: typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["config_serialized",b"config_serialized"]) -> None: ...
global___GetProjectConfigResponse = GetProjectConfigResponse

class UpdateDatabaseRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    PROJECT_IDS_FIELD_NUMBER: builtins.int
    @property
    def project_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
        """List of project_ids of which to update the database"""
        pass
    def __init__(self,
        *,
        project_ids: typing.Optional[typing.Iterable[typing.Text]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["project_ids",b"project_ids"]) -> None: ...
global___UpdateDatabaseRequest = UpdateDatabaseRequest

class UpdateDatabaseResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    ERROR_MESSAGES_FIELD_NUMBER: builtins.int
    @property
    def error_messages(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]: ...
    def __init__(self,
        *,
        error_messages: typing.Optional[typing.Iterable[typing.Text]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["error_messages",b"error_messages"]) -> None: ...
global___UpdateDatabaseResponse = UpdateDatabaseResponse
