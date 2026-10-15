from src.app.api.v1.docs.docs_router import DocsRouter
from src.app.core.utils.error_handler import ErrorHandler


def include_route(routerobj : DocsRouter) -> None:
    @routerobj.router.get("/doc_id")
    async def get_doc_by_id(doc_id: str):
        try:
            doc = await routerobj.docs_service.get_doc_by_id(doc_id=doc_id)
            return ErrorHandler.handle_success(
                data={"doc": doc},
                message="document found"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)
        