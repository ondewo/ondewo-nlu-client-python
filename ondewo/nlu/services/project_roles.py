from google.protobuf.empty_pb2 import Empty

from ondewo.nlu.project_role_pb2 import ProjectRole, CreateProjectRoleRequest, GetProjectRoleRequest, \
    DeleteProjectRoleRequest, UpdateProjectRoleRequest, ListProjectRolesRequest, ListProjectRolesResponse
from ondewo.nlu.project_role_pb2_grpc import ProjectRolesStub
from ondewo.nlu.core.services_interface import ServicesInterface


class ProjectRoles(ServicesInterface):
    """
    Exposes the project-role-related endpoints of ONDEWO NLU services in a user-friendly way.

    See agent.proto.
    """

    @property
    def stub(self) -> ProjectRolesStub:
        stub: ProjectRolesStub = ProjectRolesStub(channel=self.grpc_channel)
        return stub

    def create_project_role(self, request: CreateProjectRoleRequest) -> ProjectRole:
        response: ProjectRole = self.stub.CreateProjectRole(request, metadata=self.metadata)
        return response

    def get_project_role(self, request: GetProjectRoleRequest) -> ProjectRole:
        response: ProjectRole = self.stub.GetProjectRole(request, metadata=self.metadata)
        return response

    def delete_project_role(self, request: DeleteProjectRoleRequest) -> Empty:
        response: Empty = self.stub.DeleteProjectRole(request, metadata=self.metadata)
        return response

    def update_project_role(self, request: UpdateProjectRoleRequest) -> ProjectRole:
        response: ProjectRole = self.stub.UpdateProjectRole(request, metadata=self.metadata)
        return response

    def list_project_roles(self, request: ListProjectRolesRequest) -> ListProjectRolesResponse:
        response: ListProjectRolesResponse = self.stub.ListProjectRoles(request, metadata=self.metadata)
        return response
