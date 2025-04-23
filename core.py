
# core.py
from news_sentiment_tool_demo import get_news, filter_articles, run_sentiment_analysis, summarize_by_sentiment
from config import INDUSTRY_KEYWORDS, COUNTRY_LIST
from news_sentiment_tool_demo import TOPIC_SETTINGS

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

    expert_summary = (
        "✅ **Positive Insight**\n\n"
        + summarize_by_sentiment(analyzed, "POSITIVE", keywords)
        + "\n\n❗ **Negative Insight**\n\n"
        + summarize_by_sentiment(analyzed, "NEGATIVE", keywords)
    )

    return {
        "sentiment_counts": sentiment_counts,
        "positive_news": pos_news,
        "negative_news": neg_news,
        "expert_summary": expert_summary
    }
