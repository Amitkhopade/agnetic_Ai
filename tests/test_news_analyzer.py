import unittest
import pandas as pd
import numpy as np
from src.news_analyzer import NewsAnalyzer

class TestNewsAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = NewsAnalyzer()
        self.sample_df = pd.DataFrame({
            'numeric_col': [1, 2, 3, 4, 5],
            'text_col': ['apple', 'banana', 'orange', 'grape', 'mango'],
            'date_col': pd.date_range(start='2024-01-01', periods=5)
        })

    def test_extract_keywords(self):
        keywords = self.analyzer.extract_keywords(self.sample_df)
        self.assertIsInstance(keywords, list)
        self.assertTrue(len(keywords) > 0)
        self.assertTrue(all(isinstance(k, str) for k in keywords))

    def test_analyze_sentiment(self):
        test_articles = pd.DataFrame({
            'text': ['This is a positive article.', 'This is a negative article.'],
            'title': ['Good News', 'Bad News'],
            'url': ['http://example.com/1', 'http://example.com/2']
        })
        result = self.analyzer.analyze_sentiment(test_articles)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue('sentiment' in result.columns)

    def test_get_impact_analysis(self):
        test_articles = pd.DataFrame({
            'title': ['Test Article'],
            'summary': ['Test Summary'],
            'sentiment': [{'compound': 0.5, 'pos': 0.6, 'neg': 0.1, 'neu': 0.3}],
            'source': ['test.com'],
            'url': ['http://test.com']
        })
        result = self.analyzer.get_impact_analysis(test_articles)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertTrue('sentiment' in result.columns)
        self.assertTrue('confidence' in result.columns)

if __name__ == '__main__':
    unittest.main() 