#!/usr/bin/env python3
"""
Script to ingest and preprocess medical datasets for the Medical RAG system.
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path to allow importing app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.document_processor import process_document
from app.database.vector_store import init_vector_store
from app.utils.text_preprocessing import preprocess_medical_document

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('data_ingestion')


async def ingest_json_data(file_path: str, category: str = "general") -> List[Dict[str, Any]]:
    """
    Ingest data from a JSON file with medical information.
    
    Args:
        file_path (str): Path to the JSON file
        category (str): Category to assign to the documents
        
    Returns:
        List[Dict[str, Any]]: List of processed documents
    """
    logger.info(f"Ingesting data from {file_path}")
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"Error reading JSON file: {e}")
        return []
    
    processed_docs = []
    
    # Process each item in the JSON data
    for i, item in enumerate(data):
        # Check if the item has the required fields
        if not isinstance(item, dict) or "text" not in item:
            logger.warning(f"Skipping item {i}: missing required fields")
            continue
            
        # Create a document with metadata
        document = {
            "content": item["text"],
            "metadata": {
                "source": os.path.basename(file_path),
                "id": item.get("id", f"item_{i}"),
                "category": category,
                "tags": item.get("tags", []),
                "title": item.get("title", f"Medical Document {i}")
            }
        }
        
        # Preprocess the document
        preprocessed = preprocess_medical_document(document)
        
        # Process document into chunks
        try:
            docs = await process_document(preprocessed)
            processed_docs.extend(docs)
            logger.info(f"Processed item {i} into {len(docs)} chunks")
        except Exception as e:
            logger.error(f"Error processing item {i}: {e}")
    
    return processed_docs


async def ingest_text_directory(directory_path: str, category: str = "general") -> List[Dict[str, Any]]:
    """
    Ingest all text files from a directory.
    
    Args:
        directory_path (str): Path to the directory containing text files
        category (str): Category to assign to the documents
        
    Returns:
        List[Dict[str, Any]]: List of processed documents
    """
    logger.info(f"Ingesting text files from {directory_path}")
    
    dir_path = Path(directory_path)
    if not dir_path.is_dir():
        logger.error(f"Directory not found: {directory_path}")
        return []
    
    processed_docs = []
    
    # Process each text file in the directory
    for file_path in dir_path.glob("*.txt"):
        try:
            # Read the file content
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Create a document with metadata
            document = {
                "content": content,
                "metadata": {
                    "source": file_path.name,
                    "category": category,
                    "title": file_path.stem
                }
            }
            
            # Preprocess the document
            preprocessed = preprocess_medical_document(document)
            
            # Process document into chunks
            docs = await process_document(preprocessed)
            processed_docs.extend(docs)
            logger.info(f"Processed {file_path.name} into {len(docs)} chunks")
            
        except Exception as e:
            logger.error(f"Error processing {file_path.name}: {e}")
    
    return processed_docs


async def main():
    parser = argparse.ArgumentParser(description="Ingest medical data into the vector store")
    
    # Add arguments
    parser.add_argument("--json", help="Path to JSON file with medical data")
    parser.add_argument("--text-dir", help="Path to directory with text files")
    parser.add_argument("--category", default="general", help="Category for the documents")
    parser.add_argument("--collection", default="medical_documents", 
                      help="Name of the collection to add documents to")
    
    args = parser.parse_args()
    
    # Set the collection name environment variable
    os.environ["COLLECTION_NAME"] = args.collection
    
    processed_docs = []
    
    # Process JSON data if provided
    if args.json:
        json_docs = await ingest_json_data(args.json, args.category)
        processed_docs.extend(json_docs)
    
    # Process text files if directory is provided
    if args.text_dir:
        text_docs = await ingest_text_directory(args.text_dir, args.category)
        processed_docs.extend(text_docs)
    
    if not processed_docs:
        logger.error("No documents were processed. Please provide valid input data.")
        return
    
    # Add documents to vector store
    logger.info(f"Adding {len(processed_docs)} documents to vector store collection '{args.collection}'")
    await init_vector_store(processed_docs)
    logger.info("Ingestion complete")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
