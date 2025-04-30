# news_sentiment_tool_demo.py

import requests
from transformers import pipeline
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)

# 뉴스 API 설정
NEWS_API_ENDPOINT = 'https://newsapi.org/v2/everything'
NEWS_API_KEY = '0e28b7f94fc04e6b9d130092886cabc6'

# 토픽별 검색어 및 키워드 (V2)
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
# :contentReference[oaicite:2]{index=2}&#8203;:contentReference[oaicite:3]{index=3}

# 3일 전 날짜
FROM_DATE = (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')

# 전역 파이프라인 (한 번만 로드)
_sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)
_summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

def get_news(search_term, max_pages=4, page_size=100):
    """NewsAPI에서 기사 수집, 중복 URL 제거."""
    all_articles = []
    seen_urls = set()
    params = {
        "q": search_term,
        "from": FROM_DATE,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": NEWS_API_KEY
    }
    for page in range(1, max_pages + 1):
        params["page"] = page
        try:
            resp = requests.get(NEWS_API_ENDPOINT, params=params)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            logging.error(f"News API error: {e}")
            break

        for art in data.get("articles", []):
            url = art.get("url")
            if url and url not in seen_urls:
                seen_urls.add(url)
                all_articles.append({
                    "source": art.get("source", {}).get("name", "Unknown"),
                    "title": art.get("title", "") or "",
                    "description": art.get("description", "") or "",
                    "url": url
                })

        if len(data.get("articles", [])) < page_size:
            break

    return all_articles

def contains_keywords(text, keywords):
    """문자열 키워드만 필터링하고, 최소 2개 이상 매칭 여부."""
    text = (text or "").lower()
    valid = [k.lower() for k in keywords if isinstance(k, str)]
    return sum(1 for k in valid if k in text) >= 2

def filter_articles(articles, keywords, max_filtered=50):
    """키워드 기반 필터링 후 상위 max_filtered개 반환."""
    filtered = []
    for art in articles:
        combined = f"{art['title']} {art['description']}"
        if contains_keywords(combined, keywords):
            filtered.append(art)
        if len(filtered) >= max_filtered:
            break
    return filtered  # :contentReference[oaicite:4]{index=4}&#8203;:contentReference[oaicite:5]{index=5}

def run_sentiment_analysis(articles):
    """각 기사에 대해 감정 분석 수행."""
    results = []
    for art in articles:
        text = f"{art['title']}. {art['description']}"
        try:
            res = _sentiment_pipeline(text)[0]
        except Exception as e:
            logging.error(f"Sentiment error: {e}")
            continue
        results.append({
            "source": art["source"],
            "title": art["title"],
            "description": art["description"],
            "sentiment": res["label"],
            "score": round(res["score"], 2),
            "url": art.get("url")
        })
    return results

def summarize_by_sentiment(articles, label, keywords, max_articles=5):
    """
    지정된 감정(label)의 기사 상위 max_articles개를
    500단어 이하로 묶어서 요약.
    """
    texts = []
    for art in articles:
        if art["sentiment"] == label and contains_keywords(
            f"{art['title']} {art['description']}", keywords
        ):
            texts.append(f"{art['title']}. {art['description']}")
        if len(texts) >= max_articles:
            break

    if not texts:
        return ""

    # 단일 묶음이 너무 길어지지 않도록 제한
    combined = []
    total_words = 0
    for t in texts:
        wc = len(t.split())
        if total_words + wc > 500:
            break
        combined.append(t)
        total_words += wc

    chunk = " ".join(combined)
    try:
        summary = _summarizer(chunk, max_length=200, min_length=60, do_sample=False)[0]["summary_text"]
        return summary
    except Exception as e:
        logging.error(f"Summarization error: {e}")
        return "Summarization failed."

