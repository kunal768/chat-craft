from fastapi import Header
from app.api.v1.query.query_router import QueryRouter
from app.core.utils.error_handler import ErrorHandler
from app.schemas.query_req import QueryRequest

def include_route(routerobj: QueryRouter) -> None:
    @routerobj.router.post("/prompt")
    async def prompt_query(
        req : QueryRequest,
        user_id: str = Header(..., alias="user-id"),
    ):
        try:
            docs = await routerobj.search_svc.vector_search(
                user_id=user_id,
                query=req.query
            )

            answer = await routerobj.query_svc.async_structured_answer(
                query=req.query,
                docs=docs,
            )

            return ErrorHandler.handle_success(
                message="answer generation successfull",
                data={
                    "llm_answer" : answer,
                }
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)

        