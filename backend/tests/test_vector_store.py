import pytest
from unittest.mock import patch, MagicMock

from app.database.vector_store import (
    get_vector_store,
    init_vector_store,
    search_similar_documents,
)


@pytest.mark.asyncio
async def test_get_vector_store():
    """Test that the vector store is initialized correctly"""
    with patch("qdrant_client.QdrantClient") as mock_client, \
         patch("langchain_community.vectorstores.Qdrant") as mock_qdrant:
        
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance
        
        mock_qdrant_instance = MagicMock()
        mock_qdrant.return_value = mock_qdrant_instance
        
        vector_store = get_vector_store()
        
        assert vector_store == mock_qdrant_instance
        mock_client.assert_called_once()
        mock_qdrant.assert_called_once()


@pytest.mark.asyncio
async def test_init_vector_store():
    """Test initialization of vector store with documents"""
    test_docs = [
        {"page_content": "Test medical document 1", "metadata": {"source": "test1.pdf"}},
        {"page_content": "Test medical document 2", "metadata": {"source": "test2.pdf"}},
    ]
    
    with patch("app.database.vector_store.get_vector_store") as mock_get_store, \
         patch("app.core.embeddings.get_embeddings_model") as mock_get_embeddings:
        
        mock_store = MagicMock()
        mock_get_store.return_value = mock_store
        
        mock_embeddings = MagicMock()
        mock_get_embeddings.return_value = mock_embeddings
        
        await init_vector_store(test_docs)
        
        mock_get_store.assert_called_once()
        # Check if the store was initialized with documents
        mock_store.from_documents.assert_called_once()


@pytest.mark.asyncio
async def test_search_similar_documents():
    """Test searching for similar documents"""
    test_query = "What are diabetes symptoms?"
    expected_docs = ["Diabetes symptoms include increased thirst and frequent urination."]
    
    with patch("app.database.vector_store.get_vector_store") as mock_get_store:
        mock_store = MagicMock()
        mock_doc = MagicMock()
        mock_doc.page_content = expected_docs[0]
        mock_store.similarity_search_with_score.return_value = [(mock_doc, 0.95)]
        mock_get_store.return_value = mock_store
        
        results = await search_similar_documents(test_query, k=1)
        
        assert len(results) == 1
        assert results[0] == expected_docs[0]
        mock_store.similarity_search_with_score.assert_called_once()
