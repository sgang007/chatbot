from typing import List, Dict
from src.services.nlp_service import NLPProcessor
from src.services.search_service import SearchService

class ResponseGenerator:
    def __init__(self):
        self.nlp_processor = NLPProcessor()
        self.search_service = SearchService()

    async def generate_response(self, user_query: str) -> Dict:
        # Process the query
        context = self.nlp_processor.get_context(user_query)
        
        # Get search results
        search_results = await self.search_service.aggregate_search_results(
            user_query, 
            num_results=3
        )
        
        # Combine and format response
        if not search_results:
            return {
                "response": "I apologize, but I couldn't find relevant information to answer your query.",
                "context": context,
                "sources": []
            }
        
        # Extract relevant information from search results
        combined_info = ""
        sources = []
        
        for result in search_results:
            combined_info += f"{result['snippet']} "
            sources.append({
                "title": result['title'],
                "link": result['link']
            })
        
        # Generate human-friendly response
        response = self.nlp_processor.humanize_response(combined_info)
        
        return {
            "response": response,
            "context": context,
            "sources": sources
        }