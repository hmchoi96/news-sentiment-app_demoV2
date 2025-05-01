import requests
from config import TOPIC_SETTINGS, SECTOR_KEYWORDS, FROM_DATE
from transformers import pipeline
import streamlit as st

NEWS_API_KEY = '0e28b7f94fc04e6b9d130092886cabc6'
NEWSDATA_API_KEY = 'pub_840368c52ddb1759503f2c24741bcaa218f23'


def fetch_news_articles(topic, country, industry, max_pages=4, page_size=100):
    search_term = TOPIC_SETTINGS[topic]["search_term"]
    all_articles = []

    for page in range(1, max_pages + 1):
        url = (
            f'https://newsapi.org/v2/everything?q="{search_term}"'
            f'&from={FROM_DATE}&language=en&pageSize={page_size}&page={page}&sortBy=publishedAt'
            f'&apiKey={NEWS_API_KEY}'
        )
        response = requests.get(url)
        data = response.json()
        if 'articles' in data:
            all_articles.extend(data['articles'])
        if len(data.get("articles", [])) < page_size:
            break

    # NewsData 보조로 사용
    backup_articles = get_news_newsdata(search_term, country_code_map(country))[:5]
    all_articles = deduplicate_articles(all_articles + backup_articles)
    return all_articles


def get_news_newsdata(query, country_code="ca", language="en"):
    url = "https://newsdata.io/api/1/news"
    params = {
        "apikey": NEWSDATA_API_KEY,
        "q": query,
        "language": language,
        "country": country_code,
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


def country_code_map(country_name):
    code_map = {
        "United States": "us",
        "Canada": "ca",
        "Japan": "jp",
        "China": "cn",
        "Germany": "de",
        "India": "in",
        "South Korea": "kr",
    }
    return code_map.get(country_name, "us")


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


def filter_articles_by_keywords(articles, topic, industry):
    topic_keywords = TOPIC_SETTINGS[topic]["keywords"]
    industry_keywords = SECTOR_KEYWORDS.get(industry, [])
    all_keywords = topic_keywords + industry_keywords

    filtered = []
    for a in articles:
        text = " ".join([
            a.get("title", ""),
            a.get("description", ""),
            a.get("content", "")
        ])
        if any(kw.lower() in text.lower() for kw in all_keywords):
            filtered.append(a)
        if len(filtered) >= 50:
            break
    return filtered


@st.cache_resource
def load_sentiment_pipeline():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")


@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


def run_sentiment_analysis(articles):
    sentiment_pipeline = load_sentiment_pipeline()
    results = []
    for a in articles:
        text = f"{a['title']}. {a.get('description', '')}"
        try:
            sentiment = sentiment_pipeline(text[:512])[0]
            results.append({
                "source": a['source']['name'] if isinstance(a['source'], dict) else a['source'],
                "title": a['title'],
                "description": a['description'],
                "sentiment": sentiment['label'].lower(),
                "score": round(sentiment['score'], 2)
            })
        except Exception:
            continue
    return results


def summarize_by_sentiment(articles, sentiment_label, topic, industry):
    summarizer = load_summarizer()
    topic_keywords = TOPIC_SETTINGS[topic]["keywords"]
    industry_keywords = SECTOR_KEYWORDS.get(industry, [])
    keywords = topic_keywords + industry_keywords

    texts = [
        f"{a['description']} (Title: {a['title']})"
        for a in articles
        if a['sentiment'] == sentiment_label and contains_keywords(f"{a['description']} {a['title']}", keywords)
    ]

    if len(texts) < 1:
        return "No matching articles found for summarization."

    # 글자 수 제한된 요약 입력 구성
    truncated = " ".join(texts)[:1000]
    try:
        summary = summarizer(truncated, max_length=200, min_length=60, do_sample=False)[0]['summary_text']
        return summary
    except Exception:
        return "Summarization failed due to model error."


def contains_keywords(text, keywords):
    text = (text or "").lower()
    return any(k.lower() in text for k in keywords)
