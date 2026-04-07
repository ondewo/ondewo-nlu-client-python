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
from typing import Iterator

from ondewo.nlu.rag_pb2 import (
    RagAddCrawlerResultsToDatasetsRequest,
    RagCrawler,
    RagCrawlerResult,
    RagCreateCrawlerRequest,
    RagCreateDatasetRequest,
    RagDataset,
    RagDatasetList,
    RagDeleteCrawlerRequest,
    RagDeleteCrawlerResponse,
    RagDeleteCrawlerRunsRequest,
    RagDeleteCrawlerRunsResponse,
    RagDeleteCrawlersRequest,
    RagDeleteCrawlersResponse,
    RagDeleteRequest,
    RagDocument,
    RagDocumentIdsRequest,
    RagDocumentList,
    RagDownloadDocumentRequest,
    RagFileChunk,
    RagGetCrawlerAttachedDatasetsRequest,
    RagGetCrawlerAttachedDatasetsResponse,
    RagGetCrawlerRequest,
    RagGetCrawlerResultRequest,
    RagGetCrawlerResultsRequest,
    RagGetCrawlerResultsResponse,
    RagGetCrawlerRunRequest,
    RagListCrawlerRunsRequest,
    RagListCrawlerRunsResponse,
    RagListCrawlersRequest,
    RagListCrawlersResponse,
    RagListDatasetsRequest,
    RagListDocumentsRequest,
    RagPartialSuccess,
    RagRemoveCrawlerResultsFromDatasetsRequest,
    RagRetrievalRequest,
    RagRetrievalResponse,
    RagStartCrawlerRequest,
    RagStopCrawlerRequest,
    RagStopCrawlerResponse,
    RagUpdateCrawlerRequest,
    RagUpdateDatasetRequest,
    RagUpdateDocumentRequest,
    RagUploadDocumentRequest,
)
from ondewo.nlu.rag_pb2_grpc import RagsStub
from ondewo.nlu.core.services_interface import ServicesInterface
from ondewo.nlu.operations_pb2 import Operation


