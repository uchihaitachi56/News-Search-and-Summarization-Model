import os
import requests
import csv
import spacy
from collections import Counter
from dotenv import load_dotenv
import torch
import warnings
from transformers import PegasusForConditionalGeneration, PegasusTokenizer, T5ForConditionalGeneration, T5Tokenizer

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")  # Load API key from environment variables

# Load Spacy model and summarizer
nlp = spacy.load("en_core_web_sm")

# Check if GPU is available and set device accordingly
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Suppress specific warnings related to model weights and tokenizer
warnings.filterwarnings("ignore", category=UserWarning)

# Load Pegasus model and tokenizer for summarization
model_name = "google/pegasus-xsum"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)

# Load T5 model and tokenizer for translation (set legacy=False to use the new behavior)
translation_model_name = "t5-base"  # or "t5-small", "t5-large", etc.
translation_tokenizer = T5Tokenizer.from_pretrained(translation_model_name, legacy=False)
translation_model = T5ForConditionalGeneration.from_pretrained(translation_model_name).to(device)

# Function to fetch the top 15 articles
def fetch_news(topic, language="en"):
    url = f"https://gnews.io/api/v4/search?q={topic}&lang={language}&token={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or 'articles' not in data:
        print("Error fetching news:", response.status_code, data.get("message"))
        return [], []  # Return empty lists on error

    articles = data.get("articles", [])
    return articles[:15], articles  # Return top-15 and full list

# Function to save articles to a CSV file
def save_to_csv(articles, filename="articles.csv"):
    with open(filename, mode='w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "URL", "Published Date"])
        for article in articles:
            writer.writerow([article["title"], article["url"], article["publishedAt"]])

# Function to summarize article titles
def summarize_articles(articles):
    summaries = []
    for article in articles:
        if 'content' in article:  # Ensure 'content' is available
            input_text = "summarize: " + article['content']
            input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=1024, truncation=True).to(device)
            outputs = model.generate(input_ids, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
            summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
            summaries.append(summary)
        else:
            summaries.append("No content available for summarization.")
    return summaries

# Function to extract entities
def extract_named_entities(articles):
    titles = [article["title"] for article in articles]
    entity_counter = Counter()
    for title in titles:
        doc = nlp(title)
        for ent in doc.ents:
            entity_counter[ent.text] += 1
    return entity_counter.most_common()

# Function to translate text into German using T5
def t5_translate(text, target_lang="de"):
    input_text = f"translate English to {target_lang}: {text}"
    input_ids = translation_tokenizer.encode(input_text, return_tensors="pt").to(device)
    output_ids = translation_model.generate(input_ids, max_length=512)
    return translation_tokenizer.decode(output_ids[0], skip_special_tokens=True)


# MAIN FUNCTION
def main():
    while True:
        topic = input("Enter the topic you want to Search: ")
        language = input("Choose language:\nType 'en' for English and 'de' for German: ")
        top_articles, all_articles = fetch_news(topic, language)

        # If no German articles are found, fetch English articles and translate
        if language == 'de' and not top_articles:
            print("No German articles found. Fetching English articles...")
            top_articles, all_articles = fetch_news(topic, 'en')
            if top_articles:
                print("Generating summaries in English...")
                summaries = summarize_articles(top_articles)

                print("Translating summaries to German...")
                summaries = [t5_translate(summary) for summary in summaries]
            else:
                print("No articles found in English either.")
                summaries = []
        else:
            # Generate summaries in the chosen language
            summaries = summarize_articles(top_articles)

        save_to_csv(all_articles)

        entities = extract_named_entities(top_articles)

        print("\nTop Articles:")
        for i, article in enumerate(top_articles, start=1):  # Numbering starts from 1
            print(f"{i}. {article['title']} ({article['publishedAt']}) - {article['url']}")

        print("\nSummary of Top Articles:")
        for i, summary in enumerate(summaries):
            print(f"Article {i + 1}: {summary}")

        print("\nNamed Entities in Headlines:")
        for entity, count in entities:
            print(f"{entity}: {count}")

        if input("\nSearch another topic? (y/n): ").lower() != "y":
            break

if __name__ == "__main__":
    main()
