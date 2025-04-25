from news_sentiment_tool_demo import (
    get_news,
    filter_articles,
    run_sentiment_analysis,
    summarize_by_sentiment,
    TOPIC_SETTINGS
)
from config import INDUSTRY_KEYWORDS, SECTOR_KEYWORDS, INDUSTRY_SUBSECTORS
from collections import Counter

def detect_impacted_sectors(articles, sector_keywords):
    impact_map = {}
    source_map = {}
    for a in articles:
        text = f"{a['title']} {a.get('description', '')}".lower()
        for sector, keywords in sector_keywords.items():
            if any(k in text for k in keywords):
                impact_map.setdefault(sector, []).append(text)
                source_map.setdefault(sector, []).append(a.get('source', 'Unknown'))
    return impact_map, source_map

def summarize_sector_impact(sector_texts):
    if not sector_texts:
        return "No clear impact found."
    from transformers import pipeline
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    text_block = " ".join(sector_texts)[:512]
    try:
        summary = summarizer(text_block, max_length=40, min_length=10, do_sample=False)[0]["summary_text"]
        return summary
    except:
        return "Summary model failed."

def compute_subsector_sentiment_scores(analyzed, subsector_keywords_dict):
    """
    선택된 industry의 subsector 별 감정 점수 계산
    """
    sentiment_map = {"NEGATIVE": 0.0, "NEUTRAL": 0.5, "POSITIVE": 1.0}
    subsector_scores = {}
    subsector_counts = {}

    for a in analyzed:
        text = f"{a['title']} {a.get('description', '')}".lower()
        score = sentiment_map.get(a["sentiment"], 0.5)
        for subsector, keywords in subsector_keywords_dict.items():
            if any(k in text for k in keywords):
                subsector_scores.setdefault(subsector, 0.0)
                subsector_counts.setdefault(subsector, 0)
                subsector_scores[subsector] += score
                subsector_counts[subsector] += 1

    averaged = {
        s: (subsector_scores[s] / subsector_counts[s])
        for s in subsector_scores
    }
    return averaged

def analyze_topic(topic, industry, country):
    setting = TOPIC_SETTINGS[topic]
    search_term = setting["search_term"]
    if country != "Global":
        search_term += f" {country}"

    keywords = setting["keywords"].copy()
    if industry != "All":
        keywords += INDUSTRY_KEYWORDS.get(industry, [])

    raw = get_news(search_term)
    filtered = filter_articles(raw, keywords)
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
        + summarize_by_sentiment(analyzed, "POSITIVE", keywords)
        + "\n\n❗ **Negative Insight**\n\n"
        + summarize_by_sentiment(analyzed, "NEGATIVE", keywords)
    )

    dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get)
    top_issue_summary = "renewed US tariff threats and China's retaliatory stance"
    executive_summary = (
        f"Over the past 3 days, news coverage on **{topic}** has been predominantly "
        f"**{dominant_sentiment.lower()}**, with a focus on {top_issue_summary}."
    )

    # Subsector 기반 분석
    subsector_sentiment_scores = {}
    if industry != "All" and industry in INDUSTRY_SUBSECTORS:
        subsector_keywords = INDUSTRY_SUBSECTORS[industry]
        subsector_sentiment_scores = compute_subsector_sentiment_scores(analyzed, subsector_keywords)

    # 기존 섹터 분석 유지 (선택사항)
    impact_summary = []
    impact_map, source_map = detect_impacted_sectors(analyzed, SECTOR_KEYWORDS)
    for sector, texts in impact_map.items():
        sources = source_map.get(sector, [])
        most_common_source = Counter(sources).most_common(1)[0][0] if sources else "Unknown"
        impact_summary.append({
            "sector": sector,
            "impact": summarize_sector_impact(texts),
            "source": most_common_source
        })

    return {
        "sentiment_counts": sentiment_counts,
        "positive_news": pos_news,
        "negative_news": neg_news,
        "positive_sources": pos_sources,
        "negative_sources": neg_sources,
        "expert_summary": expert_summary,
        "executive_summary": executive_summary,
        "impact_summary": impact_summary,
        "subsector_sentiment_scores": subsector_sentiment_scores  # ✅ 새 필드
    }
