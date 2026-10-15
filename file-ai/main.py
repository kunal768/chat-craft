from langchain_ollama import OllamaEmbeddings, OllamaLLM
from fastapi import FastAPI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from app.core.db.connect import ping_server
from contextlib import asynccontextmanager
from os import environ
from langchain_ollama import OllamaEmbeddings
from app.crud.file_search.service import FileSearchService
from app.crud.file_upload.service import FileUploadService
from app.crud.llm_query.service import LLMQueryService
from app.core.utils.doc_loader import DocumentLoaders
from app.api.v1.upload_file.upload_router import UploadRouter
from app.api.v1.query.query_router import QueryRouter
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # load env, configs, etc.

    env_variables = {
        "mongo_uri" : str(environ.get('MONGO_URI')),
        "embed_model_name" : str(environ.get('EMBED_MODEL_NAME')),
        "llm_model_name" : str(environ.get('LLM_MODEL_NAME')),
        "db_name" : str(environ.get('db_name')),
        "collection_name" : str(environ.get('collection_name')),
        "vector_search_index" : str(environ.get('vector_search_index')),
        "doc_storage_path" : str(environ.get('storage_path')),
    }

    # Initialize client connections
    embed_model = OllamaEmbeddings(model=env_variables['embed_model_name'])
    genai_model = OllamaLLM(model=env_variables['llm_model_name'], temperature=0)

    # database client 
    client = await ping_server(env_variables['mongo_uri'])
    if isinstance(client, Exception):
        # throw error and exit
        print("error connecting to mongodb client")
        return 
    
    database_name = env_variables['db_name']
    collection_name = env_variables['collection_name']
    namespace = f"{database_name}.{collection_name}"
    collection = client.get_database(database_name).get_collection(collection_name)


    vector_store = MongoDBAtlasVectorSearch.from_connection_string(
        connection_string = env_variables['mongo_uri'],        
        namespace = namespace,  # Database and collection name
        embedding = embed_model,
        index = env_variables['vector_search_index'],
    )

    doc_loaders = DocumentLoaders()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=20)

    # load services 
    file_upload_service = FileUploadService(
                            vector_stores=vector_store, 
                            doc_loaders=doc_loaders, 
                            text_splitter=text_splitter, 
                            storage_location=env_variables['doc_storage_path']
    )

    vector_search_service = FileSearchService(
                            embed_model=embed_model, 
                            collection=collection
    )

    llm_query_service = LLMQueryService(llm_model=genai_model)


    # routers 
    upload_router = UploadRouter(service=file_upload_service)
    query_router = QueryRouter(search_svc=vector_search_service, query_svc=llm_query_service)

    # include endpoints
    app.include_router(upload_router.include_all_routes())
    app.include_router(query_router.include_all_routes())


    yield
    
    #shutdown 
    client.close()
    vector_store.close()


app = FastAPI(lifespan=lifespan)