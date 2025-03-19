import pytest
from src.services.response_service import ResponseGenerator

@pytest.fixture
def response_generator():
    return ResponseGenerator()

@pytest.mark.asyncio
async def test_generate_response(response_generator):
    query = "What is Python programming?"
    result = await response_generator.generate_response(query)
    
    assert "response" in result
    assert "context" in result
    assert "sources" in result
    assert isinstance(result["sources"], list)
    assert isinstance(result["response"], str)