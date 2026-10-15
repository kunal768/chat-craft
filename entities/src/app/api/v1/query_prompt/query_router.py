from fastapi import APIRouter, Depends
from src.app.api.v1.base_router import BaseRouter
from src.app.crud.file_upload.service import FileUploadService
from src.app.core.utils.singleton import Singleton


class QueryRouter(BaseRouter, metaclass = Singleton):
    def __init__(self, service: FileUploadService = Depends(FileUploadService)):
        super().__init__(
            prefix="/v1/query",
            tags=["query"]
        )
        self.service = service

    def include_query_routes(self) -> APIRouter:
        from src.app.api.v1.query_prompt import prompt_query

        prompt_query.include_route(self)
        
        return self.router