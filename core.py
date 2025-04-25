from news_sentiment_tool_demo import (
    get_news,
    filter_articles,
    run_sentiment_analysis,
    summarize_by_sentiment,
    TOPIC_SETTINGS
)
from config import INDUSTRY_KEYWORDS, SECTOR_KEYWORDS, INDUSTRY_SUBSECTORS
from collections import Counter
from transformers import pipeline

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
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    text_block = " ".join(sector_texts)[:512]
    try:
        summary = summarizer(text_block, max_length=40, min_length=10, do_sample=False)[0]["summary_text"]
        return summary
    except:
        return "Summary model failed."

def compute_subsector_sentiment_scores(analyzed, subsector_keywords_dict):
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

def extract_top_issue_summary(articles):
    if not articles:
        return "global macro concerns"
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    content = " ".join([f"{a['title']}. {a.get('description', '')}" for a in articles])[:512]
    try:
        summary = summarizer(content, max_length=40, min_length=10, do_sample=False)[0]['summary_text']
        return summary
    except:
        return "market events and policy responses"

def analyze_topic(topic, industry, country):
    setting = TOPIC_SETTINGS[topic]
    search_term = setting["search_term"]
    if country != "Global":
        search_term += f" {country}"

    base_keywords = setting["keywords"].copy()
    industry_keywords = INDUSTRY_KEYWORDS.get(industry, []) if industry != "All" else None

    # ✅ industry_keywords를 get_news에서 제거 (단일 쿼리만)
    raw = get_news(search_term)

    # ✅ 필터링은 base_keywords + industry_keywords 조합으로 진행
    filtered = filter_articles(raw, base_keywords, industry_keywords)

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
        + summarize_by_sentiment(analyzed, "POSITIVE", base_keywords)
        + "\n\n❗ **Negative Insight**\n\n"
        + summarize_by_sentiment(analyzed, "NEGATIVE", base_keywords)
    )

    dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get)
    top_issue_summary = extract_top_issue_summary(analyzed)
    executive_summary = (
        f"Over the past 3 days, news coverage on **{topic}** has been predominantly "
        f"**{dominant_sentiment.lower()}**, with a focus on {top_issue_summary}."
    )

    subsector_sentiment_scores = {}
    if industry != "All" and industry in INDUSTRY_SUBSECTORS:
        subsector_keywords = INDUSTRY_SUBSECTORS[industry]
        subsector_sentiment_scores = compute_subsector_sentiment_scores(analyzed, subsector_keywords)

    impact_summary = []
    impact_map, source_map = detect_impacted_sectors(analyzed, SECTOR_KEYWORDS)
    for sector, texts in impact_map.items():
        sources = source_map.get(sector, [])
        most_common_source = Counter(sources).most_common(1)[0][0] if sources else "Unknown"
        impact_summary.append({
            "sector": sector,
            "impact": summarize_sector_impact(texts),
            "source": f"{most_common_source}, {len(texts)} articles"
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
        "subsector_sentiment_scores": subsector_sentiment_scores
    }
