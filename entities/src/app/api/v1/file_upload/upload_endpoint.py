from fastapi import Form, File, UploadFile
from src.app.models.doctype import DocType
from src.app.models.update_interval import UpdateInterval
from src.app.api.v1.file_upload.upload_router import UploadRouter
from src.app.core.utils.error_handler import ErrorHandler


def include_route(routerobj : UploadRouter) -> None:
    @routerobj.router.post("/file")
    async def file_upload(user_id: str = Form(...),
        doc_name: str = Form(...),
        doc_type: str = Form(default=DocType.PDF.name),
        doc_url: str = Form(...),
        update_interval: str = Form(default=UpdateInterval.TIME_NONE),
        file: UploadFile = File(...)):
        try:
            doc = await routerobj.service.upload_file(
                user_id=user_id,
                doc_name=doc_name,
                doc_type=doc_type,
                doc_url=doc_url,
                update_interval=update_interval,
                file=file,
            )
            return ErrorHandler.handle_success(
                message="file upload process initiated",
                data=doc
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)
        