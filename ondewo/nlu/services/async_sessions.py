# Copyright 2021-2025 ONDEWO GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import Iterator

from google.protobuf.empty_pb2 import Empty

from ondewo.nlu.common_pb2 import Comment
from ondewo.nlu.core.async_services_interface import AsyncServicesInterface
from ondewo.nlu.session_pb2 import (
    AddAudioFilesRequest,
    AddAudioFilesResponse,
    AddSessionCommentRequest,
    AddSessionLabelsRequest,
    AudioFileResource,
    CreateSessionRequest,
    CreateSessionReviewRequest,
    CreateSessionStepRequest,
    DeleteAudioFilesRequest,
    DeleteAudioFilesResponse,
    DeleteSessionCommentsRequest,
    DeleteSessionLabelsRequest,
    DeleteSessionRequest,
    DeleteSessionStepRequest,
    DetectIntentRequest,
    DetectIntentResponse,
    GetAudioFileOfSessionRequest,
    GetAudioFilesRequest,
    GetAudioFilesResponse,
    GetLatestSessionReviewRequest,
    GetSessionRequest,
    GetSessionReviewRequest,
    GetSessionStepRequest,
    ListAccountIdsOfAllSessionsRequest,
    ListAccountIdsResponse,
    ListAudioFilesRequest,
    ListAudioFilesResponse,
    ListDatastreamIdsOfAllSessionsRequest,
    ListDatastreamIdsResponse,
    ListIdentifiedUserIdsOfAllSessionsRequest,
    ListIdentifiedUserIdsResponse,
    ListInputContextsOfAllSessionsRequest,
    ListInputContextsResponse,
    ListLanguageCodesOfAllSessionsRequest,
    ListLanguageCodesResponse,
    ListMatchedEntityTypesOfAllSessionsRequest,
    ListMatchedEntityTypesResponse,
    ListMatchedIntentsOfAllSessionsRequest,
    ListMatchedIntentsResponse,
    ListOriginIdsOfAllSessionsRequest,
    ListOriginIdsResponse,
    ListOutputContextsOfAllSessionsRequest,
    ListOutputContextsResponse,
    ListPlatformsOfAllSessionsRequest,
    ListPlatformsResponse,
    ListPropertyIdsOfAllSessionsRequest,
    ListPropertyIdsResponse,
    ListSessionCommentsRequest,
    ListSessionCommentsResponse,
    ListSessionLabelsOfAllSessionsRequest,
    ListSessionLabelsRequest,
    ListSessionLabelsResponse,
    ListSessionReviewsRequest,
    ListSessionReviewsResponse,
    ListSessionsRequest,
    ListSessionsResponse,
    ListTagsOfAllSessionsRequest,
    ListTagsResponse,
    ListUserIdsOfAllSessionsRequest,
    ListUserIdsResponse,
    Session,
    SessionReview,
    SessionStep,
    StreamingDetectIntentRequest,
    StreamingDetectIntentResponse,
    UpdateSessionCommentsRequest,
    UpdateSessionStepRequest,
)
from ondewo.nlu.session_pb2_grpc import SessionsStub


