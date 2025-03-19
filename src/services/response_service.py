"""
Response service module for generating chatbot responses.
"""

from typing import Dict
from src.services.nlp_service import NLPProcessor
from src.services.search_service import SearchService

class ResponseGenerator:
    """Service for generating coherent chatbot responses."""

    def __init__(self):
        """Initialize NLP and Search services."""
        self.nlp_processor = NLPProcessor()
        self.search_service = SearchService()

    async def generate_response(self, user_query: str) -> Dict:
        """
        Generate a response based on user query.

        Args:
            user_query: User's input message

        Returns:
            Dict containing response, context, and sources
        """
        context = self.nlp_processor.get_context(user_query)
        search_results = await self.search_service.aggregate_search_results(
            user_query,
            num_results=3
        )

        if not search_results:
            return {
                "response": "I apologize, but I couldn't find relevant information.",
                "context": context,
                "sources": []
            }

        combined_info = ""
        sources = []

        for result in search_results:
            combined_info += f"{result['snippet']} "
            sources.append({
                "title": result['title'],
                "link": result['link']
            })

        response = self.nlp_processor.humanize_response(combined_info)

        return {
            "response": response,
            "context": context,
            "sources": sources
        }