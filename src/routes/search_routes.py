from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.services.search_service import SearchService
from src.services.nlp_service import NLPProcessor

router = APIRouter()
search_service = SearchService()
nlp_processor = NLPProcessor()

class SearchRequest(BaseModel):
    query: str
    num_results: int = 5

@router.post("/search")
async def search(request: SearchRequest):
    try:
        # Process query using NLP
        processed_query = nlp_processor.format_search_query(request.query)
        
        # Get search results
        results = await search_service.aggregate_search_results(
            processed_query, 
            request.num_results
        )
        
        # Humanize the results
        humanized_results = []
        for result in results:
            humanized_results.append({
                **result,
                'snippet': nlp_processor.humanize_response(result['snippet'])
            })

        return {
            "status": "success",
            "original_query": request.query,
            "processed_query": processed_query,
            "results": humanized_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))