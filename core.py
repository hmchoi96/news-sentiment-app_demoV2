import streamlit as st
from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor
from news_sentiment_tool_demo import fetch_news_articles, filter_articles_by_keywords
from config import TOPIC_SETTINGS, SECTOR_KEYWORDS

# ✅ 감성 분석 모델은 최초 1회만 로드
@st.cache_resource
def load_sentiment_pipeline():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# ✅ 요약 모델도 캐싱
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# ✅ 뉴스 캐싱
@st.cache_data(ttl=1800)
def cached_fetch_articles(topic, country, industry):
    return fetch_news_articles(topic, country, industry)

def contains_keywords(text, keywords):
    text = (text or "").lower()
    return any(k.lower() in text for k in keywords)

# ✅ 기사 요약 기능
def summarize_by_sentiment(articles, sentiment_label, topic, industry):
    summarizer = load_summarizer()
    topic_keywords = TOPIC_SETTINGS[topic]["keywords"]
    industry_keywords = SECTOR_KEYWORDS.get(industry, [])
    keywords = topic_keywords + industry_keywords

    texts = [
        f"{a['description']} (Title: {a['title']})"
        for a in articles
        if a['sentiment'] == sentiment_label and contains_keywords(f"{a['description']} {a['title']}", keywords)
    ]

    if len(texts) < 1:
        return "No matching articles found for summarization."

    truncated = " ".join(texts)[:1000]
    try:
        summary = summarizer(truncated, max_length=200, min_length=60, do_sample=False)[0]['summary_text']
        return summary
    except Exception:
        return "Summarization failed due to model error."

# ✅ 메인 분석 함수
def analyze_topic(topic, country, industry):
    articles = cached_fetch_articles(topic, country, industry)
    filtered = filter_articles_by_keywords(articles, topic, industry)

    sentiment_model = load_sentiment_pipeline()
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(sentiment_model, [a["content"] for a in filtered]))

    for i, res in enumerate(results):
        filtered[i]["sentiment"] = res[0]["label"].lower()

    positive_articles = [a for a in filtered if a["sentiment"] == "positive"]
    negative_articles = [a for a in filtered if a["sentiment"] == "negative"]
    neutral_count = len(filtered) - len(positive_articles) - len(negative_articles)

    sentiment_counts = {
        "positive": len(positive_articles),
        "negative": len(negative_articles),
        "neutral": neutral_count
    }

    # ✅ 요약 기능 그대로 포함
    pos_summary = summarize_by_sentiment(positive_articles, "positive", topic, industry)
    neg_summary = summarize_by_sentiment(negative_articles, "negative", topic, industry)

    expert_summary = f"✅ Positive Summary:\n{pos_summary}\n\n⚠️ Negative Summary:\n{neg_summary}"

    return {
        "positive_articles": positive_articles,
        "negative_articles": negative_articles,
        "sentiment_counts": sentiment_counts,
        "expert_summary": expert_summary
    }
