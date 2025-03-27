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
from google.protobuf import empty_pb2

from ondewo.nlu import (
    intent_pb2,
    operations_pb2,
)
from ondewo.nlu.core.async_services_interface import AsyncServicesInterface
from ondewo.nlu.intent_pb2 import (
    BatchCreateParametersRequest,
    BatchCreateResponseMessagesRequest,
    BatchCreateTrainingPhrasesRequest,
    BatchDeleteParametersRequest,
    BatchDeleteParametersResponse,
    BatchDeleteResponseMessagesRequest,
    BatchDeleteResponseMessagesResponse,
    BatchDeleteTrainingPhrasesRequest,
    BatchDeleteTrainingPhrasesResponse,
    BatchGetParametersRequest,
    BatchGetResponseMessagesRequest,
    BatchGetTrainingPhrasesRequest,
    BatchParametersStatusResponse,
    BatchResponseMessagesStatusResponse,
    BatchTrainingPhrasesStatusResponse,
    BatchUpdateParametersRequest,
    BatchUpdateResponseMessagesRequest,
    BatchUpdateTrainingPhrasesRequest,
    GetAllIntentTagsRequest,
    GetIntentTagsRequest,
    GetIntentTagsResponse,
    IntentTagRequest,
    ListParametersRequest,
    ListParametersResponse,
    ListResponseMessagesRequest,
    ListResponseMessagesResponse,
    ListTrainingPhrasesRequest,
    ListTrainingPhrasesResponse,
    ListTrainingPhrasesofIntentsWithEnrichmentRequest,
    ListTrainingPhrasesofIntentsWithEnrichmentResponse,
)
from ondewo.nlu.intent_pb2_grpc import IntentsStub


