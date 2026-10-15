from fastapi import HTTPException, Header
from os import environ
from app.core.utils.status_codes import StatusCodes
from typing import Annotated


def validate_api_key(x_api_key: Annotated[str, Header()]):
    if x_api_key != environ.get('API_KEY'):
        raise HTTPException(status_code=StatusCodes.UNAUTHORIZED.value, detail="Invalid API key")


