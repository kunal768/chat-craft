import pytest
from unittest.mock import Mock, AsyncMock, patch
from fastapi import File
from app.crud.file_upload.service import FileUploadService
from app.crud.file_search.service import FileSearchService
from app.crud.llm_query.service import LLMQueryService
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_core.documents import Document
import os

# Test data
TEST_USER_ID = "test_user_123"
TEST_QUERY = "test query"
TEST_FILE_CONTENT = b"test file content"
TEST_FILE_NAME = "test.txt"
TEST_STORAGE_PATH = "/tmp/test_storage"
TEST_DOCUMENTS = [
    Document(page_content="Document 1", metadata={"user_id": TEST_USER_ID}),
    Document(page_content="Document 2", metadata={"user_id": TEST_USER_ID})
]

class AsyncCursor:
    def __init__(self, items):
        self._items = items
    def __aiter__(self):
        self._iter = iter(self._items)
        return self
    async def __anext__(self):
        try:
            return next(self._iter)
        except StopIteration:
            raise StopAsyncIteration

@pytest.fixture
def mock_vector_store():
    return AsyncMock()

@pytest.fixture
def mock_doc_loaders():
    return AsyncMock()

@pytest.fixture
def mock_text_splitter():
    return RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=20)

@pytest.fixture
def mock_embed_model():
    return AsyncMock(spec=OllamaEmbeddings)

@pytest.fixture
def mock_collection():
    return AsyncMock()

@pytest.fixture
def mock_llm_model():
    return AsyncMock(spec=OllamaLLM)

@pytest.fixture
def file_upload_service(mock_vector_store, mock_doc_loaders, mock_text_splitter):
    return FileUploadService(
        vector_stores=mock_vector_store,
        doc_loaders=mock_doc_loaders,
        text_splitter=mock_text_splitter,
        storage_location=TEST_STORAGE_PATH
    )

@pytest.fixture
def file_search_service(mock_embed_model, mock_collection):
    return FileSearchService(
        embed_model=mock_embed_model,
        collection=mock_collection
    )

@pytest.fixture
def llm_query_service(mock_llm_model):
    return LLMQueryService(llm_model=mock_llm_model)

class TestFileUploadService:
    @pytest.mark.asyncio
    async def test_store_file_locally_success(self, file_upload_service):
        # Create a mock file
        mock_file = Mock(spec=File)
        mock_file.filename = TEST_FILE_NAME
        mock_file.read = AsyncMock(return_value=TEST_FILE_CONTENT)

        # Create test directory if it doesn't exist
        os.makedirs(TEST_STORAGE_PATH, exist_ok=True)

        success, file_location = await file_upload_service.store_file_locally(mock_file)
        
        assert success is True
        assert file_location == os.path.join(TEST_STORAGE_PATH, TEST_FILE_NAME)
        assert os.path.exists(file_location)

        # Cleanup
        os.remove(file_location)

    @pytest.mark.asyncio
    async def test_parse_and_add_file_success(self, file_upload_service, mock_doc_loaders, mock_vector_store):
        # Setup mocks
        mock_doc_loaders.parse_doc.return_value = TEST_DOCUMENTS
        mock_vector_store.aadd_documents = AsyncMock()

        result = await file_upload_service.parse_and_add_file(TEST_USER_ID, "test_path.txt")
        
        assert result is True
        mock_doc_loaders.parse_doc.assert_called_once_with(file_path="test_path.txt")
        mock_vector_store.aadd_documents.assert_called_once()

class TestFileSearchService:
    pass

class TestLLMQueryService:
    @pytest.mark.asyncio
    async def test_async_structured_answer(self, llm_query_service, mock_llm_model):
        # Setup mocks
        mock_llm_model.ainvoke = AsyncMock(return_value="Test response")
        
        response = await llm_query_service.async_structured_answer(TEST_QUERY, TEST_DOCUMENTS)
        
        assert response == "Test response"
        mock_llm_model.ainvoke.assert_called_once()
