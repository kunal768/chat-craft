from pydantic import BaseModel, Field, ConfigDict
from uuid import uuid4 

class ApiKeys(BaseModel):
    user_id: str 
    api_key: str = Field(default_factory=lambda : uuid4().hex) 
    model_config = ConfigDict(arbitrary_types_allowed=True) 

   