class Sessions(AsyncServicesInterface):
    """
    Exposes the sessions-related endpoints of ONDEWO NLU services in a user-friendly way.

    See sessions.proto.
    """

    @property
    def stub(self) -> SessionsStub:
        stub: SessionsStub = SessionsStub(channel=self.grpc_channel)
        return stub

    async def detect_intent(self, request: DetectIntentRequest) -> DetectIntentResponse:
        response: DetectIntentResponse = await self.stub.DetectIntent(request, metadata=self.metadata)
        return response

    async def streaming_detect_intent(
        self,
        request_iterator: Iterator[StreamingDetectIntentRequest],
    ) -> Iterator[StreamingDetectIntentResponse]:
        response_iterator: Iterator[StreamingDetectIntentResponse] = await self.stub.StreamingDetectIntent(
            request_iterator=request_iterator,
            metadata=self.metadata,
        )
        return response_iterator

    async def list_sessions(self, request: ListSessionsRequest) -> ListSessionsResponse:
        response: ListSessionsResponse = await self.stub.ListSessions(request, metadata=self.metadata)
        return response

    async def get_session(self, request: GetSessionRequest) -> Session:
        response: Session = await self.stub.GetSession(request, metadata=self.metadata)
        return response

    async def create_session(self, request: CreateSessionRequest) -> Session:
        response: Session = await self.stub.CreateSession(request, metadata=self.metadata)
        return response

    async def create_session_step(self, request: CreateSessionStepRequest) -> SessionStep:
        response: SessionStep = await self.stub.CreateSessionStep(request, metadata=self.metadata)
        return response

    async def get_session_step(self, request: GetSessionStepRequest) -> SessionStep:
        response: SessionStep = await self.stub.GetSessionStep(request, metadata=self.metadata)
        return response

    async def update_session_step(self, request: UpdateSessionStepRequest) -> SessionStep:
        response: SessionStep = await self.stub.UpdateSessionStep(request, metadata=self.metadata)
        return response

    async def delete_session_step(self, request: DeleteSessionStepRequest) -> Empty:
        response: Empty = await self.stub.DeleteSessionStep(request, metadata=self.metadata)
        return response

    async def delete_session(self, request: DeleteSessionRequest) -> Empty:
        response: Empty = await self.stub.DeleteSession(request, metadata=self.metadata)
        return response

    async def list_session_labels(self, request: ListSessionLabelsRequest) -> ListSessionLabelsResponse:
        response: ListSessionLabelsResponse = await self.stub.ListSessionLabels(request, metadata=self.metadata)
        return response

    async def add_session_labels(self, request: AddSessionLabelsRequest) -> Session:
        response: Session = await self.stub.AddSessionLabels(request, metadata=self.metadata)
        return response

    async def delete_session_labels(self, request: DeleteSessionLabelsRequest) -> Session:
        response: Session = await self.stub.DeleteSessionLabels(request, metadata=self.metadata)
        return response

    async def list_session_reviews(self, request: ListSessionReviewsRequest) -> ListSessionReviewsResponse:
        response: ListSessionReviewsResponse = await self.stub.ListSessionReviews(request, metadata=self.metadata)
        return response

    async def get_session_review(self, request: GetSessionReviewRequest) -> SessionReview:
        response: SessionReview = await self.stub.GetSessionReview(request, metadata=self.metadata)
        return response

    async def get_latest_session_review(self, request: GetLatestSessionReviewRequest) -> SessionReview:
        response: SessionReview = await self.stub.GetLatestSessionReview(request, metadata=self.metadata)
        return response

    async def create_session_review(self, request: CreateSessionReviewRequest) -> SessionReview:
        response: SessionReview = await self.stub.CreateSessionReview(request, metadata=self.metadata)
        return response

    # region audio handling for sessions
    async def get_audio_files(self, request: GetAudioFilesRequest) -> GetAudioFilesResponse:
        response: GetAudioFilesResponse = await self.stub.GetAudioFiles(request, metadata=self.metadata)
        return response

    async def add_audio_files(self, request: AddAudioFilesRequest) -> AddAudioFilesResponse:
        response: AddAudioFilesResponse = await self.stub.AddAudioFiles(request, metadata=self.metadata)
        return response

    async def delete_audio_files(self, request: DeleteAudioFilesRequest) -> DeleteAudioFilesResponse:
        response: DeleteAudioFilesResponse = await self.stub.DeleteAudioFiles(request, metadata=self.metadata)
        return response

    async def get_audio_file_of_session(self, request: GetAudioFileOfSessionRequest) -> AudioFileResource:
        response: AudioFileResource = await self.stub.GetAudioFileOfSession(request, metadata=self.metadata)
        return response

    async def list_audio_files(self, request: ListAudioFilesRequest) -> ListAudioFilesResponse:
        response: ListAudioFilesResponse = await self.stub.ListAudioFiles(request, metadata=self.metadata)
        return response

    # endregion audio handling for sessions

    async def list_session_labels_of_all_sessions(
        self, request: ListSessionLabelsOfAllSessionsRequest
    ) -> ListSessionLabelsResponse:
        response: ListSessionLabelsResponse = await self.stub.ListSessionLabelsOfAllSessions(
            request, metadata=self.metadata
        )
        return response

    async def list_language_codes_of_all_sessions(
        self,
        request: ListLanguageCodesOfAllSessionsRequest,
    ) -> ListLanguageCodesResponse:
        response: ListLanguageCodesResponse = await self.stub.ListLanguageCodesOfAllSessions(
            request, metadata=self.metadata
        )
        return response

    async def list_matched_intents_of_all_sessions(
        self,
        request: ListMatchedIntentsOfAllSessionsRequest,
    ) -> ListMatchedIntentsResponse:
        response: ListMatchedIntentsResponse = await self.stub.ListMatchedIntentsOfAllSessions(
            request,
            metadata=self.metadata,
        )
        return response

    async def list_matched_entity_types_of_all_sessions(
        self,
        request: ListMatchedEntityTypesOfAllSessionsRequest,
    ) -> ListMatchedEntityTypesResponse:
        response: ListMatchedEntityTypesResponse = await self.stub.ListMatchedEntityTypesOfAllSessions(
            request,
            metadata=self.metadata,
        )
        return response

    async def list_user_ids_of_all_sessions(self, request: ListUserIdsOfAllSessionsRequest) -> ListUserIdsResponse:
        response: ListUserIdsResponse = await self.stub.ListUserIdsOfAllSessions(request, metadata=self.metadata)
        return response

    async def list_identified_user_ids_of_all_sessions(
        self,
        request: ListIdentifiedUserIdsOfAllSessionsRequest,
    ) -> ListIdentifiedUserIdsResponse:
        response: ListIdentifiedUserIdsResponse = await self.stub.ListIdentifiedUserIdsOfAllSessions(
            request,
            metadata=self.metadata,
        )
        return response

    async def list_tags_of_all_sessions(self, request: ListTagsOfAllSessionsRequest) -> ListTagsResponse:
        response: ListTagsResponse = await self.stub.ListTagsOfAllSessions(request, metadata=self.metadata)
        return response

    async def list_input_contexts_of_all_sessions(
        self,
        request: ListInputContextsOfAllSessionsRequest,
    ) -> ListInputContextsResponse:
        response: ListInputContextsResponse = await self.stub.ListInputContextsOfAllSessions(
            request, metadata=self.metadata
        )
        return response

    async def list_output_contexts_of_all_sessions(
        self,
        request: ListOutputContextsOfAllSessionsRequest,
    ) -> ListOutputContextsResponse:
        response: ListOutputContextsResponse = await self.stub.ListOutputContextsOfAllSessions(
            request,
            metadata=self.metadata,
        )
        return response

    async def list_platforms_of_all_sessions(self, request: ListPlatformsOfAllSessionsRequest) -> ListPlatformsResponse:
        response: ListPlatformsResponse = await self.stub.ListPlatformsOfAllSessions(request, metadata=self.metadata)
        return response

    async def list_account_ids_of_all_sessions(
        self, request: ListAccountIdsOfAllSessionsRequest
    ) -> ListAccountIdsResponse:
        response: ListAccountIdsResponse = await self.stub.ListAccountIdsOfAllSessions(request, metadata=self.metadata)
        return response

    async def list_property_ids_of_all_sessions(
        self,
        request: ListPropertyIdsOfAllSessionsRequest,
    ) -> ListPropertyIdsResponse:
        response: ListPropertyIdsResponse = await self.stub.ListPropertyIdsOfAllSessions(
            request, metadata=self.metadata
        )
        return response

    async def list_datastream_ids_of_all_sessions(
        self,
        request: ListDatastreamIdsOfAllSessionsRequest,
    ) -> ListDatastreamIdsResponse:
        response: ListDatastreamIdsResponse = await self.stub.ListDatastreamIdsOfAllSessions(
            request, metadata=self.metadata
        )
        return response

    async def list_origin_ids_of_all_sessions(
        self, request: ListOriginIdsOfAllSessionsRequest
    ) -> ListOriginIdsResponse:
        response: ListOriginIdsResponse = await self.stub.ListOriginIdsOfAllSessions(request, metadata=self.metadata)
        return response

    async def add_session_comment(self, request: AddSessionCommentRequest) -> Comment:
        response: Comment = await self.stub.AddSessionComment(request, metadata=self.metadata)
        return response

    async def delete_session_comments(self, request: DeleteSessionCommentsRequest) -> Session:
        response: Session = await self.stub.DeleteSessionComments(request, metadata=self.metadata)
        return response

    async def update_session_comments(self, request: UpdateSessionCommentsRequest) -> Session:
        response: Session = await self.stub.UpdateSessionComments(request, metadata=self.metadata)
        return response

    async def list_session_comments(self, request: ListSessionCommentsRequest) -> ListSessionCommentsResponse:
        response: ListSessionCommentsResponse = await self.stub.ListSessionComments(request, metadata=self.metadata)
        return response
