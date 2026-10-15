from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from src.app.models.document import Document
from bson import ObjectId
from datetime import datetime, timezone

class UserDocs(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id", default=None)
    user_id: str
    docs: List[Document] = Field(default_factory=list)  
    update_time : str = Field(default= datetime.now(timezone.utc).isoformat())
    model_config = ConfigDict(arbitrary_types_allowed=True) 
    


    