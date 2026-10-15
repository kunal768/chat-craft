from pydantic import BaseModel

class EmailLoginReq(BaseModel):
    email: str
    
    class Config:
        extra = "forbid"

        