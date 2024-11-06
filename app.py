from fastapi import FastAPI, UploadFile, File
import uvicorn
from chromadb import Client as ChromaConnector
from sentence_transformers import SentenceTransformer
from fastapi.responses import JSONResponse
from typing import List
import logging
import uuid

# Initialize FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Load SentenceTransformer model (CPU)
try:
    embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    log.info("SentenceTransformer model initialized successfully.")
except Exception as err:
    log.error(f"Model loading failed: {str(err)}")
    raise err

# Configure ChromaDB client for persistence
try:
    db_client = ChromaConnector()
    doc_collection = db_client.get_or_create_collection(name="text_docs")
    log.info("ChromaDB client initialized; collection created.")
except Exception as err:
    log.error(f"ChromaDB initialization error: {str(err)}")
    raise err

@app.post("/ingest/", response_class=JSONResponse)
async def upload_docs(files: List[UploadFile] = File(...)):
    """ Endpoint to upload documents for later retrieval """
    content_list = []
    vector_list = []
    doc_ids = []
    
    try:
        # Read files and prepare documents
        for file in files:
            try:
                raw_data = await file.read()
                text_content = raw_data.decode('utf-8')
                doc_id = str(uuid.uuid4())
                doc_entry = {"text": text_content, "metadata": {'filename': file.filename}}
                content_list.append(doc_entry)
                doc_ids.append(doc_id)
                log.info(f"Successfully read '{file.filename}'.")

            except UnicodeDecodeError:
                log.error(f"Cannot decode '{file.filename}'. Unsupported text format.")
                return JSONResponse(content={"error": f"Cannot decode '{file.filename}'."}, status_code=400)
            except Exception as err:
                log.error(f"File reading error for '{file.filename}': {str(err)}")
                return JSONResponse(content={"error": f"File error: {str(err)}"}, status_code=500)

        # Generate embeddings for documents
        try:
            vector_list = [embedder.encode(entry["text"]).tolist() for entry in content_list]
            log.info("Document embeddings created.")
        except Exception as err:
            log.error(f"Embedding generation error: {str(err)}")
            return JSONResponse(content={"error": f"Embedding error: {str(err)}"}, status_code=500)

        # Store documents in ChromaDB
        try:
            doc_collection.add(ids=doc_ids, documents=[entry["text"] for entry in content_list], 
                               metadatas=[entry["metadata"] for entry in content_list], embeddings=vector_list)
            log.info("Documents stored in ChromaDB.")
        except Exception as err:
            log.error(f"Error adding to database: {str(err)}")
            return JSONResponse(content={"error": f"Database error: {str(err)}"}, status_code=500)

        return JSONResponse(content={"status": "Documents uploaded successfully"})

    except Exception as err:
        log.error(f"Unexpected error during upload: {str(err)}")
        return JSONResponse(content={"error": f"Server Error: {str(err)}"}, status_code=500)

@app.get("/query/", response_class=JSONResponse)
async def search_docs(query_text: str):
    """ Endpoint to search documents """
    try:
        # Generate embedding for the query
        query_vector = embedder.encode(query_text).tolist()
        log.info("Query embedding generated.")
        
        # Query ChromaDB
        search_results = doc_collection.query(query_embeddings=[query_vector], n_results=5)
        response_data = [
            {
                "filename": meta.get('filename', 'unknown') if isinstance(meta, dict) else 'unknown',
                "score": score,
                "text": doc_text
            }
            for meta, score, doc_text in zip(search_results['metadatas'], search_results['distances'], search_results['documents'])
        ]
        log.info("Query processed successfully.")
        return JSONResponse(content={"results": response_data})
    
    except Exception as err:
        log.error(f"Query error: {str(err)}")
        return JSONResponse(content={"error": f"Server Error: {str(err)}"}, status_code=500)

@app.get("/database/", response_class=JSONResponse)
async def view_database():
    """ Endpoint to display all documents in the database """
    try:
        stored_docs = doc_collection.get()
        response_data = [
            {
                "filename": meta.get('filename', 'unknown') if isinstance(meta, dict) else 'unknown',
                "text": doc_text
            }
            for meta, doc_text in zip(stored_docs['metadatas'], stored_docs['documents'])
        ]
        log.info("Database retrieval successful.")
        return JSONResponse(content={"documents": response_data})
    except Exception as err:
        log.error(f"Database retrieval error: {str(err)}")
        return JSONResponse(content={"error": f"Server Error: {str(err)}"}, status_code=500)

if __name__ == "__main__":
    # Start the FastAPI app with live-reload enabled
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
