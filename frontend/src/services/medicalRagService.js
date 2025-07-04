/**
 * Service for interacting with the Medical RAG API
 */

const API_URL = 'http://localhost:8000/api';

/**
 * Query the medical RAG system with a question
 * @param {string} query - The medical question
 * @returns {Promise} - Promise with the response data
 */
export const queryMedicalRAG = async (query) => {
  try {
    const response = await fetch(`${API_URL}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        query,
        max_documents: 5
      }),
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error querying medical RAG:', error);
    throw error;
  }
};

/**
 * Upload a document to the medical RAG system
 * @param {FormData} formData - Form data with file and metadata
 * @returns {Promise} - Promise with the response data
 */
export const uploadDocument = async (formData) => {
  try {
    const response = await fetch(`${API_URL}/documents`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error uploading document:', error);
    throw error;
  }
};

/**
 * Add text content directly to the medical RAG system
 * @param {Object} data - Object with content and metadata
 * @returns {Promise} - Promise with the response data
 */
export const addTextContent = async (content, metadata = {}) => {
  try {
    const response = await fetch(`${API_URL}/text`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        content,
        metadata
      }),
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error adding text content:', error);
    throw error;
  }
};

/**
 * Check health status of the medical RAG system
 * @returns {Promise} - Promise with the health status
 */
export const checkHealth = async () => {
  try {
    const response = await fetch(`${API_URL}/health`);

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error checking health:', error);
    throw error;
  }
};
