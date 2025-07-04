"""
Text preprocessing utilities for the Medical RAG system.
These functions help clean and normalize medical text data before indexing.
"""

import re
import unicodedata
from typing import List, Dict, Any


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace, normalizing unicode characters,
    and fixing common OCR issues in medical texts.
    
    Args:
        text (str): Text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Normalize unicode
    text = unicodedata.normalize('NFKC', text)
    
    # Fix common OCR errors in medical text
    text = text.replace("rn", "m")  # Common OCR mistake
    text = re.sub(r'(\d)l', r'\1l', text)  # Fix 1l -> 11 issue
    
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Fix common medical abbreviations
    text = re.sub(r'\bb\.i\.d\b', 'twice daily', text, flags=re.IGNORECASE)
    text = re.sub(r'\bt\.i\.d\b', 'three times daily', text, flags=re.IGNORECASE)
    text = re.sub(r'\bq\.i\.d\b', 'four times daily', text, flags=re.IGNORECASE)
    
    # Remove URLs (often not useful in medical context)
    text = re.sub(r'https?://\S+', '', text)
    
    return text.strip()


def extract_medical_entities(text: str) -> Dict[str, List[str]]:
    """
    Extract medical entities from text using regex patterns.
    This is a simple implementation - in production, you might use a medical NER model.
    
    Args:
        text (str): Text to extract entities from
        
    Returns:
        Dict[str, List[str]]: Dictionary of entity types and their values
    """
    entities = {
        "medications": [],
        "conditions": [],
        "measurements": []
    }
    
    # Extract medication mentions (simplified approach)
    medication_pattern = r'\b(tablets?|capsules?|mg|mcg|dose|injection|infusion)\b'
    medication_matches = re.findall(r'([A-Z][a-z]+(?:\s+[a-z]+)?\s+' + medication_pattern + r')', text)
    if medication_matches:
        entities["medications"] = [m.strip() for m in medication_matches]
    
    # Extract measurements
    measurement_pattern = r'\b\d+(?:\.\d+)?\s*(?:mg|ml|kg|cm|mm|mmHg|bpm)\b'
    measurement_matches = re.findall(measurement_pattern, text)
    if measurement_matches:
        entities["measurements"] = measurement_matches
    
    return entities


def preprocess_medical_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """
    Preprocess a medical document by cleaning the text and extracting entities.
    
    Args:
        document (Dict[str, Any]): Document with content and metadata
        
    Returns:
        Dict[str, Any]: Preprocessed document with cleaned content and extracted entities
    """
    content = document.get("content", "")
    metadata = document.get("metadata", {})
    
    # Clean the text
    cleaned_content = clean_text(content)
    
    # Extract medical entities
    entities = extract_medical_entities(cleaned_content)
    
    # Add extracted entities to metadata
    metadata["extracted_entities"] = entities
    
    return {
        "content": cleaned_content,
        "metadata": metadata
    }
