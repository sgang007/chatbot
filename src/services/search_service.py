import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
import json
import time

load_dotenv()

class SearchService:
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.google_cx = os.getenv("GOOGLE_CX")
        self.cache = {}
        self.cache_timeout = 3600  # 1 hour

    async def search_google(self, query: str, num_results: int = 5) -> List[Dict]:
        """Search using Google Custom Search API"""
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
            response = requests.get(url, params=params)
            results = response.json()
            
            if 'items' not in results:
                return self.search_fallback(query, num_results)

            return [{
                'title': item.get('title', ''),
                'link': item.get('link', ''),
                'snippet': item.get('snippet', ''),
                'source': 'google'
            } for item in results['items']]

        except Exception:
            return self.search_fallback(query, num_results)

    def search_fallback(self, query: str, num_results: int = 5) -> List[Dict]:
        """Fallback to DuckDuckGo search"""
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        
        try:
            response = requests.get(url)
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
        except Exception as e:
            return []

    def cache_results(self, query: str, results: List[Dict]):
        """Cache search results"""
        self.cache[query] = {
            'results': results,
            'timestamp': time.time()
        }

    def get_cached_results(self, query: str) -> Optional[List[Dict]]:
        """Get cached results if available and not expired"""
        if query in self.cache:
            cache_data = self.cache[query]
            if time.time() - cache_data['timestamp'] < self.cache_timeout:
                return cache_data['results']
        return None

    async def aggregate_search_results(self, query: str, num_results: int = 5) -> List[Dict]:
        """Aggregate results from multiple search sources"""
        # Check cache first
        cached_results = self.get_cached_results(query)
        if cached_results:
            return cached_results

        # Perform new search
        results = await self.search_google(query, num_results)
        
        # Cache the results
        self.cache_results(query, results)
        
        return results