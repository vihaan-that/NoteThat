#!/usr/bin/env python3
"""
Script to download the Bio-Mistral 7B model for the Medical RAG system.
"""

import os
import argparse
import requests
from tqdm import tqdm
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('model_downloader')

# Define the model URLs
MODELS = {
    'biomistral-7b-q4': {
        'url': 'https://huggingface.co/TheBloke/BioMistral-7B-GGUF/resolve/main/biomistral-7b.Q4_K_M.gguf',
        'filename': 'biomistral-7b-q4.gguf'
    },
    'pubmedbert': {
        'url': 'https://huggingface.co/pritamdeka/PubMedBERT-mnli-sts',
        'is_directory': True
    }
}

def download_file(url, destination, chunk_size=8192):
    """
    Download a file from the given URL to the destination path with progress bar.
    
    Args:
        url (str): URL to download from
        destination (str): Path to save the file to
        chunk_size (int): Size of chunks to download
    """
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    logger.info(f"Downloading {url} to {destination}")
    
    with open(destination, 'wb') as f:
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=os.path.basename(destination)) as pbar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
    
    logger.info(f"Download completed: {destination}")

def download_model(model_name, output_dir):
    """
    Download the specified model.
    
    Args:
        model_name (str): Name of the model to download
        output_dir (str): Directory to save the model to
    """
    if model_name not in MODELS:
        logger.error(f"Unknown model: {model_name}")
        logger.info(f"Available models: {', '.join(MODELS.keys())}")
        return False
    
    model_info = MODELS[model_name]
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    if model_info.get('is_directory', False):
        logger.info(f"For {model_name}, please install via pip:")
        logger.info(f"pip install -q transformers sentence-transformers")
        logger.info(f"The model will be downloaded automatically when first used.")
        return True
    else:
        # Download the file
        destination = os.path.join(output_dir, model_info['filename'])
        
        if os.path.exists(destination):
            logger.info(f"Model {model_name} already exists at {destination}")
            return True
        
        try:
            download_file(model_info['url'], destination)
            return True
        except Exception as e:
            logger.error(f"Error downloading {model_name}: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Download models for Medical RAG system')
    parser.add_argument('--model', choices=list(MODELS.keys()), default='biomistral-7b-q4',
                        help='Model to download')
    parser.add_argument('--output-dir', default='../models', 
                        help='Directory to save models to')
    args = parser.parse_args()
    
    # Convert relative path to absolute path
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), args.output_dir))
    
    logger.info(f"Downloading {args.model} to {output_dir}")
    
    if download_model(args.model, output_dir):
        logger.info(f"Successfully downloaded {args.model}")
    else:
        logger.error(f"Failed to download {args.model}")

if __name__ == "__main__":
    main()
