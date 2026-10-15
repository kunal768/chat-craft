# RAG (Retrieval-Augmented Generation) Project

This project implements a Retrieval-Augmented Generation (RAG) system using LangChain, MongoDB Atlas Vector Search, and Ollama models. The system is capable of processing various document types and answering questions based on the content.

## Project Structure

The project consists of two main components:

1. `script.py`: A production-ready implementation using LangChain and MongoDB Atlas
2. `project.ipynb`: A Jupyter notebook implementation using Llama.cpp and FAISS

## script.py

This script implements a RAG system with the following features:

### Key Components

- **Document Processing**:
  - Supports multiple document formats: PDF, CSV, DOCX, and HTML
  - Uses LangChain's document loaders for parsing
  - Implements text chunking with RecursiveCharacterTextSplitter

- **Vector Storage**:
  - Uses MongoDB Atlas Vector Search for document storage and retrieval
  - Implements efficient vector search with configurable parameters
  - Supports async operations for better performance

- **Language Models**:
  - Uses Ollama for both embeddings and text generation
  - Implements a structured prompt template for consistent responses
  - Supports temperature control for response generation

### Usage

1. Set up environment variables in `.env`:
   ```env
   MONGO_URI=your_mongodb_connection_string
   pdf_path=path_to_pdf
   csv_path=path_to_csv
   docx_path=path_to_docx
   html_path=path_to_html
   ```

2. Run the script:
   ```zsh
   python script.py
   ```

## project.ipynb

This Jupyter notebook implements a simpler RAG system using different technologies:

### Key Components

- **Document Processing**:
  - Uses simple text chunking (500 characters per chunk)
  - Implements basic text file reading

- **Vector Storage**:
  - Uses FAISS for efficient vector similarity search
  - Implements a simple chunk mapping system

- **Language Models**:
  - Uses Llama.cpp for text generation
  - Uses SentenceTransformer for embeddings
  - Implements a simple question-answering system

### Usage

1. Install required packages:
   ```bash
   pip install llama-cpp-python faiss-cpu sentence-transformers
   ```

2. Prepare your model:
   - Download the Llama 2 model (llama-2-7b-chat.Q4_K_M.gguf)
   - Place it in the project directory

3. Run the notebook:
   - Open `project.ipynb` in Jupyter
   - Execute cells in sequence
   - Use the interactive question-answering interface

## Key Differences

- `script.py` is more production-ready with:
  - Support for multiple document types
  - MongoDB Atlas integration
  - Async operations
  - More robust error handling

- `project.ipynb` is more experimental with:
  - Simpler implementation
  - Local vector storage (FAISS)
  - Interactive notebook interface
  - Easier to modify and experiment with

## Requirements

All required packages are listed in `requirements.txt`. You can install them using:
```bash
pip install -r requirements.txt
```

The main dependencies include:

### Core Dependencies
- python-dotenv - For environment variable management
- pymongo - For MongoDB integration

### LangChain Dependencies
- langchain - Core LangChain functionality
- langchain-ollama - Ollama integration
- langchain-mongodb - MongoDB vector store integration
- langchain-community - Community integrations

### Document Processing
- PyPDF2 - PDF processing
- python-docx - DOCX processing
- unstructured - HTML and other document processing
- docx2txt - Additional DOCX support

### Vector Storage and Embeddings
- faiss-cpu - For local vector similarity search
- sentence-transformers - For text embeddings
- numpy - Required for numerical operations

### LLM Dependencies
- llama-cpp-python - For local LLM inference
- torch - Required for transformers
- transformers - For model loading and inference

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables in `.env`
4. Download required models:
   - For `script.py`: No additional model downloads needed (uses Ollama)
   - For `project.ipynb`: Download llama-2-7b-chat.Q4_K_M.gguf
5. Run either the script or notebook based on your needs
