# Data Analysis Dashboard with News Integration

A powerful data analysis dashboard that combines data visualization, analysis, and real-time news integration. The dashboard allows users to upload data, analyze it, and get relevant news articles with sentiment analysis.

## Features

- 📊 Data Analysis and Visualization
- 📰 Real-time News Integration
- 💬 Interactive Chat with Data
- 🎯 Sentiment Analysis
- 📈 Multiple Chart Types
- 🔍 Keyword Extraction
- 📱 Responsive UI

## Project Structure

```
dashboard/
│
├── src/
│   ├── __init__.py
│   ├── data_analyzer.py      # Data analysis and processing
│   ├── news_analyzer.py      # News fetching and sentiment analysis
│   └── visualization.py      # Data visualization utilities
│
├── static/
│   └── styles/              # CSS and styling files
│
├── tests/                   # Unit tests
│   └── __init__.py
│
├── app.py                   # Main Streamlit application
├── requirements.txt         # Project dependencies
├── setup.py                # Package setup file
└── README.md               # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd dashboard
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download required NLTK data:
```bash
python download_nltk_data.py
```

## Usage

1. Start the dashboard:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Upload your data file (supported formats: CSV, Excel, JSON, TXT, PDF, DOCX)

4. Use the different tabs to:
   - Analyze your data
   - Create visualizations
   - Chat with your data
   - Get relevant news articles

## Features in Detail

### Data Analysis
- Basic statistics
- Data type information
- Missing value analysis
- Correlation analysis

### Visualization
- Bar charts
- Line charts
- Scatter plots
- Histograms
- Box plots
- Violin plots

### News Analysis
- Industry-specific news
- Sentiment analysis
- Impact assessment
- Confidence scoring

### Chat Interface
- Natural language queries
- Context-aware responses
- Data-driven insights

## Dependencies

- streamlit>=1.31.0
- pandas>=2.1.0
- numpy>=1.24.0
- scikit-learn>=1.3.0
- google-generativeai>=0.3.0
- matplotlib>=3.7.0
- seaborn>=0.12.0
- PyPDF2>=3.0.0
- python-docx>=0.8.11
- requests>=2.31.0
- beautifulsoup4>=4.12.0
- newspaper3k>=0.2.8
- nltk>=3.8.1
- googlesearch-python>=1.2.3

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Streamlit for the web framework
- NLTK for natural language processing
- Newspaper3k for news article extraction
- Google News for news data

## Author

- **Amit Khopade**
  - GitHub: [@Amitkhopade](https://github.com/Amitkhopade)
