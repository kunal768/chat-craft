from src.app.models.userdocs import UserDocs
from src.app.models.document import Document
from src.app.crud.docs.repo import DocsRepo
from src.app.core.utils.errors import CustomException
from typing import List
from src.app.core.utils.errors import (
    DocumentNotFoundError,
    DocumentCreationError,
    DocumentUpdateError,
    DocumentDeletionError,
    InvalidDocumentDataError
)

class DocsService:
    def __init__(self, repo: DocsRepo):
        self.repo = repo

    async def create_userdoc(self, doc: UserDocs) -> UserDocs:
        try:
            result = await self.repo.create_userdoc(doc)
            if isinstance(result, Exception):
                raise DocumentCreationError(str(result))
            return result
        except Exception as e:
            if isinstance(e, CustomException):
                raise e
            raise DocumentCreationError(str(e))
    
    async def get_doc_by_id(self, doc_id: str) -> Document:
        try:
            if not doc_id:
                raise InvalidDocumentDataError("Document ID is required")
            result = await self.repo.get_doc_by_id(doc_id)
            if not result or isinstance(result, Exception):
                raise DocumentNotFoundError(f"Document with ID {doc_id} not found")
            return result
        except Exception as e:
            if isinstance(e, CustomException):
                raise e
            raise DocumentNotFoundError(str(e))
    
    async def get_all_docs_by_userid(self, user_id : str) -> List[Document]:
        try:
            result = await self.repo.get_all_docs_by_userid(user_id)
            if isinstance(result, Exception):
                raise DocumentNotFoundError("Failed to fetch documents")
            return result
        except Exception as e:
            if isinstance(e, CustomException):
                raise e
            raise DocumentNotFoundError(str(e))
    
    async def update_doc(self, doc_id: str, doc: Document) -> Document:
        try:
            if not doc_id or not doc:
                raise InvalidDocumentDataError("Document ID and data are required")
            result = await self.repo.update_doc(doc_id, doc)
            if isinstance(result, Exception):
                raise DocumentUpdateError(f"Failed to update document with ID {doc_id}")
            return doc
        except Exception as e:
            if isinstance(e, CustomException):
                raise e
            raise DocumentUpdateError(str(e))
    
    async def delete_doc(self, doc_id: str) -> bool:
        try:
            if not doc_id:
                raise InvalidDocumentDataError("Document ID is required")
            result = await self.repo.delete_doc(doc_id)
            if isinstance(result, Exception):
                raise DocumentDeletionError(f"Failed to delete document with ID {doc_id}")
            return True 
        except Exception as e:
            if isinstance(e, CustomException):
                raise e
            raise DocumentDeletionError(str(e))
   
    async def get_docs_by_user_id_and_status(self, user_id: str, status: bool) -> List[Document]:
        try:
            if not user_id:
                raise InvalidDocumentDataError("User ID is required")
            result = await self.repo.get_docs_by_user_id_and_status(user_id, status)
            if isinstance(result, Exception):
                raise DocumentNotFoundError(f"Failed to fetch documents for user {user_id}")
            return result
        except Exception as e:
            if isinstance(e, CustomException):
                raise e
            raise DocumentNotFoundError(str(e))
    
    async def get_docs_by_user_id(self, user_id: str) -> List[Document]:
        try:
            if not user_id:
                raise InvalidDocumentDataError("User ID is required")
            result = await self.repo.get_docs_by_user_id(user_id)
            if isinstance(result, Exception):
                raise DocumentNotFoundError(f"Failed to fetch documents for user {user_id}")
            return result
        except Exception as e:
            if isinstance(e, CustomException):
                raise e
            raise DocumentNotFoundError(str(e))
    
    async def add_document(self, user_id : str, doc : Document):
        try:
            if not user_id:
                raise InvalidDocumentDataError("User ID is required")
            result = await self.repo.upload_doc(user_id=user_id, doc=doc)
            if isinstance(result, Exception):
                raise DocumentNotFoundError(f"Failed to fetch documents for user {user_id}")
            return result
        except Exception as e:
            if isinstance(e, CustomException):
                raise e
            raise DocumentNotFoundError(f"Failed to fetch documents for user {user_id}")
    
            

    