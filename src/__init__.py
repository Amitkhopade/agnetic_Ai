"""
Data Analysis Dashboard with News Integration
===========================================

A powerful data analysis dashboard that combines data visualization,
analysis, and real-time news integration.
"""

__version__ = "1.0.0"
__author__ = "Amit Khopade"

from .data_analyzer import DataAnalyzer
from .news_analyzer import NewsAnalyzer
from .visualization import create_visualization

__all__ = ['DataAnalyzer', 'NewsAnalyzer', 'create_visualization'] 