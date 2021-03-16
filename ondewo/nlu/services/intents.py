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


from google.longrunning import operations_pb2
from google.protobuf import empty_pb2
from ondewo.nlu import intent_pb2
from ondewo.nlu.intent_pb2_grpc import IntentsStub
from ondewo.nlu.core.services_interface import ServicesInterface


class Intents(ServicesInterface):
    """
    Exposes the intent-related endpoints of ONDEWO NLU services in a user-friendly way.

    See intent.proto.
    """

    @property
    def stub(self) -> IntentsStub:
        stub: IntentsStub = IntentsStub(channel=self.grpc_channel)
        return stub

    def get_intent(self, request: intent_pb2.GetIntentRequest) -> intent_pb2.Intent:
        response: intent_pb2.Intent = self.stub.GetIntent(request, metadata=self.metadata)
        return response

    def list_intents(self, request: intent_pb2.ListIntentsRequest) -> intent_pb2.ListIntentsResponse:
        response: intent_pb2.ListIntentsResponse = self.stub.ListIntents(request, metadata=self.metadata)
        return response

    def create_intent(self, request: intent_pb2.CreateIntentRequest) -> intent_pb2.Intent:
        response: intent_pb2.Intent = self.stub.CreateIntent(request, metadata=self.metadata)
        return response

    def update_intent(self, request: intent_pb2.UpdateIntentRequest) -> intent_pb2.Intent:
        response: intent_pb2.Intent = self.stub.UpdateIntent(request, metadata=self.metadata)
        return response

    def delete_intent(self, request: intent_pb2.DeleteIntentRequest) -> empty_pb2.Empty:
        response: empty_pb2.Empty = self.stub.DeleteIntent(request, metadata=self.metadata)
        return response

    def batch_update_intents(self, request: intent_pb2.BatchUpdateIntentsRequest) -> operations_pb2.Operation:
        response: operations_pb2.Operation = self.stub.BatchUpdateIntents(request, metadata=self.metadata)
        return response

    def batch_delete_intents(self, request: intent_pb2.BatchDeleteIntentsRequest) -> operations_pb2.Operation:
        response: operations_pb2.Operation = self.stub.BatchDeleteIntents(request, metadata=self.metadata)
        return response
