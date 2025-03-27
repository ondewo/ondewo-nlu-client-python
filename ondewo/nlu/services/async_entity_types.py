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
from google.protobuf.empty_pb2 import Empty

from ondewo.nlu.core.async_services_interface import AsyncServicesInterface
from ondewo.nlu.entity_type_pb2 import (
    BatchCreateEntitiesRequest,
    BatchDeleteEntitiesRequest,
    BatchDeleteEntitiesResponse,
    BatchDeleteEntityTypesRequest,
    BatchEntitiesResponse,
    BatchGetEntitiesRequest,
    BatchUpdateEntitiesRequest,
    BatchUpdateEntityTypesRequest,
    CreateEntityRequest,
    CreateEntityTypeRequest,
    DeleteEntityRequest,
    DeleteEntityStatus,
    DeleteEntityTypeRequest,
    EntityType,
    GetEntityRequest,
    GetEntityTypeRequest,
    ListEntitiesRequest,
    ListEntitiesResponse,
    ListEntityTypesRequest,
    ListEntityTypesResponse,
    UpdateEntityRequest,
    UpdateEntityTypeRequest,
)
from ondewo.nlu.entity_type_pb2_grpc import EntityTypesStub
from ondewo.nlu.operations_pb2 import Operation


class EntityTypes(AsyncServicesInterface):
    """
    Exposes the entity=type-related endpoints of ONDEWO NLU services in a user-friendly way.

    See entity_type.proto.
    """

    @property
    def stub(self) -> EntityTypesStub:
        stub: EntityTypesStub = EntityTypesStub(channel=self.grpc_channel)
        return stub

    async def list_entity_types(self, request: ListEntityTypesRequest) -> ListEntityTypesResponse:
        response: ListEntityTypesResponse = await self.stub.ListEntityTypes(request, metadata=self.metadata)
        return response

    async def get_entity_type(self, request: GetEntityTypeRequest) -> EntityType:
        response: EntityType = await self.stub.GetEntityType(request, metadata=self.metadata)
        return response

    async def create_entity_type(self, request: CreateEntityTypeRequest) -> EntityType:
        response: EntityType = await self.stub.CreateEntityType(request, metadata=self.metadata)
        return response

    async def update_entity_type(self, request: UpdateEntityTypeRequest) -> EntityType:
        response: EntityType = await self.stub.UpdateEntityType(request, metadata=self.metadata)
        return response

    async def delete_entity_type(self, request: DeleteEntityTypeRequest) -> Empty:
        response: Empty = await self.stub.DeleteEntityType(request, metadata=self.metadata)
        return response

    async def batch_update_entity_types(self, request: BatchUpdateEntityTypesRequest) -> Operation:
        response: Operation = await self.stub.BatchUpdateEntityTypes(request, metadata=self.metadata)
        return response

    async def batch_delete_entity_types(self, request: BatchDeleteEntityTypesRequest) -> Operation:
        response: Operation = await self.stub.BatchDeleteEntityTypes(request, metadata=self.metadata)
        return response

    async def batch_create_entities(self, request: BatchCreateEntitiesRequest) -> BatchEntitiesResponse:
        response: BatchEntitiesResponse = await self.stub.BatchCreateEntities(request, metadata=self.metadata)
        return response

    async def batch_update_entities(self, request: BatchUpdateEntitiesRequest) -> BatchEntitiesResponse:
        response: BatchEntitiesResponse = await self.stub.BatchUpdateEntities(request, metadata=self.metadata)
        return response

    async def batch_get_entities(self, request: BatchGetEntitiesRequest) -> BatchEntitiesResponse:
        response: BatchEntitiesResponse = await self.stub.BatchUpdateEntities(request, metadata=self.metadata)
        return response

    async def batch_delete_entities(self, request: BatchDeleteEntitiesRequest) -> BatchDeleteEntitiesResponse:
        response: BatchDeleteEntitiesResponse = await self.stub.BatchDeleteEntities(request, metadata=self.metadata)
        return response

    async def list_entities(self, request: ListEntitiesRequest) -> ListEntitiesResponse:
        response: ListEntitiesResponse = await self.stub.ListEntities(request, metadata=self.metadata)
        return response

    async def get_entity(self, request: GetEntityRequest) -> EntityType.Entity:
        response: EntityType.Entity = await self.stub.GetEntity(request, metadata=self.metadata)
        return response

    async def create_entity(self, request: CreateEntityRequest) -> EntityType.Entity:
        response: EntityType.Entity = await self.stub.CreateEntity(request, metadata=self.metadata)
        return response

    async def update_entity(self, request: UpdateEntityRequest) -> EntityType.Entity:
        response: EntityType.Entity = await self.stub.UpdateEntity(request, metadata=self.metadata)
        return response

    async def delete_entity(self, request: DeleteEntityRequest) -> DeleteEntityStatus:
        response: DeleteEntityStatus = await self.stub.DeleteEntity(request, metadata=self.metadata)
        return response
