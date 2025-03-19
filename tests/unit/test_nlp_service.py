import pytest
from src.services.nlp_service import NLPProcessor

@pytest.fixture
def nlp_processor():
    return NLPProcessor()

def test_tokenize_text(nlp_processor):
    text = "Hello, this is a test message!"
    result = nlp_processor.tokenize_text(text)
    
    assert "words" in result
    assert "sentences" in result
    assert "original_text" in result
    assert len(result["words"]) > 0
    assert len(result["sentences"]) > 0
    assert result["original_text"] == text

def test_extract_keywords(nlp_processor):
    text = "Python programming is amazing for artificial intelligence and machine learning"
    keywords = nlp_processor.extract_keywords(text, top_n=3)
    
    assert len(keywords) <= 3
    assert isinstance(keywords, list)
    assert all(isinstance(k, str) for k in keywords)

def test_humanize_response(nlp_processor):
    text = "Additionally, this is a test. Furthermore, it should be humanized."
    result = nlp_processor.humanize_response(text)
    
    assert "additionally" not in result.lower()
    assert "furthermore" not in result.lower()
    assert "also" in result.lower()