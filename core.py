import streamlit as st
from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor

from news_sentiment_tool_demo import fetch_news_articles, filter_articles_by_keywords
from summary_utils import summarize_articles, generate_expert_commentary

# ✅ 감성 분석 모델은 최초 1회만 로드
@st.cache_resource
def load_sentiment_pipeline():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# ✅ 뉴스 기사도 캐시 (30분 TTL)
@st.cache_data(ttl=1800)
def cached_fetch_articles(topic, country, industry):
    return fetch_news_articles(topic, country, industry)

# 🔍 주요 분석 함수
def analyze_topic(topic, country, industry):
    articles = cached_fetch_articles(topic, country, industry)
    filtered = filter_articles_by_keywords(articles, topic, industry)

    sentiment_model = load_sentiment_pipeline()

    # 🔄 기사별 감성 분석 병렬 처리
    with ThreadPoolExecutor() as executor:
        sentiment_results = list(executor.map(sentiment_model, [a["content"] for a in filtered]))

    # 분석 결과를 각 기사에 매핑
    for i, res in enumerate(sentiment_results):
        filtered[i]["sentiment"] = res[0]["label"].lower()  # e.g., "positive", "negative"

    # 분류
    positive_articles = [a for a in filtered if a["sentiment"] == "positive"]
    negative_articles = [a for a in filtered if a["sentiment"] == "negative"]
    neutral_count = len(filtered) - len(positive_articles) - len(negative_articles)
    sentiment_counts = {
        "positive": len(positive_articles),
        "negative": len(negative_articles),
        "neutral": neutral_count
    }

    # 요약 및 전문가 해석 생성
    summary = summarize_articles(positive_articles, negative_articles)
    expert_summary = generate_expert_commentary(summary, topic, country, industry)

    return {
        "positive_articles": positive_articles,
        "negative_articles": negative_articles,
        "sentiment_counts": sentiment_counts,
        "expert_summary": expert_summary
    }
