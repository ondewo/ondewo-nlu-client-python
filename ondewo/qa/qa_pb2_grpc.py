# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from ondewo.qa import qa_pb2 as ondewo_dot_qa_dot_qa__pb2


class QAStub(object):
    """///// Services ///////

    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAnswer = channel.unary_unary(
                '/ondewo.qa.QA/GetAnswer',
                request_serializer=ondewo_dot_qa_dot_qa__pb2.GetAnswerRequest.SerializeToString,
                response_deserializer=ondewo_dot_qa_dot_qa__pb2.GetAnswerResponse.FromString,
                )
        self.RunScraper = channel.unary_unary(
                '/ondewo.qa.QA/RunScraper',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=ondewo_dot_qa_dot_qa__pb2.RunScraperResponse.FromString,
                )
        self.RunTraining = channel.unary_unary(
                '/ondewo.qa.QA/RunTraining',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=ondewo_dot_qa_dot_qa__pb2.RunTrainingResponse.FromString,
                )
        self.GetServerState = channel.unary_unary(
                '/ondewo.qa.QA/GetServerState',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=ondewo_dot_qa_dot_qa__pb2.GetServerStateResponse.FromString,
                )
        self.ListProjectIds = channel.unary_unary(
                '/ondewo.qa.QA/ListProjectIds',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=ondewo_dot_qa_dot_qa__pb2.ListProjectIdsResponse.FromString,
                )
        self.GetProjectConfig = channel.unary_unary(
                '/ondewo.qa.QA/GetProjectConfig',
                request_serializer=ondewo_dot_qa_dot_qa__pb2.GetProjectConfigRequest.SerializeToString,
                response_deserializer=ondewo_dot_qa_dot_qa__pb2.GetProjectConfigResponse.FromString,
                )


class QAServicer(object):
    """///// Services ///////

    """

    def GetAnswer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RunScraper(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RunTraining(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetServerState(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListProjectIds(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetProjectConfig(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_QAServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAnswer': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAnswer,
                    request_deserializer=ondewo_dot_qa_dot_qa__pb2.GetAnswerRequest.FromString,
                    response_serializer=ondewo_dot_qa_dot_qa__pb2.GetAnswerResponse.SerializeToString,
            ),
            'RunScraper': grpc.unary_unary_rpc_method_handler(
                    servicer.RunScraper,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=ondewo_dot_qa_dot_qa__pb2.RunScraperResponse.SerializeToString,
            ),
            'RunTraining': grpc.unary_unary_rpc_method_handler(
                    servicer.RunTraining,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=ondewo_dot_qa_dot_qa__pb2.RunTrainingResponse.SerializeToString,
            ),
            'GetServerState': grpc.unary_unary_rpc_method_handler(
                    servicer.GetServerState,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=ondewo_dot_qa_dot_qa__pb2.GetServerStateResponse.SerializeToString,
            ),
            'ListProjectIds': grpc.unary_unary_rpc_method_handler(
                    servicer.ListProjectIds,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=ondewo_dot_qa_dot_qa__pb2.ListProjectIdsResponse.SerializeToString,
            ),
            'GetProjectConfig': grpc.unary_unary_rpc_method_handler(
                    servicer.GetProjectConfig,
                    request_deserializer=ondewo_dot_qa_dot_qa__pb2.GetProjectConfigRequest.FromString,
                    response_serializer=ondewo_dot_qa_dot_qa__pb2.GetProjectConfigResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ondewo.qa.QA', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class QA(object):
    """///// Services ///////

    """

    @staticmethod
    def GetAnswer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.qa.QA/GetAnswer',
            ondewo_dot_qa_dot_qa__pb2.GetAnswerRequest.SerializeToString,
            ondewo_dot_qa_dot_qa__pb2.GetAnswerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RunScraper(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.qa.QA/RunScraper',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ondewo_dot_qa_dot_qa__pb2.RunScraperResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RunTraining(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.qa.QA/RunTraining',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ondewo_dot_qa_dot_qa__pb2.RunTrainingResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetServerState(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.qa.QA/GetServerState',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ondewo_dot_qa_dot_qa__pb2.GetServerStateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListProjectIds(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.qa.QA/ListProjectIds',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ondewo_dot_qa_dot_qa__pb2.ListProjectIdsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetProjectConfig(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.qa.QA/GetProjectConfig',
            ondewo_dot_qa_dot_qa__pb2.GetProjectConfigRequest.SerializeToString,
            ondewo_dot_qa_dot_qa__pb2.GetProjectConfigResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
