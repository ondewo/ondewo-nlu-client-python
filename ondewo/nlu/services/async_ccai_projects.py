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
from ondewo.nlu.ccai_project_pb2 import (
    CcaiProject,
    CcaiService,
    CreateCcaiProjectRequest,
    CreateCcaiProjectResponse,
    DeleteCcaiProjectRequest,
    DeleteCcaiProjectResponse,
    GetCcaiProjectRequest,
    GetCcaiServiceRequest,
    ListCcaiProjectsRequest,
    ListCcaiProjectsResponse,
    UpdateCcaiProjectRequest,
    UpdateCcaiProjectResponse,
)
from ondewo.nlu.ccai_project_pb2_grpc import CcaiProjectsStub
from ondewo.nlu.core.async_services_interface import AsyncServicesInterface


class CcaiProjects(AsyncServicesInterface):
    """
    Exposes the ccai projects endpoints of ONDEWO NLU services in a user-friendly way.
    See ccai_project.proto.
    """

    @property
    def stub(self) -> CcaiProjectsStub:
        stub: CcaiProjectsStub = CcaiProjectsStub(channel=self.grpc_channel)
        return stub

    async def create_ccai_project(self, request: CreateCcaiProjectRequest) -> CreateCcaiProjectResponse:
        """
        Create a new CcaiProject.

        Args:
            request (CreateCcaiProjectRequest): The request message to create a new CcaiProject.

        Returns:
            CreateCcaiProjectResponse:
                The response message containing the details of the created CcaiProject.
        """
        response: CreateCcaiProjectResponse = await self.stub.CreateCcaiProject(request=request, metadata=self.metadata)
        return response

    async def get_ccai_project(self, request: GetCcaiProjectRequest) -> CcaiProject:
        """
        Get details of a specific CcaiProject.

        Args:
            request (GetCcaiProjectRequest): The request message to get details of a CcaiProject.

        Returns:
            CcaiProject: The response message containing the details of the specified CcaiProject.
        """
        response: CcaiProject = await self.stub.GetCcaiProject(request=request, metadata=self.metadata)
        return response

    async def update_ccai_project(self, request: UpdateCcaiProjectRequest) -> UpdateCcaiProjectResponse:
        """
        Update an existing CcaiProject.

        Args:
            request (UpdateCcaiProjectRequest): The request message to update an existing CcaiProject.

        Returns:
            UpdateCcaiProjectResponse:
                The response message containing the details of the updated CcaiProject.
        """
        response: UpdateCcaiProjectResponse = await self.stub.UpdateCcaiProject(request=request, metadata=self.metadata)
        return response

    async def delete_ccai_project(self, request: DeleteCcaiProjectRequest) -> DeleteCcaiProjectResponse:
        """
        Delete an existing CcaiProject.

        Args:
            request (DeleteCcaiProjectRequest): The request message to delete an existing CcaiProject.

        Returns:
            DeleteCcaiProjectResponse:
                The response message containing the details of the deleted CcaiProject.
        """
        response: DeleteCcaiProjectResponse = await self.stub.DeleteCcaiProject(request=request, metadata=self.metadata)
        return response

    # def deploy_ccai_project(
    #     self,
    #     request: DeployCcaiProjectRequest
    # ) -> DeployCcaiProjectResponse:
    #     """
    #     Deploy a CcaiProject.
    #
    #     Args:
    #         request (DeployCcaiProjectRequest): The request message to deploy a CcaiProject.
    #
    #     Returns:
    #         DeployCcaiProjectResponse: The response message containing the details of the
    #          deployed CcaiProject.
    #     """
    #     return await self.stub.DeployCcaiProject(request=request, metadata=self.metadata)
    #
    # def undeploy_ccai_project(
    #     self,
    #     request: UndeployCcaiProjectRequest
    # ) -> UndeployCcaiProjectResponse:
    #     """
    #     Undeploy a CcaiProject.
    #
    #     Args:
    #         request (UndeployCcaiProjectRequest): The request message to undeploy a CcaiProject.
    #
    #     Returns:
    #         UndeployCcaiProjectResponse: The response message containing the details
    #         of the undeployed CcaiProject.
    #     """
    #     return await self.stub.UndeployCcaiProject(request=request, metadata=self.metadata)

    async def list_ccai_projects(self, request: ListCcaiProjectsRequest) -> ListCcaiProjectsResponse:
        """
        List all CcaiProjects.

        Args:
            request (ListCcaiProjectsRequest): The request message to list all CcaiProjects.

        Returns:
            ListCcaiProjectsResponse: The response message containing a list of all CcaiProjects.
        """
        response: ListCcaiProjectsResponse = await self.stub.ListCcaiProjects(request=request, metadata=self.metadata)
        return response

    async def get_ccai_service(self, request: GetCcaiServiceRequest) -> CcaiService:
        """
        Get details of a specific CcaiService.

        Args:
            request (GetCcaiServiceRequest): The request message to get details of a CcaiService.

        Returns:
            CcaiService: The response message containing the details of the specified CcaiService.
        """
        response: CcaiService = await self.stub.GetCcaiService(request=request, metadata=self.metadata)
        return response
