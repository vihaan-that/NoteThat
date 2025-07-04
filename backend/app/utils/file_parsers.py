"""
File parser utilities for handling different file types in the Medical RAG system.
"""

import os
import mimetypes
from typing import Dict, Any, Optional


async def parse_file(file_content: bytes, file_name: str) -> Dict[str, Any]:
    """
    Parse a file based on its type/extension and extract its text content.
    
    Args:
        file_content (bytes): Raw file content
        file_name (str): Name of the file with extension
        
    Returns:
        Dict[str, Any]: Dictionary with extracted content and metadata
    """
    file_extension = os.path.splitext(file_name.lower())[1]
    
    # Determine MIME type
    mime_type, _ = mimetypes.guess_type(file_name)
    
    # Text files
    if file_extension in ['.txt', '.md'] or mime_type == 'text/plain':
        return await parse_text_file(file_content, file_name)
    
    # PDF files - in a real implementation, we'd use a PDF parsing library
    # For demonstration purposes, we'll just return placeholder content
    elif file_extension == '.pdf' or mime_type == 'application/pdf':
        return {
            "content": f"This is placeholder content for PDF file: {file_name}. In a real implementation, this would use a PDF parser.",
            "metadata": {
                "source": file_name,
                "file_type": "pdf",
                "mime_type": mime_type
            }
        }
    
    # Default case - try to decode as text
    else:
        try:
            content = file_content.decode('utf-8')
            return {
                "content": content,
                "metadata": {
                    "source": file_name,
                    "file_type": file_extension.replace('.', ''),
                    "mime_type": mime_type or "application/octet-stream"
                }
            }
        except UnicodeDecodeError:
            # If we can't decode it, return a placeholder
            return {
                "content": f"Unable to extract text from {file_name}. File type not supported.",
                "metadata": {
                    "source": file_name,
                    "file_type": file_extension.replace('.', ''),
                    "mime_type": mime_type or "application/octet-stream",
                    "error": "Unable to decode file content"
                }
            }


async def parse_text_file(file_content: bytes, file_name: str) -> Dict[str, Any]:
    """
    Parse a text file and extract its content.
    
    Args:
        file_content (bytes): Raw file content
        file_name (str): Name of the file
        
    Returns:
        Dict[str, Any]: Dictionary with extracted content and metadata
    """
    try:
        # Try UTF-8 first
        content = file_content.decode('utf-8')
    except UnicodeDecodeError:
        try:
            # Try Latin-1 as a fallback
            content = file_content.decode('latin-1')
        except:
            # If all else fails, decode with errors ignored
            content = file_content.decode('utf-8', errors='ignore')
    
    return {
        "content": content,
        "metadata": {
            "source": file_name,
            "file_type": "text",
            "mime_type": "text/plain",
            "char_count": len(content)
        }
    }


# Note: In a real implementation, you would include parsers for other file types:
# - parse_pdf_file: using PyPDF2, pdfminer, or similar
# - parse_docx_file: using python-docx
# - parse_image_file: using OCR with pytesseract
# These are omitted here to keep dependencies minimal
