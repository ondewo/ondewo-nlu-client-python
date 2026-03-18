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
    RagUploadDocumentRequest,
    RagUploadFilesRequest,
)
from ondewo.nlu.rag_pb2_grpc import RagsStub
from ondewo.nlu.core.async_services_interface import AsyncServicesInterface


class Rags(AsyncServicesInterface):
    """
    Exposes the RAG-related endpoints of ONDEWO NLU services in a user-friendly way.

    See rag.proto.
    """

    @property
    def stub(self) -> RagsStub:
        stub: RagsStub = RagsStub(channel=self.grpc_channel)
        return stub

    async def rag_create_dataset(self, request: RagCreateDatasetRequest) -> RagDataset:
        response: RagDataset = await self.stub.RagCreateDataset(request, metadata=self.metadata)
        return response

    async def rag_update_dataset(self, request: RagUpdateDatasetRequest) -> RagDataset:
        response: RagDataset = await self.stub.RagUpdateDataset(request, metadata=self.metadata)
        return response

    async def rag_delete_datasets(self, request: RagDeleteRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = await self.stub.RagDeleteDatasets(request, metadata=self.metadata)
        return response

    async def rag_list_datasets(self, request: RagListDatasetsRequest) -> RagDatasetList:
        response: RagDatasetList = await self.stub.RagListDatasets(request, metadata=self.metadata)
        return response

    async def rag_get_knowledge_graph(self, request: RagDatasetIdRequest) -> RagGetKnowledgeGraphResponse:
        response: RagGetKnowledgeGraphResponse = await self.stub.RagGetKnowledgeGraph(request, metadata=self.metadata)
        return response

    async def rag_delete_knowledge_graph(self, request: RagDatasetIdRequest) -> Empty:
        response: Empty = await self.stub.RagDeleteKnowledgeGraph(request, metadata=self.metadata)
        return response

    async def rag_construct_knowledge_graph(self, request: RagDatasetIdRequest) -> RagConstructKnowledgeGraphResponse:
        response: RagConstructKnowledgeGraphResponse = await self.stub.RagConstructKnowledgeGraph(
            request, metadata=self.metadata
        )
        return response

    async def rag_knowledge_graph_status(self, request: RagDatasetIdRequest) -> RagTaskStatus:
        response: RagTaskStatus = await self.stub.RagKnowledgeGraphStatus(request, metadata=self.metadata)
        return response

    async def rag_construct_raptor(self, request: RagDatasetIdRequest) -> RagConstructRaptorResponse:
        response: RagConstructRaptorResponse = await self.stub.RagConstructRaptor(request, metadata=self.metadata)
        return response

    async def rag_raptor_status(self, request: RagDatasetIdRequest) -> RagTaskStatus:
        response: RagTaskStatus = await self.stub.RagRaptorStatus(request, metadata=self.metadata)
        return response

    async def rag_upload_document(self, request: Iterator[RagUploadDocumentRequest]) -> RagDocument:
        response: RagDocument = await self.stub.RagUploadDocument(request, metadata=self.metadata)
        return response

    async def rag_update_document(self, request: RagUpdateDocumentRequest) -> RagDocument:
        response: RagDocument = await self.stub.RagUpdateDocument(request, metadata=self.metadata)
        return response

    async def rag_download_document(self, request: RagDownloadDocumentRequest) -> Iterator[RagFileChunk]:
        response: Iterator[RagFileChunk] = await self.stub.RagDownloadDocument(request, metadata=self.metadata)
        return response

    async def rag_list_documents(self, request: RagListDocumentsRequest) -> RagListDocumentsResponse:
        response: RagListDocumentsResponse = await self.stub.RagListDocuments(request, metadata=self.metadata)
        return response

    async def rag_delete_documents(self, request: RagDeleteDocumentsRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = await self.stub.RagDeleteDocuments(request, metadata=self.metadata)
        return response

    async def rag_parse_documents(self, request: RagParseDocumentsRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = await self.stub.RagParseDocuments(request, metadata=self.metadata)
        return response

    async def rag_stop_parsing(self, request: RagStopParsingRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = await self.stub.RagStopParsing(request, metadata=self.metadata)
        return response

    async def rag_list_chunks(self, request: RagListChunksRequest) -> RagListChunksResponse:
        response: RagListChunksResponse = await self.stub.RagListChunks(request, metadata=self.metadata)
        return response

    async def rag_add_chunk(self, request: RagAddChunkRequest) -> RagAddChunkResponse:
        response: RagAddChunkResponse = await self.stub.RagAddChunk(request, metadata=self.metadata)
        return response

    async def rag_remove_chunks(self, request: RagRemoveChunksRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = await self.stub.RagRemoveChunks(request, metadata=self.metadata)
        return response

    async def rag_update_chunk(self, request: RagUpdateChunkRequest) -> Empty:
        response: Empty = await self.stub.RagUpdateChunk(request, metadata=self.metadata)
        return response

    async def rag_retrieval(self, request: RagRetrievalRequest) -> RagRetrievalResponse:
        response: RagRetrievalResponse = await self.stub.RagRetrieval(request, metadata=self.metadata)
        return response

    async def rag_upload_files(self, request: Iterator[RagUploadFilesRequest]) -> RagFileList:
        response: RagFileList = await self.stub.RagUploadFiles(request, metadata=self.metadata)
        return response

    async def rag_create_file(self, request: RagCreateFileRequest) -> RagFile:
        response: RagFile = await self.stub.RagCreateFile(request, metadata=self.metadata)
        return response

    async def rag_list_files(self, request: RagListFilesRequest) -> RagListFilesResponse:
        response: RagListFilesResponse = await self.stub.RagListFiles(request, metadata=self.metadata)
        return response

    async def rag_get_root_folder(self, request: RagGetRootFolderRequest) -> RagGetRootFolderResponse:
        response: RagGetRootFolderResponse = await self.stub.RagGetRootFolder(request, metadata=self.metadata)
        return response

    async def rag_get_parent_folder(self, request: RagFileIdRequest) -> RagGetParentFolderResponse:
        response: RagGetParentFolderResponse = await self.stub.RagGetParentFolder(request, metadata=self.metadata)
        return response

    async def rag_get_all_parent_folders(self, request: RagFileIdRequest) -> RagParentFoldersList:
        response: RagParentFoldersList = await self.stub.RagGetAllParentFolders(request, metadata=self.metadata)
        return response

    async def rag_delete_files(self, request: RagDeleteFilesRequest) -> Empty:
        response: Empty = await self.stub.RagDeleteFiles(request, metadata=self.metadata)
        return response

    async def rag_rename_file(self, request: RagRenameFileRequest) -> Empty:
        response: Empty = await self.stub.RagRenameFile(request, metadata=self.metadata)
        return response

    async def rag_download_file(self, request: RagFileIdRequest) -> Iterator[RagFileChunk]:
        response: Iterator[RagFileChunk] = await self.stub.RagDownloadFile(request, metadata=self.metadata)
        return response

    async def rag_move_file(self, request: RagMoveFileRequest) -> Empty:
        response: Empty = await self.stub.RagMoveFile(request, metadata=self.metadata)
        return response

    async def rag_file_to_document(self, request: RagFileToDocumentRequest) -> RagFileToDocumentList:
        response: RagFileToDocumentList = await self.stub.RagFileToDocument(request, metadata=self.metadata)
        return response

    async def rag_create_chat_assistant(self, request: RagCreateChatAssistantRequest) -> RagChatAssistant:
        response: RagChatAssistant = await self.stub.RagCreateChatAssistant(request, metadata=self.metadata)
        return response

    async def rag_update_chat_assistant(self, request: RagUpdateChatAssistantRequest) -> Empty:
        response: Empty = await self.stub.RagUpdateChatAssistant(request, metadata=self.metadata)
        return response

    async def rag_delete_chat_assistants(self, request: RagDeleteRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = await self.stub.RagDeleteChatAssistants(request, metadata=self.metadata)
        return response

    async def rag_list_chat_assistants(self, request: RagListChatAssistantsRequest) -> RagChatAssistantList:
        response: RagChatAssistantList = await self.stub.RagListChatAssistants(request, metadata=self.metadata)
        return response

    async def rag_create_agent(self, request: RagCreateAgentRequest) -> Empty:
        response: Empty = await self.stub.RagCreateAgent(request, metadata=self.metadata)
        return response

    async def rag_update_agent(self, request: RagUpdateAgentRequest) -> Empty:
        response: Empty = await self.stub.RagUpdateAgent(request, metadata=self.metadata)
        return response

    async def rag_delete_agent(self, request: RagDeleteAgentRequest) -> Empty:
        response: Empty = await self.stub.RagDeleteAgent(request, metadata=self.metadata)
        return response

    async def rag_list_agents(self, request: RagListAgentsRequest) -> RagAgentList:
        response: RagAgentList = await self.stub.RagListAgents(request, metadata=self.metadata)
        return response

    async def rag_create_chat_session(self, request: RagCreateChatSessionRequest) -> RagChatSession:
        response: RagChatSession = await self.stub.RagCreateChatSession(request, metadata=self.metadata)
        return response

    async def rag_update_chat_session(self, request: RagUpdateChatSessionRequest) -> Empty:
        response: Empty = await self.stub.RagUpdateChatSession(request, metadata=self.metadata)
        return response

    async def rag_list_chat_sessions(self, request: RagListChatSessionsRequest) -> RagChatSessionList:
        response: RagChatSessionList = await self.stub.RagListChatSessions(request, metadata=self.metadata)
        return response

    async def rag_delete_chat_sessions(self, request: RagDeleteChatSessionsRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = await self.stub.RagDeleteChatSessions(request, metadata=self.metadata)
        return response

    async def rag_list_agent_sessions(self, request: RagListAgentSessionsRequest) -> RagAgentSessionList:
        response: RagAgentSessionList = await self.stub.RagListAgentSessions(request, metadata=self.metadata)
        return response

    async def rag_delete_agent_sessions(self, request: RagDeleteAgentSessionsRequest) -> RagPartialSuccess:
        response: RagPartialSuccess = await self.stub.RagDeleteAgentSessions(request, metadata=self.metadata)
        return response

    async def rag_chat_completion(self, request: RagChatCompletionRequest) -> Iterator[RagChatCompletionResponse]:
        response: Iterator[RagChatCompletionResponse] = await self.stub.RagChatCompletion(
            request, metadata=self.metadata
        )
        return response

    async def rag_agent_completion(self, request: RagAgentCompletionRequest) -> Iterator[RagAgentCompletionResponse]:
        response: Iterator[RagAgentCompletionResponse] = await self.stub.RagAgentCompletion(
            request, metadata=self.metadata
        )
        return response

    async def rag_ask(self, request: RagAskRequest) -> Iterator[RagAskResponse]:
        response: Iterator[RagAskResponse] = await self.stub.RagAsk(request, metadata=self.metadata)
        return response

    async def rag_related_questions(self, request: RagRelatedQuestionsRequest) -> RagRelatedQuestionsResponse:
        response: RagRelatedQuestionsResponse = await self.stub.RagRelatedQuestions(request, metadata=self.metadata)
        return response
