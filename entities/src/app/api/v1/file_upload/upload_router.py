from fastapi import APIRouter, Depends
from src.app.api.v1.base_router import BaseRouter
from src.app.crud.file_upload.service import FileUploadService
from src.app.core.utils.singleton import Singleton


class UploadRouter(BaseRouter, metaclass = Singleton):
    def __init__(self, service: FileUploadService = Depends(FileUploadService)):
        super().__init__(
            prefix="/v1/upload",
            tags=["upload"]
        )
        self.service = service

    def include_upload_routes(self) -> APIRouter:
        from src.app.api.v1.file_upload import upload_endpoint

        upload_endpoint.include_route(self)
        
        return self.router