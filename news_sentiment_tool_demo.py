import requests
from transformers import pipeline
from datetime import datetime, timedelta

# ✅ API Key
NEWS_API_KEY = '0e28b7f94fc04e6b9d130092886cabc6'
NEWSDATA_API_KEY = 'pub_840368c52ddb1759503f2c24741bcaa218f23'

# ✅ Keyword Setting


FROM_DATE = (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')

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

    # ✅ 항상 NewsData에서 5개만 보조로 가져옴
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

def run_sentiment_analysis(articles):
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", framework="pt")
    results = []
    for a in articles:
        text = f"{a['title']}. {a['description'] or ''}"
        sentiment = sentiment_pipeline(text)[0]
        results.append({
            "source": a['source']['name'] if isinstance(a['source'], dict) else a['source'],
            "title": a['title'],
            "description": a['description'],
            "sentiment": sentiment['label'],
            "score": round(sentiment['score'], 2)
        })
    return results

def summarize_by_sentiment(articles, sentiment_label, keywords):
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
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
        summary = summarizer(truncated, max_length=200, min_length=60, do_sample=False)[0]['summary_text']
        return summary
    except Exception as e:
        return "Summarization failed due to model input error."
