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
