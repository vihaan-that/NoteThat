import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Set test environment variables
os.environ["EMBEDDINGS_MODEL"] = "test-embedding-model"
os.environ["MODEL_PATH"] = "test-model-path"
os.environ["QDRANT_HOST"] = "localhost"
os.environ["QDRANT_PORT"] = "6333"
os.environ["COLLECTION_NAME"] = "test_collection"

# Import after environment variables are set
from app.main import app
from app.core.embeddings import get_embeddings_model
from app.core.llm import get_llm_model
from app.database.vector_store import get_vector_store


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_embeddings():
    with patch("app.core.embeddings.get_embeddings_model") as mock:
        model = MagicMock()
        model.encode.return_value = [0.1] * 768  # Mock embedding dimension
        mock.return_value = model
        yield mock


@pytest.fixture
def mock_llm():
    with patch("app.core.llm.get_llm_model") as mock:
        model = MagicMock()
        model.return_value = "This is a mock LLM response"
        mock.return_value = model
        yield mock


@pytest.fixture
def mock_vector_store():
    with patch("app.database.vector_store.get_vector_store") as mock:
        store = MagicMock()
        store.similarity_search_with_score.return_value = [
            (
                MagicMock(
                    page_content="Mock document content",
                    metadata={"source": "test.pdf", "page": 1}
                ),
                0.95
            )
        ]
        mock.return_value = store
        yield mock
