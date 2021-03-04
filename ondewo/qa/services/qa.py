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
