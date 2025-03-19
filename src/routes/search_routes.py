"""
Search routes module handling search functionality endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.search_service import SearchService

router = APIRouter()
search_service = SearchService()

class SearchRequest(BaseModel):
    """Search request model containing query parameters."""
    query: str
    num_results: int = 5

@router.post("/search")
async def search(request: SearchRequest):
    """
    Process search request and return results.
    
    Args:
        request: SearchRequest containing query and number of results
    
    Returns:
        Dict containing search results and metadata
    """
    try:
        results = await search_service.aggregate_search_results(
            request.query,
            request.num_results
        )
        
        return {
            "status": "success",
            "query": request.query,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e