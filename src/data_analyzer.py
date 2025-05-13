import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DataAnalyzer:
    def __init__(self):
        # Set style for better visualizations
        plt.style.use('default')  # Using default style instead of seaborn
        sns.set_theme(style="whitegrid")  # Using seaborn's set_theme instead
        
    def load_data(self, uploaded_file):
        """Load data from Streamlit uploaded file"""
        try:
            # Get the file name to determine the file type
            file_name = uploaded_file.name.lower()
            
            if file_name.endswith('.csv'):
                return pd.read_csv(uploaded_file)
            elif file_name.endswith(('.xlsx', '.xls')):
                return pd.read_excel(uploaded_file)
            else:
                print("Error: Unsupported file format. Please use .csv, .xlsx, or .xls files.")
                return None
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return None

    def clean_data(self, df):
        """Perform comprehensive data cleaning"""
        if df is None:
            return None
            
        # Create a copy to avoid modifying original data
        df_clean = df.copy()
        
        # 1. Handle missing values
        missing_values = df_clean.isnull().sum()
        missing_percentage = (missing_values / len(df_clean)) * 100
        
        print("\n=== Missing Value Analysis ===")
        missing_stats = pd.DataFrame({
            'Missing Values': missing_values,
            'Percentage': missing_percentage
        })
        print(missing_stats[missing_stats['Missing Values'] > 0])
        
        # 2. Handle duplicates
        duplicates = df_clean.duplicated().sum()
        print(f"\nNumber of duplicate rows: {duplicates}")
        
        # 3. Remove duplicates
        df_clean = df_clean.drop_duplicates()
        
        # 4. Handle outliers using IQR method for numeric columns
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = ((df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)).sum()
            print(f"\nOutliers in {col}: {outliers}")
        
        return df_clean

    def analyze_data(self, df):
        """Perform comprehensive data analysis"""
        if df is None:
            return
            
        print("\n=== Basic Data Information ===")
        print(f"Number of rows: {len(df)}")
        print(f"Number of columns: {len(df.columns)}")
        
        print("\n=== Data Types ===")
        print(df.dtypes)
        
        print("\n=== Basic Statistics ===")
        print(df.describe())
        
        # Correlation analysis for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            print("\n=== Correlation Analysis ===")
            correlation = df[numeric_cols].corr()
            plt.figure(figsize=(10, 8))
            sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
            plt.title('Correlation Heatmap')
            plt.tight_layout()
            plt.show()

    def visualize_data(self, df):
        """Create various visualizations for data insights"""
        if df is None:
            return
            
        # 1. Distribution of numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols[:4]:  # Limit to first 4 numeric columns
            plt.figure(figsize=(10, 6))
            sns.histplot(data=df, x=col, kde=True)
            plt.title(f'Distribution of {col}')
            plt.show()
        
        # 2. Box plots for numeric columns
        if len(numeric_cols) > 0:
            plt.figure(figsize=(12, 6))
            df[numeric_cols[:4]].boxplot()  # Limit to first 4 numeric columns
            plt.title('Box Plot of Numeric Columns')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        
        # 3. Categorical columns analysis
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols[:4]:  # Limit to first 4 categorical columns
            plt.figure(figsize=(10, 6))
            value_counts = df[col].value_counts()
            sns.barplot(x=value_counts.index, y=value_counts.values)
            plt.title(f'Distribution of {col}')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show() 