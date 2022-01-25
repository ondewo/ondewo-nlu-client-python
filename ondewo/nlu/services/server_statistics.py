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
from google.protobuf.empty_pb2 import Empty

from ondewo.nlu.common_pb2 import StatResponse
from ondewo.nlu.core.services_interface import ServicesInterface
from ondewo.nlu.server_statistics_pb2 import GetUserProjectCountRequest
from ondewo.nlu.server_statistics_pb2_grpc import ServerStatisticsStub


class ServerStatistics(ServicesInterface):
    """
    Exposes the server-statistics-related endpoints of ONDEWO NLU services in a user-friendly way.

    See server_statistics.proto.
    """

    @property
    def stub(self) -> ServerStatisticsStub:
        stub: ServerStatisticsStub = ServerStatisticsStub(channel=self.grpc_channel)
        return stub

    def get_project_count(self) -> StatResponse:
        response: StatResponse = self.stub.GetProjectCount(Empty(), metadata=self.metadata)
        return response

    def get_user_project_count(self, request: GetUserProjectCountRequest) -> StatResponse:
        response: StatResponse = self.stub.GetUserProjectCount(request, metadata=self.metadata)
        return response

    def get_user_count(self) -> StatResponse:
        response: StatResponse = self.stub.GetUserCount(Empty(), metadata=self.metadata)
        return response
