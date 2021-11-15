# Copyright 2021 ONDEWO GmbH
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

from ondewo.nlu.core.services_interface import ServicesInterface
from ondewo.nlu.session_pb2 import ListSessionsResponse, \
    ListSessionsRequest, DetectIntentResponse, DetectIntentRequest, Session, GetSessionRequest, \
    ListSessionReviewsRequest, ListSessionReviewsResponse, SessionReview, GetLatestSessionReviewRequest, \
    GetSessionReviewRequest, CreateSessionReviewRequest, StreamingDetectIntentRequest, \
    StreamingDetectIntentResponse, TrackSessionStepRequest, DeleteSessionRequest, ListSessionLabelsRequest, \
    ListSessionLabelsResponse, AddSessionLabelsRequest, RemoveSessionLabelsRequest, CreateSessionRequest
from ondewo.nlu.session_pb2_grpc import SessionsStub


class Sessions(ServicesInterface):
    """
    Exposes the sessions-related endpoints of ONDEWO NLU services in a user-friendly way.

    See sessions.proto.
    """

    @property
    def stub(self) -> SessionsStub:
        stub: SessionsStub = SessionsStub(channel=self.grpc_channel)
        return stub

    def detect_intent(self, request: DetectIntentRequest) -> DetectIntentResponse:
        response: DetectIntentResponse = self.stub.DetectIntent(request, metadata=self.metadata)
        return response

    def streaming_detect_intent(
            self,
            request_iterator: Iterator[StreamingDetectIntentRequest],
    ) -> Iterator[StreamingDetectIntentResponse]:
        response_iterator: Iterator[StreamingDetectIntentResponse] = self.stub.StreamingDetectIntent(
            request_iterator, metadata=self.metadata)
        return response_iterator

    def list_sessions(self, request: ListSessionsRequest) -> ListSessionsResponse:
        response: ListSessionsResponse = self.stub.ListSessions(request, metadata=self.metadata)
        return response

    def get_session(self, request: GetSessionRequest) -> Session:
        response: Session = self.stub.GetSession(request, metadata=self.metadata)
        return response

    def create_session(self, request: CreateSessionRequest) -> Session:
        response: Session = self.stub.CreateSession(request, metadata=self.metadata)
        return response

    def track_session_step(self, request: TrackSessionStepRequest) -> Session:
        response: Session = self.stub.TrackSessionStep(request, metadata=self.metadata)
        return response

    def delete_session(self, request: DeleteSessionRequest) -> Empty:
        response: Empty = self.stub.DeleteSession(request, metadata=self.metadata)
        return response

    def list_session_labels(self, request: ListSessionLabelsRequest) -> ListSessionLabelsResponse:
        response: ListSessionLabelsResponse = self.stub.ListSessionLabels(request, metadata=self.metadata)
        return response

    def add_session_labels(self, request: AddSessionLabelsRequest) -> Session:
        response: Session = self.stub.AddSessionLabels(request, metadata=self.metadata)
        return response

    def remove_session_labels(self, request: RemoveSessionLabelsRequest) -> Session:
        response: Session = self.stub.RemoveSessionLabels(request, metadata=self.metadata)
        return response

    def list_session_reviews(self, request: ListSessionReviewsRequest) -> ListSessionReviewsResponse:
        response: ListSessionReviewsResponse = self.stub.ListSessionReviews(request, metadata=self.metadata)
        return response

    def get_session_review(self, request: GetSessionReviewRequest) -> SessionReview:
        response: SessionReview = self.stub.GetSessionReview(request, metadata=self.metadata)
        return response

    def get_latest_session_review(self, request: GetLatestSessionReviewRequest) -> SessionReview:
        response: SessionReview = self.stub.GetLatestSessionReview(request, metadata=self.metadata)
        return response

    def create_session_review(self, request: CreateSessionReviewRequest) -> SessionReview:
        response: SessionReview = self.stub.CreateSessionReview(request, metadata=self.metadata)
        return response
