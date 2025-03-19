from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.response_service import ResponseGenerator
from src.database.config import get_db
from src.models.chat import Chat
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter()
response_generator = ResponseGenerator()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    sources: List[Dict[str, str]]

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # Generate response
        result = await response_generator.generate_response(request.message)
        
        # Store conversation in database
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
        raise HTTPException(status_code=500, detail=str(e))