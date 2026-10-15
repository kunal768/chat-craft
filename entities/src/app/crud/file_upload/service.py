from fastapi import UploadFile, Form, File
from httpx import AsyncClient, TimeoutException
from src.app.crud.docs.service import DocsService
from src.app.models.document import Document
from src.app.models.doctype import DocType
from src.app.models.update_interval import UpdateInterval
import asyncio

class FileUploadService:
    def __init__(self, base_url : str, api_key : str, client : AsyncClient, docs_service : DocsService):
        self.client = client 
        self.base_url = base_url
        self.api_key = api_key
        self.docs_serive = docs_service
    
    async def upload_file(self, 
        user_id: str = Form(...),
        doc_name: str = Form(...),
        doc_type: str = Form(default=DocType.PDF.name),
        doc_url: str = Form(...),
        update_interval: str = Form(default=UpdateInterval.TIME_NONE),
        file: UploadFile = File(...)
        ):
        file_bytes = await file.read()
        files = {'file': (file.filename, file_bytes, file.content_type)}
        headers = {'x-api-key' : self.api_key, "user-id" : user_id}
        response = await self.client.post(
            f"{self.base_url}/upload/",
            files=files,
            headers=headers
        )
        #TODO: handle response status
        response.raise_for_status()
        #TODO: convert it into proper response model 
        # update db 
        doc = Document(
            doc_name=doc_name,
            doc_type=doc_type,
            doc_url=doc_url,
            update_interval=update_interval
        )
        await self.docs_serive.add_document(user_id=user_id, doc=doc)
        return response.json()
    
    
    async def query_prompt(self, user_id: str, query: str) -> dict:
        """
        Calls the /query/prompt endpoint with the given user_id and query.
        """
        url = f"{self.base_url}/query/prompt"
        headers = {
            "accept": "application/json",
            "user-id": user_id,
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        json_body = {"query": query}
        try:
            response = await asyncio.wait_for(
                self.client.post(url, headers=headers, json=json_body),
                timeout=60
            )
            response.raise_for_status()
            print("response from svc", response.json())
            return response.json()
        except asyncio.TimeoutError:
            print("LLM service timed out")
            return {"error": "LLM service timed out"}
        except TimeoutException:
            print("HTTPX timeout")
            return {"error": "LLM service HTTPX timeout"}
        except Exception as e:
            print(f"Error calling LLM service: {e}")
            return {"error": str(e)}
        
    # async def query_prompt(self, user_id: str, query: str) -> dict:
    #     """
    #     Calls the /query/prompt endpoint with the given user_id and query.
    #     """
    #     url = f"{self.base_url}/query/prompt"
    #     headers = {
    #         "accept": "application/json",
    #         "user-id": user_id,
    #         "x-api-key": self.api_key,
    #         "Content-Type": "application/json"
    #     }
    #     json_body = {"query": query}
    #     response = await self.client.post(url, headers=headers, json=json_body)
    #     response.raise_for_status()
    #     print("response from svc", response.json())
    #     return response.json()



        

    