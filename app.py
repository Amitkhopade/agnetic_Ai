import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
from datetime import datetime
import requests
import json
import random
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
import PyPDF2
import docx

from src.data_analyzer import DataAnalyzer
from src.visualization import create_visualization
from src.news_analyzer import NewsAnalyzer

# Initialize session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'df' not in st.session_state:
    st.session_state.df = None
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = DataAnalyzer()
if 'news_analyzer' not in st.session_state:
    st.session_state.news_analyzer = NewsAnalyzer()
if 'news_data' not in st.session_state:
    st.session_state.news_data = None

# Set page configuration
st.set_page_config(
    page_title="Data Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #ffffff;
        padding: 2rem;
    }
    
    /* Card styling */
    .stCard {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e0e0e0;
        margin-bottom: 1.5rem;
    }
    
    /* News card styling */
    .news-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #2c5530;
    }
    
    .news-card.positive {
        border-left-color: #28a745;
    }
    
    .news-card.negative {
        border-left-color: #dc3545;
    }
    
    .news-card.neutral {
        border-left-color: #6c757d;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        background-color: #f8f9fa;
        border-radius: 5px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2c5530;
        color: white;
    }
    
    /* Button styling */
    .stButton button {
        background-color: #2c5530;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: 500;
    }
    
    .stButton button:hover {
        background-color: #1e3b21;
    }
</style>
""", unsafe_allow_html=True)

# Configure Gemini API
GOOGLE_API_KEY = "Google_API_KEY"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def get_gemini_response(df, query, analyzer):
    """Get response from Gemini model using RAG approach"""
    try:
        # Search for relevant documents
        relevant_docs = analyzer.search_documents(query)
        
        # Prepare context with relevant documents
        context = f"""
        You are a data analysis expert. Analyze the following data and answer the user's question.
        Base your response ONLY on the provided data from the Excel file.
        
        Relevant Data from Excel:
        {json.dumps(relevant_docs, indent=2)}
        
        Dataset Information:
        - Number of rows: {len(df)}
        - Number of columns: {len(df.columns)}
        - Column names: {', '.join(df.columns)}
        
        User Query: {query}
        
        Please provide:
        1. A detailed analysis answering the query based on the actual data
        2. Specific numerical insights and statistics from the data
        3. Relevant trends or patterns observed
        4. Suggestions for further analysis if applicable
        
        If the query involves calculations, perform them on the provided data and show your work.
        Format your response in a clear, structured way with specific numbers and insights from the data.
        """
        
        # Prepare the API request
        headers = {
            'Content-Type': 'application/json'
        }
        
        data = {
            "contents": [{
                "parts": [{"text": context}]
            }]
        }
        
        # Make the API request
        response = requests.post(
            f"{GEMINI_API_URL}?key={GOOGLE_API_KEY}",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return "I apologize, but I'm having trouble processing your request. Please try again or rephrase your question."
            
    except Exception as e:
        st.error(f"Error with Gemini API: {str(e)}")
        return "I apologize, but I'm having trouble processing your request. Please try again or rephrase your question."

def process_file(uploaded_file):
    """Process uploaded file and return DataFrame"""
    try:
        if uploaded_file is not None:
            df = st.session_state.analyzer.load_data(uploaded_file)
            if df is not None:
                # Clean the data
                df = st.session_state.analyzer.clean_data(df)
                return df
        return None
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

def display_news_analysis(news_data):
    """Display news analysis in a structured format"""
    if news_data is None:
        st.warning("No news data available. Please try analyzing the news again.")
        return
        
    st.markdown("### 📰 Related News Analysis")
    
    # Display impact summary
    impact_df = news_data['impact']
    if impact_df is not None and not impact_df.empty:
        # Calculate sentiment distribution
        sentiment_counts = impact_df['sentiment'].value_counts()
        
        # Create columns for sentiment distribution
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Positive News", sentiment_counts.get('Positive', 0))
        with col2:
            st.metric("Negative News", sentiment_counts.get('Negative', 0))
        with col3:
            st.metric("Neutral News", sentiment_counts.get('Neutral', 0))
        
        # Display news articles
        st.markdown("### Latest News Articles")
        for _, article in impact_df.iterrows():
            sentiment_class = article['sentiment'].lower()
            st.markdown(f"""
            <div class="news-card {sentiment_class}">
                <h4>{article['title']}</h4>
                <p>{article['summary']}</p>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span>Source: {article['source']}</span>
                    <span>Sentiment: {article['sentiment']} (Confidence: {article['confidence']:.2f})</span>
                </div>
                <a href="{article['url']}" target="_blank">Read More</a>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No relevant news articles found. Try uploading a different dataset or try again later.")

def main():
    st.title("📊 Data Analysis Dashboard")
    
    # File upload section
    uploaded_file = st.file_uploader("Upload your data file", type=['csv', 'xlsx', 'json', 'txt', 'pdf', 'docx'])
    
    if uploaded_file is not None:
        df = process_file(uploaded_file)
        if df is not None:
            st.session_state.df = df
            
            # Create tabs
            tab1, tab2, tab3, tab4 = st.tabs([
                "📈 Data Analysis", 
                "📊 Visualization", 
                "💬 Chat with Data",
                "📰 News Analysis"
            ])
            
            with tab1:
                st.markdown("### Data Analysis")
                # Perform and display analysis
                st.session_state.analyzer.analyze_data(df)
                
                # Display basic statistics
                st.markdown("#### Basic Statistics")
                st.write(df.describe())
                
                # Display data types
                st.markdown("#### Data Types")
                st.write(df.dtypes)
            
            with tab2:
                st.markdown("### Visualization")
                # Visualization options
                chart_type = st.selectbox("Select Chart Type", 
                    ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", "Box Plot", "Violin Plot"])
                
                # Column selection
                x_col = st.selectbox("Select X-axis column", df.columns)
                
                if chart_type in ["Bar Chart", "Line Chart", "Scatter Plot", "Box Plot", "Violin Plot"]:
                    y_col = st.selectbox("Select Y-axis column", df.columns)
                else:
                    y_col = None
                
                if chart_type == "Scatter Plot":
                    color_col = st.selectbox("Select color column (optional)", ["None"] + list(df.columns))
                    if color_col == "None":
                        color_col = None
                else:
                    color_col = None
                
                if st.button("Generate Visualization"):
                    fig = create_visualization(df, chart_type, x_col, y_col, color_col)
                    if fig is not None:
                        st.pyplot(fig)
            
            with tab3:
                st.markdown("### Chat with Your Data")
                user_query = st.text_input("Ask a question about your data:")
                
                if user_query:
                    response = get_gemini_response(df, user_query, st.session_state.analyzer)
                    st.write(response)
            
            with tab4:
                st.markdown("### News Analysis")
                if st.button("Analyze Related News"):
                    with st.spinner("Analyzing news related to your data... This may take a few moments."):
                        try:
                            news_data = st.session_state.news_analyzer.analyze_news_for_dataset(df)
                            st.session_state.news_data = news_data
                            display_news_analysis(news_data)
                        except Exception as e:
                            st.error(f"Error analyzing news: {str(e)}")
                            st.info("Please try again or upload a different dataset.")
                elif st.session_state.news_data is not None:
                    display_news_analysis(st.session_state.news_data)

if __name__ == "__main__":
    main() 
