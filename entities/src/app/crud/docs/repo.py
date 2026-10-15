from src.app.models.userdocs import UserDocs
from motor.motor_asyncio import AsyncIOMotorClient
from src.app.models.document import Document
from typing import List
from datetime import datetime, timezone
from src.app.core.utils.errors import UserNotFoundError

class DocsRepo:
    def __init__(self, client: AsyncIOMotorClient):
        self.collection = client.get_database("test_d").get_collection("userdocs")


    async def create_userdoc(self, docs: UserDocs):
        try:
            doc_dump = docs.model_dump()
            result = await self.collection.insert_one(doc_dump)
            inserted_doc = await self.collection.find_one({"_id": result.inserted_id})
            if not inserted_doc or not isinstance(inserted_doc, dict):
                raise ValueError("Inserted document not found or not a valid dict")
            inserted_doc.pop('_id', None)
            return UserDocs(**inserted_doc)
        except Exception as e:
            # Handle exceptions as needed
            raise e
        
    async def get_doc_by_id(self, doc_id: str) :
        try:
            doc = await self.collection.find_one({"docs.doc_id": doc_id})
            return doc
        except Exception as e:
            raise e 

    async def get_all_docs_by_userid(self, user_id : str) -> List[Document]:
        try:
            filter = {"user_id" : user_id}
            projections = {
                "user_id" : 0,
                "docs" : 1,
                "update_time" : 0
            }
            docs = await self.collection.find_one(filter, projections)
            if not docs :
                raise FileNotFoundError("Document not found")
            return list(Document(**doc) for doc in docs) 
        except Exception as e:
            raise e 
        
    async def update_doc(self, doc_id: str, doc: Document):
        try:
            res = await self.collection.update_one({"doc_id": doc_id}, {"$set": doc.model_dump()})
            return 
        except Exception as e:
            raise e 
        
    async def delete_doc(self, doc_id: str) -> bool | Exception :
        try:
            doc = await self.collection.delete_one({"doc_id": doc_id})
            if not doc :
                raise FileNotFoundError("Document not found")
            return True 
        except Exception as e:
            raise e 
        
    async def get_docs_by_user_id(self, user_id: str) -> List[Document] | Exception :
        try:
            docs = await self.collection.find({"user_id": user_id}).to_list(length=100)   
            return docs 
        except Exception as e:
            raise e 
        
    async def get_docs_by_doc_id(self, doc_id: str) :
        try:
            doc = await self.collection.find_one({"doc_id": doc_id})
            if not doc : return None
            return doc
        except Exception as e:
            raise e 
        
    async def get_docs_by_doc_name(self, doc_name: str):
        try:
            doc = await self.collection.find_one({"doc_name": doc_name})
            return doc 
        except Exception as e:
            raise e 
        
    async def get_docs_by_doc_type(self, doc_type: str):
        try:
            docs = await self.collection.find({"doc_type": doc_type}).to_list(length=100)
            return docs
        except Exception as e:
            raise e 
        
    async def get_docs_by_doc_url(self, doc_url: str):
        try:
            doc = await self.collection.find_one({"doc_url": doc_url})
            return doc
        except Exception as e:
            raise e     
    
    async def get_docs_by_doc_created_at(self, doc_created_at: datetime):
        try:
            docs = await self.collection.find({"doc_created_at": doc_created_at}).to_list(length=100)
            return docs 
        except Exception as e:
            raise e 

    async def get_docs_by_doc_updated_at(self, doc_updated_at: datetime):
        try:
            docs = await self.collection.find({"doc_updated_at": doc_updated_at}).to_list(length=100)
            return docs 
        except Exception as e:
            raise e 
                    
    async def get_docs_by_user_id_and_status(self, user_id: str, status: bool):
        try:
            docs = await self.collection.find({
                "user_id": user_id,
                "status": status
            }).to_list(length=100)
            return docs 
        
        except Exception as e:
            raise e
    
    async def upload_doc(self, user_id : str, doc : Document):
        try:
            user_doc_obj = await self.collection.update_one(
                {"user_id": user_id},  # Filter: Find the user by user_id
                {
                    "$push": {"docs": doc.model_dump()},  # Append the new document to the docs list
                    "$set": {"update_time": datetime.now(timezone.utc).isoformat()}  # Update timestamp
                }
            )

            if user_doc_obj.matched_count == 0:
                raise UserNotFoundError("user not found")

            return user_doc_obj
        
        except Exception as e :
            raise e 