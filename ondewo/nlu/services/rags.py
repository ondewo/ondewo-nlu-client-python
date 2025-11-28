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
from google.protobuf.struct_pb2 import Struct

from ondewo.nlu.rag_pb2 import (
    RagAddChunkRequest,
    RagAddChunkResponse,
    RagAgentCompletionRequest,
    RagAgentCompletionResponse,
    RagAgentSession,
    RagAgentSessionList,
    RagAgentbotCompletionRequest,
    RagAgentbotInputsRequest,
    RagAgentbotInputsResponse,
    RagAskRequest,
    RagAskResponse,
    RagChat,
    RagChatCompletionRequest,
    RagChatCompletionResponse,
    RagChatList,
    RagChatSession,
    RagChatSessionList,
    RagChatbotCompletionRequest,
    RagChatbotInfoRequest,
    RagChatbotInfoResponse,
    RagCreateAgentSessionRequest,
    RagCreateChatRequest,
    RagCreateChatSessionRequest,
    RagCreateDatasetRequest,
    RagCreateFileRequest,
    RagCreateAgentRequest,
    RagDataset,
    RagDatasetList,
    RagDeleteAgentSessionsRequest,
    RagDeleteChatSessionsRequest,
    RagDeleteChatsRequest,
    RagDeleteDatasetsRequest,
    RagDeleteDocumentsRequest,
    RagDeleteFilesRequest,
    RagDeleteKnowledgeGraphRequest,
    RagDeleteAgentRequest,
    RagDifyRecordList,
    RagDifyRetrievalRequest,
    RagDocument,
    RagDocumentList,
    RagDownloadDocumentRequest,
    RagFile,
    RagFileChunk,
    RagFileList,
    RagFileToDocumentList,
    RagFileToDocumentRequest,
    RagGetAllParentFoldersRequest,
    RagGetAllParentFoldersResponse,
    RagGetFileRequest,
    RagGetKnowledgeGraphRequest,
    RagGetKnowledgeGraphResponse,
    RagGetParentFolderRequest,
    RagGetParentFolderResponse,
    RagGetRootFolderRequest,
    RagGetRootFolderResponse,
    RagListAgentSessionsRequest,
    RagListChatSessionsRequest,
    RagListChatsRequest,
    RagListChunksRequest,
    RagListChunksResponse,
    RagListDatasetsRequest,
    RagListDocumentsRequest,
    RagListDocumentsResponse,
    RagListFilesRequest,
    RagListFilesResponse,
    RagListAgentsRequest,
    RagMoveFileRequest,
    RagOpenAiAgentCompletionRequest,
    RagOpenAiChatCompletionRequest,
    RagOpenAiChatCompletionResponse,
    RagParseDocumentsRequest,
    RagPartialSuccess,
    RagAgentList,
    RagRelatedQuestionsRequest,
    RagRelatedQuestionsResponse,
    RagRemoveChunksRequest,
    RagRenameFileRequest,
    RagRetrievalRequest,
    RagRetrievalResponse,
    RagSearchbotAskRequest,
    RagSearchbotDetailRequest,
    RagSearchbotDetailResponse,
    RagSearchbotMindmapRequest,
    RagSearchbotRelatedQuestionsRequest,
    RagSearchbotRetrievalRequest,
    RagSearchbotRetrievalResponse,
    RagStopParsingRequest,
    RagUpdateChatRequest,
    RagUpdateChatSessionRequest,
    RagUpdateChunkRequest,
    RagUpdateDatasetRequest,
    RagUpdateDocumentRequest,
    RagUpdateAgentRequest,
    RagUploadDocumentsRequest,
    RagUploadFilesRequest
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

    def rag_delete_datasets(self, request: RagDeleteDatasetsRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = self.stub.RagDeleteDatasets(request, metadata=self.metadata)
        return response

    def rag_list_datasets(self, request: RagListDatasetsRequest) -> RagDatasetList:
        response: RagDatasetList = self.stub.RagListDatasets(request, metadata=self.metadata)
        return response

    def rag_get_knowledge_graph(self, request: RagGetKnowledgeGraphRequest) -> RagGetKnowledgeGraphResponse:
        response: RagGetKnowledgeGraphResponse = self.stub.RagGetKnowledgeGraph(request, metadata=self.metadata)
        return response

    def rag_delete_knowledge_graph(self, request: RagDeleteKnowledgeGraphRequest) -> Empty:
        response: Empty = self.stub.RagDeleteKnowledgeGraph(request, metadata=self.metadata)
        return response

    def rag_upload_documents(self, request_iterator: Iterator[RagUploadDocumentsRequest]) -> RagDocumentList:
        response: RagDocumentList = self.stub.RagUploadDocuments(request_iterator, metadata=self.metadata)
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

    def rag_create_chat(self, request: RagCreateChatRequest) -> RagChat:
        response: RagChat = self.stub.RagCreateChat(request, metadata=self.metadata)
        return response

    def rag_update_chat(self, request: RagUpdateChatRequest) -> Empty:
        response: Empty = self.stub.RagUpdateChat(request, metadata=self.metadata)
        return response

    def rag_delete_chats(self, request: RagDeleteChatsRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = self.stub.RagDeleteChats(request, metadata=self.metadata)
        return response

    def rag_list_chats(self, request: RagListChatsRequest) -> RagChatList:
        response: RagChatList = self.stub.RagListChats(request, metadata=self.metadata)
        return response

    def rag_create_chat_session(self, request: RagCreateChatSessionRequest) -> RagChatSession:
        response: RagChatSession = self.stub.RagCreateChatSession(request, metadata=self.metadata)
        return response

    def rag_create_agent_session(self, request: RagCreateAgentSessionRequest) -> RagAgentSession:
        response: RagAgentSession = self.stub.RagCreateAgentSession(request, metadata=self.metadata)
        return response

    def rag_update_chat_session(self, request: RagUpdateChatSessionRequest) -> Empty:
        response: Empty = self.stub.RagUpdateChatSession(request, metadata=self.metadata)
        return response

    def rag_list_chat_sessions(self, request: RagListChatSessionsRequest) -> RagChatSessionList:
        response: RagChatSessionList = self.stub.RagListChatSessions(request, metadata=self.metadata)
        return response

    def rag_list_agent_sessions(self, request: RagListAgentSessionsRequest) -> RagAgentSessionList:
        response: RagAgentSessionList = self.stub.RagListAgentSessions(request, metadata=self.metadata)
        return response

    def rag_delete_chat_sessions(self, request: RagDeleteChatSessionsRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = self.stub.RagDeleteChatSessions(request, metadata=self.metadata)
        return response

    def rag_delete_agent_sessions(self, request: RagDeleteAgentSessionsRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = self.stub.RagDeleteAgentSessions(request, metadata=self.metadata)
        return response

    def rag_chat_completion(self, request: RagChatCompletionRequest) -> Iterator[RagChatCompletionResponse]:
        response: Iterator[RagChatCompletionResponse] = self.stub.RagChatCompletion(request, metadata=self.metadata)
        return response

    def rag_open_ai_chat_completion(
            self, request: RagOpenAiChatCompletionRequest) -> Iterator[RagOpenAiChatCompletionResponse]:
        response: Iterator[RagOpenAiChatCompletionResponse] = self.stub.RagOpenAiChatCompletion(
            request, metadata=self.metadata)
        return response

    def rag_agent_completion(self, request: RagAgentCompletionRequest) -> Iterator[RagAgentCompletionResponse]:
        response: Iterator[RagAgentCompletionResponse] = self.stub.RagAgentCompletion(request, metadata=self.metadata)
        return response

    def rag_open_ai_agent_completion(
            self, request: RagOpenAiAgentCompletionRequest) -> Iterator[RagOpenAiChatCompletionResponse]:
        response: Iterator[RagOpenAiChatCompletionResponse] = self.stub.RagOpenAiAgentCompletion(
            request, metadata=self.metadata)
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

    def rag_upload_files(self, request_iterator: Iterator[RagUploadFilesRequest]) -> RagFileList:
        response: RagFileList = self.stub.RagUploadFiles(request_iterator, metadata=self.metadata)
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

    def rag_get_parent_folder(self, request: RagGetParentFolderRequest) -> RagGetParentFolderResponse:
        response: RagGetParentFolderResponse = self.stub.RagGetParentFolder(request, metadata=self.metadata)
        return response

    def rag_get_all_parent_folders(self, request: RagGetAllParentFoldersRequest) -> RagGetAllParentFoldersResponse:
        response: RagGetAllParentFoldersResponse = self.stub.RagGetAllParentFolders(request, metadata=self.metadata)
        return response

    def rag_delete_files(self, request: RagDeleteFilesRequest) -> Empty:
        response: Empty = self.stub.RagDeleteFiles(request, metadata=self.metadata)
        return response

    def rag_rename_file(self, request: RagRenameFileRequest) -> Empty:
        response: Empty = self.stub.RagRenameFile(request, metadata=self.metadata)
        return response

    def rag_get_file(self, request: RagGetFileRequest) -> Iterator[RagFileChunk]:
        response: Iterator[RagFileChunk] = self.stub.RagGetFile(request, metadata=self.metadata)
        return response

    def rag_move_file(self, request: RagMoveFileRequest) -> Empty:
        response: Empty = self.stub.RagMoveFile(request, metadata=self.metadata)
        return response

    def rag_file_to_document(self, request: RagFileToDocumentRequest) -> RagFileToDocumentList:
        response: RagFileToDocumentList = self.stub.RagFileToDocument(request, metadata=self.metadata)
        return response

    def rag_dify_retrieval(self, request: RagDifyRetrievalRequest) -> RagDifyRecordList:
        response: RagDifyRecordList = self.stub.RagDifyRetrieval(request, metadata=self.metadata)
        return response

    def rag_ask(self, request: RagAskRequest) -> Iterator[RagAskResponse]:
        response: Iterator[RagAskResponse] = self.stub.RagAsk(request, metadata=self.metadata)
        return response

    def rag_related_questions(self, request: RagRelatedQuestionsRequest) -> RagRelatedQuestionsResponse:
        response: RagRelatedQuestionsResponse = self.stub.RagRelatedQuestions(request, metadata=self.metadata)
        return response

    def rag_chatbot_completion(self, request: RagChatbotCompletionRequest) -> Iterator[RagChatCompletionResponse]:
        response: Iterator[RagChatCompletionResponse] = self.stub.RagChatbotCompletion(request, metadata=self.metadata)
        return response

    def rag_chatbot_info(self, request: RagChatbotInfoRequest) -> RagChatbotInfoResponse:
        response: RagChatbotInfoResponse = self.stub.RagChatbotInfo(request, metadata=self.metadata)
        return response

    def rag_agentbot_completion(self, request: RagAgentbotCompletionRequest) -> Iterator[RagAgentCompletionResponse]:
        response: Iterator[RagAgentCompletionResponse] = self.stub.RagAgentbotCompletion(
            request, metadata=self.metadata)
        return response

    def rag_agentbot_inputs(self, request: RagAgentbotInputsRequest) -> RagAgentbotInputsResponse:
        response: RagAgentbotInputsResponse = self.stub.RagAgentbotInputs(request, metadata=self.metadata)
        return response

    def rag_searchbot_ask(self, request: RagSearchbotAskRequest) -> Iterator[RagAskResponse]:
        response: Iterator[RagAskResponse] = self.stub.RagSearchbotAsk(request, metadata=self.metadata)
        return response

    def rag_searchbot_retrieval(self, request: RagSearchbotRetrievalRequest) -> RagSearchbotRetrievalResponse:
        response: RagSearchbotRetrievalResponse = self.stub.RagSearchbotRetrieval(request, metadata=self.metadata)
        return response

    def rag_searchbot_related_questions(
            self, request: RagSearchbotRelatedQuestionsRequest) -> RagRelatedQuestionsResponse:
        response: RagRelatedQuestionsResponse = self.stub.RagSearchbotRelatedQuestions(request, metadata=self.metadata)
        return response

    def rag_searchbot_detail(self, request: RagSearchbotDetailRequest) -> RagSearchbotDetailResponse:
        response: RagSearchbotDetailResponse = self.stub.RagSearchbotDetail(request, metadata=self.metadata)
        return response

    def rag_searchbot_mindmap(self, request: RagSearchbotMindmapRequest) -> Struct:
        response: Struct = self.stub.RagSearchbotMindmap(request, metadata=self.metadata)
        return response
