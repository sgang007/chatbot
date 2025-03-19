"""
Search service module providing search functionality across multiple sources.
"""

import json
import os
import time
from typing import List, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

class SearchService:
    """Service for handling search operations across different search engines."""

    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.google_cx = os.getenv("GOOGLE_CX")
        self.cache = {}
        self.cache_timeout = 3600  # 1 hour
        self.request_timeout = 10  # seconds

    async def search_google(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Search using Google Custom Search API.
        
        Args:
            query: Search query string
            num_results: Number of results to return
            
        Returns:
            List of search results
        """
        if not self.google_api_key or not self.google_cx:
            return self.search_fallback(query, num_results)

        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': self.google_api_key,
            'cx': self.google_cx,
            'q': query,
            'num': num_results
        }

        try:
            response = requests.get(
                url,
                params=params,
                timeout=self.request_timeout
            )
            results = response.json()
            
            if 'items' not in results:
                return self.search_fallback(query, num_results)

            return [{
                'title': item.get('title', ''),
                'link': item.get('link', ''),
                'snippet': item.get('snippet', ''),
                'source': 'google'
            } for item in results['items']]

        except requests.RequestException:
            return self.search_fallback(query, num_results)

    def search_fallback(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Fallback search using DuckDuckGo when Google search fails.
        
        Args:
            query: Search query string
            num_results: Number of results to return
            
        Returns:
            List of search results
        """
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        
        try:
            response = requests.get(url, timeout=self.request_timeout)
            data = response.json()
            
            results = []
            for result in data.get('RelatedTopics', [])[:num_results]:
                results.append({
                    'title': result.get('Text', ''),
                    'link': result.get('FirstURL', ''),
                    'snippet': result.get('Text', ''),
                    'source': 'duckduckgo'
                })
            
            return results
        except requests.RequestException:
            return []

    def cache_results(self, query: str, results: List[Dict]) -> None:
        """Cache search results with timestamp."""
        self.cache[query] = {
            'results': results,
            'timestamp': time.time()
        }

    def get_cached_results(self, query: str) -> Optional[List[Dict]]:
        """Retrieve cached results if they haven't expired."""
        if query in self.cache:
            cache_data = self.cache[query]
            if time.time() - cache_data['timestamp'] < self.cache_timeout:
                return cache_data['results']
        return None

    async def aggregate_search_results(
        self,
        query: str,
        num_results: int = 5
    ) -> List[Dict]:
        """
        Aggregate results from multiple search sources.
        
        Args:
            query: Search query string
            num_results: Number of results to return
            
        Returns:
            List of aggregated search results
        """
        cached_results = self.get_cached_results(query)
        if cached_results:
            return cached_results

        results = await self.search_google(query, num_results)
        self.cache_results(query, results)
        return results