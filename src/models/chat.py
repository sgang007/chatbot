from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.database.config import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String)
    bot_response = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)