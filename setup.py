from setuptools import setup, find_packages

setup(
    name="data-analysis-dashboard",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.31.0",
        "pandas>=2.1.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "google-generativeai>=0.3.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "PyPDF2>=3.0.0",
        "python-docx>=0.8.11",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "newspaper3k>=0.2.8",
        "nltk>=3.8.1",
        "googlesearch-python>=1.2.3"
    ],
    author="Amit Khopade",
    author_email="your.email@example.com",
    description="A data analysis dashboard with news integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Amitkhopade/agnetic_Ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 