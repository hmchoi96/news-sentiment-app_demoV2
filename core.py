from news_sentiment_tool_demo import (
    get_news,
    filter_articles,
    run_sentiment_analysis,
    summarize_by_sentiment,
    TOPIC_SETTINGS
)
from config import INDUSTRY_SUBSECTORS, SECTOR_KEYWORDS
from collections import Counter
from transformers import pipeline


def detect_impacted_sectors(articles, selected_industry):
    """선택된 산업에 따라 관련된 섹터 뉴스만 추출"""
    impact_map = {}
    source_map = {}
    relevant_sectors = (
        list(SECTOR_KEYWORDS.keys()) if selected_industry == "All"
        else list(INDUSTRY_SUBSECTORS.get(selected_industry, {}).keys())
    )
    for a in articles:
        text = f"{a['title']} {a.get('description', '')}".lower()
        for sector in relevant_sectors:
            keywords = SECTOR_KEYWORDS.get(sector, [])
            if any(k.lower() in text for k in keywords):
                impact_map.setdefault(sector, []).append(text)
                source_map.setdefault(sector, []).append(a.get('source', 'Unknown'))
    return impact_map, source_map


def summarize_sector_impact(sector_texts):
    if not sector_texts:
        return "No clear impact found."
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    text_block = " ".join(sector_texts)[:512]
    try:
        summary = summarizer(text_block, max_length=40, min_length=10, do_sample=False)[0]["summary_text"]
        return summary
    except Exception:
        return "Summary model failed."


def compute_sector_sentiment_scores(analyzed, selected_industry):
    sentiment_map = {"NEGATIVE": 0.0, "NEUTRAL": 0.5, "POSITIVE": 1.0}
    sector_scores = {}
    sector_counts = {}
    relevant_sectors = (
        list(SECTOR_KEYWORDS.keys()) if selected_industry == "All"
        else list(INDUSTRY_SUBSECTORS.get(selected_industry, {}).keys())
    )

    for sector in relevant_sectors:
        sector_scores[sector] = 0.0
        sector_counts[sector] = 0

    for a in analyzed:
        text = f"{a['title']} {a.get('description', '')}".lower()
        score = sentiment_map.get(a["sentiment"], 0.5)
        for sector in relevant_sectors:
            keywords = SECTOR_KEYWORDS.get(sector, [])
            if any(k.lower() in text for k in keywords):
                sector_scores[sector] += score
                sector_counts[sector] += 1
                break

    averaged_scores = {
        sector: (sector_scores[sector] / sector_counts[sector]) if sector_counts[sector] else 0.0
        for sector in relevant_sectors
    }
    return averaged_scores


def analyze_topic(topic, country="Global", industry="All", language="English"):
    setting = TOPIC_SETTINGS[topic]
    search_term = setting["search_term"]
    if country != "Global":
        search_term += f" {country}"

    keywords = setting["keywords"].copy()
    if industry != "All":
        industry_keywords = [kw for s in INDUSTRY_SUBSECTORS.get(industry, {}).values() for kw in s]
        keywords += industry_keywords

    raw_articles = get_news(search_term)
    filtered_articles = filter_articles(raw_articles, keywords)
    analyzed_articles = run_sentiment_analysis(filtered_articles)

    sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for a in analyzed_articles:
        label = a["sentiment"].capitalize()
        if label in sentiment_counts:
            sentiment_counts[label] += 1

    pos_news = [a for a in analyzed_articles if a["sentiment"] == "POSITIVE"]
    neg_news = [a for a in analyzed_articles if a["sentiment"] == "NEGATIVE"]

    pos_sources = sorted(set(a["source"] for a in pos_news))
    neg_sources = sorted(set(a["source"] for a in neg_news))

    dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get)
    top_issue_summary = "renewed US tariff threats and China's retaliatory stance"  # future: automate this
    executive_summary = (
        f"Over the past 3 days, news coverage on **{topic}** has been predominantly "
        f"**{dominant_sentiment.lower()}**, with a focus on {top_issue_summary}."
    )

    impact_summary = []
    impact_map, source_map = detect_impacted_sectors(analyzed_articles, industry)
    for sector, texts in impact_map.items():
        sources = source_map.get(sector, [])
        most_common_source = Counter(sources).most_common(1)[0][0] if sources else "Unknown"
        impact_summary.append({
            "sector": sector,
            "impact": summarize_sector_impact(texts),
            "source": most_common_source
        })

    sector_sentiment_scores = compute_sector_sentiment_scores(analyzed_articles, industry)
    expert_summary = {
        "positive_summary": summarize_by_sentiment(analyzed_articles, "POSITIVE", keywords),
        "negative_summary": summarize_by_sentiment(analyzed_articles, "NEGATIVE", keywords)
    }

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
