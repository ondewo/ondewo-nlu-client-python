from google.protobuf import empty_pb2
from ondewo.nlu import context_pb2_grpc, context_pb2
from ondewo.nlu.core.services_interface import ServicesInterface


class Contexts(ServicesInterface):
    """
    Exposes the contexts-related endpoints of ONDEWO NLU services in a user-friendly way.

    See contexts.proto.
    """

    @property
    def stub(self) -> context_pb2_grpc.ContextsStub:
        stub: context_pb2_grpc.ContextsStub = context_pb2_grpc.ContextsStub(channel=self.grpc_channel)
        return stub

    def list_contexts(self, request: context_pb2.ListContextsRequest) -> context_pb2.ListContextsResponse:
        response: context_pb2.ListContextsResponse = self.stub.ListContexts(request, metadata=self.metadata)
        return response

    def get_context(self, request: context_pb2.GetContextRequest) -> context_pb2.Context:
        response: context_pb2.Context = self.stub.GetContext(request, metadata=self.metadata)
        return response

    def create_context(self, request: context_pb2.CreateContextRequest) -> context_pb2.Context:
        response: context_pb2.Context = self.stub.CreateContext(request, metadata=self.metadata)
        return response

    def update_context(self, request: context_pb2.UpdateContextRequest) -> context_pb2.Context:
        response: context_pb2.Context = self.stub.UpdateContext(request, metadata=self.metadata)
        return response

    def delete_context(self, request: context_pb2.DeleteContextRequest) -> empty_pb2.Empty:
        response: empty_pb2.Empty = self.stub.DeleteContext(request, metadata=self.metadata)
        return response

    def delete_all_contexts(self, request: context_pb2.DeleteAllContextsRequest) -> empty_pb2.Empty:
        response: empty_pb2.Empty = self.stub.DeleteAllContexts(request, metadata=self.metadata)
        return response
