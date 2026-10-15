from fastapi import File
from app.core.utils.doc_loader import DocumentLoaders
from langchain.text_splitter import TextSplitter
from os import path


class FileUploadService:
    def __init__(self, vector_stores, doc_loaders : DocumentLoaders, text_splitter: TextSplitter, storage_location : str):
        self.vector_stores = vector_stores
        self.doc_loaders = doc_loaders
        self.text_splitter = text_splitter
        self.storage_location = storage_location
    
    async def store_file_locally(self, file : File):
        try :
            file_location = path.join(self.storage_location, file.filename)
            with open(file_location, "wb") as buffer:
                buffer.write(await file.read())
            return True , file_location
        except Exception as e:
            raise e

    
    async def parse_and_add_file(self, user_id : str, file_path : str):
        try :
            file_content = await self.doc_loaders.parse_doc(file_path=file_path)
            if isinstance(file_content, Exception):
                raise Exception("error uploading file")
            documents = self.text_splitter.split_documents(file_content) 
            for doc in documents:
                if hasattr(doc, "metadata"):
                    doc.metadata["user_id"] = user_id
                else:
                    doc.metadata = {"user_id": user_id}
            _ = await self.vector_stores.aadd_documents(documents=documents)
            return True
        
        except Exception as e :
                raise e 



        
