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
    AddChunkRequest,
    AddChunkResponse,
    AgentCompletionRequest,
    AgentCompletionResponse,
    AgentSession,
    AgentSessionList,
    AgentbotCompletionRequest,
    AgentbotInputsRequest,
    AgentbotInputsResponse,
    AskRequest,
    AskResponse,
    Chat,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatList,
    ChatSession,
    ChatSessionList,
    ChatbotCompletionRequest,
    ChatbotInfoRequest,
    ChatbotInfoResponse,
    CreateAgentSessionRequest,
    CreateChatRequest,
    CreateChatSessionRequest,
    CreateDatasetRequest,
    CreateFileRequest,
    CreateRagAgentRequest,
    Dataset,
    DatasetList,
    DeleteAgentSessionsRequest,
    DeleteChatSessionsRequest,
    DeleteChatsRequest,
    DeleteDatasetsRequest,
    DeleteDocumentsRequest,
    DeleteFilesRequest,
    DeleteKnowledgeGraphRequest,
    DeleteRagAgentRequest,
    DifyRecordList,
    DifyRetrievalRequest,
    Document,
    DocumentList,
    DownloadDocumentRequest,
    File,
    FileChunk,
    FileList,
    FileToDocumentList,
    FileToDocumentRequest,
    GetAllParentFoldersRequest,
    GetAllParentFoldersResponse,
    GetFileRequest,
    GetKnowledgeGraphRequest,
    GetKnowledgeGraphResponse,
    GetParentFolderRequest,
    GetParentFolderResponse,
    GetRootFolderRequest,
    GetRootFolderResponse,
    ListAgentSessionsRequest,
    ListChatSessionsRequest,
    ListChatsRequest,
    ListChunksRequest,
    ListChunksResponse,
    ListDatasetsRequest,
    ListDocumentsRequest,
    ListDocumentsResponse,
    ListFilesRequest,
    ListFilesResponse,
    ListRagAgentsRequest,
    MoveFileRequest,
    OpenAIAgentCompletionRequest,
    OpenAIChatCompletionRequest,
    OpenAIChatCompletionResponse,
    ParseDocumentsRequest,
    PartialSuccess,
    RagAgentList,
    RelatedQuestionsRequest,
    RelatedQuestionsResponse,
    RemoveChunksRequest,
    RenameFileRequest,
    RetrievalRequest,
    RetrievalResponse,
    SearchbotAskRequest,
    SearchbotDetailRequest,
    SearchbotDetailResponse,
    SearchbotMindmapRequest,
    SearchbotRelatedQuestionsRequest,
    SearchbotRetrievalRequest,
    SearchbotRetrievalResponse,
    StopParsingRequest,
    UpdateChatRequest,
    UpdateChatSessionRequest,
    UpdateChunkRequest,
    UpdateDatasetRequest,
    UpdateDocumentRequest,
    UpdateRagAgentRequest,
    UploadDocumentsRequest,
    UploadFilesRequest,
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

    async def create_dataset(self, request: CreateDatasetRequest) -> Dataset:
        response: Dataset = await self.stub.CreateDataset(request, metadata=self.metadata)
        return response

    async def update_dataset(self, request: UpdateDatasetRequest) -> Dataset:
        response: Dataset = await self.stub.UpdateDataset(request, metadata=self.metadata)
        return response

    async def delete_datasets(self, request: DeleteDatasetsRequest) -> PartialSuccess:
        response: PartialSuccess = await self.stub.DeleteDatasets(request, metadata=self.metadata)
        return response

    async def list_datasets(self, request: ListDatasetsRequest) -> DatasetList:
        response: DatasetList = await self.stub.ListDatasets(request, metadata=self.metadata)
        return response

    async def get_knowledge_graph(self, request: GetKnowledgeGraphRequest) -> GetKnowledgeGraphResponse:
        response: GetKnowledgeGraphResponse = await self.stub.GetKnowledgeGraph(request, metadata=self.metadata)
        return response

    async def delete_knowledge_graph(self, request: DeleteKnowledgeGraphRequest) -> Empty:
        response: Empty = await self.stub.DeleteKnowledgeGraph(request, metadata=self.metadata)
        return response

    async def upload_documents(self, request_iterator: Iterator[UploadDocumentsRequest]) -> DocumentList:
        response: DocumentList = await self.stub.UploadDocuments(request_iterator, metadata=self.metadata)
        return response

    async def update_document(self, request: UpdateDocumentRequest) -> Document:
        response: Document = await self.stub.UpdateDocument(request, metadata=self.metadata)
        return response

    async def download_document(self, request: DownloadDocumentRequest) -> Iterator[FileChunk]:
        response: Iterator[FileChunk] = await self.stub.DownloadDocument(request, metadata=self.metadata)
        return response

    async def list_documents(self, request: ListDocumentsRequest) -> ListDocumentsResponse:
        response: ListDocumentsResponse = await self.stub.ListDocuments(request, metadata=self.metadata)
        return response

    async def delete_documents(self, request: DeleteDocumentsRequest) -> PartialSuccess:
        response: PartialSuccess = await self.stub.DeleteDocuments(request, metadata=self.metadata)
        return response

    async def parse_documents(self, request: ParseDocumentsRequest) -> PartialSuccess:
        response: PartialSuccess = await self.stub.ParseDocuments(request, metadata=self.metadata)
        return response

    async def stop_parsing(self, request: StopParsingRequest) -> PartialSuccess:
        response: PartialSuccess = await self.stub.StopParsing(request, metadata=self.metadata)
        return response

    async def list_chunks(self, request: ListChunksRequest) -> ListChunksResponse:
        response: ListChunksResponse = await self.stub.ListChunks(request, metadata=self.metadata)
        return response

    async def add_chunk(self, request: AddChunkRequest) -> AddChunkResponse:
        response: AddChunkResponse = await self.stub.AddChunk(request, metadata=self.metadata)
        return response

    async def remove_chunks(self, request: RemoveChunksRequest) -> PartialSuccess:
        response: PartialSuccess = await self.stub.RemoveChunks(request, metadata=self.metadata)
        return response

    async def update_chunk(self, request: UpdateChunkRequest) -> Empty:
        response: Empty = await self.stub.UpdateChunk(request, metadata=self.metadata)
        return response

    async def retrieval(self, request: RetrievalRequest) -> RetrievalResponse:
        response: RetrievalResponse = await self.stub.Retrieval(request, metadata=self.metadata)
        return response

    async def create_chat(self, request: CreateChatRequest) -> Chat:
        response: Chat = await self.stub.CreateChat(request, metadata=self.metadata)
        return response

    async def update_chat(self, request: UpdateChatRequest) -> Empty:
        response: Empty = await self.stub.UpdateChat(request, metadata=self.metadata)
        return response

    async def delete_chats(self, request: DeleteChatsRequest) -> PartialSuccess:
        response: PartialSuccess = await self.stub.DeleteChats(request, metadata=self.metadata)
        return response

    async def list_chats(self, request: ListChatsRequest) -> ChatList:
        response: ChatList = await self.stub.ListChats(request, metadata=self.metadata)
        return response

    async def create_chat_session(self, request: CreateChatSessionRequest) -> ChatSession:
        response: ChatSession = await self.stub.CreateChatSession(request, metadata=self.metadata)
        return response

    async def create_agent_session(self, request: CreateAgentSessionRequest) -> AgentSession:
        response: AgentSession = await self.stub.CreateAgentSession(request, metadata=self.metadata)
        return response

    async def update_chat_session(self, request: UpdateChatSessionRequest) -> Empty:
        response: Empty = await self.stub.UpdateChatSession(request, metadata=self.metadata)
        return response

    async def list_chat_sessions(self, request: ListChatSessionsRequest) -> ChatSessionList:
        response: ChatSessionList = await self.stub.ListChatSessions(request, metadata=self.metadata)
        return response

    async def list_agent_sessions(self, request: ListAgentSessionsRequest) -> AgentSessionList:
        response: AgentSessionList = await self.stub.ListAgentSessions(request, metadata=self.metadata)
        return response

    async def delete_chat_sessions(self, request: DeleteChatSessionsRequest) -> PartialSuccess:
        response: PartialSuccess = await self.stub.DeleteChatSessions(request, metadata=self.metadata)
        return response

    async def delete_agent_sessions(self, request: DeleteAgentSessionsRequest) -> PartialSuccess:
        response: PartialSuccess = await self.stub.DeleteAgentSessions(request, metadata=self.metadata)
        return response

    async def chat_completion(self, request: ChatCompletionRequest) -> Iterator[ChatCompletionResponse]:
        response: Iterator[ChatCompletionResponse] = await self.stub.ChatCompletion(request, metadata=self.metadata)
        return response

    async def open_ai_chat_completion(
        self, request: OpenAIChatCompletionRequest
    ) -> Iterator[OpenAIChatCompletionResponse]:
        response: Iterator[OpenAIChatCompletionResponse] = await self.stub.OpenAIChatCompletion(
            request, metadata=self.metadata
        )
        return response

    async def agent_completion(self, request: AgentCompletionRequest) -> Iterator[AgentCompletionResponse]:
        response: Iterator[AgentCompletionResponse] = await self.stub.AgentCompletion(request, metadata=self.metadata)
        return response

    async def open_ai_agent_completion(
        self, request: OpenAIAgentCompletionRequest
    ) -> Iterator[OpenAIChatCompletionResponse]:
        response: Iterator[OpenAIChatCompletionResponse] = await self.stub.OpenAIAgentCompletion(
            request, metadata=self.metadata
        )
        return response

    async def create_agent(self, request: CreateRagAgentRequest) -> Empty:
        response: Empty = await self.stub.CreateAgent(request, metadata=self.metadata)
        return response

    async def update_agent(self, request: UpdateRagAgentRequest) -> Empty:
        response: Empty = await self.stub.UpdateAgent(request, metadata=self.metadata)
        return response

    async def delete_agent(self, request: DeleteRagAgentRequest) -> Empty:
        response: Empty = await self.stub.DeleteAgent(request, metadata=self.metadata)
        return response

    async def list_agents(self, request: ListRagAgentsRequest) -> RagAgentList:
        response: RagAgentList = await self.stub.ListAgents(request, metadata=self.metadata)
        return response

    async def upload_files(self, request_iterator: Iterator[UploadFilesRequest]) -> FileList:
        response: FileList = await self.stub.UploadFiles(request_iterator, metadata=self.metadata)
        return response

    async def create_file(self, request: CreateFileRequest) -> File:
        response: File = await self.stub.CreateFile(request, metadata=self.metadata)
        return response

    async def list_files(self, request: ListFilesRequest) -> ListFilesResponse:
        response: ListFilesResponse = await self.stub.ListFiles(request, metadata=self.metadata)
        return response

    async def get_root_folder(self, request: GetRootFolderRequest) -> GetRootFolderResponse:
        response: GetRootFolderResponse = await self.stub.GetRootFolder(request, metadata=self.metadata)
        return response

    async def get_parent_folder(self, request: GetParentFolderRequest) -> GetParentFolderResponse:
        response: GetParentFolderResponse = await self.stub.GetParentFolder(request, metadata=self.metadata)
        return response

    async def get_all_parent_folders(self, request: GetAllParentFoldersRequest) -> GetAllParentFoldersResponse:
        response: GetAllParentFoldersResponse = await self.stub.GetAllParentFolders(request, metadata=self.metadata)
        return response

    async def delete_files(self, request: DeleteFilesRequest) -> Empty:
        response: Empty = await self.stub.DeleteFiles(request, metadata=self.metadata)
        return response

    async def rename_file(self, request: RenameFileRequest) -> Empty:
        response: Empty = await self.stub.RenameFile(request, metadata=self.metadata)
        return response

    async def get_file(self, request: GetFileRequest) -> Iterator[FileChunk]:
        response: Iterator[FileChunk] = await self.stub.GetFile(request, metadata=self.metadata)
        return response

    async def move_file(self, request: MoveFileRequest) -> Empty:
        response: Empty = await self.stub.MoveFile(request, metadata=self.metadata)
        return response

    async def file_to_document(self, request: FileToDocumentRequest) -> FileToDocumentList:
        response: FileToDocumentList = await self.stub.FileToDocument(request, metadata=self.metadata)
        return response

    async def dify_retrieval(self, request: DifyRetrievalRequest) -> DifyRecordList:
        response: DifyRecordList = await self.stub.DifyRetrieval(request, metadata=self.metadata)
        return response

    async def ask(self, request: AskRequest) -> Iterator[AskResponse]:
        response: Iterator[AskResponse] = await self.stub.Ask(request, metadata=self.metadata)
        return response

    async def related_questions(self, request: RelatedQuestionsRequest) -> RelatedQuestionsResponse:
        response: RelatedQuestionsResponse = await self.stub.RelatedQuestions(request, metadata=self.metadata)
        return response

    async def chatbot_completion(self, request: ChatbotCompletionRequest) -> Iterator[ChatCompletionResponse]:
        response: Iterator[ChatCompletionResponse] = await self.stub.ChatbotCompletion(request, metadata=self.metadata)
        return response

    async def chatbot_info(self, request: ChatbotInfoRequest) -> ChatbotInfoResponse:
        response: ChatbotInfoResponse = await self.stub.ChatbotInfo(request, metadata=self.metadata)
        return response

    async def agentbot_completion(self, request: AgentbotCompletionRequest) -> Iterator[AgentCompletionResponse]:
        response: Iterator[AgentCompletionResponse] = await self.stub.AgentbotCompletion(
            request, metadata=self.metadata
        )
        return response

    async def agentbot_inputs(self, request: AgentbotInputsRequest) -> AgentbotInputsResponse:
        response: AgentbotInputsResponse = await self.stub.AgentbotInputs(request, metadata=self.metadata)
        return response

    async def searchbot_ask(self, request: SearchbotAskRequest) -> Iterator[AskResponse]:
        response: Iterator[AskResponse] = await self.stub.SearchbotAsk(request, metadata=self.metadata)
        return response

    async def searchbot_retrieval(self, request: SearchbotRetrievalRequest) -> SearchbotRetrievalResponse:
        response: SearchbotRetrievalResponse = await self.stub.SearchbotRetrieval(request, metadata=self.metadata)
        return response

    async def searchbot_related_questions(self, request: SearchbotRelatedQuestionsRequest) -> RelatedQuestionsResponse:
        response: RelatedQuestionsResponse = await self.stub.SearchbotRelatedQuestions(request, metadata=self.metadata)
        return response

    async def searchbot_detail(self, request: SearchbotDetailRequest) -> SearchbotDetailResponse:
        response: SearchbotDetailResponse = await self.stub.SearchbotDetail(request, metadata=self.metadata)
        return response

    async def searchbot_mindmap(self, request: SearchbotMindmapRequest) -> Struct:
        response: Struct = await self.stub.SearchbotMindmap(request, metadata=self.metadata)
        return response
