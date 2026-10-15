import os 

def get_file_type(file_path: str) -> str:
        _, ext = os.path.splitext(file_path)
        return ext.lower()

def extract_text(doc):
        for field in ["page_content", "text", "content", "body"]:
                if field in doc:
                        return doc[field]
        return str(doc)