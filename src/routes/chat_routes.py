"""
Chat routes module handling conversation endpoints.
"""

from typing import List, Dict
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.services.response_service import ResponseGenerator
from src.database.config import get_db
from src.models.chat import Chat

router = APIRouter()
response_generator = ResponseGenerator()

class ChatRequest(BaseModel):
    """Chat request model."""
    message: str

class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    sources: List[Dict[str, str]]

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Process chat request and generate response.
    
    Args:
        request: Chat request containing user message
        db: Database session
    
    Returns:
        ChatResponse containing bot's response and sources
    """
    try:
        result = await response_generator.generate_response(request.message)
        
        chat_entry = Chat(
            user_message=request.message,
            bot_response=result["response"]
        )
        db.add(chat_entry)
        db.commit()
        
        return {
            "response": result["response"],
            "sources": result["sources"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e