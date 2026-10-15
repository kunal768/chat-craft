from motor.motor_asyncio import AsyncIOMotorClient
from src.app.models.user import User 
from bson import ObjectId


class Repository:
    def __init__(self, client: AsyncIOMotorClient):
        self.collection =  client.get_database("test_d").get_collection("users")

    async def create_user(self, user: User) -> str | None:
        try:
            res = await self.collection.insert_one(user.model_dump())
            return res.inserted_id if res else ""
        except Exception as e:
            raise e 
    
    async def delete_user(self, user_id: str):
        try:
            user = await self.collection.delete_one({"_id": ObjectId(user_id)})
            if not user : return None
            return user
        except Exception as e:
            raise e 

    async def get_user_by_email(self, email: str):
        try:
            user = await self.collection.find_one({"email": email})
            if not user : return None
            return user
        except Exception as e:
            raise e 
    
    async def get_user_id_by_email(self, email: str) -> str | Exception :
        try:
            user = await self.collection.find_one({"email": email})
            if not user : return ""
            return user["user_id"]
        except Exception as e:
            raise e  
        
    async def get_user_by_id(self, user_id: str):
        try:
            user = await self.collection.find_one({"_id": ObjectId(user_id)})
            return user 
        except Exception as e:
            raise e 
   


