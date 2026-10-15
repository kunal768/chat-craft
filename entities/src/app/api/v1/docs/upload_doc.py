from src.app.api.v1.docs.docs_router import DocsRouter
from src.app.core.utils.error_handler import ErrorHandler
from src.app.schemas.docs.doc_upload_req import DocsUploadReq
from src.app.models.document import Document


def include_route(routerobj : DocsRouter) -> None:
    @routerobj.router.post("/upload")
    async def upload_doc(docobj : DocsUploadReq):
        try:
            doc = Document(
                doc_name=docobj.doc_name,
                doc_type=docobj.doc_type,
                doc_url=docobj.doc_url,
                update_interval=str(docobj.update_interval)
            )
            _ = await routerobj.docs_service.add_document(user_id=docobj.user_id, doc=doc)
            return ErrorHandler.handle_success(
                data={"doc": doc},
                message="document uploaded"
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)
        
