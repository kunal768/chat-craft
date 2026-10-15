from typing import Optional
from pydantic import BaseModel, Field
from src.app.models.doctype import DocType
from src.app.models.update_interval import UpdateInterval

class DocsUploadReq(BaseModel):
    user_id  : str
    doc_name : str = Field(..., max_length=255)
    doc_type : str = Field(default=DocType.PDF.name)
    doc_url : str = Field(..., max_length=300)  
    update_interval : Optional[str] = Field(default=UpdateInterval.TIME_NONE.name)

    class Config:
        extra = "forbid"