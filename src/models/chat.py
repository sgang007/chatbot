"""
Chat model module for database schema definition.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from src.database.config import Base

class Chat(Base):
    """
    Chat model for storing conversation history.
    
    Attributes:
        id (int): Primary key
        user_message (str): Message from user
        bot_response (str): Response from bot
        timestamp (datetime): Message timestamp
    """
    
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String)
    bot_response = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        """Return string representation of Chat."""
        return f"Chat(id={self.id}, timestamp={self.timestamp})"