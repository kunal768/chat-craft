from pydantic import BaseModel
from app.core.utils.status_codes import StatusCodes
from app.core.utils.errors import CustomException

class StdResponse(BaseModel):
    message: str
    error: str | None = None
    data: dict | None = None
    status_code: int
    success: bool
    
    class Config:
        extra = "forbid"
        
        
        
        
