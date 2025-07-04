import pytest
from fastapi.testclient import TestClient
import json
import os
from unittest.mock import patch, MagicMock

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Test that health endpoint returns 200 and correct data structure"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "models_loaded" in data
    assert "vector_db_connected" in data


@pytest.mark.asyncio
async def test_query_endpoint(client):
    """Test query endpoint with mocked functions"""
    with patch("app.api.routes.search_similar_documents") as mock_search, \
         patch("app.api.routes.generate_response") as mock_generate:
        
        # Mock the search and generation functions
        mock_search.return_value = ["Diabetes symptoms include increased thirst and frequent urination."]
        mock_generate.return_value = "Symptoms of diabetes include increased thirst and frequent urination."
        
        # Make the request
        query = {"query": "What are the symptoms of diabetes?", "max_documents": 3}
        response = client.post("/api/query", json=query)
        
        # Check response
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert data["answer"] == "Symptoms of diabetes include increased thirst and frequent urination."
        assert len(data["sources"]) > 0


@pytest.mark.asyncio
async def test_text_endpoint(client):
    """Test adding text directly to the RAG system"""
    with patch("app.api.routes.process_document") as mock_process, \
         patch("app.api.routes.init_vector_store") as mock_init:
        
        # Mock the document processing
        mock_process.return_value = [
            {"page_content": "Diabetes test content", "metadata": {"source": "test"}}
        ]
        mock_init.return_value = None
        
        # Create test document
        document = {
            "content": "Diabetes is a metabolic disorder characterized by high blood sugar.",
            "metadata": {"source": "test_document", "title": "Diabetes Info"}
        }
        
        # Make the request
        response = client.post("/api/text", json=document)
        
        # Check response
        assert response.status_code == 201
        data = response.json()
        assert "message" in data
        assert "chunks" in data
        assert data["chunks"] == 1


@pytest.mark.asyncio
async def test_upload_document_endpoint(client, tmp_path):
    """Test document upload endpoint with a temporary file"""
    with patch("app.api.routes.process_document") as mock_process, \
         patch("app.api.routes.init_vector_store") as mock_init:
        
        # Mock the document processing
        mock_process.return_value = [
            {"page_content": "Test medical content", "metadata": {"source": "test.txt"}}
        ]
        mock_init.return_value = None
        
        # Create a temporary test file
        test_file_content = "This is a test medical document for upload."
        test_file = tmp_path / "test.txt"
        test_file.write_text(test_file_content)
        
        # Make the request with file upload
        with open(test_file, "rb") as f:
            response = client.post(
                "/api/documents",
                files={"file": ("test.txt", f, "text/plain")},
                data={"title": "Test Document", "source_type": "upload"}
            )
        
        # Check response
        assert response.status_code == 201
        data = response.json()
        assert "message" in data
        assert "chunks" in data
