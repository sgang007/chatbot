from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.nlp_service import NLPProcessor

router = APIRouter()
nlp_processor = NLPProcessor()

class TextRequest(BaseModel):
    text: str

@router.post("/analyze")
async def analyze_text(request: TextRequest):
    try:
        context = nlp_processor.get_context(request.text)
        return {
            "status": "success",
            "analysis": context
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search-query")
async def format_search_query(request: TextRequest):
    try:
        query = nlp_processor.format_search_query(request.text)
        return {
            "status": "success",
            "search_query": query
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/humanize")
async def humanize_text(request: TextRequest):
    try:
        response = nlp_processor.humanize_response(request.text)
        return {
            "status": "success",
            "humanized_text": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))