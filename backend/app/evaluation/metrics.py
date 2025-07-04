"""
Evaluation metrics for the Medical RAG system.
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class EvaluationResult:
    """Data class for evaluation results"""
    query_id: str
    query: str
    answer: str
    sources: List[str]
    metrics: Dict[str, float]
    feedback: Optional[Dict[str, Any]] = None


def count_medical_terms(text: str) -> int:
    """
    Count medical terms in text using basic regex patterns.
    In a production system, this would use a comprehensive medical dictionary.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        int: Count of identified medical terms
    """
    # Basic patterns for medical terms (simplified)
    patterns = [
        r'\b(?:disease|syndrome|disorder|condition)\b',
        r'\b(?:medication|drug|treatment|therapy|dosage)\b',
        r'\b(?:diagnosis|prognosis|symptoms|signs)\b',
        r'\b(?:mg|ml|mcg|units)\b',
        r'\b(?:diabetes|hypertension|asthma|cancer|arthritis)\b'
    ]
    
    count = 0
    for pattern in patterns:
        count += len(re.findall(pattern, text, re.IGNORECASE))
    
    return count


def citation_count(answer: str) -> int:
    """
    Count number of citations in the answer.
    
    Args:
        answer (str): Generated answer text
        
    Returns:
        int: Number of citations
    """
    # Look for citation patterns like [1], [2], etc.
    citations = re.findall(r'\[\d+\]', answer)
    return len(citations)


def calculate_answer_relevance(query: str, answer: str) -> float:
    """
    Calculate a simple relevance score between query and answer.
    In a production system, this would use more sophisticated NLP techniques.
    
    Args:
        query (str): The user query
        answer (str): The generated answer
        
    Returns:
        float: Relevance score between 0.0 and 1.0
    """
    # Convert to lowercase for comparison
    query_lower = query.lower()
    answer_lower = answer.lower()
    
    # Extract key terms from query
    query_terms = set(re.findall(r'\b\w+\b', query_lower))
    
    # Count how many query terms appear in answer
    matches = sum(1 for term in query_terms if term in answer_lower)
    
    if len(query_terms) == 0:
        return 0.0
    
    return matches / len(query_terms)


def calculate_source_quality(sources: List[str]) -> float:
    """
    Assess quality of sources based on simple heuristics.
    In a production system, this would check against trusted medical databases.
    
    Args:
        sources (List[str]): List of source texts
        
    Returns:
        float: Source quality score between 0.0 and 1.0
    """
    if not sources:
        return 0.0
    
    total_score = 0.0
    
    for source in sources:
        # Check source length (longer sources might be more comprehensive)
        length_score = min(len(source) / 500, 1.0)  # Cap at 1.0
        
        # Check for medical terms
        term_count = count_medical_terms(source)
        term_score = min(term_count / 5, 1.0)  # Cap at 1.0
        
        # Average the scores for this source
        source_score = (length_score + term_score) / 2
        total_score += source_score
    
    return total_score / len(sources)


def evaluate_response(query: str, 
                      answer: str, 
                      sources: List[str], 
                      query_id: str = None) -> EvaluationResult:
    """
    Evaluate a RAG system response using multiple metrics.
    
    Args:
        query (str): The user query
        answer (str): The generated answer
        sources (List[str]): List of source texts used for answer generation
        query_id (str): Optional identifier for the query
        
    Returns:
        EvaluationResult: Evaluation results with multiple metrics
    """
    # Generate query ID if not provided
    if not query_id:
        query_id = f"query_{hash(query) % 10000}"
    
    # Calculate metrics
    relevance_score = calculate_answer_relevance(query, answer)
    source_quality = calculate_source_quality(sources)
    citations = citation_count(answer)
    medical_term_count = count_medical_terms(answer)
    
    # Calculate an overall score
    overall_score = (relevance_score * 0.4 + 
                    source_quality * 0.3 + 
                    min(citations / 3, 1.0) * 0.2 + 
                    min(medical_term_count / 5, 1.0) * 0.1)
    
    # Create metrics dictionary
    metrics = {
        "relevance": relevance_score,
        "source_quality": source_quality,
        "citation_count": citations,
        "medical_term_count": medical_term_count,
        "overall_score": overall_score
    }
    
    return EvaluationResult(
        query_id=query_id,
        query=query,
        answer=answer,
        sources=sources,
        metrics=metrics
    )
