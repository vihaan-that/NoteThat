import os
from functools import lru_cache
import numpy as np
from sentence_transformers import SentenceTransformer

@lru_cache(maxsize=1)
def get_embeddings_model():
    """
    Load and return the embeddings model using the model name from environment variables.
    Uses LRU cache to prevent reloading the model on each call.
    
    Returns:
        SentenceTransformer: The loaded embeddings model
    """
    model_name = os.getenv("EMBEDDINGS_MODEL", "pritamdeka/PubMedBERT-mnli-sts")
    return SentenceTransformer(model_name)

async def embed_text(text: str) -> np.ndarray:
    """
    Generate embeddings for the given text using the loaded model
    
    Args:
        text (str): Text to embed
        
    Returns:
        np.ndarray: The embedding vector
    """
    model = get_embeddings_model()
    return model.encode(text)

async def embed_documents(documents: list[str]) -> list[np.ndarray]:
    """
    Generate embeddings for multiple documents
    
    Args:
        documents (list[str]): List of documents to embed
        
    Returns:
        list[np.ndarray]: List of embedding vectors
    """
    model = get_embeddings_model()
    return model.encode(documents)
