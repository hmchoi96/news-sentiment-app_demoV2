import requests
from transformers import pipeline
from datetime import datetime, timedelta

# ✅ API Key
NEWS_API_KEY = '0e28b7f94fc04e6b9d130092886cabc6'

# ✅ Topic 설정
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

# ✅ 기본 날짜 범위 설정 (3일 전부터)
FROM_DATE = (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')

# ✅ 뉴스 수집
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
    return all_articles

# ✅ 키워드 포함 여부 확인
def contains_keywords(text, keywords):
    text = (text or "").lower()
    return sum(k in text for k in keywords) >= 1

# ✅ 기사 필터링 (중복 소스 제거, 키워드 매칭)
def filter_articles(articles, keywords, max_filtered=50):
    seen_sources = set()
    filtered = []
    for a in articles:
        source = a.get('source', {}).get('name', 'Unknown')
        title = a.get('title', '')
        desc = a.get('description', '')
        if not title or not desc:
            continue
        combined = f"{title} {desc}"
        if contains_keywords(combined, keywords) and source not in seen_sources:
            filtered.append({
                "title": title,
                "description": desc,
                "publishedAt": a.get('publishedAt', ''),
                "source": source,
                "url": a.get('url', '')
            })
            seen_sources.add(source)
        if len(filtered) >= max_filtered:
            break
    return filtered

# ✅ 감성 분석 실행
def run_sentiment_analysis(articles):
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", framework="pt")
    results = []
    for a in articles:
        text = f"{a['title']}. {a['description']}"
        try:
            sentiment = sentiment_pipeline(text[:512])[0]  # 너무 긴 경우 방지
        except Exception:
            sentiment = {"label": "NEUTRAL", "score": 0.5}

        results.append({
            "source": a.get('source', 'Unknown'),
            "title": a.get('title', ''),
            "description": a.get('description', ''),
            "sentiment": sentiment['label'],
            "score": round(sentiment['score'], 2)
        })
    return results

# ✅ 감성별 요약 생성
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
    except Exception:
        return "Summarization failed due to model input error."
