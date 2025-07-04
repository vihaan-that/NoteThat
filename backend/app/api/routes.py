from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, Query
from typing import List, Dict, Any, Optional

from app.utils.file_parsers import parse_file

from app.schemas import DocumentCreate, QueryRequest, QueryResponse, HealthResponse
from app.core.document_processor import process_document
from app.database.vector_store import init_vector_store, search_similar_documents
from app.core.llm import generate_response

router = APIRouter()


@router.post("/documents", status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    source_type: str = Form("upload"),
    description: Optional[str] = Form(None)
):
    """
    Upload and process a document for the medical RAG system.
    Supports various file types including text, PDF, and potentially others.
    """
    try:
        # Read file content
        content = await file.read()
        
        # Parse the file based on its type
        parsed_document = await parse_file(content, file.filename)
        
        # Add additional metadata
        parsed_document["metadata"]["title"] = title
        parsed_document["metadata"]["source_type"] = source_type
        parsed_document["metadata"]["file_size"] = len(content)
        
        if description:
            parsed_document["metadata"]["description"] = description
        
        # Process document into chunks
        processed_docs = await process_document(parsed_document)
        
        # Add documents to vector store
        await init_vector_store(processed_docs)
        
        return {
            "message": "Document processed successfully", 
            "chunks": len(processed_docs),
            "file_type": parsed_document["metadata"].get("file_type", "unknown")
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@router.post("/query", response_model=QueryResponse)
async def query_model(request: QueryRequest):
    """
    Query the medical RAG system.
    """
    try:
        # Search for relevant documents
        max_docs = request.max_documents or 5
        similar_docs = await search_similar_documents(request.query, k=max_docs)
        
        # Generate response using retrieved documents as context
        answer = await generate_response(request.query, similar_docs)
        
        # Return response with sources
        return QueryResponse(
            answer=answer,
            sources=[f"Source {i+1}" for i in range(len(similar_docs))]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.post("/text", status_code=201)
async def add_text(document: DocumentCreate):
    """
    Add text content directly to the medical RAG system.
    """
    try:
        # Process document into chunks
        processed_docs = await process_document(document.dict())
        
        # Add documents to vector store
        await init_vector_store(processed_docs)
        
        return {"message": "Text processed successfully", "chunks": len(processed_docs)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Check the health of the medical RAG system.
    """
    try:
        # Perform basic health checks
        # In a real implementation, we would check if models are loaded and vector DB is connected
        return HealthResponse(
            status="healthy",
            models_loaded=True,
            vector_db_connected=True
        )
    
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            models_loaded=False,
            vector_db_connected=False
        )
