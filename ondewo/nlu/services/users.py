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

from ondewo.nlu.core.services_interface import ServicesInterface
from ondewo.nlu.user_pb2 import CreateUserRequest, User, GetUserRequest, UserInfo, UpdateUserRequest, \
    ListUsersRequest, ListUsersResponse, ListUserInfosResponse, CreateServerRoleRequest, ServerRole, \
    GetServerRoleRequest, DeleteServerRoleRequest, UpdateServerRoleRequest, ListServerRolesRequest, \
    ListServerRolesResponse, ListServerPermissionsRequest, ListServerPermissionsResponse, LoginResponse, \
    LoginRequest
from ondewo.nlu.user_pb2_grpc import UsersStub


class Users(ServicesInterface):
    """
    Exposes the user-related endpoints of ONDEWO NLU services in a user-friendly way.

    See user.proto.
    """

    @property
    def stub(self) -> UsersStub:
        stub: UsersStub = UsersStub(channel=self.grpc_channel)
        return stub

    def create_user(self, request: CreateUserRequest) -> User:
        response: User = self.stub.CreateUser(request, metadata=self.metadata)
        return response

    def get_user(self, request: GetUserRequest) -> User:
        response: User = self.stub.GetUser(request, metadata=self.metadata)
        return response

    def get_user_info(self, request: GetUserRequest) -> UserInfo:
        response: UserInfo = self.stub.GetUserInfo(request, metadata=self.metadata)
        return response

    def delete_user(self, request: GetUserRequest) -> Empty:
        response: Empty = self.stub.DeleteUser(request, metadata=self.metadata)
        return response

    def update_user(self, request: UpdateUserRequest) -> User:
        response: User = self.stub.UpdateUser(request, metadata=self.metadata)
        return response

    def list_users(self, request: ListUsersRequest) -> ListUsersResponse:
        response: ListUsersResponse = self.stub.ListUsers(request, metadata=self.metadata)
        return response

    def list_user_infos(self, request: ListUsersRequest) -> ListUserInfosResponse:
        response: ListUserInfosResponse = self.stub.ListUserInfos(request, metadata=self.metadata)
        return response

    def create_server_role(self, request: CreateServerRoleRequest) -> ServerRole:
        response: ServerRole = self.stub.CreateServerRole(request, metadata=self.metadata)
        return response

    def get_server_role(self, request: GetServerRoleRequest) -> ServerRole:
        response: ServerRole = self.stub.GetServerRole(request, metadata=self.metadata)
        return response

    def delete_server_role(self, request: DeleteServerRoleRequest) -> Empty:
        response: Empty = self.stub.DeleteServerRole(request, metadata=self.metadata)
        return response

    def update_server_role(self, request: UpdateServerRoleRequest) -> ServerRole:
        response: ServerRole = self.stub.UpdateServerRole(request, metadata=self.metadata)
        return response

    def list_server_roles(self, request: ListServerRolesRequest) -> ListServerRolesResponse:
        response: ListServerRolesResponse = self.stub.ListServerRoles(request, metadata=self.metadata)
        return response

    def list_server_permissions(self, request: ListServerPermissionsRequest) -> ListServerPermissionsResponse:
        response: ListServerPermissionsResponse = \
            self.stub.ListServerPermissions(request, metadata=self.metadata)
        return response

    def login(self, request: LoginRequest) -> LoginResponse:
        response: LoginResponse = self.stub.Login(request, metadata=self.metadata)
        return response

    def check_login(self) -> Empty:
        response: Empty = self.stub.CheckLogin(Empty(), metadata=self.metadata)
        return response
