import requests
from transformers import pipeline
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)

# 전역 파이프라인 생성 (한 번만 로드)
_sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    framework="pt"
)
_summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "0e28b7f94fc04e6b9d130092886cabc6"

TOPIC_SETTINGS = {
    "tariff": {
        "search_term": "tariff",
        "keywords": [
            "tariff", "tariffs", "duties", "customs", "import", "export",
            "trade", "sanction", "levy", "protectionism", "trade war",
            "tariff hike", "border tax", "retaliatory", "quota"
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
            "inflation", "price index", "cpi", "ppi", "consume",
            "inflation rate", "cost of living"
        ]
    },
    "fed": {
        "search_term": "Federal Reserve",
        "keywords": [
            "fed", "federal reserve", "interest rate", "quantitative easing",
            "fomc", "chairman powell"
        ]
    },
    "unemployment": {
        "search_term": "unemployment",
        "keywords": [
            "unemployment", "jobless", "laid off", "nonfarm payroll",
            "job growth", "labor market", "hiring", "layoffs"
        ]
    }
}

def get_news(search_term, max_pages=4, page_size=100):
    """뉴스 API 호출 + URL 중복 제거"""
    all_articles = []
    seen = set()
    from_date = (datetime.today() - timedelta(days=3)).strftime("%Y-%m-%d")
    params = {
        "q": search_term,
        "from": from_date,
        "language": "en",
        "pageSize": page_size,
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY
    }
    for page in range(1, max_pages + 1):
        params["page"] = page
        try:
            resp = requests.get(NEWS_API_ENDPOINT, params=params)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logging.error(f"News API failed: {e}")
            break
        for a in data.get("articles", []):
            url = a.get("url")
            if url and url not in seen:
                seen.add(url)
                all_articles.append(a)
        if len(data.get("articles", [])) < page_size:
            break
    return all_articles

def contains_keywords(text, keywords):
    text = (text or "").lower()
    return any(k.lower() in text for k in keywords)

def filter_articles(articles, keywords, max_filtered=50):
    """키워드 필터링 후 상위 max_filtered개 반환"""
    filtered = []
    for a in articles:
        title = a.get("title")
        desc = a.get("description")
        if not title or not desc:
            continue
        if contains_keywords(f"{title} {desc}", keywords):
            filtered.append(a)
        if len(filtered) >= max_filtered:
            break
    return filtered

def run_sentiment_analysis(articles):
    """각 기사별 감정 분석"""
    results = []
    for a in articles:
        text = f"{a.get('title','')}. {a.get('description','')}"
        try:
            res = _sentiment_pipeline(text)[0]
        except Exception as e:
            logging.error(f"Sentiment pipeline error: {e}")
            continue
        results.append({
            "source": a.get("source", {}).get("name", "Unknown"),
            "url": a.get("url"),
            "title": a.get("title"),
            "description": a.get("description"),
            "sentiment": res["label"],
            "score": round(res["score"], 2)
        })
    return results

def summarize_by_sentiment(articles, sentiment_label, keywords):
    """긍정/부정 기사 묶음 요약"""
    texts = [
        f"{a['description']} (Title: {a['title']})"
        for a in articles
        if a.get("sentiment") == sentiment_label
        and contains_keywords(f"{a.get('description')} {a.get('title')}", keywords)
    ]
    if not texts:
        return "No matching articles found."
    word_limit = 300
    chunk, total = [], 0
    for t in texts:
        w = len(t.split())
        if total + w > word_limit:
            break
        chunk.append(t)
        total += w
    combined = " ".join(chunk)
    try:
        summary = _summarizer(combined, max_length=150, min_length=30, do_sample=False)[0]["summary_text"]
    except Exception as e:
        logging.error(f"Summarization error: {e}")
        return "Summarization failed."
    return summary
