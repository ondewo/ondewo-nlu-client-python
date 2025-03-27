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
from ondewo.nlu.core.async_services_interface import AsyncServicesInterface
from ondewo.nlu.utility_pb2 import (
    AddTrainingPhrasesFromCSVRequest,
    AddTrainingPhrasesRequest,
    AddTrainingPhrasesResponse,
    CleanAllEntityTypesRequest,
    CleanAllEntityTypesResponse,
    CleanAllIntentsRequest,
    CleanAllIntentsResponse,
    CleanEntityTypeRequest,
    CleanEntityTypeResponse,
    CleanIntentRequest,
    CleanIntentResponse,
    ValidateEmbeddedRegexRequest,
    ValidateEmbeddedRegexResponse,
    ValidateRegexRequest,
    ValidateRegexResponse,
)
from ondewo.nlu.utility_pb2_grpc import UtilitiesStub


class Utilities(AsyncServicesInterface):
    """
    Exposes the utilities endpoints of ONDEWO NLU services in a user-friendly way.

    See utility.proto.
    """

    @property
    def stub(self) -> UtilitiesStub:
        stub: UtilitiesStub = UtilitiesStub(channel=self.grpc_channel)
        return stub

    async def validate_regex(self, request: ValidateRegexRequest) -> ValidateRegexResponse:
        response: ValidateRegexResponse = await self.stub.ValidateRegex(request, metadata=self.metadata)
        return response

    async def validate_embedded_regex(self, request: ValidateEmbeddedRegexRequest) -> ValidateEmbeddedRegexResponse:
        response: ValidateEmbeddedRegexResponse = await self.stub.ValidateEmbeddedRegex(request, metadata=self.metadata)
        return response

    async def clean_all_intents(self, request: CleanAllIntentsRequest) -> CleanAllIntentsResponse:
        response: CleanAllIntentsResponse = await self.stub.CleanAllIntents(request, metadata=self.metadata)
        return response

    async def clean_intent(self, request: CleanIntentRequest) -> CleanIntentResponse:
        response: CleanIntentResponse = await self.stub.CleanIntent(request, metadata=self.metadata)
        return response

    async def clean_all_entity_types(self, request: CleanAllEntityTypesRequest) -> CleanAllEntityTypesResponse:
        response: CleanAllEntityTypesResponse = await self.stub.CleanAllEntityTypes(request, metadata=self.metadata)
        return response

    async def clean_entity_type(self, request: CleanEntityTypeRequest) -> CleanEntityTypeResponse:
        response: CleanEntityTypeResponse = await self.stub.CleanEntityType(request, metadata=self.metadata)
        return response

    async def add_training_phrases(self, request: AddTrainingPhrasesRequest) -> AddTrainingPhrasesResponse:
        response: AddTrainingPhrasesResponse = await self.stub.AddTrainingPhrases(request, metadata=self.metadata)
        return response

    async def add_training_phrases_from_csv(
        self,
        request: AddTrainingPhrasesFromCSVRequest,
    ) -> AddTrainingPhrasesResponse:
        response: AddTrainingPhrasesResponse = await self.stub.AddTrainingPhrasesFromCSV(
            request,
            metadata=self.metadata,
        )
        return response
