from news_sentiment_tool_demo import (
    get_news,
    filter_articles,
    run_sentiment_analysis,
    summarize_by_sentiment,
    TOPIC_SETTINGS
)
from config import INDUSTRY_KEYWORDS, SECTOR_KEYWORDS

def detect_impacted_sectors(articles):
    impact_map = {}
    for a in articles:
        text = f"{a['title']} {a['description'] or ''}".lower()
        for sector, keywords in SECTOR_KEYWORDS.items():
            if any(k in text for k in keywords):
                impact_map.setdefault(sector, []).append(text)
    return impact_map

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

def analyze_topic(topic, industry, country):
    setting = TOPIC_SETTINGS[topic]
    search_term = setting["search_term"]
    if country != "Global":
        search_term += f" {country}"

    keywords = setting["keywords"]
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

    impact_summary = []
    detected = detect_impacted_sectors(analyzed)
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
