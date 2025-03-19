"""
NLP routes module handling natural language processing endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.nlp_service import NLPProcessor

router = APIRouter()
nlp_processor = NLPProcessor()

class TextRequest(BaseModel):
    """Request model for text processing endpoints."""
    text: str

@router.post("/analyze")
async def analyze_text(request: TextRequest):
    """
    Analyze text using NLP processing.
    
    Args:
        request: TextRequest containing text to analyze
    
    Returns:
        Dict containing analysis results
    """
    try:
        context = nlp_processor.get_context(request.text)
        return {
            "status": "success",
            "analysis": context
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.post("/search-query")
async def format_search_query(request: TextRequest):
    """
    Format text into search-friendly query.
    
    Args:
        request: TextRequest containing text to format
    
    Returns:
        Dict containing formatted search query
    """
    try:
        query = nlp_processor.format_search_query(request.text)
        return {
            "status": "success",
            "search_query": query
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.post("/humanize")
async def humanize_text(request: TextRequest):
    """
    Convert text into more conversational format.
    
    Args:
        request: TextRequest containing text to humanize
    
    Returns:
        Dict containing humanized text
    """
    try:
        response = nlp_processor.humanize_response(request.text)
        return {
            "status": "success",
            "humanized_text": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e