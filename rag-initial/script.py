from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.document_loaders import PyPDFLoader, CSVLoader, Docx2txtLoader, UnstructuredHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import asyncio
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from dotenv import load_dotenv
from os import environ
from pymongo import MongoClient
load_dotenv()

database_name = "test_d"
collection_name = "doc_vectors"
namespace = f"{database_name}.{collection_name}"
mongo_uri = str(environ.get('MONGO_URI'))
mongo_client = MongoClient(mongo_uri)
db = mongo_client['test_d']
collection = db[collection_name]


pdf_path = str(environ.get('pdf_path'))
csv_path = str(environ.get('csv_path'))
docx_path =str(environ.get('docx_path'))
html_path =str(environ.get('html_path'))

model_name = "nomic-embed-text" # "mxbai-embed-large"
embed_model = OllamaEmbeddings(model=model_name)
genai_model = OllamaLLM(model="llama2", temperature=0)

# Instantiate the vector store using your MongoDB connection string
vector_store = MongoDBAtlasVectorSearch.from_connection_string(
  connection_string = mongo_uri,        # Atlas cluster or local deployment URI
  namespace = namespace,  # Database and collection name
  embedding = embed_model,
  index = "vectorsearch",
)

async def vector_search(query: str, num_candidates=100, limit=5):
    # 1. Generate the embedding for the query
    query_vector = await embed_model.aembed_query(query)  # Should return a list of floats

    # 2. Build the aggregation pipeline
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vectorsearch",
                "path": "embedding",
                "queryVector": query_vector,
                "numCandidates": num_candidates,
                "limit": limit
            }
        }
    ]

    # 3. Run the aggregation
    results = collection.aggregate(pipeline)
    return list(results)

from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
You are an assistant for business document summarization.
ONLY use the information provided in the documents below to answer the question.
If the answer is not present in the documents, reply: "I don't know based on the provided documents."
Be concise and structured.

Question: {question}

Documents:
{documents}

Answer:
""")

chain = prompt | genai_model

async def async_structured_answer(query: str, docs: list):
    """
    Args:
        query (str): The user's question.
        docs (list): List of MongoDB documents (dicts).
    Returns:
        str: The structured answer from the LLM.
    """
    # Extract text from MongoDB docs (customize field as needed)
    def extract_text(doc):
        # Try common text fields
        for field in ["page_content", "text", "content", "body"]:
            if field in doc:
                return doc[field]
        return str(doc)

    documents_str = "\n\n".join([extract_text(doc) for doc in docs])

    response = await chain.ainvoke({
        "question": query,
        "documents": documents_str
    })

    return response

# csv_path: str, pdf_path: str
async def parse(csv_path, pdf_path) -> list[list[float]]:
        csv_loader, pdf_loader, docx_loader, html_loader = CSVLoader(csv_path), PyPDFLoader(pdf_path), Docx2txtLoader(docx_path), UnstructuredHTMLLoader(html_path)
        csv_content = await csv_loader.aload()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=20)
        documents = text_splitter.split_documents(csv_content)
        store_success = await vector_store.aadd_documents(documents=documents)
        print(store_success)


      
user_query = """What is the temperature today in San Jose ?"""

# Run the async function and print the result
if __name__ == "__main__":
    # asyncio.run(parse(csv_path=csv_path, pdf_path=pdf_path))
    # result = asyncio.run(answer(query=user_query))
    # 1. Run vector search (sync)
    docs = asyncio.run(vector_search(user_query))
    answer = asyncio.run(async_structured_answer(user_query, docs))
    print(answer)
