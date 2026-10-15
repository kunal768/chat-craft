from src.app.api.v1.query_prompt.query_router import QueryRouter
from src.app.core.utils.error_handler import ErrorHandler
from src.app.schemas.query.query_req import QueryRequest


def include_route(routerobj : QueryRouter) -> None:
    @routerobj.router.post("/prompt")
    async def prompt_query(
        req : QueryRequest,
        user_id: str
        ):
        try:
            query_answer = await routerobj.service.query_prompt(
                user_id=user_id,
                query=req.query,
            )
            return ErrorHandler.handle_success(
                message="query_answered_successfully",
                data={
                    "answer" : query_answer,
                }
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)
        