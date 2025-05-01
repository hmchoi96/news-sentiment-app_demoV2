import requests
from transformers import pipeline
from datetime import datetime, timedelta
import plotly.express as px
import pandas as pd
import streamlit as st
from concurrent.futures import ThreadPoolExecutor

# ✅ API Key
NEWS_API_KEY = '0e28b7f94fc04e6b9d130092886cabc6'
NEWSDATA_API_KEY = 'pub_840368c52ddb1759503f2c24741bcaa218f23'

# ✅ Keyword Setting
TOPIC_SETTINGS = {
    "tariff": {
        "search_term": "tariff",
        "keywords": [
            "tariff", "tariffs", "duties", "customs", "import", "export", "trade",
            "sanction", "levy", "protectionism", "trade war", "tariff hike",
            "border tax", "retaliatory", "quota"
        ]
    },
    "trump": {
        "search_term": "Donald Trump",
        "keywords": [
            "trump", "donald", "republican", "president", "white house",
            "gop", "maga", "trump administration", "former president",
            "2024 election", "trump rally", "indictment", "mar-a-lago"
        ]
    },
    "inflation": {
        "search_term": "inflation",
        "keywords": [
            "inflation", "price index", "cpi", "ppi", "consumer price", "core inflation",
            "cost of living", "rising prices", "inflationary pressure",
            "interest rates", "wage growth", "monetary tightening", "headline inflation",
            "economic overheating", "sticky inflation", "disinflation"
        ]
    },
    "fed": {
        "search_term": "fed",
        "keywords": [
            "federal reserve", "interest rate", "rate hike", "rate cut", "jerome powell",
            "fed", "fomc", "central bank", "tightening", "pause", "pivot", "monetary policy"
        ]
    },
    "unemployment": {
        "search_term": "employment",
        "keywords": [
            "unemployment", "employment", "jobless", "nonfarm payroll", "labor market", "jobs report",
            "layoffs", "job cuts", "hiring freeze", "job growth", "employment rate"
        ]
    }
}

FROM_DATE = (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')

@st.cache_resource
def get_sentiment_pipeline():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", framework="pt")

@st.cache_resource
def get_summary_pipeline():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def get_news_newsdata(query, language="en", country="ca", max_results=30):
    url = "https://newsdata.io/api/1/news"
    params = {
        "apikey": NEWSDATA_API_KEY,
        "q": query,
        "language": language,
        "country": country,
        "category": "business",
        "page": 1
    }
    articles = []
    try:
        response = requests.get(url, params=params)
        data = response.json()
        for item in data.get("results", []):
            articles.append({
                "title": item.get("title", ""),
                "description": item.get("description", ""),
                "content": item.get("content", item.get("description", "")),
                "source": item.get("source_id", "NewsData"),
                "url": item.get("link", "")
            })
    except Exception as e:
        print(f"NewsData API error: {e}")
    return articles

def deduplicate_articles(articles):
    seen = set()
    unique = []
    for a in articles:
        source = a["source"]
        if isinstance(source, dict):
            source = source.get("name", "Unknown")
        key = (a["title"], source)
        if key not in seen:
            unique.append(a)
            seen.add(key)
    return unique

def get_news(search_term, max_pages=4, page_size=100):
    all_articles = []
    for page in range(1, max_pages + 1):
        url = (
            f'https://newsapi.org/v2/everything?q={search_term}'
            f'&from={FROM_DATE}&language=en&pageSize={page_size}&page={page}&sortBy=publishedAt'
            f'&apiKey={NEWS_API_KEY}'
        )
        response = requests.get(url)
        data = response.json()
        if 'articles' in data:
            all_articles.extend(data['articles'])
        if len(data.get("articles", [])) < page_size:
            break
    backup_articles = get_news_newsdata(search_term)[:5]
    all_articles = deduplicate_articles(all_articles + backup_articles)
    return all_articles

def contains_keywords(text, keywords):
    text = (text or "").lower()
    return sum(k in text for k in keywords) >= 1

def filter_articles(articles, keywords, max_filtered=50):
    filtered = []
    for a in articles:
        title = a['title']
        desc = a['description']
        if not title or not desc:
            continue
        combined = f"{title} {desc}"
        if contains_keywords(combined, keywords):
            filtered.append(a)
        if len(filtered) >= max_filtered:
            break
    return filtered

def run_sentiment_and_summary(article):
    sentiment_pipeline = get_sentiment_pipeline()
    summary_pipeline = get_summary_pipeline()
    sentiment = sentiment_pipeline(f"{article['title']}. {article['description'] or ''}")[0]
    summary = summary_pipeline(article['description'] or article['title'])[0]['summary_text']
    return {
        "source": article['source']['name'] if isinstance(article['source'], dict) else article['source'],
        "title": article['title'],
        "description": article['description'],
        "sentiment": sentiment['label'],
        "score": round(sentiment['score'], 2),
        "summary": summary
    }

def analyze_articles_parallel(articles):
    with ThreadPoolExecutor() as executor:
        return list(executor.map(run_sentiment_and_summary, articles))

def draw_sentiment_chart(data):
    df = pd.DataFrame(data)
    counts = df['sentiment'].value_counts().reset_index()
    counts.columns = ['Sentiment', 'Count']
    fig = px.bar(counts, x='Sentiment', y='Count', title='Sentiment Distribution')
    st.plotly_chart(fig, use_container_width=True)

def summarize_by_sentiment(articles, sentiment_label, keywords):
    texts = [
        f"{a['description']} (Title: {a['title']})"
        for a in articles
        if a['sentiment'] == sentiment_label and a['description'] and contains_keywords(f"{a['description']} {a['title']}", keywords)
    ]
    if len(texts) < 1:
        return "No matching articles found for summarization."
    chunks = []
    word_limit = 500
    current_chunk = []
    total_words = 0
    for t in texts:
        w_count = len(t.split())
        if total_words + w_count > word_limit:
            break
        current_chunk.append(t)
        total_words += w_count
    truncated = " ".join(current_chunk)
    try:
        summary = get_summary_pipeline()(truncated, max_length=200, min_length=60, do_sample=False)[0]['summary_text']
        return summary
    except Exception:
        return "Summarization failed due to model input error."
