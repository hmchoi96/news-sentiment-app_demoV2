import streamlit as st
from datetime import datetime

# 🔗 모듈 임포트 (기존 구조 유지)
from config import TOPIC_SETTINGS
from news_sentiment_tool_demo import get_news, filter_articles, summarize_by_sentiment
from core import analyze_articles_parallel
from ui_components import draw_sentiment_chart

# ✅ 앱 설정
st.set_page_config(page_title="Wiserbond News Sentiment Report", layout="wide")
st.title("📊 Wiserbond News Sentiment Analyzer")

# ✅ 토픽 선택
topic_choice = st.selectbox("Choose a topic", list(TOPIC_SETTINGS.keys()))
topic_config = TOPIC_SETTINGS[topic_choice]
search_term = topic_config["search_term"]
keywords = topic_config["keywords"]

# ✅ 뉴스 불러오기 및 분석
with st.spinner("🔍 Fetching and analyzing news..."):
    raw_articles = get_news(search_term)
    filtered_articles = filter_articles(raw_articles, keywords)
    analyzed_articles = analyze_articles_parallel(filtered_articles)

# ✅ 시각화 출력 (3단계 Plotly 적용)
st.subheader("📈 Sentiment Breakdown")
draw_sentiment_chart(analyzed_articles)

# ✅ 감정별 요약
st.subheader("✅ Positive Summary")
st.markdown(summarize_by_sentiment(analyzed_articles, "POSITIVE", keywords))

st.subheader("⚠️ Negative Summary")
st.markdown(summarize_by_sentiment(analyzed_articles, "NEGATIVE", keywords))

# ✅ 전체 뉴스 결과 (선택)
with st.expander("🔍 Show All Analyzed Articles"):
    for a in analyzed_articles:
        st.write(f"**{a['title']}**")
        st.write(f"*Sentiment:* {a['sentiment']} ({a['score']}) | *Source:* {a['source']}")
        st.write(f"*Summary:* {a['summary']}")
        st.markdown("---")
