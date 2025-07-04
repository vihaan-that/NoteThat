import os
from functools import lru_cache
from typing import List, Dict, Any, Tuple

from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from langchain_community.vectorstores import Qdrant
from langchain_community.docstore.document import Document

from app.core.embeddings import get_embeddings_model


@lru_cache(maxsize=1)
def get_vector_store():
    """
    Initialize and return the Qdrant vector store client.
    Uses LRU cache to prevent recreating the client on each call.
    
    Returns:
        Qdrant: The configured vector store
    """
    # Get environment variables
    qdrant_host = os.getenv("QDRANT_HOST", "localhost")
    qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))
    collection_name = os.getenv("COLLECTION_NAME", "medical_documents")
    
    # Initialize Qdrant client
    client = QdrantClient(host=qdrant_host, port=qdrant_port)
    
    # Get embeddings model
    embeddings_model = get_embeddings_model()
    
    # Check if collection exists, if not create it
    collections = client.get_collections().collections
    collection_names = [collection.name for collection in collections]
    
    if collection_name not in collection_names:
        # Create a new collection with the PubMedBERT embedding size (768)
        client.create_collection(
            collection_name=collection_name,
            vectors_config=rest.VectorParams(
                size=768,
                distance=rest.Distance.COSINE
            )
        )
    
    # Return the Qdrant vector store
    return Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings_model
    )


async def init_vector_store(documents: List[Dict[str, Any]]) -> None:
    """
    Initialize the vector store with documents.
    
    Args:
        documents (List[Dict[str, Any]]): List of documents to add to the vector store
    """
    vector_store = get_vector_store()
    
    # Convert to Document objects if needed
    doc_objects = []
    for doc in documents:
        if isinstance(doc, dict):
            doc_objects.append(
                Document(
                    page_content=doc["page_content"],
                    metadata=doc["metadata"]
                )
            )
        else:
            doc_objects.append(doc)
    
    # Add documents to the vector store
    vector_store.from_documents(
        documents=doc_objects,
        embedding=get_embeddings_model()
    )


async def search_similar_documents(query: str, k: int = 5) -> List[str]:
    """
    Search for documents similar to the query.
    
    Args:
        query (str): The query to search for
        k (int): Number of documents to return
        
    Returns:
        List[str]: List of similar document contents
    """
    vector_store = get_vector_store()
    
    # Get similar documents with their similarity scores
    docs_and_scores = vector_store.similarity_search_with_score(query, k=k)
    
    # Extract document content
    return [doc.page_content for doc, _ in docs_and_scores]
