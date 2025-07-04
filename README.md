# NoteThat

NoteThat is an AI-powered cross-platform mobile assistant for voice and text note-taking with intelligent retrieval. It indexes information from videos, recordings, and MBBS textbooks using speech-to-text, OCR, and Retrieval-Augmented Generation (RAG).

## Project Overview

NoteThat is built using React Native with Expo for the mobile application, with a Next.js web interface and FastAPI backend. The application leverages modern AI technologies to provide intelligent note-taking and information retrieval capabilities.

The project is divided into two main components:
1. **Frontend**: React Native mobile app and Next.js web interface
2. **Backend**: FastAPI server with Medical RAG capabilities powered by Bio-Mistral 7B

## Features

- Voice-to-text note taking
- OCR for extracting text from images and documents
- Intelligent information retrieval using RAG
- Medical RAG powered by Bio-Mistral 7B for healthcare information
- Cross-platform support (iOS, Android, Web)
- User-friendly interface

## Setup Instructions

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Expo CLI

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd NoteThat
   ```

2. Navigate to the project directory:
   ```bash
   cd NoteThat
   ```

3. Install dependencies:
   ```bash
   npm install
   ```

### Running the Application

- **For iOS:**
  ```bash
  npm run ios
  ```

- **For Android:**
  ```bash
  npm run android
  ```

- **For Web:**
  ```bash
  npm run web
  ```

- **General development:**
  ```bash
  npm start
  ```

## Project Structure

The project follows the Expo Router file-based routing structure:

- `/app`: Main application code with file-based routing
- `/assets`: Static assets like images and fonts
- `/components`: Reusable UI components
- `/constants`: Application constants and configuration
- `/hooks`: Custom React hooks

## Development

To start developing, edit the files in the `/app` directory. The application uses Expo Router for file-based routing.

## License

[Specify your license here]
