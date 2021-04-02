# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.longrunning import operations_pb2 as google_dot_longrunning_dot_operations__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from ondewo.nlu import entity_type_pb2 as ondewo_dot_nlu_dot_entity__type__pb2


class EntityTypesStub(object):
    """Entities are extracted from user input and represent parameters that are
    meaningful to your application. For example, a date range, a proper name
    such as a geographic location or landmark, and so on. Entities represent
    actionable data for your application.

    When you define an entity, you can also include synonyms that all map to
    that entity. For example, "soft drink", "soda", "pop", and so on.

    There are three types of entities:

    *   **System** - entities that are defined by the Dialogflow API for common
    data types such as date, time, currency, and so on. A system entity is
    represented by the `EntityType` type.

    *   **Developer** - entities that are defined by you that represent
    actionable data that is meaningful to your application. For example,
    you could define a `pizza.sauce` entity for red or white pizza sauce,
    a `pizza.cheese` entity for the different types of cheese on a pizza,
    a `pizza.topping` entity for different toppings, and so on. A developer
    entity is represented by the `EntityType` type.

    *   **User** - entities that are built for an individual user such as
    favorites, preferences, playlists, and so on. A user entity is
    represented by the [SessionEntityType][google.cloud.dialogflow.v2.SessionEntityType] type.

    For more information about entity types, see the
    [Dialogflow documentation](https://dialogflow.com/docs/entities).
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListEntityTypes = channel.unary_unary(
                '/ondewo.nlu.EntityTypes/ListEntityTypes',
                request_serializer=ondewo_dot_nlu_dot_entity__type__pb2.ListEntityTypesRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.ListEntityTypesResponse.FromString,
                )
        self.GetEntityType = channel.unary_unary(
                '/ondewo.nlu.EntityTypes/GetEntityType',
                request_serializer=ondewo_dot_nlu_dot_entity__type__pb2.GetEntityTypeRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.EntityType.FromString,
                )
        self.CreateEntityType = channel.unary_unary(
                '/ondewo.nlu.EntityTypes/CreateEntityType',
                request_serializer=ondewo_dot_nlu_dot_entity__type__pb2.CreateEntityTypeRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.EntityType.FromString,
                )
        self.UpdateEntityType = channel.unary_unary(
                '/ondewo.nlu.EntityTypes/UpdateEntityType',
                request_serializer=ondewo_dot_nlu_dot_entity__type__pb2.UpdateEntityTypeRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.EntityType.FromString,
                )
        self.DeleteEntityType = channel.unary_unary(
                '/ondewo.nlu.EntityTypes/DeleteEntityType',
                request_serializer=ondewo_dot_nlu_dot_entity__type__pb2.DeleteEntityTypeRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.BatchUpdateEntityTypes = channel.unary_unary(
                '/ondewo.nlu.EntityTypes/BatchUpdateEntityTypes',
                request_serializer=ondewo_dot_nlu_dot_entity__type__pb2.BatchUpdateEntityTypesRequest.SerializeToString,
                response_deserializer=google_dot_longrunning_dot_operations__pb2.Operation.FromString,
                )
        self.BatchDeleteEntityTypes = channel.unary_unary(
                '/ondewo.nlu.EntityTypes/BatchDeleteEntityTypes',
                request_serializer=ondewo_dot_nlu_dot_entity__type__pb2.BatchDeleteEntityTypesRequest.SerializeToString,
                response_deserializer=google_dot_longrunning_dot_operations__pb2.Operation.FromString,
                )
        self.CreateEntityBatch = channel.unary_unary(
                '/ondewo.nlu.EntityTypes/CreateEntityBatch',
                request_serializer=ondewo_dot_nlu_dot_entity__type__pb2.CreateEntityBatchRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.EntityBatchResponse.FromString,
                )
        self.UpdateEntityBatch = channel.unary_unary(
                '/ondewo.nlu.EntityTypes/UpdateEntityBatch',
                request_serializer=ondewo_dot_nlu_dot_entity__type__pb2.UpdateEntityBatchRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.EntityBatchResponse.FromString,
                )
        self.GetEntityBatch = channel.unary_unary(
                '/ondewo.nlu.EntityTypes/GetEntityBatch',
                request_serializer=ondewo_dot_nlu_dot_entity__type__pb2.GetEntityBatchRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.EntityBatchResponse.FromString,
                )
        self.DeleteEntityBatch = channel.unary_unary(
                '/ondewo.nlu.EntityTypes/DeleteEntityBatch',
                request_serializer=ondewo_dot_nlu_dot_entity__type__pb2.DeleteEntityBatchRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.DeleteEntityBatchResponse.FromString,
                )
        self.ListEntities = channel.unary_unary(
                '/ondewo.nlu.EntityTypes/ListEntities',
                request_serializer=ondewo_dot_nlu_dot_entity__type__pb2.ListEntitiesRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.ListEntitiesResponse.FromString,
                )


class EntityTypesServicer(object):
    """Entities are extracted from user input and represent parameters that are
    meaningful to your application. For example, a date range, a proper name
    such as a geographic location or landmark, and so on. Entities represent
    actionable data for your application.

    When you define an entity, you can also include synonyms that all map to
    that entity. For example, "soft drink", "soda", "pop", and so on.

    There are three types of entities:

    *   **System** - entities that are defined by the Dialogflow API for common
    data types such as date, time, currency, and so on. A system entity is
    represented by the `EntityType` type.

    *   **Developer** - entities that are defined by you that represent
    actionable data that is meaningful to your application. For example,
    you could define a `pizza.sauce` entity for red or white pizza sauce,
    a `pizza.cheese` entity for the different types of cheese on a pizza,
    a `pizza.topping` entity for different toppings, and so on. A developer
    entity is represented by the `EntityType` type.

    *   **User** - entities that are built for an individual user such as
    favorites, preferences, playlists, and so on. A user entity is
    represented by the [SessionEntityType][google.cloud.dialogflow.v2.SessionEntityType] type.

    For more information about entity types, see the
    [Dialogflow documentation](https://dialogflow.com/docs/entities).
    """

    def ListEntityTypes(self, request, context):
        """Returns the list of all entity types in the specified agent.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetEntityType(self, request, context):
        """Retrieves the specified entity type.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateEntityType(self, request, context):
        """Creates an entity type in the specified agent.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateEntityType(self, request, context):
        """Updates the specified entity type.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteEntityType(self, request, context):
        """Deletes the specified entity type.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BatchUpdateEntityTypes(self, request, context):
        """Updates/Creates multiple entity types in the specified agent.

        Operation <response: [BatchUpdateEntityTypesResponse][google.cloud.dialogflow.v2.BatchUpdateEntityTypesResponse],
        metadata: [google.protobuf.Struct][google.protobuf.Struct]>
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BatchDeleteEntityTypes(self, request, context):
        """Deletes entity types in the specified agent.

        Operation <response: [google.protobuf.Empty][google.protobuf.Empty],
        metadata: [google.protobuf.Struct][google.protobuf.Struct]>
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateEntityBatch(self, request, context):
        """Creates an entity value in an entity type.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateEntityBatch(self, request, context):
        """Updates a specific entity value.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetEntityBatch(self, request, context):
        """Gets a specific entity value.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteEntityBatch(self, request, context):
        """Deletes the specified entity value.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListEntities(self, request, context):
        """List entities of an entity type
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_EntityTypesServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListEntityTypes': grpc.unary_unary_rpc_method_handler(
                    servicer.ListEntityTypes,
                    request_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.ListEntityTypesRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_entity__type__pb2.ListEntityTypesResponse.SerializeToString,
            ),
            'GetEntityType': grpc.unary_unary_rpc_method_handler(
                    servicer.GetEntityType,
                    request_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.GetEntityTypeRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_entity__type__pb2.EntityType.SerializeToString,
            ),
            'CreateEntityType': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateEntityType,
                    request_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.CreateEntityTypeRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_entity__type__pb2.EntityType.SerializeToString,
            ),
            'UpdateEntityType': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateEntityType,
                    request_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.UpdateEntityTypeRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_entity__type__pb2.EntityType.SerializeToString,
            ),
            'DeleteEntityType': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteEntityType,
                    request_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.DeleteEntityTypeRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'BatchUpdateEntityTypes': grpc.unary_unary_rpc_method_handler(
                    servicer.BatchUpdateEntityTypes,
                    request_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.BatchUpdateEntityTypesRequest.FromString,
                    response_serializer=google_dot_longrunning_dot_operations__pb2.Operation.SerializeToString,
            ),
            'BatchDeleteEntityTypes': grpc.unary_unary_rpc_method_handler(
                    servicer.BatchDeleteEntityTypes,
                    request_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.BatchDeleteEntityTypesRequest.FromString,
                    response_serializer=google_dot_longrunning_dot_operations__pb2.Operation.SerializeToString,
            ),
            'CreateEntityBatch': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateEntityBatch,
                    request_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.CreateEntityBatchRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_entity__type__pb2.EntityBatchResponse.SerializeToString,
            ),
            'UpdateEntityBatch': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateEntityBatch,
                    request_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.UpdateEntityBatchRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_entity__type__pb2.EntityBatchResponse.SerializeToString,
            ),
            'GetEntityBatch': grpc.unary_unary_rpc_method_handler(
                    servicer.GetEntityBatch,
                    request_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.GetEntityBatchRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_entity__type__pb2.EntityBatchResponse.SerializeToString,
            ),
            'DeleteEntityBatch': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteEntityBatch,
                    request_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.DeleteEntityBatchRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_entity__type__pb2.DeleteEntityBatchResponse.SerializeToString,
            ),
            'ListEntities': grpc.unary_unary_rpc_method_handler(
                    servicer.ListEntities,
                    request_deserializer=ondewo_dot_nlu_dot_entity__type__pb2.ListEntitiesRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_entity__type__pb2.ListEntitiesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ondewo.nlu.EntityTypes', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class EntityTypes(object):
    """Entities are extracted from user input and represent parameters that are
    meaningful to your application. For example, a date range, a proper name
    such as a geographic location or landmark, and so on. Entities represent
    actionable data for your application.

    When you define an entity, you can also include synonyms that all map to
    that entity. For example, "soft drink", "soda", "pop", and so on.

    There are three types of entities:

    *   **System** - entities that are defined by the Dialogflow API for common
    data types such as date, time, currency, and so on. A system entity is
    represented by the `EntityType` type.

    *   **Developer** - entities that are defined by you that represent
    actionable data that is meaningful to your application. For example,
    you could define a `pizza.sauce` entity for red or white pizza sauce,
    a `pizza.cheese` entity for the different types of cheese on a pizza,
    a `pizza.topping` entity for different toppings, and so on. A developer
    entity is represented by the `EntityType` type.

    *   **User** - entities that are built for an individual user such as
    favorites, preferences, playlists, and so on. A user entity is
    represented by the [SessionEntityType][google.cloud.dialogflow.v2.SessionEntityType] type.

    For more information about entity types, see the
    [Dialogflow documentation](https://dialogflow.com/docs/entities).
    """

    @staticmethod
    def ListEntityTypes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.nlu.EntityTypes/ListEntityTypes',
            ondewo_dot_nlu_dot_entity__type__pb2.ListEntityTypesRequest.SerializeToString,
            ondewo_dot_nlu_dot_entity__type__pb2.ListEntityTypesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetEntityType(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.nlu.EntityTypes/GetEntityType',
            ondewo_dot_nlu_dot_entity__type__pb2.GetEntityTypeRequest.SerializeToString,
            ondewo_dot_nlu_dot_entity__type__pb2.EntityType.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateEntityType(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.nlu.EntityTypes/CreateEntityType',
            ondewo_dot_nlu_dot_entity__type__pb2.CreateEntityTypeRequest.SerializeToString,
            ondewo_dot_nlu_dot_entity__type__pb2.EntityType.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateEntityType(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.nlu.EntityTypes/UpdateEntityType',
            ondewo_dot_nlu_dot_entity__type__pb2.UpdateEntityTypeRequest.SerializeToString,
            ondewo_dot_nlu_dot_entity__type__pb2.EntityType.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteEntityType(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.nlu.EntityTypes/DeleteEntityType',
            ondewo_dot_nlu_dot_entity__type__pb2.DeleteEntityTypeRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BatchUpdateEntityTypes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.nlu.EntityTypes/BatchUpdateEntityTypes',
            ondewo_dot_nlu_dot_entity__type__pb2.BatchUpdateEntityTypesRequest.SerializeToString,
            google_dot_longrunning_dot_operations__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BatchDeleteEntityTypes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.nlu.EntityTypes/BatchDeleteEntityTypes',
            ondewo_dot_nlu_dot_entity__type__pb2.BatchDeleteEntityTypesRequest.SerializeToString,
            google_dot_longrunning_dot_operations__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateEntityBatch(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.nlu.EntityTypes/CreateEntityBatch',
            ondewo_dot_nlu_dot_entity__type__pb2.CreateEntityBatchRequest.SerializeToString,
            ondewo_dot_nlu_dot_entity__type__pb2.EntityBatchResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateEntityBatch(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.nlu.EntityTypes/UpdateEntityBatch',
            ondewo_dot_nlu_dot_entity__type__pb2.UpdateEntityBatchRequest.SerializeToString,
            ondewo_dot_nlu_dot_entity__type__pb2.EntityBatchResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetEntityBatch(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.nlu.EntityTypes/GetEntityBatch',
            ondewo_dot_nlu_dot_entity__type__pb2.GetEntityBatchRequest.SerializeToString,
            ondewo_dot_nlu_dot_entity__type__pb2.EntityBatchResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteEntityBatch(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.nlu.EntityTypes/DeleteEntityBatch',
            ondewo_dot_nlu_dot_entity__type__pb2.DeleteEntityBatchRequest.SerializeToString,
            ondewo_dot_nlu_dot_entity__type__pb2.DeleteEntityBatchResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListEntities(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.nlu.EntityTypes/ListEntities',
            ondewo_dot_nlu_dot_entity__type__pb2.ListEntitiesRequest.SerializeToString,
            ondewo_dot_nlu_dot_entity__type__pb2.ListEntitiesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
