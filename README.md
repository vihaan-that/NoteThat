# NoteThat

NoteThat is an AI-powered cross-platform mobile assistant for voice and text note-taking with intelligent retrieval. It indexes information from videos, recordings, and MBBS textbooks using speech-to-text, OCR, and Retrieval-Augmented Generation (RAG).

## Project Overview

NoteThat is built using React Native with Expo for the mobile application, with a Next.js web interface and FastAPI backend. The application leverages modern AI technologies to provide intelligent note-taking and information retrieval capabilities.

The project is divided into two main components:
1. **Frontend**: React Native mobile app and Next.js web interface
2. **Backend**: FastAPI server with Medical RAG capabilities powered by Bio-Mistral 7B

## Features

- Voice-to-text note taking (planned)
- OCR for extracting text from images and documents
- Intelligent information retrieval using RAG
- Medical RAG powered by Bio-Mistral 7B for healthcare information
- Web interface with Next.js (mobile support planned)
- User-friendly interface

## Backend Architecture

The Medical RAG system follows DDIA (Designing Data-Intensive Applications) principles with a focus on:
- **Reliability**: Robust error handling and health checks
- **Scalability**: Docker containerization and vector database integration
- **Maintainability**: TDD approach with comprehensive testing

> **Note**: 
> - The current architecture does not support multimodal indexing yet. This capability will be added in future commits to enhance the system's ability to process and retrieve information from multiple modalities (text, images, audio) simultaneously.
> - Although mentioned in the project overview, React Native mobile implementation has not been completed yet. Currently, only the Next.js web frontend is available. React Native support will be added in future commits to enable cross-platform mobile functionality.

Components:
1. **Bio-Mistral 7B**: Specialized medical language model for generating responses
2. **PubMedBERT**: Domain-specific embedding model for medical text
3. **Qdrant**: Vector database for efficient similarity search
4. **FastAPI**: Backend API framework for handling requests
5. **LangChain**: Orchestration framework for RAG workflow

### Architecture Decisions

- **Quantized Model**: Using GGUF format for efficient CPU inference
- **Vector Chunking**: Documents are split into semantic chunks for better retrieval
- **Docker Deployment**: Ensures consistent environment across systems
- **Embedding Caching**: Improves response time for similar queries

## Setup Instructions

### Frontend Prerequisites

- Node.js (v18 or higher)
- npm or yarn

### Frontend Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd NoteThat
   ```

2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

3. Install dependencies:
   ```bash
   npm install
   ```

### Running the Frontend Application

- **Development mode:**
  ```bash
  npm run dev
  ```

- **Build for production:**
  ```bash
  npm run build
  ```

- **Start production server:**
  ```bash
  npm start
  ```

### Backend Prerequisites

- Docker and Docker Compose
- Python 3.10+
- Minimum 8GB RAM (16GB recommended)

### Backend Setup

1. Create a `.env` file from the example:
   ```bash
   cd backend
   cp .env.example .env
   ```

2. Download the required models:
   ```bash
   cd scripts
   python download_model.py --model biomistral-7b-q4
   ```
   Note: This will download the quantized 4-bit model (~4GB).

3. Build and run the Docker containers (from project root):
   ```bash
   docker-compose up -d
   ```

4. The API will be available at [http://localhost:8000](http://localhost:8000) and the frontend at [http://localhost:3000](http://localhost:3000)

## API Endpoints

- `POST /api/documents`: Upload and process a document
- `POST /api/text`: Add text content directly
- `POST /api/query`: Query the medical RAG system
- `GET /api/health`: Check system health

## Project Structure

### Frontend Structure

The frontend follows the Next.js file-based routing structure:

- `/app`: Main application code with file-based routing
- `/assets`: Static assets like images and fonts
- `/components`: Reusable UI components
- `/constants`: Application constants and configuration
- `/hooks`: Custom React hooks

### Backend Structure

The backend follows a modular design for the Medical RAG system:

- `/models`: LLM and embedding models
- `/database`: Vector database configuration
- `/api`: API endpoints and routing
- `/tests`: Test suite for TDD approach

## Development

- **Frontend**: To start developing, edit the files in the `/app` directory. The application uses Expo Router for file-based routing.
- **Backend**: Edit the FastAPI backend files in the `/backend` directory. Run tests using `pytest` to ensure reliability.

## Testing

The backend is built using Test-Driven Development (TDD). Run the backend tests with:

```bash
cd backend
pytest
```

## License

MIT
