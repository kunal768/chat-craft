from fastapi import APIRouter, Depends
from app.api.v1.base_router import BaseRouter
from app.core.utils.singleton import Singleton
from app.crud.file_search.service import FileSearchService
from app.crud.llm_query.service import LLMQueryService


class QueryRouter(BaseRouter, metaclass = Singleton):
    def __init__(self, search_svc: FileSearchService, query_svc : LLMQueryService):
        super().__init__(
            prefix="/query",
            tags=["query"]
        )
        self.search_svc = search_svc
        self.query_svc = query_svc

    def include_all_routes(self) -> APIRouter:
        from app.api.v1.query import prompt_query

        prompt_query.include_route(self)
        
        return self.router