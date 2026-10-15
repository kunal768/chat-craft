from src.app.models.apikeys import ApiKeys
from src.app.crud.apikeys.repo import ApiKeysRepo


class ApiKeysService:
    def __init__(self, repo: ApiKeysRepo):
        self.repo = repo

    async def create_api_key(self, api_key: ApiKeys) -> ApiKeys | Exception :
        res = await self.repo.create_api_key(api_key)
        inserted_doc = await self.repo.fetch_doc_by_id(res.inserted_id)
        return api_key
    
    async def get_api_key(self, api_key: ApiKeys) -> ApiKeys | Exception :
        res = await self.repo.get_api_key(api_key)
        return ApiKeys.model_validate(res)

    
    async def get_api_key_by_user_id(self, user_id: str) -> ApiKeys | Exception :
        res = await self.repo.get_api_key_by_user_id(user_id)
        return ApiKeys.model_validate(res)
    
    async def create_api_key_for_user(self, user_id: str) -> ApiKeys | Exception :
        res = await self.repo.create_api_key(ApiKeys(user_id=user_id))
        return ApiKeys.model_validate(res)
    