import os
import re
from typing import List, Dict, Any

from app.utils.text_preprocessing import preprocess_medical_document

def chunk_text(text: str, chunk_size: int = None, chunk_overlap: int = None) -> List[str]:
    """
    Split a text into overlapping chunks of specified size.
    
    Args:
        text (str): The text to split
        chunk_size (int): Maximum size of each chunk
        chunk_overlap (int): Amount of overlap between chunks
    
    Returns:
        List[str]: List of text chunks
    """
    # Get values from environment if not provided
    if chunk_size is None:
        chunk_size = int(os.getenv("CHUNK_SIZE", "500"))
    if chunk_overlap is None:
        chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "50"))
    
    # If text is shorter than chunk size, return it as is
    if len(text) <= chunk_size:
        return [text]
    
    # Split text into sentences for better chunking
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence_length = len(sentence)
        
        # If adding this sentence exceeds the chunk size and we already have content
        if current_length + sentence_length > chunk_size and current_chunk:
            # Join the current chunk into a string and add to chunks
            chunks.append(" ".join(current_chunk))
            
            # Keep some sentences for overlap
            overlap_sentences = []
            overlap_length = 0
            
            # Work backwards through current_chunk to build overlap
            for s in reversed(current_chunk):
                if overlap_length + len(s) <= chunk_overlap:
                    overlap_sentences.insert(0, s)
                    overlap_length += len(s) + 1  # +1 for space
                else:
                    break
            
            # Reset current chunk with overlap sentences
            current_chunk = overlap_sentences
            current_length = overlap_length
        
        # Add the sentence to the current chunk
        current_chunk.append(sentence)
        current_length += sentence_length + 1  # +1 for space
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks


async def process_document(document: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Process a document and split it into chunks.
    
    Args:
        document (Dict[str, Any]): Document with content and metadata
    
    Returns:
        List[Dict[str, Any]]: List of processed document chunks with metadata
    """
    # Apply text preprocessing
    preprocessed_doc = preprocess_medical_document(document)
    content = preprocessed_doc["content"]
    metadata = preprocessed_doc["metadata"]
    
    # Get chunk size and overlap from environment
    chunk_size = int(os.getenv("CHUNK_SIZE", "500"))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "50"))
    
    # Split text into chunks
    text_chunks = chunk_text(content, chunk_size, chunk_overlap)
    
    # Create document objects with metadata
    processed_docs = []
    for i, chunk in enumerate(text_chunks):
        # Copy metadata and add chunk info
        chunk_metadata = metadata.copy()
        chunk_metadata["chunk"] = i
        
        processed_docs.append({
            "page_content": chunk,
            "metadata": chunk_metadata
        })
    
    return processed_docs
