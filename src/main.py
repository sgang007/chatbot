"""
Main application module for the Chatbot API.
Configures FastAPI application, middleware, and routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import nltk
from src.routes import nlp_routes, search_routes, chat_routes

# Download required NLTK datasets
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')

app = FastAPI(
    title="Chatbot API",
    description="An AI-powered chatbot API using NLP",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(nlp_routes.router, prefix="/nlp", tags=["NLP"])
app.include_router(search_routes.router, prefix="/search", tags=["Search"])
app.include_router(chat_routes.router, prefix="/chat", tags=["Chat"])

@app.get("/")
async def root():
    """Root endpoint returning welcome message."""
    return {"message": "Welcome to the Chatbot API"}