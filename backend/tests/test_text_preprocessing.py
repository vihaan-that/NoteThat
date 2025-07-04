import pytest
from app.utils.text_preprocessing import clean_text, extract_medical_entities, preprocess_medical_document


def test_clean_text():
    """Test text cleaning functionality"""
    # Test basic cleaning
    input_text = "  Multiple   spaces   between  words  "
    expected = "Multiple spaces between words"
    assert clean_text(input_text) == expected
    
    # Test unicode normalization
    input_text = "Caf\u00e9 with accents"
    expected = "Café with accents"
    assert clean_text(input_text) == expected
    
    # Test OCR error correction
    input_text = "The patient was prescribed 10rng of medication"
    expected = "The patient was prescribed 10mg of medication"
    assert clean_text(input_text) == expected
    
    # Test medical abbreviation expansion
    input_text = "Take 5mg b.i.d."
    expected = "Take 5mg twice daily."
    assert clean_text(input_text) == expected
    
    # Test empty input
    assert clean_text("") == ""
    assert clean_text(None) == ""


def test_extract_medical_entities():
    """Test medical entity extraction"""
    # Test medication extraction
    input_text = "Patient is on Metformin 500mg tablets twice daily and Lisinopril 10mg."
    entities = extract_medical_entities(input_text)
    
    assert "medications" in entities
    assert len(entities["medications"]) > 0
    assert any("Metformin" in med for med in entities["medications"])
    
    # Test measurement extraction
    input_text = "Blood pressure was 120/80 mmHg, weight 70kg, and height 175cm."
    entities = extract_medical_entities(input_text)
    
    assert "measurements" in entities
    assert len(entities["measurements"]) >= 2
    assert any("mmHg" in m for m in entities["measurements"])
    assert any("kg" in m for m in entities["measurements"])
    assert any("cm" in m for m in entities["measurements"])
    
    # Test with text containing no entities
    input_text = "The patient was seen in clinic today."
    entities = extract_medical_entities(input_text)
    
    assert all(len(entity_list) == 0 for entity_list in entities.values())


def test_preprocess_medical_document():
    """Test complete document preprocessing"""
    # Create a test document
    document = {
        "content": "  Patient reports taking Metformin 500mg b.i.d.  Blood pressure was 140/90 mmHg. ",
        "metadata": {
            "source": "test_document.pdf",
            "page": 1
        }
    }
    
    # Process the document
    result = preprocess_medical_document(document)
    
    # Check that content is cleaned
    assert "  " not in result["content"]
    assert "twice daily" in result["content"]
    
    # Check that metadata is preserved and entities are added
    assert "source" in result["metadata"]
    assert result["metadata"]["source"] == "test_document.pdf"
    assert "extracted_entities" in result["metadata"]
    assert "medications" in result["metadata"]["extracted_entities"]
    assert "measurements" in result["metadata"]["extracted_entities"]
    
    # Test with empty document
    empty_document = {"content": "", "metadata": {}}
    result = preprocess_medical_document(empty_document)
    
    assert result["content"] == ""
    assert "extracted_entities" in result["metadata"]
