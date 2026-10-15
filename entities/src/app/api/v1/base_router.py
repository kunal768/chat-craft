from fastapi import APIRouter, Depends
from src.app.core.security.api_key_validator import validate_api_key
from typing import List
from enum import Enum


class BaseRouter:
    def __init__(self, prefix: str, tags: List[str | Enum] | None):
        self.router = APIRouter(
            prefix=prefix,
            tags=tags,  
            dependencies=[Depends(validate_api_key)]
        )
    
    def get_router(self) -> APIRouter:
        return self.router

