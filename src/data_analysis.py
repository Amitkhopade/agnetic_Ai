import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import docx

class DataAnalyzer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.df = None
        self.df_clean = None
        self.document_texts = []
        self.tfidf_matrix = None
        self.documents = []
        
    def load_data(self, file):
        """Load and preprocess the file based on its type"""
        try:
            file_type = file.name.split('.')[-1].lower()
            
            if file_type in ['xlsx', 'xls']:
                # Handle Excel files
                df = pd.read_excel(file)
                self.df = df
                self.df_clean = df.copy()
                self._update_document_texts()
                return df
                
            elif file_type == 'pdf':
                # Handle PDF files
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                self._add_document(text, file.name)
                return None
                
            elif file_type == 'docx':
                # Handle Word files
                doc = docx.Document(file)
                text = ""
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                self._add_document(text, file.name)
                return None
                
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return None
    
    def _add_document(self, text, filename):
        """Add document to the collection"""
        self.documents.append({
            'text': text,
            'filename': filename
        })
        self._update_document_texts()
    
    def _update_document_texts(self):
        """Update document texts and TF-IDF matrix"""
        self.document_texts = []
        
        # Add Excel data if available
        if self.df_clean is not None:
            for _, row in self.df_clean.iterrows():
                doc_text = " | ".join([f"{col}: {val}" for col, val in row.items()])
                self.document_texts.append(doc_text)
        
        # Add PDF/Word documents
        for doc in self.documents:
            self.document_texts.append(doc['text'])
        
        # Update TF-IDF matrix if we have documents
        if self.document_texts:
            self.tfidf_matrix = self.vectorizer.fit_transform(self.document_texts)
    
    def search_documents(self, query, k=5):
        """Search documents using TF-IDF and cosine similarity"""
        if not self.document_texts or self.tfidf_matrix is None:
            return []
            
        # Transform query to TF-IDF
        query_vector = self.vectorizer.transform([query])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Get top k similar documents
        top_k_indices = similarities.argsort()[-k:][::-1]
        
        # Get the relevant documents
        relevant_docs = [self.document_texts[i] for i in top_k_indices]
        
        return relevant_docs 