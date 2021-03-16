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

from ondewo.qa.core.services_interface import ServicesInterface
from ondewo.qa import qa_pb2
from ondewo.qa.qa_pb2_grpc import QAStub


class QA(ServicesInterface):
    """
    Exposes the qa-related endpoints of ONDEWO NLU services in a user-friendly way.

    See qa.proto.
    """

    @property
    def stub(self) -> QAStub:
        stub: QAStub = QAStub(channel=self.grpc_channel)
        return stub

    def get_answer(self, request: qa_pb2.GetAnswerRequest) -> qa_pb2.GetAnswerResponse:
        response: qa_pb2.GetAnswerResponse = self.stub.GetAnswer(request)
        return response

    def run_scraper(self) -> qa_pb2.RunScraperResponse:
        response: qa_pb2.RunScraperResponse = self.stub.RunScraper(Empty())
        return response

    def run_training(self) -> qa_pb2.RunTrainingResponse:
        response: qa_pb2.RunTrainingResponse = self.stub.RunTraining(Empty())
        return response
