import streamlit as st
from datetime import datetime
from news_sentiment_fast import TOPIC_SETTINGS, get_news, filter_articles, analyze_articles_parallel, draw_sentiment_chart, summarize_by_sentiment

# ✅ 앱 설정
st.set_page_config(page_title="Wiserbond News Sentiment Report", layout="wide")
st.title("📊 Wiserbond News Sentiment Analyzer")

# ✅ 토픽 선택
topic_choice = st.selectbox("Choose a topic", list(TOPIC_SETTINGS.keys()))
topic_config = TOPIC_SETTINGS[topic_choice]
search_term = topic_config["search_term"]
keywords = topic_config["keywords"]

# ✅ 뉴스 불러오기
with st.spinner("Fetching and analyzing news..."):
    raw_articles = get_news(search_term)
    filtered_articles = filter_articles(raw_articles, keywords)
    analyzed_articles = analyze_articles_parallel(filtered_articles)

# ✅ 시각화
st.subheader("📈 Sentiment Breakdown")
draw_sentiment_chart(analyzed_articles)

# ✅ 감정별 요약
st.subheader("✅ Positive Summary")
st.markdown(summarize_by_sentiment(analyzed_articles, "POSITIVE", keywords))

st.subheader("⚠️ Negative Summary")
st.markdown(summarize_by_sentiment(analyzed_articles, "NEGATIVE", keywords))

# ✅ 뉴스 상세 보기 (선택)
with st.expander("🔍 Show All Analyzed Articles"):
    for a in analyzed_articles:
        st.write(f"**{a['title']}**")
        st.write(f"*Sentiment:* {a['sentiment']} ({a['score']}) | *Source:* {a['source']}")
        st.write(f"*Summary:* {a['summary']}")
        st.markdown("---")
