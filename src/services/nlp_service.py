"""
NLP Service module for text processing and analysis.
This module provides functionality for tokenization, keyword extraction,
and text transformation using natural language processing techniques.
"""

from typing import List, Dict, Any
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer


class NLPProcessor:
    """
    Natural Language Processing service for text analysis and transformation.
    Provides methods for tokenization, keyword extraction, and text humanization.
    """

    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer()

    def tokenize_text(self, text: str) -> Dict[str, Any]:
        """
        Tokenize text into words and sentences.
        
        Args:
            text: Input text to tokenize
            
        Returns:
            Dictionary containing processed words, sentences, and original text
        """
        words = word_tokenize(text.lower())
        sentences = sent_tokenize(text)
        
        processed_words = [
            self.lemmatizer.lemmatize(word)
            for word in words
            if word.isalnum() and word not in self.stop_words
        ]

        return {
            "words": processed_words,
            "sentences": sentences,
            "original_text": text
        }

    def extract_keywords(self, text: str, top_n: int = 5) -> List[str]:
        """
        Extract key terms from text using TF-IDF.
        
        Args:
            text: Input text for keyword extraction
            top_n: Number of top keywords to return
            
        Returns:
            List of extracted keywords
        """
        tfidf_matrix = self.vectorizer.fit_transform([text])
        feature_names = self.vectorizer.get_feature_names_out()
        
        dense = tfidf_matrix.todense()
        scores = [(score, term) for term, score in 
                zip(feature_names, dense[0].tolist()[0])]
        sorted_scores = sorted(scores, reverse=True)
        
        return [term for score, term in sorted_scores[:top_n]]

    def get_context(self, text: str) -> Dict[str, Any]:
        """
        Analyze text to understand context and key information.
        
        Args:
            text: Input text for context analysis
            
        Returns:
            Dictionary containing keywords, POS tags, tokens, and sentence count
        """
        tokens = self.tokenize_text(text)
        keywords = self.extract_keywords(text)
        pos_tags = nltk.pos_tag(tokens["words"])
        
        return {
            "keywords": keywords,
            "pos_tags": pos_tags,
            "tokens": tokens,
            "sentence_count": len(tokens["sentences"])
        }

    def format_search_query(self, text: str) -> str:
        """
        Format text into search-friendly query.
        
        Args:
            text: Input text to format
            
        Returns:
            Formatted search query
        """
        keywords = self.extract_keywords(text, top_n=3)
        return " ".join(keywords)

    def humanize_response(self, text: str) -> str:
        """
        Convert formal text into more conversational format.
        
        Args:
            text: Input text to humanize
            
        Returns:
            Humanized conversational text
        """
        replacements = {
            "additionally": "also",
            "furthermore": "also",
            "moreover": "plus",
            "consequently": "so",
            "therefore": "so",
            "thus": "so",
            "nevertheless": "but",
            "however": "but",
            "in addition": "also",
            "in conclusion": "finally"
        }
        
        result = text.lower()
        for formal, casual in replacements.items():
            result = result.replace(formal.lower(), casual)
        
        sentences = sent_tokenize(result)
        result = ". ".join(s.capitalize() for s in sentences)
        
        if len(sentences) > 1:
            result = result.replace(". ", ". Well, ", result.count(". ") - 1)
        
        return result