import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from googlesearch import search
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import warnings
import logging
warnings.filterwarnings('ignore')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

class NewsAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        # Default industry keywords
        self.default_keywords = {
            'finance': ['stock market', 'cryptocurrency', 'banking', 'investment', 'fintech'],
            'ai': ['artificial intelligence', 'machine learning', 'deep learning', 'robotics', 'neural networks'],
            'real_estate': ['property market', 'real estate trends', 'housing market', 'commercial property', 'real estate investment']
        }
        
    def extract_keywords(self, df):
        """Extract relevant keywords from the dataset and combine with default industry keywords"""
        try:
            keywords = []
            
            # Add default industry keywords
            for industry_keywords in self.default_keywords.values():
                keywords.extend(industry_keywords)
            
            # Get column names as keywords
            keywords.extend(df.columns.tolist())
            
            # Get unique values from categorical columns
            categorical_cols = df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                try:
                    unique_values = df[col].unique()
                    # Convert all values to strings and filter out None/NaN
                    keywords.extend([str(val) for val in unique_values if pd.notna(val)])
                except Exception as e:
                    logger.warning(f"Error processing column {col}: {str(e)}")
                    continue
                
            # Get statistical keywords from numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                keywords.extend([
                    f"{col} trend",
                    f"{col} analysis",
                    f"{col} forecast"
                ])
                
            # Clean and filter keywords
            keywords = [k for k in keywords if isinstance(k, str) and len(k.strip()) > 0]
            return list(set(keywords))  # Remove duplicates
            
        except Exception as e:
            logger.error(f"Error in extract_keywords: {str(e)}")
            return []
    
    def search_news(self, keywords, num_articles=3):
        """Search for news articles related to the keywords"""
        articles = []
        
        for keyword in keywords[:5]:  # Limit to first 5 keywords to avoid too many requests
            try:
                # Search Google News
                search_query = f"{keyword} news {datetime.now().year}"
                search_results = search(search_query, num_results=num_articles)
                
                for url in search_results:
                    try:
                        article = Article(url)
                        article.download()
                        article.parse()
                        article.nlp()  # This will extract keywords, summary, etc.
                        
                        articles.append({
                            'title': str(article.title) if article.title else '',
                            'text': str(article.text) if article.text else '',
                            'summary': str(article.summary) if article.summary else '',
                            'keywords': list(article.keywords) if article.keywords else [],
                            'url': str(url),
                            'published_date': article.publish_date,
                            'source': str(url.split('/')[2]) if len(url.split('/')) > 2 else url
                        })
                    except Exception as e:
                        logger.warning(f"Error processing article {url}: {str(e)}")
                        continue
                        
            except Exception as e:
                logger.warning(f"Error searching for keyword {keyword}: {str(e)}")
                continue
                
        return pd.DataFrame(articles) if articles else pd.DataFrame()
    
    def analyze_sentiment(self, articles_df):
        """Analyze sentiment of news articles"""
        if articles_df is None or len(articles_df) == 0:
            return pd.DataFrame()
            
        sentiments = []
        for text in articles_df['text']:
            try:
                sentiment = self.sia.polarity_scores(str(text))
                sentiments.append({
                    'compound': float(sentiment['compound']),
                    'positive': float(sentiment['pos']),
                    'negative': float(sentiment['neg']),
                    'neutral': float(sentiment['neu'])
                })
            except Exception as e:
                logger.warning(f"Error analyzing sentiment: {str(e)}")
                sentiments.append({
                    'compound': 0.0,
                    'positive': 0.0,
                    'negative': 0.0,
                    'neutral': 1.0
                })
            
        articles_df['sentiment'] = sentiments
        return articles_df
    
    def get_impact_analysis(self, articles_df):
        """Analyze the potential impact of news on the dataset"""
        if articles_df is None or len(articles_df) == 0:
            return pd.DataFrame()
            
        impact_analysis = []
        for _, article in articles_df.iterrows():
            try:
                sentiment = article['sentiment']
                impact = {
                    'title': str(article['title']),
                    'summary': str(article['summary']),
                    'sentiment': 'Positive' if sentiment['compound'] > 0.2 else 
                                'Negative' if sentiment['compound'] < -0.2 else 
                                'Neutral',
                    'confidence': float(abs(sentiment['compound'])),
                    'source': str(article['source']),
                    'url': str(article['url'])
                }
                impact_analysis.append(impact)
            except Exception as e:
                logger.warning(f"Error processing impact analysis: {str(e)}")
                continue
            
        return pd.DataFrame(impact_analysis) if impact_analysis else pd.DataFrame()
    
    def analyze_news_for_dataset(self, df):
        """Main function to analyze news for a given dataset"""
        try:
            # Extract keywords from dataset
            keywords = self.extract_keywords(df)
            if not keywords:
                logger.warning("No keywords extracted from dataset")
                return {
                    'news': pd.DataFrame(),
                    'impact': pd.DataFrame(),
                    'keywords': []
                }
            
            # Search for relevant news
            news_df = self.search_news(keywords)
            if news_df.empty:
                logger.warning("No news articles found")
                return {
                    'news': pd.DataFrame(),
                    'impact': pd.DataFrame(),
                    'keywords': keywords
                }
            
            # Analyze sentiment
            news_df = self.analyze_sentiment(news_df)
            
            # Get impact analysis
            impact_df = self.get_impact_analysis(news_df)
            
            return {
                'news': news_df,
                'impact': impact_df,
                'keywords': keywords
            }
            
        except Exception as e:
            logger.error(f"Error in analyze_news_for_dataset: {str(e)}")
            return {
                'news': pd.DataFrame(),
                'impact': pd.DataFrame(),
                'keywords': []
            } 