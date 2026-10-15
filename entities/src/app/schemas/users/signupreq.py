from pydantic import BaseModel, Field, EmailStr


class SignUpReq(BaseModel):
    email: EmailStr
    name: str = Field(..., max_length=100)
    
    class Config:
        extra = "forbid"

        
        