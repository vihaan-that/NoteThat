import pytest
from unittest.mock import patch, MagicMock

from app.core.llm import get_llm_model, generate_response


@pytest.mark.asyncio
async def test_get_llm_model():
    """Test that the LLM model is loaded correctly"""
    with patch("langchain.llms.LlamaCpp") as mock_llm:
        mock_instance = MagicMock()
        mock_llm.return_value = mock_instance
        
        model = get_llm_model()
        
        assert model == mock_instance
        mock_llm.assert_called_once()


@pytest.mark.asyncio
async def test_generate_response():
    """Test response generation with context"""
    test_query = "What are the symptoms of diabetes?"
    test_context = ["Diabetes symptoms include increased thirst, frequent urination."]
    expected_response = "Symptoms of diabetes include increased thirst and frequent urination."
    
    with patch("app.core.llm.get_llm_model") as mock_get_model:
        mock_model = MagicMock()
        mock_model.return_value = expected_response
        mock_get_model.return_value = mock_model
        
        result = await generate_response(test_query, test_context)
        
        assert result == expected_response
        mock_model.assert_called_once()
