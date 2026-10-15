from pydantic import BaseModel, ConfigDict
from pydantic import Field
from datetime import datetime, timezone
from src.app.models.doctype import DocType
from src.app.models.update_interval import UpdateInterval
from uuid import uuid4

class Document(BaseModel):
    doc_id : str = Field(default_factory= lambda: uuid4().hex)
    doc_name : str = Field(max_length=255)
    doc_type : str = Field(default=DocType.PDF.name)
    doc_url : str = Field(max_length=300)   
    doc_created_at : datetime = Field(default_factory= lambda : datetime.now(timezone.utc))
    doc_updated_at : datetime = Field(default_factory= lambda : datetime.now(timezone.utc))
    update_interval : str = Field(default=UpdateInterval.TIME_NONE.name)
    model_config = ConfigDict(arbitrary_types_allowed=True) 




