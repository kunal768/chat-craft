from pydantic import BaseModel
from src.app.core.utils.status_codes import StatusCodes
from src.app.core.utils.errors import CustomException

class StdResponse(BaseModel):
    message: str
    error: str | None = None
    data: dict | None = None
    status_code: int
    success: bool
    
    class Config:
        extra = "forbid"
        
        
        
        
