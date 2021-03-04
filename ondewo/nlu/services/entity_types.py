from google.protobuf.empty_pb2 import Empty

from google.longrunning.operations_pb2 import Operation
from ondewo.nlu.entity_type_pb2 import ListEntityTypesRequest, ListEntityTypesResponse, GetEntityTypeRequest, \
    EntityType, CreateEntityTypeRequest, UpdateEntityTypeRequest, DeleteEntityTypeRequest, \
    BatchUpdateEntityTypesRequest, BatchDeleteEntityTypesRequest, BatchCreateEntitiesRequest, \
    BatchUpdateEntitiesRequest, BatchDeleteEntitiesRequest
from ondewo.nlu.entity_type_pb2_grpc import EntityTypesStub
from ondewo.nlu.core.services_interface import ServicesInterface


class EntityTypes(ServicesInterface):
    """
    Exposes the entity=type-related endpoints of ONDEWO NLU services in a user-friendly way.

    See entity_type.proto.
    """

    @property
    def stub(self) -> EntityTypesStub:
        stub: EntityTypesStub = EntityTypesStub(channel=self.grpc_channel)
        return stub

    def list_entity_types(self, request: ListEntityTypesRequest) -> ListEntityTypesResponse:
        response: ListEntityTypesResponse = self.stub.ListEntityTypes(request, metadata=self.metadata)
        return response

    def get_entity_type(self, request: GetEntityTypeRequest) -> EntityType:
        response: EntityType = self.stub.GetEntityType(request, metadata=self.metadata)
        return response

    def create_entity_type(self, request: CreateEntityTypeRequest) -> EntityType:
        response: EntityType = self.stub.CreateEntityType(request, metadata=self.metadata)
        return response

    def update_entity_type(self, request: UpdateEntityTypeRequest) -> EntityType:
        response: EntityType = self.stub.UpdateEntityType(request, metadata=self.metadata)
        return response

    def delete_entity_type(self, request: DeleteEntityTypeRequest) -> Empty:
        response: Empty = self.stub.DeleteEntityType(request, metadata=self.metadata)
        return response

    def batch_update_entity_types(self, request: BatchUpdateEntityTypesRequest) -> Operation:
        response: Operation = self.stub.BatchUpdateEntityTypes(request, metadata=self.metadata)
        return response

    def batch_delete_entity_types(self, request: BatchDeleteEntityTypesRequest) -> Operation:
        response: Operation = self.stub.BatchDeleteEntityTypes(request, metadata=self.metadata)
        return response

    def batch_create_entities(self, request: BatchCreateEntitiesRequest) -> Operation:
        response: Operation = self.stub.BatchCreateEntities(request, metadata=self.metadata)
        return response

    def batch_update_entities(self, request: BatchUpdateEntitiesRequest) -> Operation:
        response: Operation = self.stub.BatchUpdateEntities(request, metadata=self.metadata)
        return response

    def batch_delete_entities(self, request: BatchDeleteEntitiesRequest) -> Operation:
        response: Operation = self.stub.BatchDeleteEntities(request, metadata=self.metadata)
        return response
