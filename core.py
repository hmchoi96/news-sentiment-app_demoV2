# core.py
from news_sentiment_tool_demo import (
    get_news,
    filter_articles,
    run_sentiment_analysis,
    summarize_by_sentiment,
    TOPIC_SETTINGS
)
from config import INDUSTRY_KEYWORDS, SECTOR_KEYWORDS

def analyze_topic(topic, industry, country):
    # 1. 검색어 설정
    setting = TOPIC_SETTINGS[topic]
    search_term = setting["search_term"]
    if country != "Global":
        search_term += f" {country}"

    # 2. 키워드 결합
    keywords = setting["keywords"]
    if industry != "All":
        keywords += INDUSTRY_KEYWORDS.get(industry, [])

    # 3. 뉴스 수집 및 필터링
    raw = get_news(search_term)
    filtered = filter_articles(raw, keywords)
    analyzed = run_sentiment_analysis(filtered)

    # 4. 감정 분류 집계
    sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for a in analyzed:
        label = a["sentiment"].capitalize()
        if label in sentiment_counts:
            sentiment_counts[label] += 1

    # 5. 감정별 뉴스 분류
    pos_news = [a for a in analyzed if a["sentiment"] == "POSITIVE"]
    neg_news = [a for a in analyzed if a["sentiment"] == "NEGATIVE"]

    # 6. 각 감정별 사용된 뉴스 소스 추출 (중복 제거)
    pos_sources = sorted(set(a["source"] for a in pos_news))
    neg_sources = sorted(set(a["source"] for a in neg_news))

    # 7. 요약 생성
    expert_summary = (
        "✅ **Positive Insight**\n\n"
        + summarize_by_sentiment(analyzed, "POSITIVE", keywords)
        + "\n\n❗ **Negative Insight**\n\n"
        + summarize_by_sentiment(analyzed, "NEGATIVE", keywords)
    )

    # 8. 결과 반환
    return {
        "sentiment_counts": sentiment_counts,
        "positive_news": pos_news,
        "negative_news": neg_news,
        "positive_sources": pos_sources,
        "negative_sources": neg_sources,
        "expert_summary": expert_summary
    }
