"""
Database initialization module.
Creates all defined tables in the database.
"""

from src.database.config import engine
from src.models.chat import Base

def init_db():
    """Initialize the database by creating all defined tables."""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()