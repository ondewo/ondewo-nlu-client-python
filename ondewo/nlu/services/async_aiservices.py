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

from ondewo.nlu.aiservices_pb2 import (
    ClassifyIntentsRequest,
    ClassifyIntentsResponse,
    ExtractEntitiesFuzzyRequest,
    ExtractEntitiesRequest,
    ExtractEntitiesResponse,
    GenerateResponsesRequest,
    GenerateResponsesResponse,
    GenerateUserSaysRequest,
    GenerateUserSaysResponse,
    GetAlternativeSentencesRequest,
    GetAlternativeSentencesResponse,
    GetAlternativeTrainingPhrasesRequest,
    GetAlternativeTrainingPhrasesResponse,
    GetSynonymsRequest,
    GetSynonymsResponse,
    ListLlmModelsRequest,
    ListLlmModelsResponse,
    LlmGenerateRequest,
    LlmGenerateResponse,
    StreamingLlmGenerateResponse,
)
from ondewo.nlu.aiservices_pb2_grpc import AiServicesStub
from ondewo.nlu.core.async_services_interface import AsyncServicesInterface


class AIServices(AsyncServicesInterface):
    """
    Exposes the ai-services-related endpoints of ONDEWO NLU services in a user-friendly way.

    See aiservices.proto.
    """

    @property
    def stub(self) -> AiServicesStub:
        stub: AiServicesStub = AiServicesStub(channel=self.grpc_channel)
        return stub

    async def extract_entities(self, request: ExtractEntitiesRequest) -> ExtractEntitiesResponse:
        response: ExtractEntitiesResponse = await self.stub.ExtractEntities(request, metadata=self.metadata)
        return response

    async def generate_user_says(self, request: GenerateUserSaysRequest) -> GenerateUserSaysResponse:
        response: GenerateUserSaysResponse = await self.stub.GenerateUserSays(request, metadata=self.metadata)
        return response

    async def generate_responses(self, request: GenerateResponsesRequest) -> GenerateResponsesResponse:
        response: GenerateResponsesResponse = await self.stub.GenerateResponses(request, metadata=self.metadata)
        return response

    async def get_alternative_sentences(
        self, request: GetAlternativeSentencesRequest
    ) -> GetAlternativeSentencesResponse:
        response: GetAlternativeSentencesResponse = await self.stub.GetAlternativeSentences(
            request, metadata=self.metadata
        )
        return response

    async def get_alternative_training_phrases(
        self, request: GetAlternativeTrainingPhrasesRequest
    ) -> GetAlternativeTrainingPhrasesResponse:
        response: GetAlternativeTrainingPhrasesResponse = await self.stub.GetAlternativeTrainingPhrases(
            request, metadata=self.metadata
        )
        return response

    async def get_synonyms(self, request: GetSynonymsRequest) -> GetSynonymsResponse:
        response: GetSynonymsResponse = await self.stub.GetSynonyms(request, metadata=self.metadata)
        return response

    async def classify_intents(self, request: ClassifyIntentsRequest) -> ClassifyIntentsResponse:
        response: ClassifyIntentsResponse = await self.stub.ClassifyIntents(request, metadata=self.metadata)
        return response

    async def extract_entities_fuzzy(self, request: ExtractEntitiesFuzzyRequest) -> ExtractEntitiesResponse:
        response: ExtractEntitiesResponse = await self.stub.ExtractEntitiesFuzzy(request, metadata=self.metadata)
        return response

    # region large language model support

    async def llm_generate(self, request: LlmGenerateRequest) -> LlmGenerateResponse:
        response: LlmGenerateResponse = await self.stub.LlmGenerate(request, metadata=self.metadata)
        return response

    async def llm_generate_stream(self, request: LlmGenerateRequest) -> Iterator[StreamingLlmGenerateResponse]:
        response_iterator: Iterator[StreamingLlmGenerateResponse] = await self.stub.StreamingLlmGenerate(
            request=request,
            metadata=self.metadata,
        )
        return response_iterator

    async def list_llm_models(self, request: ListLlmModelsRequest) -> ListLlmModelsResponse:
        response: ListLlmModelsResponse = await self.stub.ListLlmModels(request, metadata=self.metadata)
        return response

    # endregion large language model support
