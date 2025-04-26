from news_sentiment_tool_demo import (
    get_news,
    filter_articles,
    run_sentiment_analysis,
    summarize_by_sentiment,
    TOPIC_SETTINGS
)
from config import INDUSTRY_KEYWORDS, SECTOR_KEYWORDS
from collections import Counter
from transformers import pipeline

def detect_impacted_sectors(articles):
    """기사 텍스트를 통해 산업 영향 파악"""
    impact_map = {}
    source_map = {}
    for a in articles:
        text = f"{a['title']} {a.get('description', '')}".lower()
        for sector, keywords in SECTOR_KEYWORDS.items():
            if any(k in text for k in keywords):
                impact_map.setdefault(sector, []).append(text)
                source_map.setdefault(sector, []).append(a.get('source', 'Unknown'))
    return impact_map, source_map

def summarize_sector_impact(sector_texts):
    """산업별 임팩트 요약"""
    if not sector_texts:
        return "No clear impact found."
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    text_block = " ".join(sector_texts)[:512]
    try:
        summary = summarizer(text_block, max_length=40, min_length=10, do_sample=False)[0]["summary_text"]
        return summary
    except Exception:
        return "Summary model failed."

def compute_sector_sentiment_scores(analyzed, sector_keywords):
    """섹터별 평균 감정 점수 계산"""
    sentiment_map = {"NEGATIVE": 0.0, "NEUTRAL": 0.5, "POSITIVE": 1.0}
    sector_scores = {}
    sector_counts = {}

    for a in analyzed:
        text = f"{a['title']} {a.get('description', '')}".lower()
        score = sentiment_map.get(a["sentiment"], 0.5)
        for sector, keywords in sector_keywords.items():
            if any(k in text for k in keywords):
                sector_scores.setdefault(sector, 0.0)
                sector_counts.setdefault(sector, 0)
                sector_scores[sector] += score
                sector_counts[sector] += 1

    averaged_scores = {
        sector: (sector_scores[sector] / sector_counts[sector])
        for sector in sector_scores
    }

    return averaged_scores

def analyze_topic(topic, country="Global", industry="All", language="English"):
    """전체 토픽 분석 메인 함수"""
    # 검색어 준비
    setting = TOPIC_SETTINGS[topic]
    search_term = setting["search_term"]
    if country != "Global":
        search_term += f" {country}"

    # 키워드 설정
    keywords = setting["keywords"].copy()
    if industry != "All":
        keywords += INDUSTRY_KEYWORDS.get(industry, [])

    # 1. 뉴스 수집 및 필터링
    raw_articles = get_news(search_term)
    filtered_articles = filter_articles(raw_articles, keywords)

    # 2. 감정 분석
    analyzed_articles = run_sentiment_analysis(filtered_articles)

    # 3. 감정 통계
    sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for a in analyzed_articles:
        label = a["sentiment"].capitalize()
        if label in sentiment_counts:
            sentiment_counts[label] += 1

    # 긍정/부정 기사 및 소스
    pos_news = [a for a in analyzed_articles if a["sentiment"] == "POSITIVE"]
    neg_news = [a for a in analyzed_articles if a["sentiment"] == "NEGATIVE"]

    pos_sources = sorted(set(a["source"] for a in pos_news))
    neg_sources = sorted(set(a["source"] for a in neg_news))

    # 4. Executive Summary (핵심요약)
    dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get)
    top_issue_summary = "renewed US tariff threats and China's retaliatory stance"  # ★ 임시 고정 (나중에 자동추출 가능)
    executive_summary = (
        f"Over the past 3 days, news coverage on **{topic}** has been predominantly "
        f"**{dominant_sentiment.lower()}**, with a focus on {top_issue_summary}."
    )

    # 5. Sector별 Impact Summary
    impact_summary = []
    impact_map, source_map = detect_impacted_sectors(analyzed_articles)
    for sector, texts in impact_map.items():
        sources = source_map.get(sector, [])
        most_common_source = Counter(sources).most_common(1)[0][0] if sources else "Unknown"
        impact_summary.append({
            "sector": sector,
            "impact": summarize_sector_impact(texts),
            "source": most_common_source
        })

    # 6. Sector별 Sentiment Score
    sector_sentiment_scores = compute_sector_sentiment_scores(analyzed_articles, SECTOR_KEYWORDS)

    # 7. 전문가 요약 (Positive/Negative 따로)
    expert_summary = {
        "positive_summary": summarize_by_sentiment(analyzed_articles, "POSITIVE", keywords),
        "negative_summary": summarize_by_sentiment(analyzed_articles, "NEGATIVE", keywords)
    }

    # 최종 결과 리턴
    return {
        "sentiment_counts": sentiment_counts,
        "positive_news": pos_news,
        "negative_news": neg_news,
        "positive_sources": pos_sources,
        "negative_sources": neg_sources,
        "executive_summary": executive_summary,
        "impact_summary": impact_summary,
        "sector_sentiment_scores": sector_sentiment_scores,
        "expert_summary": expert_summary
    }
