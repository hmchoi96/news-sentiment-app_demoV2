# news_sentiment_tool_demo.py
import requests
from transformers import pipeline
from datetime import datetime, timedelta

# ✅ API Key 및 엔드포인트
NEWS_API_KEY = '0e28b7f94fc04e6b9d130092886cabc6'
NEWS_ENDPOINT = 'https://newsapi.org/v2/everything'

# ✅ Topic 설정 (생략)
TOPIC_SETTINGS = {
    "tariff": { "search_term":"tariff", "keywords":[ ... ] },
    # ... 나머지 topic ...
}

# 날짜 기준 (3일 전)
FROM_DATE = (datetime.utcnow() - timedelta(days=3)).strftime('%Y-%m-%d')

# 캐시된 파이프라인
_summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
_sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def get_news(search_term, max_pages=4, page_size=100):
    all_articles = []
    seen = set()
    for page in range(1, max_pages+1):
        params = {
            "q": search_term,
            "from": FROM_DATE,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": page_size,
            "page": page,
            "apiKey": NEWS_API_KEY
        }
        res = requests.get(NEWS_ENDPOINT, params=params)
        data = res.json()
        arts = data.get("articles", [])
        if not arts:
            break
        for art in arts:
            url = art.get("url")
            if url and url not in seen:
                seen.add(url)
                all_articles.append({
                    "source": art.get("source",{}).get("name","Unknown"),
                    "title": art.get("title",""),
                    "description": art.get("description","")
                })
        if len(arts) < page_size:
            break
    return all_articles

def contains_keywords(text, keywords):
    text = (text or "").lower()
    return sum(1 for k in keywords if k in text) >= 2  # 최소 2개 이상 매칭

def filter_articles(articles, keywords, max_filtered=50):
    filtered = []
    for a in articles:
        combined = f"{a['title']} {a['description']}"
        if contains_keywords(combined, keywords):
            filtered.append(a)
        if len(filtered) >= max_filtered:
            break
    return filtered

def run_sentiment_analysis(articles):
    results = []
    for a in articles:
        txt = f"{a['title']}. {a['description'] or ''}"
        r = _sentiment_pipeline(txt)[0]
        results.append({
            "source": a["source"],
            "title": a["title"],
            "description": a["description"],
            "sentiment": r["label"],
            "score": round(r["score"],2)
        })
    return results

def summarize_by_sentiment(articles, sentiment_label, keywords, max_articles=5):
    texts = [
        f"{a['title']}. {a['description']}"
        for a in articles
        if a["sentiment"] == sentiment_label and contains_keywords(f"{a['title']} {a['description']}", keywords)
    ][:max_articles]
    if not texts:
        return ""
    summaries = []
    for t in texts:
        try:
            s = _summarizer(t, max_length=100, min_length=40, do_sample=False)[0]["summary_text"]
            summaries.append(s)
        except:
            continue
    return " ".join(summaries)
