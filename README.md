
# FastAPI Server for Retrieval-Augmented Generation (RAG)

This repository hosts a streamlined FastAPI server built for Retrieval-Augmented Generation (RAG). Utilizing ChromaDB’s persistent client, the server allows for efficient ingestion and querying of documents across multiple formats, including PDF, DOC, DOCX, and TXT. Document embeddings are generated with the `sentence-transformers/all-MiniLM-L6-v2` model, optimized for CPU usage, and API endpoints are designed to be non-blocking with efficient concurrency handling.

## Features
- **Document Ingestion & Retrieval**: Supports document ingestion and querying across various formats using ChromaDB.
- **Efficient Embeddings**: Leverages `sentence-transformers/all-MiniLM-L6-v2` for high-quality embeddings.
- **Non-blocking API**: Optimized for handling concurrent requests with FastAPI.

## Tech Stack
- **FastAPI**: Framework for developing API endpoints.
- **ChromaDB**: Manages storage and retrieval of document embeddings.
- **Sentence-Transformers**: Embedding model used for text processing.
- **Python**: Core programming language.
- **Uvicorn**: ASGI server for FastAPI app deployment.

## Libraries and Technologies
1. **FastAPI**: Modern web framework for fast API development.
2. **Uvicorn**: High-performance ASGI server for FastAPI.
3. **ChromaDB**: Vector database for managing and querying embeddings.
4. **Sentence-Transformers**: Library for generating sentence embeddings.
5. **Langchain**: Assists in document processing and loading.
6. **Python Standard Libraries**: Includes `uuid` for ID generation and `logging`.

## Getting Started
### Prerequisites
- Python 3.8+
- `pip` for package installation

### Installation
1. **Clone the Repository**
   ```sh
   git clone https://github.com/<username>/fastapi-rag-server.git
   cd fastapi-rag-server
   ```

2. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the Server**
   ```sh
   uvicorn main:app --reload
   ```
   Access the server at `http://127.0.0.1:8000`.

## API Endpoints
### 1. `/ingest/` [POST]
Upload documents (PDF, DOC, DOCX, TXT) for retrieval.
- **Request**: Multipart form with files.
- **Example Input**: `sample1.txt`, `sample2.pdf`
- **Example Response**:
  ```json
  { "status": "Documents ingested successfully" }
  ```

### 2. `/query/` [GET]
Query stored documents.
- **Parameters**: `query` (str) - Text to search for.
- **Example URL**: `http://127.0.0.1:8000/query/?query=What is FastAPI?`
- **Example Response**:
  ```json
  {
    "results": [
      {
        "filename": "sample1.txt",
        "score": 0.7214,
        "text": "Title: Introduction to FastAPI\n\nFastAPI is a modern, fast (high-performance), web framework..."
      }
    ]
  }
  ```

### 3. `/database/` [GET]
Retrieve metadata and text from all stored documents.
- **Example Response**:
  ```json
  {
    "documents": [
      { "filename": "sample1.txt", "text": "Introduction to FastAPI..." },
      { "filename": "sample2.pdf", "text": "Sample PDF document text..." }
    ]
  }
  ```

## Running the Server
1. **Start the Server**
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
   The server will be available at `http://localhost:8000`.

2. **Testing Endpoints**
   - Use tools like **Postman**, **Thunder Client**, or a web browser.

## Usage Example
### Document Ingestion
Use tools like Postman to upload documents via `/ingest/`.
- **URL**: `http://localhost:8000/ingest/`
- **Method**: POST with files in form-data.

### Document Querying
Make a GET request to `/query/` with your query string.
- **URL**: `http://localhost:8000/query/?query=<your_query>`

## Contributing
Contributions are welcome! Submit a Pull Request.

For questions, reach out at [jatinavi15@gmail.com](mailto:jatinavi15@gmail.com) or visit [jatinavi](https://github.com/jatinavi).

## License
Licensed under the MIT License.

## Acknowledgements
- [FastAPI](https://fastapi.tiangolo.com/)
- [ChromaDB](https://github.com/chroma-core/chroma)
- [Sentence-Transformers](https://www.sbert.net/)
- [Langchain](https://langchain.com/)
