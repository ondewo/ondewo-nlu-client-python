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


from typing import Optional

from google.longrunning import operations_pb2
from google.protobuf.empty_pb2 import Empty

from google.longrunning.operations_grpc_pb2 import OperationsStub
from ondewo.nlu.core.services_interface import ServicesInterface


class Operations(ServicesInterface):
    """
    Exposes the operations-related endpoints of ONDEWO NLU services in a user-friendly way.

    See operations.proto.
    """

    @property
    def stub(self) -> OperationsStub:
        stub: OperationsStub = OperationsStub(channel=self.grpc_channel)
        return stub

    def get_operation(self, request: operations_pb2.GetOperationRequest) -> Optional[operations_pb2.Operation]:
        response: Optional[operations_pb2.Operation] = self.stub.GetOperation(request, metadata=self.metadata)
        return response

    def list_operations(self, request: operations_pb2.ListOperationsRequest) -> operations_pb2.ListOperationsResponse:
        response: operations_pb2.ListOperationsResponse = self.stub.ListOperations(request, metadata=self.metadata)
        return response

    def delete_operation(self, request: operations_pb2.DeleteOperationRequest) -> Empty:
        response: Empty = self.stub.DeleteOperation(request, metadata=self.metadata)
        return response

    def cancel_operation(self, request: operations_pb2.CancelOperationRequest) -> Empty:
        response: Empty = self.stub.CancelOperation(request, metadata=self.metadata)
        return response
