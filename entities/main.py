from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.app.core.db.connect import ping_server
from src.app.crud.user.service import UserService
from src.app.crud.docs.service import DocsService
from src.app.crud.apikeys.service import ApiKeysService
from src.app.crud.file_upload.service import FileUploadService
from src.app.crud.user.repo import Repository
from src.app.crud.docs.repo import DocsRepo
from src.app.crud.apikeys.repo import ApiKeysRepo
from src.app.api.v1.users.user_router import UserRouter
from src.app.api.v1.docs.docs_router import DocsRouter
from src.app.api.v1.file_upload.upload_router import UploadRouter
from src.app.api.v1.query_prompt.query_router import QueryRouter
from httpx import AsyncClient 
from os import environ
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # load env 
    env_variables = {
        "mongo_uri" : str(environ.get('MONGO_URI')),
        "file_service_uri" : str(environ.get('FILE_SVC_URI')),
        "file_service_apikey" : str(environ.get('FILE_SVC_APIKEY')),
    }

    # Initialize client connections

    # database client 
    client = await ping_server(env_variables['mongo_uri'])
    if isinstance(client, Exception):
        # throw error and exit
        print("error connecting to mongodb client")
        return 

    # httpx client 
    httpx_client = AsyncClient(timeout=60)


    # Initialize repositories
    user_repo = Repository(client)
    docs_repo = DocsRepo(client)
    apikeys_repo = ApiKeysRepo(client)


    
    # Initialize services
    apikeys_service = ApiKeysService(repo=apikeys_repo)

    docs_service = DocsService(repo=docs_repo)

    user_service = UserService(
        repo=user_repo, 
        api_keys_service = apikeys_service, 
        docs_service = docs_service
    )
    
    
    file_upload_service = FileUploadService(
        base_url=env_variables['file_service_uri'], 
        api_key=env_variables['file_service_apikey'],
        client=httpx_client,
        docs_service=docs_service,
    )


    # Initialize routers 
    user_router = UserRouter(user_service=user_service)
    docs_router = DocsRouter(docs_service=docs_service)
    upload_router = UploadRouter(service=file_upload_service)
    query_router = QueryRouter(service=file_upload_service)
   
    app.include_router(user_router.include_user_routes())
    app.include_router(docs_router.include_docs_routes())
    app.include_router(upload_router.include_upload_routes())
    app.include_router(query_router.include_query_routes())

    yield

    # shutdown 
    await httpx_client.aclose() 
    client.close()

app = FastAPI(lifespan=lifespan)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

