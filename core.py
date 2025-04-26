from news_sentiment_tool_demo import (
    run_sentiment_analysis,
    summarize_by_sentiment,
    TOPIC_SETTINGS
)
from config import INDUSTRY_KEYWORDS, SECTOR_KEYWORDS
from newsapi import NewsApiClient
from datetime import datetime, timedelta

# 1. 산업 키워드 기반 뉴스 가져오기
def get_news(industry_keywords, from_days=1):
    newsapi = NewsApiClient(api_key="0e28b7f94fc04e6b9d130092886cabc6")  # 실제 API 키로 교체할 것

    query = " OR ".join(industry_keywords)  # ex: "manufacturing OR semiconductor OR supply chain"

    today = datetime.today()
    from_date = (today - timedelta(days=from_days)).strftime("%Y-%m-%d")
    to_date = today.strftime("%Y-%m-%d")

    all_articles = newsapi.get_everything(
        q=query,
        from_param=from_date,
        to=to_date,
        language="en",
        sort_by="relevancy",
        page_size=50
    )

    return all_articles["articles"]

# 2. 키워드 매칭 여부만 체크 (필터링 아님)
def filter_articles(articles, topic_keywords):
    filtered = []
    for a in articles:
        combined_text = f"{a.get('title', '')} {a.get('description', '')}".lower()
        is_relevant = any(kw.lower() in combined_text for kw in topic_keywords)

        article = {
            "title": a.get("title", ""),
            "description": a.get("description", ""),
            "url": a.get("url", ""),
            "publishedAt": a.get("publishedAt", ""),
            "source": a.get("source", {}).get("name", ""),
            "is_relevant": is_relevant
        }
        filtered.append(article)
    return filtered

# 3. 산업 섹터 임팩트 탐지
def detect_impacted_sectors(articles):
    impact_map = {}
    for a in articles:
        text = f"{a['title']} {a['description'] or ''}".lower()
        for sector, keywords in SECTOR_KEYWORDS.items():
            if any(k in text for k in keywords):
                impact_map.setdefault(sector, []).append(text)
    return impact_map

# 4. 섹터별 간단 요약
def summarize_sector_impact(sector_texts):
    if not sector_texts:
        return "No clear impact found."

    from transformers import pipeline
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    text_block = " ".join(sector_texts)[:512]
    try:
        summary = summarizer(text_block, max_length=40, min_length=10, do_sample=False)[0]["summary_text"]
        return summary
    except Exception:
        return "Summary model failed."

# 5. 최종 분석 실행
def analyze_topic(topic, industry, country, from_days=1):
    setting = TOPIC_SETTINGS[topic]
    topic_keywords = setting["keywords"]

    # 산업 키워드 준비
    if industry != "All":
        industry_keywords = INDUSTRY_KEYWORDS.get(industry, [])
    else:
        industry_keywords = []

    if not industry_keywords:
        industry_keywords = ["economy", "business", "industry"]

    raw = get_news(industry_keywords, from_days=from_days)
    filtered = filter_articles(raw, topic_keywords)
    analyzed = run_sentiment_analysis(filtered)

    sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for a in analyzed:
        label = a["sentiment"].capitalize()
        if label in sentiment_counts:
            sentiment_counts[label] += 1

    pos_news = [a for a in analyzed if a["sentiment"] == "POSITIVE"]
    neg_news = [a for a in analyzed if a["sentiment"] == "NEGATIVE"]

    pos_sources = sorted(set(a["source"] for a in pos_news))
    neg_sources = sorted(set(a["source"] for a in neg_news))

    expert_summary = (
        "✅ **Positive Insight**\n\n"
        + summarize_by_sentiment(analyzed, "POSITIVE", topic_keywords)
        + "\n\n❗ **Negative Insight**\n\n"
        + summarize_by_sentiment(analyzed, "NEGATIVE", topic_keywords)
    )

    dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get)
    top_issue_summary = "renewed US tariff threats and China's retaliatory stance"

    executive_summary = (
        f"Over the past {from_days} day(s), news coverage on **{topic}** has been predominantly "
        f"**{dominant_sentiment.lower()}**, with a focus on {top_issue_summary}."
    )

    impact_summary = []
    detected = detect_impacted_sectors(filtered)
    for sector, texts in detected.items():
        impact_summary.append({
            "sector": sector,
            "impact": summarize_sector_impact(texts)
        })

    return {
        "sentiment_counts": sentiment_counts,
        "positive_news": pos_news,
        "negative_news": neg_news,
        "positive_sources": pos_sources,
        "negative_sources": neg_sources,
        "expert_summary": expert_summary,
        "executive_summary": executive_summary,
        "impact_summary": impact_summary
    }
