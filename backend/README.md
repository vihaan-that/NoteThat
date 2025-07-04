# Medical RAG Backend for NoteThat

This backend implements a Medical Retrieval Augmented Generation (RAG) system using Bio-Mistral 7B, PubMedBERT embeddings, and Qdrant vector database.

## Overview

The Medical RAG system allows users to:
- Upload medical documents for indexing
- Ask medical questions and get accurate responses
- Trace back answers to their source documents

## Architecture

The system follows DDIA (Designing Data-Intensive Applications) principles with a focus on:
- **Reliability**: Robust error handling and health checks
- **Scalability**: Docker containerization and vector database integration
- **Maintainability**: TDD approach with comprehensive testing

Components:
1. **Bio-Mistral 7B**: Specialized medical language model for generating responses
2. **PubMedBERT**: Domain-specific embedding model for medical text
3. **Qdrant**: Vector database for efficient similarity search
4. **FastAPI**: Backend API framework for handling requests
5. **LangChain**: Orchestration framework for RAG workflow

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.10+
- Minimum 8GB RAM (16GB recommended)

### Setup

1. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

2. Download the required models:
   ```bash
   cd scripts
   python download_model.py --model biomistral-7b-q4
   ```
   Note: This will download the quantized 4-bit model (~4GB).

3. Build and run the Docker containers:
   ```bash
   cd ..
   docker-compose up -d
   ```

4. The API will be available at [http://localhost:8000](http://localhost:8000)

## API Endpoints

- `POST /api/documents`: Upload and process a document
- `POST /api/text`: Add text content directly
- `POST /api/query`: Query the medical RAG system
- `GET /api/health`: Check system health

## Testing

This project is built using Test-Driven Development (TDD). Run the tests with:

```bash
pytest
```

## Architecture Decisions

- **Quantized Model**: Using GGUF format for efficient CPU inference
- **Vector Chunking**: Documents are split into semantic chunks for better retrieval
- **Docker Deployment**: Ensures consistent environment across systems
- **Embedding Caching**: Improves response time for similar queries

## License

MIT
