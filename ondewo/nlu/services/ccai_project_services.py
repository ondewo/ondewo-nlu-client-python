# Copyright 2021-2023 ONDEWO GmbH
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

from nlu import ccai_project_pb2
from nlu.ccai_project_pb2_grpc import CcaiProjectsStub
from ondewo.nlu.core.services_interface import ServicesInterface


class CcaiProjectServices(ServicesInterface):
    """
    Exposes the ai-services-related endpoints of ONDEWO NLU services in a user-friendly way.

    See aiservices.proto.
    """

    @property
    def stub(self) -> CcaiProjectsStub:
        stub: CcaiProjectsStub = CcaiProjectsStub(channel=self.grpc_channel)
        return stub

    def create_ccai_project(
        self,
        request: ccai_project_pb2.CreateCcaiProjectRequest
    ) -> ccai_project_pb2.CreateCcaiProjectResponse:
        """
        Create a new CcaiProject.

        Args:
            request (ccai_project_pb2.CreateCcaiProjectRequest): The request message to create a new CcaiProject.

        Returns:
            ccai_project_pb2.CreateCcaiProjectResponse: The response message containing the details of the created CcaiProject.
        """
        return self.stub.CreateCcaiProject(request=request)

    def get_ccai_project(
        self,
        request: ccai_project_pb2.GetCcaiProjectRequest
    ) -> ccai_project_pb2.CcaiProject:
        """
        Get details of a specific CcaiProject.

        Args:
            request (ccai_project_pb2.GetCcaiProjectRequest): The request message to get details of a CcaiProject.

        Returns:
            ccai_project_pb2.CcaiProject: The response message containing the details of the specified CcaiProject.
        """
        return self.stub.GetCcaiProject(request=request)

    def update_ccai_project(
        self,
        request: ccai_project_pb2.UpdateCcaiProjectRequest
    ) -> ccai_project_pb2.UpdateCcaiProjectResponse:
        """
        Update an existing CcaiProject.

        Args:
            request (ccai_project_pb2.UpdateCcaiProjectRequest): The request message to update an existing CcaiProject.

        Returns:
            ccai_project_pb2.UpdateCcaiProjectResponse: The response message containing the details of the updated CcaiProject.
        """
        return self.stub.UpdateCcaiProject(request=request)

    def delete_ccai_project(
        self,
        request: ccai_project_pb2.DeleteCcaiProjectRequest
    ) -> ccai_project_pb2.DeleteCcaiProjectResponse:
        """
        Delete an existing CcaiProject.

        Args:
            request (ccai_project_pb2.DeleteCcaiProjectRequest): The request message to delete an existing CcaiProject.

        Returns:
            ccai_project_pb2.DeleteCcaiProjectResponse: The response message containing the details of the deleted CcaiProject.
        """
        return self.stub.DeleteCcaiProject(request=request)

    # def deploy_ccai_project(
    #     self,
    #     request: ccai_project_pb2.DeployCcaiProjectRequest
    # ) -> ccai_project_pb2.DeployCcaiProjectResponse:
    #     """
    #     Deploy a CcaiProject.
    #
    #     Args:
    #         request (ccai_project_pb2.DeployCcaiProjectRequest): The request message to deploy a CcaiProject.
    #
    #     Returns:
    #         ccai_project_pb2.DeployCcaiProjectResponse: The response message containing the details of the
    #          deployed CcaiProject.
    #     """
    #     return self.stub.DeployCcaiProject(request=request)
    #
    # def undeploy_ccai_project(
    #     self,
    #     request: ccai_project_pb2.UndeployCcaiProjectRequest
    # ) -> ccai_project_pb2.UndeployCcaiProjectResponse:
    #     """
    #     Undeploy a CcaiProject.
    #
    #     Args:
    #         request (ccai_project_pb2.UndeployCcaiProjectRequest): The request message to undeploy a CcaiProject.
    #
    #     Returns:
    #         ccai_project_pb2.UndeployCcaiProjectResponse: The response message containing the details
    #         of the undeployed CcaiProject.
    #     """
    #     return self.stub.UndeployCcaiProject(request=request)

    def list_ccai_projects(
        self,
        request: ccai_project_pb2.ListCcaiProjectsRequest
    ) -> ccai_project_pb2.ListCcaiProjectsResponse:
        """
        List all CcaiProjects.

        Args:
            request (ccai_project_pb2.ListCcaiProjectsRequest): The request message to list all CcaiProjects.

        Returns:
            ccai_project_pb2.ListCcaiProjectsResponse: The response message containing a list of all CcaiProjects.
        """
        return self.stub.ListCcaiProjects(request=request)
