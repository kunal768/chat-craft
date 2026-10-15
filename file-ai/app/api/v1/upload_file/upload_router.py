from fastapi import APIRouter, Depends
from app.api.v1.base_router import BaseRouter
from app.core.utils.singleton import Singleton
from app.crud.file_upload.service import FileUploadService


class UploadRouter(BaseRouter, metaclass = Singleton):
    def __init__(self, service: FileUploadService = Depends(FileUploadService)):
        super().__init__(
            prefix="/upload",
            tags=["upload"]
        )
        self.service = service

    def include_all_routes(self) -> APIRouter:
        from app.api.v1.upload_file import upload_endpoint

        upload_endpoint.include_route(self)
        
        return self.router