class Intents(AsyncServicesInterface):
    """
    Exposes the intent-related endpoints of ONDEWO NLU services in a user-friendly way.

    See intent.proto.
    """

    @property
    def stub(self) -> IntentsStub:
        stub: IntentsStub = IntentsStub(channel=self.grpc_channel)
        return stub

    async def list_intents(self, request: intent_pb2.ListIntentsRequest) -> intent_pb2.ListIntentsResponse:
        response: intent_pb2.ListIntentsResponse = await self.stub.ListIntents(request, metadata=self.metadata)
        return response

    async def get_intent(self, request: intent_pb2.GetIntentRequest) -> intent_pb2.Intent:
        response: intent_pb2.Intent = await self.stub.GetIntent(request, metadata=self.metadata)
        return response

    async def create_intent(self, request: intent_pb2.CreateIntentRequest) -> intent_pb2.Intent:
        response: intent_pb2.Intent = await self.stub.CreateIntent(request, metadata=self.metadata)
        return response

    async def update_intent(self, request: intent_pb2.UpdateIntentRequest) -> intent_pb2.Intent:
        response: intent_pb2.Intent = await self.stub.UpdateIntent(request, metadata=self.metadata)
        return response

    async def delete_intent(self, request: intent_pb2.DeleteIntentRequest) -> empty_pb2.Empty:
        response: empty_pb2.Empty = await self.stub.DeleteIntent(request, metadata=self.metadata)
        return response

    async def batch_update_intents(self, request: intent_pb2.BatchUpdateIntentsRequest) -> operations_pb2.Operation:
        response: operations_pb2.Operation = await self.stub.BatchUpdateIntents(request, metadata=self.metadata)
        return response

    async def batch_delete_intents(self, request: intent_pb2.BatchDeleteIntentsRequest) -> operations_pb2.Operation:
        response: operations_pb2.Operation = await self.stub.BatchDeleteIntents(request, metadata=self.metadata)
        return response

    async def batch_create_training_phrases(
        self, request: BatchCreateTrainingPhrasesRequest
    ) -> BatchTrainingPhrasesStatusResponse:
        response: BatchTrainingPhrasesStatusResponse = await self.stub.BatchCreateTrainingPhrases(
            request, metadata=self.metadata
        )
        return response

    async def batch_get_training_phrases(
        self, request: BatchGetTrainingPhrasesRequest
    ) -> BatchTrainingPhrasesStatusResponse:
        response: BatchTrainingPhrasesStatusResponse = await self.stub.BatchGetTrainingPhrases(
            request, metadata=self.metadata
        )
        return response

    async def batch_update_training_phrases(
        self, request: BatchUpdateTrainingPhrasesRequest
    ) -> BatchTrainingPhrasesStatusResponse:
        response: BatchTrainingPhrasesStatusResponse = await self.stub.BatchUpdateTrainingPhrases(
            request, metadata=self.metadata
        )
        return response

    async def batch_delete_training_phrases(
        self, request: BatchDeleteTrainingPhrasesRequest
    ) -> BatchDeleteTrainingPhrasesResponse:
        response: BatchDeleteTrainingPhrasesResponse = await self.stub.BatchDeleteTrainingPhrases(
            request, metadata=self.metadata
        )
        return response

    async def list_training_phrases(self, request: ListTrainingPhrasesRequest) -> ListTrainingPhrasesResponse:
        response: ListTrainingPhrasesResponse = await self.stub.ListTrainingPhrases(request, metadata=self.metadata)
        return response

    async def list_training_phrases_of_intents_with_enrichment(
        self,
        request: ListTrainingPhrasesofIntentsWithEnrichmentRequest,
    ) -> ListTrainingPhrasesofIntentsWithEnrichmentResponse:
        response: ListTrainingPhrasesofIntentsWithEnrichmentResponse = (
            await self.stub.ListTrainingPhrasesofIntentsWithEnrichment(request, metadata=self.metadata)
        )
        return response

    async def batch_create_response_messages(
        self, request: BatchCreateResponseMessagesRequest
    ) -> BatchResponseMessagesStatusResponse:
        response: BatchResponseMessagesStatusResponse = await self.stub.BatchCreateResponseMessages(
            request,
            metadata=self.metadata,
        )
        return response

    async def batch_get_response_messages(
        self,
        request: BatchGetResponseMessagesRequest,
    ) -> BatchResponseMessagesStatusResponse:
        response: BatchResponseMessagesStatusResponse = await self.stub.BatchGetResponseMessages(
            request, metadata=self.metadata
        )
        return response

    async def batch_update_response_messages(
        self,
        request: BatchUpdateResponseMessagesRequest,
    ) -> BatchResponseMessagesStatusResponse:
        response: BatchResponseMessagesStatusResponse = await self.stub.BatchUpdateResponseMessages(
            request, metadata=self.metadata
        )
        return response

    async def batch_delete_response_messages(
        self,
        request: BatchDeleteResponseMessagesRequest,
    ) -> BatchDeleteResponseMessagesResponse:
        response: BatchDeleteResponseMessagesResponse = await self.stub.BatchDeleteResponseMessages(
            request, metadata=self.metadata
        )
        return response

    async def list_response_messages(self, request: ListResponseMessagesRequest) -> ListResponseMessagesResponse:
        response: ListResponseMessagesResponse = await self.stub.ListResponseMessages(request, metadata=self.metadata)
        return response

    async def batch_create_parameters(self, request: BatchCreateParametersRequest) -> BatchParametersStatusResponse:
        response: BatchParametersStatusResponse = await self.stub.BatchCreateParameters(request, metadata=self.metadata)
        return response

    async def batch_get_parameters(self, request: BatchGetParametersRequest) -> BatchParametersStatusResponse:
        response: BatchParametersStatusResponse = await self.stub.BatchGetParameters(request, metadata=self.metadata)
        return response

    async def batch_update_parameters(self, request: BatchUpdateParametersRequest) -> BatchParametersStatusResponse:
        response: BatchParametersStatusResponse = await self.stub.BatchUpdateParameters(request, metadata=self.metadata)
        return response

    async def batch_delete_parameters(self, request: BatchDeleteParametersRequest) -> BatchDeleteParametersResponse:
        response: BatchDeleteParametersResponse = await self.stub.BatchDeleteParameters(request, metadata=self.metadata)
        return response

    async def list_parameters(self, request: ListParametersRequest) -> ListParametersResponse:
        response: ListParametersResponse = await self.stub.ListParameters(request, metadata=self.metadata)
        return response

    async def tag_intent(self, request: IntentTagRequest) -> empty_pb2.Empty:
        response: empty_pb2.Empty = await self.stub.TagIntent(request, metadata=self.metadata)
        return response

    async def delete_intent_tag(self, request: IntentTagRequest) -> empty_pb2.Empty:
        response: empty_pb2.Empty = await self.stub.DeleteIntentTag(request, metadata=self.metadata)
        return response

    async def get_intent_tags(self, request: GetIntentTagsRequest) -> GetIntentTagsResponse:
        response: GetIntentTagsResponse = await self.stub.GetIntentTags(request, metadata=self.metadata)
        return response

    async def get_all_intent_tags(self, request: GetAllIntentTagsRequest) -> GetIntentTagsResponse:
        response: GetIntentTagsResponse = await self.stub.GetAllIntentTags(request, metadata=self.metadata)
        return response
