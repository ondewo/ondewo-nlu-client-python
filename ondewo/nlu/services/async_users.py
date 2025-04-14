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

from ondewo.nlu.common_pb2 import (
    ListNotificationsRequest,
    ListNotificationsResponse,
    SetNotificationsFlaggedStatusRequest,
    SetNotificationsReadStatusRequest,
)
from ondewo.nlu.core.async_services_interface import AsyncServicesInterface
from ondewo.nlu.user_pb2 import (
    CreateServerRoleRequest,
    CreateUserRequest,
    DeleteAllUserPreferencesRequest,
    DeleteServerRoleRequest,
    DeleteUserPreferencesRequest,
    DeleteUserPreferencesResponse,
    GetServerRoleRequest,
    GetUserPreferencesRequest,
    GetUserPreferencesResponse,
    GetUserRequest,
    ListServerPermissionsRequest,
    ListServerPermissionsResponse,
    ListServerRolesRequest,
    ListServerRolesResponse,
    ListUserInfosResponse,
    ListUsersRequest,
    ListUsersResponse,
    LoginRequest,
    LoginResponse,
    ServerRole,
    SetUserPreferencesRequest,
    SetUserPreferencesResponse,
    UpdateServerRoleRequest,
    UpdateUserRequest,
    User,
    UserInfo,
)
from ondewo.nlu.user_pb2_grpc import UsersStub


class Users(AsyncServicesInterface):
    """
    Exposes the user-related endpoints of ONDEWO NLU services in a user-friendly way.

    See user.proto.
    """

    @property
    def stub(self) -> UsersStub:
        stub: UsersStub = UsersStub(channel=self.grpc_channel)
        return stub

    async def create_user(self, request: CreateUserRequest) -> User:
        response: User = await self.stub.CreateUser(request, metadata=self.metadata)
        return response

    async def get_user(self, request: GetUserRequest) -> User:
        response: User = await self.stub.GetUser(request, metadata=self.metadata)
        return response

    async def get_user_info(self, request: GetUserRequest) -> UserInfo:
        response: UserInfo = await self.stub.GetUserInfo(request, metadata=self.metadata)
        return response

    async def delete_user(self, request: GetUserRequest) -> Empty:
        response: Empty = await self.stub.DeleteUser(request, metadata=self.metadata)
        return response

    async def update_user(self, request: UpdateUserRequest) -> User:
        response: User = await self.stub.UpdateUser(request, metadata=self.metadata)
        return response

    async def list_users(self, request: ListUsersRequest) -> ListUsersResponse:
        response: ListUsersResponse = await self.stub.ListUsers(request, metadata=self.metadata)
        return response

    async def list_user_infos(self, request: ListUsersRequest) -> ListUserInfosResponse:
        response: ListUserInfosResponse = await self.stub.ListUserInfos(request, metadata=self.metadata)
        return response

    async def create_server_role(self, request: CreateServerRoleRequest) -> ServerRole:
        response: ServerRole = await self.stub.CreateServerRole(request, metadata=self.metadata)
        return response

    async def get_server_role(self, request: GetServerRoleRequest) -> ServerRole:
        response: ServerRole = await self.stub.GetServerRole(request, metadata=self.metadata)
        return response

    async def delete_server_role(self, request: DeleteServerRoleRequest) -> Empty:
        response: Empty = await self.stub.DeleteServerRole(request, metadata=self.metadata)
        return response

    async def update_server_role(self, request: UpdateServerRoleRequest) -> ServerRole:
        response: ServerRole = await self.stub.UpdateServerRole(request, metadata=self.metadata)
        return response

    async def list_server_roles(self, request: ListServerRolesRequest) -> ListServerRolesResponse:
        response: ListServerRolesResponse = await self.stub.ListServerRoles(request, metadata=self.metadata)
        return response

    async def list_server_permissions(self, request: ListServerPermissionsRequest) -> ListServerPermissionsResponse:
        response: ListServerPermissionsResponse = await self.stub.ListServerPermissions(request, metadata=self.metadata)
        return response

    async def login(self, request: LoginRequest) -> LoginResponse:
        response: LoginResponse = await self.stub.Login(request, metadata=self.metadata)
        return response

    async def check_login(self) -> Empty:
        response: Empty = await self.stub.CheckLogin(Empty(), metadata=self.metadata)
        return response

    # region notifications
    async def list_notifications(self, request: ListNotificationsRequest) -> ListNotificationsResponse:
        response: ListNotificationsResponse = await self.stub.ListNotifications(request, metadata=self.metadata)
        return response

    async def set_notifications_flagged_status(
        self,
        request: SetNotificationsFlaggedStatusRequest,
    ) -> ListNotificationsResponse:
        response: ListNotificationsResponse = await self.stub.SetNotificationsFlaggedStatus(
            request, metadata=self.metadata
        )
        return response

    async def set_notifications_read_status(
        self,
        request: SetNotificationsReadStatusRequest,
    ) -> ListNotificationsResponse:
        response: ListNotificationsResponse = await self.stub.SetNotificationsReadStatus(
            request, metadata=self.metadata
        )
        return response

    # endregion notifications

    # region user preferences
    async def get_user_preferences(self, request: GetUserPreferencesRequest) -> GetUserPreferencesResponse:
        response: GetUserPreferencesResponse = await self.stub.GetUserPreferences(request, metadata=self.metadata)
        return response

    async def set_user_preferences(self, request: SetUserPreferencesRequest) -> SetUserPreferencesResponse:
        response: SetUserPreferencesResponse = await self.stub.SetUserPreferences(request, metadata=self.metadata)
        return response

    async def delete_user_preferences(self, request: DeleteUserPreferencesRequest) -> DeleteUserPreferencesResponse:
        response: DeleteUserPreferencesResponse = await self.stub.DeleteUserPreferences(request, metadata=self.metadata)
        return response

    async def delete_all_user_preferences(
        self, request: DeleteAllUserPreferencesRequest
    ) -> DeleteUserPreferencesResponse:
        response: DeleteUserPreferencesResponse = await self.stub.DeleteAllUserPreferences(
            request, metadata=self.metadata
        )
        return response

    # endregion user preferences
