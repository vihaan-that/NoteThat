import pytest
from unittest.mock import patch, MagicMock

from app.core.document_processor import (
    chunk_text,
    process_document
)


def test_chunk_text():
    """Test text chunking with overlap"""
    text = "This is a test document. It contains multiple sentences. We need to split it into chunks. This is the end."
    chunk_size = 30
    chunk_overlap = 10
    
    chunks = chunk_text(text, chunk_size, chunk_overlap)
    
    # Check if we got the right number of chunks
    assert len(chunks) > 0
    
    # Check if chunks have appropriate size
    for chunk in chunks:
        assert len(chunk) <= chunk_size + 5  # Allow small margin for completion of words/sentences
        
    # Check if chunks contain the expected content (spot check)
    assert "This is a test document" in chunks[0]
    
    # Check for overlap between consecutive chunks
    if len(chunks) > 1:
        # Check that some content from chunk1 appears in chunk2 (overlap)
        overlap_found = False
        for i in range(len(chunks) - 1):
            # Get the end of the current chunk and beginning of next chunk
            current_end = chunks[i][-chunk_overlap:]
            next_start = chunks[i+1][:chunk_overlap]
            
            # Check if there's any overlap
            if any(word in next_start for word in current_end.split()):
                overlap_found = True
                break
                
        assert overlap_found


@pytest.mark.asyncio
async def test_process_document():
    """Test document processing"""
    mock_doc = {
        "content": "This is a medical document about diabetes. Diabetes is a condition that affects blood sugar levels.",
        "metadata": {"source": "test.pdf", "page": 1}
    }
    
    with patch("app.core.document_processor.chunk_text") as mock_chunk:
        mock_chunk.return_value = [
            "This is a medical document about diabetes.",
            "Diabetes is a condition that affects blood sugar levels."
        ]
        
        processed_docs = await process_document(mock_doc)
        
        assert len(processed_docs) == 2
        assert processed_docs[0]["page_content"] == "This is a medical document about diabetes."
        assert processed_docs[0]["metadata"]["source"] == "test.pdf"
        assert processed_docs[0]["metadata"]["page"] == 1
