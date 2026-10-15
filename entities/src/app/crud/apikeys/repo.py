from src.app.models.apikeys import ApiKeys
from motor.motor_asyncio import AsyncIOMotorClient


class ApiKeysRepo:
    def __init__(self, client: AsyncIOMotorClient):
        self.collection = client.get_database("test_d").get_collection("api_keys")
    
    async def fetch_doc_by_id(self, id):
        try:
            inserted_doc = await self.collection.find_one({"_id": id})
            return inserted_doc
        except Exception as e :
            raise e

    async def create_api_key(self, api_key: ApiKeys):
        try:
            res = await self.collection.insert_one(api_key.model_dump()) 
            return res
        except Exception as e:
            raise e 
        
    async def get_api_key(self, api_key: ApiKeys):
        try:
            res = await self.collection.find_one({"api_key": api_key.api_key})
            return res
        except Exception as e:
            raise e 
        
    async def get_api_key_by_user_id(self, user_id: str):
        try:
            res = await self.collection.find_one({"user_id": user_id})
            return res
        except Exception as e:
            raise e 
        