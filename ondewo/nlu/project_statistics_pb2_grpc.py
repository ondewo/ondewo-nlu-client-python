# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from ondewo.nlu import common_pb2 as ondewo_dot_nlu_dot_common__pb2
from ondewo.nlu import project_statistics_pb2 as ondewo_dot_nlu_dot_project__statistics__pb2

GRPC_GENERATED_VERSION = '1.67.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in ondewo/nlu/project_statistics_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ProjectStatisticsStub(object):
    """Project Root Statistics
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetIntentCount = channel.unary_unary(
                '/ondewo.nlu.ProjectStatistics/GetIntentCount',
                request_serializer=ondewo_dot_nlu_dot_project__statistics__pb2.GetIntentCountRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_common__pb2.StatResponse.FromString,
                _registered_method=True)
        self.GetEntityTypeCount = channel.unary_unary(
                '/ondewo.nlu.ProjectStatistics/GetEntityTypeCount',
                request_serializer=ondewo_dot_nlu_dot_project__statistics__pb2.GetEntityTypeCountRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_common__pb2.StatResponse.FromString,
                _registered_method=True)
        self.GetUserCount = channel.unary_unary(
                '/ondewo.nlu.ProjectStatistics/GetUserCount',
                request_serializer=ondewo_dot_nlu_dot_project__statistics__pb2.GetProjectStatRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_common__pb2.StatResponse.FromString,
                _registered_method=True)
        self.GetSessionCount = channel.unary_unary(
                '/ondewo.nlu.ProjectStatistics/GetSessionCount',
                request_serializer=ondewo_dot_nlu_dot_project__statistics__pb2.GetProjectStatRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_common__pb2.StatResponse.FromString,
                _registered_method=True)
        self.GetTrainingPhraseCount = channel.unary_unary(
                '/ondewo.nlu.ProjectStatistics/GetTrainingPhraseCount',
                request_serializer=ondewo_dot_nlu_dot_project__statistics__pb2.GetProjectElementStatRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_common__pb2.StatResponse.FromString,
                _registered_method=True)
        self.GetResponseCount = channel.unary_unary(
                '/ondewo.nlu.ProjectStatistics/GetResponseCount',
                request_serializer=ondewo_dot_nlu_dot_project__statistics__pb2.GetProjectElementStatRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_common__pb2.StatResponse.FromString,
                _registered_method=True)
        self.GetEntityValueCount = channel.unary_unary(
                '/ondewo.nlu.ProjectStatistics/GetEntityValueCount',
                request_serializer=ondewo_dot_nlu_dot_project__statistics__pb2.GetProjectElementStatRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_common__pb2.StatResponse.FromString,
                _registered_method=True)
        self.GetEntitySynonymCount = channel.unary_unary(
                '/ondewo.nlu.ProjectStatistics/GetEntitySynonymCount',
                request_serializer=ondewo_dot_nlu_dot_project__statistics__pb2.GetProjectElementStatRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_common__pb2.StatResponse.FromString,
                _registered_method=True)


class ProjectStatisticsServicer(object):
    """Project Root Statistics
    """

    def GetIntentCount(self, request, context):
        """Returns the intent count within a project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetEntityTypeCount(self, request, context):
        """Returns the entity types count within a project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUserCount(self, request, context):
        """Returns the users count within a project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSessionCount(self, request, context):
        """Returns the sessions count within a project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTrainingPhraseCount(self, request, context):
        """Returns the training phrases count within a project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetResponseCount(self, request, context):
        """Returns the responses count within a project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetEntityValueCount(self, request, context):
        """Returns the entity value count within a project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetEntitySynonymCount(self, request, context):
        """Returns the entity synonyms count within a project
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ProjectStatisticsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetIntentCount': grpc.unary_unary_rpc_method_handler(
                    servicer.GetIntentCount,
                    request_deserializer=ondewo_dot_nlu_dot_project__statistics__pb2.GetIntentCountRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_common__pb2.StatResponse.SerializeToString,
            ),
            'GetEntityTypeCount': grpc.unary_unary_rpc_method_handler(
                    servicer.GetEntityTypeCount,
                    request_deserializer=ondewo_dot_nlu_dot_project__statistics__pb2.GetEntityTypeCountRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_common__pb2.StatResponse.SerializeToString,
            ),
            'GetUserCount': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUserCount,
                    request_deserializer=ondewo_dot_nlu_dot_project__statistics__pb2.GetProjectStatRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_common__pb2.StatResponse.SerializeToString,
            ),
            'GetSessionCount': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSessionCount,
                    request_deserializer=ondewo_dot_nlu_dot_project__statistics__pb2.GetProjectStatRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_common__pb2.StatResponse.SerializeToString,
            ),
            'GetTrainingPhraseCount': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTrainingPhraseCount,
                    request_deserializer=ondewo_dot_nlu_dot_project__statistics__pb2.GetProjectElementStatRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_common__pb2.StatResponse.SerializeToString,
            ),
            'GetResponseCount': grpc.unary_unary_rpc_method_handler(
                    servicer.GetResponseCount,
                    request_deserializer=ondewo_dot_nlu_dot_project__statistics__pb2.GetProjectElementStatRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_common__pb2.StatResponse.SerializeToString,
            ),
            'GetEntityValueCount': grpc.unary_unary_rpc_method_handler(
                    servicer.GetEntityValueCount,
                    request_deserializer=ondewo_dot_nlu_dot_project__statistics__pb2.GetProjectElementStatRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_common__pb2.StatResponse.SerializeToString,
            ),
            'GetEntitySynonymCount': grpc.unary_unary_rpc_method_handler(
                    servicer.GetEntitySynonymCount,
                    request_deserializer=ondewo_dot_nlu_dot_project__statistics__pb2.GetProjectElementStatRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_common__pb2.StatResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ondewo.nlu.ProjectStatistics', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('ondewo.nlu.ProjectStatistics', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ProjectStatistics(object):
    """Project Root Statistics
    """

    @staticmethod
    def GetIntentCount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ondewo.nlu.ProjectStatistics/GetIntentCount',
            ondewo_dot_nlu_dot_project__statistics__pb2.GetIntentCountRequest.SerializeToString,
            ondewo_dot_nlu_dot_common__pb2.StatResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetEntityTypeCount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ondewo.nlu.ProjectStatistics/GetEntityTypeCount',
            ondewo_dot_nlu_dot_project__statistics__pb2.GetEntityTypeCountRequest.SerializeToString,
            ondewo_dot_nlu_dot_common__pb2.StatResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetUserCount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ondewo.nlu.ProjectStatistics/GetUserCount',
            ondewo_dot_nlu_dot_project__statistics__pb2.GetProjectStatRequest.SerializeToString,
            ondewo_dot_nlu_dot_common__pb2.StatResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetSessionCount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ondewo.nlu.ProjectStatistics/GetSessionCount',
            ondewo_dot_nlu_dot_project__statistics__pb2.GetProjectStatRequest.SerializeToString,
            ondewo_dot_nlu_dot_common__pb2.StatResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetTrainingPhraseCount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ondewo.nlu.ProjectStatistics/GetTrainingPhraseCount',
            ondewo_dot_nlu_dot_project__statistics__pb2.GetProjectElementStatRequest.SerializeToString,
            ondewo_dot_nlu_dot_common__pb2.StatResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetResponseCount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ondewo.nlu.ProjectStatistics/GetResponseCount',
            ondewo_dot_nlu_dot_project__statistics__pb2.GetProjectElementStatRequest.SerializeToString,
            ondewo_dot_nlu_dot_common__pb2.StatResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetEntityValueCount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ondewo.nlu.ProjectStatistics/GetEntityValueCount',
            ondewo_dot_nlu_dot_project__statistics__pb2.GetProjectElementStatRequest.SerializeToString,
            ondewo_dot_nlu_dot_common__pb2.StatResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetEntitySynonymCount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ondewo.nlu.ProjectStatistics/GetEntitySynonymCount',
            ondewo_dot_nlu_dot_project__statistics__pb2.GetProjectElementStatRequest.SerializeToString,
            ondewo_dot_nlu_dot_common__pb2.StatResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
