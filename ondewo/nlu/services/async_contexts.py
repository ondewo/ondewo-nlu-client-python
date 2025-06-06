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
    context_pb2,
    context_pb2_grpc,
)
from ondewo.nlu.core.async_services_interface import AsyncServicesInterface


class Contexts(AsyncServicesInterface):
    """
    Exposes the contexts-related endpoints of ONDEWO NLU services in a user-friendly way.

    See contexts.proto.
    """

    @property
    def stub(self) -> context_pb2_grpc.ContextsStub:
        stub: context_pb2_grpc.ContextsStub = context_pb2_grpc.ContextsStub(channel=self.grpc_channel)
        return stub

    async def list_contexts(self, request: context_pb2.ListContextsRequest) -> context_pb2.ListContextsResponse:
        response: context_pb2.ListContextsResponse = await self.stub.ListContexts(request, metadata=self.metadata)
        return response

    async def get_context(self, request: context_pb2.GetContextRequest) -> context_pb2.Context:
        response: context_pb2.Context = await self.stub.GetContext(request, metadata=self.metadata)
        return response

    async def create_context(self, request: context_pb2.CreateContextRequest) -> context_pb2.Context:
        response: context_pb2.Context = await self.stub.CreateContext(request, metadata=self.metadata)
        return response

    async def update_context(self, request: context_pb2.UpdateContextRequest) -> context_pb2.Context:
        response: context_pb2.Context = await self.stub.UpdateContext(request, metadata=self.metadata)
        return response

    async def delete_context(self, request: context_pb2.DeleteContextRequest) -> empty_pb2.Empty:
        response: empty_pb2.Empty = await self.stub.DeleteContext(request, metadata=self.metadata)
        return response

    async def delete_all_contexts(self, request: context_pb2.DeleteAllContextsRequest) -> empty_pb2.Empty:
        response: empty_pb2.Empty = await self.stub.DeleteAllContexts(request, metadata=self.metadata)
        return response
