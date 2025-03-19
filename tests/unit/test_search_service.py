import pytest
from src.services.search_service import SearchService

@pytest.fixture
def search_service():
    return SearchService()

@pytest.mark.asyncio
async def test_search_fallback(search_service):
    results = search_service.search_fallback("python programming")
    
    assert isinstance(results, list)
    for result in results:
        assert "title" in result
        assert "link" in result
        assert "snippet" in result
        assert "source" in result

@pytest.mark.asyncio
async def test_cache_mechanism(search_service):
    query = "test query"
    test_results = [{"title": "Test", "link": "http://test.com", "snippet": "Test"}]
    
    search_service.cache_results(query, test_results)
    cached = search_service.get_cached_results(query)
    
    assert cached == test_results