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

from google.protobuf.empty_pb2 import Empty

from ondewo.nlu.rag_pb2 import (
    RagAddChunkRequest,
    RagAddChunkResponse,
    RagAgentCompletionRequest,
    RagAgentCompletionResponse,
    RagAgentList,
    RagAgentSessionList,
    RagAskRequest,
    RagAskResponse,
    RagChatAssistant,
    RagChatAssistantList,
    RagChatCompletionRequest,
    RagChatCompletionResponse,
    RagChatSession,
    RagChatSessionList,
    RagConstructKnowledgeGraphResponse,
    RagConstructRaptorResponse,
    RagCreateAgentRequest,
    RagCreateChatAssistantRequest,
    RagCreateChatSessionRequest,
    RagCreateDatasetRequest,
    RagCreateFileRequest,
    RagDataset,
    RagDatasetIdRequest,
    RagDatasetList,
    RagDeleteAgentRequest,
    RagDeleteAgentSessionsRequest,
    RagDeleteChatSessionsRequest,
    RagDeleteDocumentsRequest,
    RagDeleteFilesRequest,
    RagDeleteRequest,
    RagDocument,
    RagDocumentList,
    RagDownloadDocumentRequest,
    RagFile,
    RagFileChunk,
    RagFileIdRequest,
    RagFileList,
    RagFileToDocumentList,
    RagFileToDocumentRequest,
    RagGetKnowledgeGraphResponse,
    RagGetParentFolderResponse,
    RagGetRootFolderRequest,
    RagGetRootFolderResponse,
    RagListAgentSessionsRequest,
    RagListAgentsRequest,
    RagListChatAssistantsRequest,
    RagListChatSessionsRequest,
    RagListChunksRequest,
    RagListChunksResponse,
    RagListDatasetsRequest,
    RagListDocumentsRequest,
    RagListDocumentsResponse,
    RagListFilesRequest,
    RagListFilesResponse,
    RagMoveFileRequest,
    RagParentFoldersList,
    RagParseDocumentsRequest,
    RagPartialSuccess,
    RagRelatedQuestionsRequest,
    RagRelatedQuestionsResponse,
    RagRemoveChunksRequest,
    RagRenameFileRequest,
    RagRetrievalRequest,
    RagRetrievalResponse,
    RagStopParsingRequest,
    RagTaskStatus,
    RagUpdateAgentRequest,
    RagUpdateChatAssistantRequest,
    RagUpdateChatSessionRequest,
    RagUpdateChunkRequest,
    RagUpdateDatasetRequest,
    RagUpdateDocumentRequest,
    RagUploadDocumentsRequest,
    RagUploadFilesRequest,
)
from ondewo.nlu.rag_pb2_grpc import RagsStub
from ondewo.nlu.core.services_interface import ServicesInterface


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

    def rag_get_knowledge_graph(self, request: RagDatasetIdRequest) -> RagGetKnowledgeGraphResponse:
        response: RagGetKnowledgeGraphResponse = self.stub.RagGetKnowledgeGraph(request, metadata=self.metadata)
        return response

    def rag_delete_knowledge_graph(self, request: RagDatasetIdRequest) -> Empty:
        response: Empty = self.stub.RagDeleteKnowledgeGraph(request, metadata=self.metadata)
        return response

    def rag_construct_knowledge_graph(self, request: RagDatasetIdRequest) -> RagConstructKnowledgeGraphResponse:
        response: RagConstructKnowledgeGraphResponse = self.stub.RagConstructKnowledgeGraph(
            request, metadata=self.metadata)
        return response

    def rag_knowledge_graph_status(self, request: RagDatasetIdRequest) -> RagTaskStatus:
        response: RagTaskStatus = self.stub.RagKnowledgeGraphStatus(request, metadata=self.metadata)
        return response

    def rag_construct_raptor(self, request: RagDatasetIdRequest) -> RagConstructRaptorResponse:
        response: RagConstructRaptorResponse = self.stub.RagConstructRaptor(request, metadata=self.metadata)
        return response

    def rag_raptor_status(self, request: RagDatasetIdRequest) -> RagTaskStatus:
        response: RagTaskStatus = self.stub.RagRaptorStatus(request, metadata=self.metadata)
        return response

    def rag_upload_documents(self, request: Iterator[RagUploadDocumentsRequest]) -> RagDocumentList:
        response: RagDocumentList = self.stub.RagUploadDocuments(request, metadata=self.metadata)
        return response

    def rag_update_document(self, request: RagUpdateDocumentRequest) -> RagDocument:
        response: RagDocument = self.stub.RagUpdateDocument(request, metadata=self.metadata)
        return response

    def rag_download_document(self, request: RagDownloadDocumentRequest) -> Iterator[RagFileChunk]:
        response: Iterator[RagFileChunk] = self.stub.RagDownloadDocument(request, metadata=self.metadata)
        return response

    def rag_list_documents(self, request: RagListDocumentsRequest) -> RagListDocumentsResponse:
        response: RagListDocumentsResponse = self.stub.RagListDocuments(request, metadata=self.metadata)
        return response

    def rag_delete_documents(self, request: RagDeleteDocumentsRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = self.stub.RagDeleteDocuments(request, metadata=self.metadata)
        return response

    def rag_parse_documents(self, request: RagParseDocumentsRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = self.stub.RagParseDocuments(request, metadata=self.metadata)
        return response

    def rag_stop_parsing(self, request: RagStopParsingRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = self.stub.RagStopParsing(request, metadata=self.metadata)
        return response

    def rag_list_chunks(self, request: RagListChunksRequest) -> RagListChunksResponse:
        response: RagListChunksResponse = self.stub.RagListChunks(request, metadata=self.metadata)
        return response

    def rag_add_chunk(self, request: RagAddChunkRequest) -> RagAddChunkResponse:
        response: RagAddChunkResponse = self.stub.RagAddChunk(request, metadata=self.metadata)
        return response

    def rag_remove_chunks(self, request: RagRemoveChunksRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = self.stub.RagRemoveChunks(request, metadata=self.metadata)
        return response

    def rag_update_chunk(self, request: RagUpdateChunkRequest) -> Empty:
        response: Empty = self.stub.RagUpdateChunk(request, metadata=self.metadata)
        return response

    def rag_retrieval(self, request: RagRetrievalRequest) -> RagRetrievalResponse:
        response: RagRetrievalResponse = self.stub.RagRetrieval(request, metadata=self.metadata)
        return response

    def rag_upload_files(self, request: Iterator[RagUploadFilesRequest]) -> RagFileList:
        response: RagFileList = self.stub.RagUploadFiles(request, metadata=self.metadata)
        return response

    def rag_create_file(self, request: RagCreateFileRequest) -> RagFile:
        response: RagFile = self.stub.RagCreateFile(request, metadata=self.metadata)
        return response

    def rag_list_files(self, request: RagListFilesRequest) -> RagListFilesResponse:
        response: RagListFilesResponse = self.stub.RagListFiles(request, metadata=self.metadata)
        return response

    def rag_get_root_folder(self, request: RagGetRootFolderRequest) -> RagGetRootFolderResponse:
        response: RagGetRootFolderResponse = self.stub.RagGetRootFolder(request, metadata=self.metadata)
        return response

    def rag_get_parent_folder(self, request: RagFileIdRequest) -> RagGetParentFolderResponse:
        response: RagGetParentFolderResponse = self.stub.RagGetParentFolder(request, metadata=self.metadata)
        return response

    def rag_get_all_parent_folders(self, request: RagFileIdRequest) -> RagParentFoldersList:
        response: RagParentFoldersList = self.stub.RagGetAllParentFolders(request, metadata=self.metadata)
        return response

    def rag_delete_files(self, request: RagDeleteFilesRequest) -> Empty:
        response: Empty = self.stub.RagDeleteFiles(request, metadata=self.metadata)
        return response

    def rag_rename_file(self, request: RagRenameFileRequest) -> Empty:
        response: Empty = self.stub.RagRenameFile(request, metadata=self.metadata)
        return response

    def rag_download_file(self, request: RagFileIdRequest) -> Iterator[RagFileChunk]:
        response: Iterator[RagFileChunk] = self.stub.RagDownloadFile(request, metadata=self.metadata)
        return response

    def rag_move_file(self, request: RagMoveFileRequest) -> Empty:
        response: Empty = self.stub.RagMoveFile(request, metadata=self.metadata)
        return response

    def rag_file_to_document(self, request: RagFileToDocumentRequest) -> RagFileToDocumentList:
        response: RagFileToDocumentList = self.stub.RagFileToDocument(request, metadata=self.metadata)
        return response

    def rag_create_chat_assistant(self, request: RagCreateChatAssistantRequest) -> RagChatAssistant:
        response: RagChatAssistant = self.stub.RagCreateChatAssistant(request, metadata=self.metadata)
        return response

    def rag_update_chat_assistant(self, request: RagUpdateChatAssistantRequest) -> Empty:
        response: Empty = self.stub.RagUpdateChatAssistant(request, metadata=self.metadata)
        return response

    def rag_delete_chat_assistants(self, request: RagDeleteRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = self.stub.RagDeleteChatAssistants(request, metadata=self.metadata)
        return response

    def rag_list_chat_assistants(self, request: RagListChatAssistantsRequest) -> RagChatAssistantList:
        response: RagChatAssistantList = self.stub.RagListChatAssistants(request, metadata=self.metadata)
        return response

    def rag_create_agent(self, request: RagCreateAgentRequest) -> Empty:
        response: Empty = self.stub.RagCreateAgent(request, metadata=self.metadata)
        return response

    def rag_update_agent(self, request: RagUpdateAgentRequest) -> Empty:
        response: Empty = self.stub.RagUpdateAgent(request, metadata=self.metadata)
        return response

    def rag_delete_agent(self, request: RagDeleteAgentRequest) -> Empty:
        response: Empty = self.stub.RagDeleteAgent(request, metadata=self.metadata)
        return response

    def rag_list_agents(self, request: RagListAgentsRequest) -> RagAgentList:
        response: RagAgentList = self.stub.RagListAgents(request, metadata=self.metadata)
        return response

    def rag_create_chat_session(self, request: RagCreateChatSessionRequest) -> RagChatSession:
        response: RagChatSession = self.stub.RagCreateChatSession(request, metadata=self.metadata)
        return response

    def rag_update_chat_session(self, request: RagUpdateChatSessionRequest) -> Empty:
        response: Empty = self.stub.RagUpdateChatSession(request, metadata=self.metadata)
        return response

    def rag_list_chat_sessions(self, request: RagListChatSessionsRequest) -> RagChatSessionList:
        response: RagChatSessionList = self.stub.RagListChatSessions(request, metadata=self.metadata)
        return response

    def rag_delete_chat_sessions(self, request: RagDeleteChatSessionsRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = self.stub.RagDeleteChatSessions(request, metadata=self.metadata)
        return response

    def rag_list_agent_sessions(self, request: RagListAgentSessionsRequest) -> RagAgentSessionList:
        response: RagAgentSessionList = self.stub.RagListAgentSessions(request, metadata=self.metadata)
        return response

    def rag_delete_agent_sessions(self, request: RagDeleteAgentSessionsRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = self.stub.RagDeleteAgentSessions(request, metadata=self.metadata)
        return response

    def rag_chat_completion(self, request: RagChatCompletionRequest) -> Iterator[RagChatCompletionResponse]:
        response: Iterator[RagChatCompletionResponse] = self.stub.RagChatCompletion(
            request, metadata=self.metadata)
        return response

    def rag_agent_completion(self, request: RagAgentCompletionRequest) -> Iterator[RagAgentCompletionResponse]:
        response: Iterator[RagAgentCompletionResponse] = self.stub.RagAgentCompletion(
            request, metadata=self.metadata)
        return response

    def rag_ask(self, request: RagAskRequest) -> Iterator[RagAskResponse]:
        response: Iterator[RagAskResponse] = self.stub.RagAsk(request, metadata=self.metadata)
        return response

    def rag_related_questions(self, request: RagRelatedQuestionsRequest) -> RagRelatedQuestionsResponse:
        response: RagRelatedQuestionsResponse = self.stub.RagRelatedQuestions(request, metadata=self.metadata)
        return response
