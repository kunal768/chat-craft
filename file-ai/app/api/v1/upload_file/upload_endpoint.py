from fastapi import  UploadFile, File, Header
from app.api.v1.upload_file.upload_router import UploadRouter
from app.core.utils.error_handler import ErrorHandler

def include_route(routerobj: UploadRouter) -> None:
    @routerobj.router.post("/")
    async def file_upload(
        file: UploadFile = File(...),
        user_id: str = Header(..., alias="user-id"),
    ):
        try:
            stored_locally, path = await routerobj.service.store_file_locally(
                file=file,
            )
            if not stored_locally:
                raise Exception("error storing file locally")
            
            # vector store file content 
            status = await routerobj.service.parse_and_add_file(user_id=user_id, file_path=path)

            if not status:
                raise Exception("could not store file content in storage vector")

            return ErrorHandler.handle_success(
                message="file uploaded and stored as vector",
                data={
                    "status" : status,
                }
            )
        except Exception as e:
            return ErrorHandler.handle_error(e)

        