import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Dict, Any

class NLPProcessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer()

    def tokenize_text(self, text: str) -> Dict[str, Any]:
        """Tokenize text into words and sentences"""
        words = word_tokenize(text.lower())
        sentences = sent_tokenize(text)
        
        # Remove stop words and lemmatize
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
        """Extract key terms from text using TF-IDF"""
        # Fit and transform the text
        tfidf_matrix = self.vectorizer.fit_transform([text])
        feature_names = self.vectorizer.get_feature_names_out()
        
        # Get top terms
        dense = tfidf_matrix.todense()
        scores = [(score, term) for term, score in 
                 zip(feature_names, dense[0].tolist()[0])]
        sorted_scores = sorted(scores, reverse=True)
        
        return [term for score, term in sorted_scores[:top_n]]

    def get_context(self, text: str) -> Dict[str, Any]:
        """Analyze text to understand context and key information"""
        tokens = self.tokenize_text(text)
        keywords = self.extract_keywords(text)
        
        # Perform POS tagging
        pos_tags = nltk.pos_tag(tokens["words"])
        
        return {
            "keywords": keywords,
            "pos_tags": pos_tags,
            "tokens": tokens,
            "sentence_count": len(tokens["sentences"])
        }

    def format_search_query(self, text: str) -> str:
        """Format text into search-friendly query"""
        keywords = self.extract_keywords(text, top_n=3)
        return " ".join(keywords)

    def humanize_response(self, text: str) -> str:
        """Convert formal text into more conversational format"""
        sentences = sent_tokenize(text)
        
        # Simple transformation rules
        if len(sentences) > 1:
            # Join sentences with conversational connectors
            response = " Well, ".join(sentences)
        else:
            response = text
            
        # Add conversational touches
        response = response.replace(" additionally ", " also ")
        response = response.replace(" furthermore ", " also ")
        response = response.replace(" moreover ", " plus ")
        
        return response