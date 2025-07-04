import pytest
from unittest.mock import patch, MagicMock
import numpy as np

from app.core.embeddings import get_embeddings_model, embed_text


@pytest.mark.asyncio
async def test_get_embeddings_model():
    """Test that the embeddings model is loaded correctly"""
    with patch("sentence_transformers.SentenceTransformer") as mock_model:
        mock_instance = MagicMock()
        mock_model.return_value = mock_instance
        
        model = get_embeddings_model()
        
        assert model == mock_instance
        mock_model.assert_called_once()


@pytest.mark.asyncio
async def test_embed_text():
    """Test text embedding functionality"""
    test_text = "This is a medical test document"
    mock_embedding = np.array([0.1] * 768)
    
    with patch("app.core.embeddings.get_embeddings_model") as mock_get_model:
        mock_model = MagicMock()
        mock_model.encode.return_value = mock_embedding
        mock_get_model.return_value = mock_model
        
        result = await embed_text(test_text)
        
        mock_model.encode.assert_called_once_with(test_text)
        assert isinstance(result, np.ndarray)
        assert result.shape == (768,)
        np.testing.assert_array_equal(result, mock_embedding)