class Rags(ServicesInterface):
    """
    Exposes the RAG-related endpoints of ONDEWO NLU services in a user-friendly way.

    See rag.proto.
    """

    @property
    def stub(self) -> RagsStub:
        stub: RagsStub = RagsStub(channel=self.grpc_channel)
        return stub

    def rag_create_dataset(self, request: RagCreateDatasetRequest) -> RagDataset:
        response: RagDataset = self.stub.RagCreateDataset(request, metadata=self.metadata)
        return response

    def rag_update_dataset(self, request: RagUpdateDatasetRequest) -> RagDataset:
        response: RagDataset = self.stub.RagUpdateDataset(request, metadata=self.metadata)
        return response

    def rag_delete_datasets(self, request: RagDeleteRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = self.stub.RagDeleteDatasets(request, metadata=self.metadata)
        return response

    def rag_list_datasets(self, request: RagListDatasetsRequest) -> RagDatasetList:
        response: RagDatasetList = self.stub.RagListDatasets(request, metadata=self.metadata)
        return response

    def rag_upload_document(self, request: Iterator[RagUploadDocumentRequest]) -> RagDocument:
        response: RagDocument = self.stub.RagUploadDocument(request, metadata=self.metadata)
        return response

    def rag_update_document(self, request: RagUpdateDocumentRequest) -> RagDocument:
        response: RagDocument = self.stub.RagUpdateDocument(request, metadata=self.metadata)
        return response

    def rag_download_document(self, request: RagDownloadDocumentRequest) -> Iterator[RagFileChunk]:
        response: Iterator[RagFileChunk] = self.stub.RagDownloadDocument(request, metadata=self.metadata)
        return response

    def rag_list_documents(self, request: RagListDocumentsRequest) -> RagDocumentList:
        response: RagDocumentList = self.stub.RagListDocuments(request, metadata=self.metadata)
        return response

    def rag_delete_documents(self, request: RagDocumentIdsRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = self.stub.RagDeleteDocuments(request, metadata=self.metadata)
        return response

    def rag_parse_documents(self, request: RagDocumentIdsRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = self.stub.RagParseDocuments(request, metadata=self.metadata)
        return response

    def rag_stop_parsing(self, request: RagDocumentIdsRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = self.stub.RagStopParsing(request, metadata=self.metadata)
        return response

    def rag_retrieval(self, request: RagRetrievalRequest) -> RagRetrievalResponse:
        response: RagRetrievalResponse = self.stub.RagRetrieval(request, metadata=self.metadata)
        return response

    def rag_create_crawler(self, request: RagCreateCrawlerRequest) -> RagCrawler:
        response: RagCrawler = self.stub.RagCreateCrawler(request, metadata=self.metadata)
        return response

    def rag_get_crawler(self, request: RagGetCrawlerRequest) -> RagCrawler:
        response: RagCrawler = self.stub.RagGetCrawler(request, metadata=self.metadata)
        return response

    def rag_list_crawlers(self, request: RagListCrawlersRequest) -> RagListCrawlersResponse:
        response: RagListCrawlersResponse = self.stub.RagListCrawlers(request, metadata=self.metadata)
        return response

    def rag_update_crawler(self, request: RagUpdateCrawlerRequest) -> RagCrawler:
        response: RagCrawler = self.stub.RagUpdateCrawler(request, metadata=self.metadata)
        return response

    def rag_delete_crawler(self, request: RagDeleteCrawlerRequest) -> RagDeleteCrawlerResponse:
        response: RagDeleteCrawlerResponse = self.stub.RagDeleteCrawler(request, metadata=self.metadata)
        return response

    def rag_start_crawler(self, request: RagStartCrawlerRequest) -> Operation:
        response: Operation = self.stub.RagStartCrawler(request, metadata=self.metadata)
        return response

    def rag_stop_crawler(self, request: RagStopCrawlerRequest) -> RagStopCrawlerResponse:
        response: RagStopCrawlerResponse = self.stub.RagStopCrawler(request, metadata=self.metadata)
        return response

    def rag_get_crawler_run(self, request: RagGetCrawlerRunRequest) -> Operation:
        response: Operation = self.stub.RagGetCrawlerRun(request, metadata=self.metadata)
        return response

    def rag_list_crawler_runs(self, request: RagListCrawlerRunsRequest) -> RagListCrawlerRunsResponse:
        response: RagListCrawlerRunsResponse = self.stub.RagListCrawlerRuns(request, metadata=self.metadata)
        return response

    def rag_delete_crawler_runs(self, request: RagDeleteCrawlerRunsRequest) -> RagDeleteCrawlerRunsResponse:
        response: RagDeleteCrawlerRunsResponse = self.stub.RagDeleteCrawlerRuns(request, metadata=self.metadata)
        return response

    def rag_get_crawler_result(self, request: RagGetCrawlerResultRequest) -> RagCrawlerResult:
        response: RagCrawlerResult = self.stub.RagGetCrawlerResult(request, metadata=self.metadata)
        return response

    def rag_get_crawler_results(self, request: RagGetCrawlerResultsRequest) -> RagGetCrawlerResultsResponse:
        response: RagGetCrawlerResultsResponse = self.stub.RagGetCrawlerResults(request, metadata=self.metadata)
        return response

    def rag_add_crawler_results_to_datasets(self, request: RagAddCrawlerResultsToDatasetsRequest) -> Operation:
        response: Operation = self.stub.RagAddCrawlerResultsToDatasets(request, metadata=self.metadata)
        return response

    def rag_remove_crawler_results_from_datasets(
            self, request: RagRemoveCrawlerResultsFromDatasetsRequest) -> Operation:
        response: Operation = self.stub.RagRemoveCrawlerResultsFromDatasets(request, metadata=self.metadata)
        return response

    def rag_get_crawler_attached_datasets(
            self, request: RagGetCrawlerAttachedDatasetsRequest) -> RagGetCrawlerAttachedDatasetsResponse:
        response: RagGetCrawlerAttachedDatasetsResponse = self.stub.RagGetCrawlerAttachedDatasets(
            request, metadata=self.metadata)
        return response

    def rag_delete_crawlers(self, request: RagDeleteCrawlersRequest) -> RagDeleteCrawlersResponse:
        response: RagDeleteCrawlersResponse = self.stub.RagDeleteCrawlers(request, metadata=self.metadata)
        return response
