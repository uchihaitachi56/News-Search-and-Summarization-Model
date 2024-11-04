# News-Search-and-Summarization-Model
A command-line tool that searches for recent news on a user-defined topic, saves articles in a CSV file, provides summaries, and extracts named entities from titles. It supports English and German, with auto-translation to German if German articles are unavailable. The tool uses APIs to retrieve, summarize, translate, and analyze news content.

## Features

- 🔍 **Search for News:** Search for recent news articles by topic
- 💾 **Save Results to CSV:** Save articles with titles, URLs, and publication dates
- 📝 **Article Summarization:** Get summaries of top-15 article headlines using Pegasus model
- 🔤 **Named Entity Extraction:** Extract and analyze entities from headlines
- 🌐 **Language Support:** English and German support with automatic T5-based translation
- 🔄 **Automatic Translation:** If German articles aren't available, automatically fetches English articles and translates summaries to German


## AI Models Used

- **Pegasus (google/pegasus-xsum)**: State-of-the-art model for text summarization
- **T5 (t5-base)**: Advanced transformer model for English to German translation
- **SpaCy**: For named entity recognition and natural language processing


## Project Structure
```
news_search_engine/
├── news_search_engine.py          # Main application code
├── unit_tests.py                  # Unit tests
├── README.md                      # README file with instructions
├── requirements.txt               # Dependencies
└── .env                           # Environment file (to store API key)
```


## Prerequisites

- Python 3.8 or higher
- GNews API Key ([Get it here](https://gnews.io/))


## Setup Instructions

1. **Set up Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key**
   - Create a `.env` file in the project root
   - Add your GNews API key:
     ```
     API_KEY=your_gnews_api_key_here
     ```

4. **Run the Application**
   ```bash
   python news_search_engine.py
   ```

5. **Run Tests**
   ```bash
   python -m unittest unit_tests.py
   ```


## Usage Guide

1. Start the application
2. Enter your search topic when prompted
3. Choose language:
   - `en` for English
   - `de` for German
4. The application will:
   - Search for articles in the selected language
   - If German is selected but no articles are found:
     - Automatically fetch English articles
     - Generate summaries using Pegasus model
     - Translate summaries to German using T5 model
5. View results:
   - Top articles list
   - Article summaries (translated if necessary)
   - Named entities from headlines
6. Check `articles.csv` for saved results
7. Choose to search again or exit


## Dependencies

- `requests`: HTTP requests to GNews API
- `spacy`: Named entity recognition
- `python-dotenv`: Environment variable management
- `torch`: Machine learning model operations
- `transformers`: For Pegasus (summarization) and T5 (translation) models


## Model Workflow

1. **Article Summarization**
   - Uses Pegasus model (google/pegasus-xsum)
   - Optimized for concise, informative summaries
   - Handles long articles efficiently

2. **Language Translation**
   - Uses T5-base model
   - Automatic translation when German articles unavailable
   - High-quality English to German translation

3. **Named Entity Recognition**
   - Uses SpaCy's English model
   - Extracts and categorizes entities from headlines
   - Provides frequency analysis of mentioned entities


## Error Handling

- Graceful handling of API errors
- Automatic fallback to English with translation for German searches
- Input validation for language selection
- Network error handling
- Model loading and inference error management


## Acknowledgments

- [GNews API](https://gnews.io/) for news data
- [Hugging Face](https://huggingface.co/) for Pegasus and T5 models
- [SpaCy](https://spacy.io/) for NLP capabilities
- Google's Pegasus team for the summarization model
- T5 team for the translation model



**Note:** Remember to replace `your_gnews_api_key_here` with your actual GNews API key in the `.env` file.




## Unit Tests

The application includes comprehensive unit tests to ensure functionality and reliability. Tests are located in `unit_tests.py`.

### Running Tests

1. **Run All Tests**
   ```bash
   python -m unittest unit_tests.py
   ```

2. **Run Specific Test**
   ```bash
   python -m unittest unit_tests.TestNewsFunctions.test_fetch_news
   ```

3. **Run with Verbose Output**
   ```bash
   python -m unittest -v unit_tests.py
   ```

### Test Structure

```
unit_tests.py
└── TestNewsFunctions
    ├── test_fetch_news()
    ├── test_save_to_csv()
    ├── test_summarize_articles()
    └── test_extract_named_entities()
```

### Testing Notes

- Tests require an active internet connection for API calls
- GNews API key must be properly configured in `.env`
- Some tests may take longer due to model loading
- Ensure all dependencies are installed before running tests
- Tests use sample data to validate functionality
- Failed tests provide detailed error messages

### Adding New Tests

To add new tests:
1. Create a new test method in `TestNewsFunctions` class
2. Follow the naming convention: `test_*`
3. Include appropriate assertions
4. Update test documentation

Example:
```python
def test_new_feature(self):
    # Setup
    test_data = {"test": "data"}
    
    # Execute
    result = new_feature(test_data)
    
    # Assert
    self.assertTrue(result)
```
