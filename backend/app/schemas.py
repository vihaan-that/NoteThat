from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class DocumentBase(BaseModel):
    """Base model for document data"""
    content: str = Field(..., description="The text content of the document")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Document metadata (source, page, etc.)")


class DocumentCreate(DocumentBase):
    """Model for creating a new document"""
    pass


class QueryRequest(BaseModel):
    """Model for query request"""
    query: str = Field(..., description="The user's query text")
    max_documents: Optional[int] = Field(5, description="Maximum number of documents to retrieve")


class QueryResponse(BaseModel):
    """Model for query response"""
    answer: str = Field(..., description="The generated answer")
    sources: List[str] = Field(default_factory=list, description="Sources used for the answer")


class HealthResponse(BaseModel):
    """Model for health check response"""
    status: str = Field(..., description="Service status")
    models_loaded: bool = Field(..., description="Whether all models are loaded")
    vector_db_connected: bool = Field(..., description="Whether connected to vector database")
