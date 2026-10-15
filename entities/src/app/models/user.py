from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime, timezone

            
class User(BaseModel):
    email: EmailStr
    name: str = Field(max_length=100)
    created_at: datetime = Field(default_factory=lambda : datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda : datetime.now(timezone.utc))
    model_config = ConfigDict(arbitrary_types_allowed=True) 

  
