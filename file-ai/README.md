# file-ai
Manages files, provides/retrieves data from AI

## Setup Instructions

### Prerequisites
- Python 3.8+
- MongoDB Atlas account
- Ollama installed locally

### MongoDB Atlas Setup
1. Create a MongoDB Atlas cluster if you haven't already
2. Create a database and collection for storing vectors
3. Create a Vector Search Index on your collection with the following configuration:
```json
{
  "fields": [
    {
      "numDimensions": 768,
      "path": "embedding",
      "similarity": "cosine",
      "type": "vector"
    },
    {
      "path": "user_id",
      "type": "filter"
    }
  ]
}
```

### Environment Setup
1. Create a `.env` file in the project root with the following variables:
```env
MONGO_URI=your_mongodb_connection_string
EMBED_MODEL_NAME=nomic-embed-text
LLM_MODEL_NAME=llama2
DB_NAME=your_database_name
COLLECTION_NAME=your_collection_name
VECTOR_SEARCH_INDEX=your_vector_search_index_name
STORAGE_PATH=path_to_store_uploaded_files
```

### Ollama Setup
1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull required models:
```bash
ollama pull nomic-embed-text
ollama pull llama2
```
3. Start Ollama server:
```bash
ollama serve
```

### Project Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run unit tests:
```bash
python -m pytest tests/unit_tests.py
```

### Test Run Screenshot 
<img src = "https://github.com/Chat-craft/.github/blob/main/fileai-tests.png" />

3. Run the project (make sure Ollama server is running):
```bash
uvicorn main:app --port 8001
```

The API will be available at `http://localhost:8001`

### API Documentation
Once the server is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`
