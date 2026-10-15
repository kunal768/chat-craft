from enum import Enum

class DocType(Enum):
    GOOGLE_SHEET = "Google Sheets"
    GOOGLE_DOC = "Google Docs"
    DOCX = "Docx"
    PDF = "PDF"
    CSV = "CSV"
    
    class Config:
        orm_mode = True
