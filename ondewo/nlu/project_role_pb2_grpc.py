# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from ondewo.nlu import project_role_pb2 as ondewo_dot_nlu_dot_project__role__pb2


class ProjectRolesStub(object):
    """Project roles
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateProjectRole = channel.unary_unary(
                '/ondewo.nlu.ProjectRoles/CreateProjectRole',
                request_serializer=ondewo_dot_nlu_dot_project__role__pb2.CreateProjectRoleRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_project__role__pb2.ProjectRole.FromString,
                )
        self.GetProjectRole = channel.unary_unary(
                '/ondewo.nlu.ProjectRoles/GetProjectRole',
                request_serializer=ondewo_dot_nlu_dot_project__role__pb2.GetProjectRoleRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_project__role__pb2.ProjectRole.FromString,
                )
        self.DeleteProjectRole = channel.unary_unary(
                '/ondewo.nlu.ProjectRoles/DeleteProjectRole',
                request_serializer=ondewo_dot_nlu_dot_project__role__pb2.DeleteProjectRoleRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.UpdateProjectRole = channel.unary_unary(
                '/ondewo.nlu.ProjectRoles/UpdateProjectRole',
                request_serializer=ondewo_dot_nlu_dot_project__role__pb2.UpdateProjectRoleRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_project__role__pb2.ProjectRole.FromString,
                )
        self.ListProjectRoles = channel.unary_unary(
                '/ondewo.nlu.ProjectRoles/ListProjectRoles',
                request_serializer=ondewo_dot_nlu_dot_project__role__pb2.ListProjectRolesRequest.SerializeToString,
                response_deserializer=ondewo_dot_nlu_dot_project__role__pb2.ListProjectRolesResponse.FromString,
                )


class ProjectRolesServicer(object):
    """Project roles
    """

    def CreateProjectRole(self, request, context):
        """Creates a project role by creating the knowledge base master
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetProjectRole(self, request, context):
        """Creates a project role by getting the knowledge base master
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteProjectRole(self, request, context):
        """Deletes project role
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateProjectRole(self, request, context):
        """Updates project role
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListProjectRoles(self, request, context):
        """List project roles
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ProjectRolesServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateProjectRole': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateProjectRole,
                    request_deserializer=ondewo_dot_nlu_dot_project__role__pb2.CreateProjectRoleRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_project__role__pb2.ProjectRole.SerializeToString,
            ),
            'GetProjectRole': grpc.unary_unary_rpc_method_handler(
                    servicer.GetProjectRole,
                    request_deserializer=ondewo_dot_nlu_dot_project__role__pb2.GetProjectRoleRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_project__role__pb2.ProjectRole.SerializeToString,
            ),
            'DeleteProjectRole': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteProjectRole,
                    request_deserializer=ondewo_dot_nlu_dot_project__role__pb2.DeleteProjectRoleRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'UpdateProjectRole': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateProjectRole,
                    request_deserializer=ondewo_dot_nlu_dot_project__role__pb2.UpdateProjectRoleRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_project__role__pb2.ProjectRole.SerializeToString,
            ),
            'ListProjectRoles': grpc.unary_unary_rpc_method_handler(
                    servicer.ListProjectRoles,
                    request_deserializer=ondewo_dot_nlu_dot_project__role__pb2.ListProjectRolesRequest.FromString,
                    response_serializer=ondewo_dot_nlu_dot_project__role__pb2.ListProjectRolesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ondewo.nlu.ProjectRoles', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ProjectRoles(object):
    """Project roles
    """

    @staticmethod
    def CreateProjectRole(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.nlu.ProjectRoles/CreateProjectRole',
            ondewo_dot_nlu_dot_project__role__pb2.CreateProjectRoleRequest.SerializeToString,
            ondewo_dot_nlu_dot_project__role__pb2.ProjectRole.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetProjectRole(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.nlu.ProjectRoles/GetProjectRole',
            ondewo_dot_nlu_dot_project__role__pb2.GetProjectRoleRequest.SerializeToString,
            ondewo_dot_nlu_dot_project__role__pb2.ProjectRole.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteProjectRole(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.nlu.ProjectRoles/DeleteProjectRole',
            ondewo_dot_nlu_dot_project__role__pb2.DeleteProjectRoleRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateProjectRole(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.nlu.ProjectRoles/UpdateProjectRole',
            ondewo_dot_nlu_dot_project__role__pb2.UpdateProjectRoleRequest.SerializeToString,
            ondewo_dot_nlu_dot_project__role__pb2.ProjectRole.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListProjectRoles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ondewo.nlu.ProjectRoles/ListProjectRoles',
            ondewo_dot_nlu_dot_project__role__pb2.ListProjectRolesRequest.SerializeToString,
            ondewo_dot_nlu_dot_project__role__pb2.ListProjectRolesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
