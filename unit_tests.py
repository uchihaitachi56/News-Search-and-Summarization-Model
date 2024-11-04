import unittest
from news_search_engine import fetch_news, save_to_csv, summarize_articles, extract_named_entities

class TestNewsFunctions(unittest.TestCase):

    def test_fetch_news(self):
        topic = "technology"
        language = "en"
        articles, all_articles = fetch_news(topic, language)
        self.assertGreater(len(articles), 0, "Should return some articles")
        self.assertIn("title", articles[0], "Articles should contain titles")

    def test_save_to_csv(self):
        articles = [
            {"title": "Test Article 1", "url": "http://example.com/1", "publishedAt": "2024-01-01"},
            {"title": "Test Article 2", "url": "http://example.com/2", "publishedAt": "2024-01-02"}
        ]
        filename = "test_articles.csv"
        save_to_csv(articles, filename)

        # Verify CSV file was created and contents are correct
        with open(filename, mode='r', encoding="utf-8") as file:
            content = file.readlines()
            self.assertEqual(len(content), 3)  # Check header + 2 articles
            self.assertIn("Test Article 1", content[1])
            self.assertIn("Test Article 2", content[2])

    def test_summarize_articles(self):
        articles = [{"content": "The quick brown fox jumps over the lazy dog."}]
        summaries = summarize_articles(articles)
        self.assertIsInstance(summaries[0], str, "Summary should be a string")
        self.assertGreater(len(summaries[0]), 0, "Summary should not be empty")

    def test_extract_named_entities(self):
        articles = [{"title": "Apple Inc. is launching the iPhone 15."}]
        entities = extract_named_entities(articles)
        self.assertGreater(len(entities), 0, "Should return some entities")
        self.assertIn("Apple Inc.", dict(entities), "Entity 'Apple Inc.' should be present")

if __name__ == "__main__":
    unittest.main()
