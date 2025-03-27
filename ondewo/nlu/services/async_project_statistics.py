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
from ondewo.nlu.common_pb2 import StatResponse
from ondewo.nlu.core.async_services_interface import AsyncServicesInterface
from ondewo.nlu.project_statistics_pb2 import (
    GetEntityTypeCountRequest,
    GetIntentCountRequest,
    GetProjectElementStatRequest,
    GetProjectStatRequest,
)
from ondewo.nlu.project_statistics_pb2_grpc import ProjectStatisticsStub


class ProjectStatistics(AsyncServicesInterface):
    """
    Exposes the project-statistics-related endpoints of ONDEWO NLU services in a user-friendly way.

    See project_statistics.proto.
    """

    @property
    def stub(self) -> ProjectStatisticsStub:
        stub: ProjectStatisticsStub = ProjectStatisticsStub(channel=self.grpc_channel)
        return stub

    async def get_intent_count(self, request: GetIntentCountRequest) -> StatResponse:
        response: StatResponse = await self.stub.GetIntentCount(request, metadata=self.metadata)
        return response

    async def get_entity_type_count(self, request: GetEntityTypeCountRequest) -> StatResponse:
        response: StatResponse = await self.stub.GetEntityTypeCount(request, metadata=self.metadata)
        return response

    async def get_user_count(self, request: GetProjectStatRequest) -> StatResponse:
        response: StatResponse = await self.stub.GetUserCount(request, metadata=self.metadata)
        return response

    async def get_session_count(self, request: GetProjectStatRequest) -> StatResponse:
        response: StatResponse = await self.stub.GetSessionCount(request, metadata=self.metadata)
        return response

    async def get_training_phrase_count(self, request: GetProjectElementStatRequest) -> StatResponse:
        response: StatResponse = await self.stub.GetTrainingPhraseCount(request, metadata=self.metadata)
        return response

    async def get_response_count(self, request: GetProjectElementStatRequest) -> StatResponse:
        response: StatResponse = await self.stub.GetResponseCount(request, metadata=self.metadata)
        return response

    async def get_entity_value_count(self, request: GetProjectElementStatRequest) -> StatResponse:
        response: StatResponse = await self.stub.GetEntityValueCount(request, metadata=self.metadata)
        return response

    async def get_entity_synonym_count(self, request: GetProjectElementStatRequest) -> StatResponse:
        response: StatResponse = await self.stub.GetEntitySynonymCount(request, metadata=self.metadata)
        return response
