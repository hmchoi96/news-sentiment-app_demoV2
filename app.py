import streamlit as st
from datetime import datetime

from core import analyze_topic, analyze_articles_parallel
from config import TOPIC_SETTINGS, COUNTRY_LIST, INDUSTRY_SUBSECTORS
from ui_components import draw_sentiment_chart
from news_sentiment_tool_demo import get_news, filter_articles, summarize_by_sentiment

# ✅ 앱 설정
st.set_page_config(page_title="Wiserbond News Sentiment Report", layout="wide")
st.title("📊 Wiserbond News Sentiment Analyzer")

# ✅ 분석 설정 (유저 선택)
st.sidebar.title("🔍 Select Analysis Settings")
topic_choice = st.sidebar.selectbox("Choose a topic", list(TOPIC_SETTINGS.keys()))
country_choice = st.sidebar.selectbox("Select Country", COUNTRY_LIST)
industry_choice = st.sidebar.selectbox("Select Industry", ["All"] + list(INDUSTRY_SUBSECTORS.keys()))
run_analysis = st.sidebar.button("Run Analysis")

# ✅ 버튼 누른 경우 분석 수행
if run_analysis:
    with st.spinner("🔍 Fetching and analyzing news..."):
        result = analyze_topic(topic_choice, country=country_choice, industry=industry_choice)

    st.session_state["result"] = result
    st.session_state["timestamp"] = datetime.now().strftime("%B %d, %Y %H:%M")
    st.session_state["topic"] = topic_choice
    st.session_state["country"] = country_choice
    st.session_state["industry"] = industry_choice

# ✅ 결과 렌더링
if "result" in st.session_state:
    result = st.session_state["result"]
    st.markdown(f"### 🕒 Analysis Date: {st.session_state['timestamp']}")
    st.markdown(f"**Topic:** {st.session_state['topic']}  |  **Country:** {st.session_state['country']}  |  **Industry:** {st.session_state['industry']}")
    st.write("---")

    # ✅ 감정 분포 시각화
    st.subheader("📈 Sentiment Breakdown")
    draw_sentiment_chart(result["sector_sentiment_scores"], selected_industry)


    # ✅ 감정별 요약
    st.subheader("✅ Positive Summary")
    st.markdown(result["expert_summary"].get("positive_summary", "No positive summary found."))

    st.subheader("⚠️ Negative Summary")
    st.markdown(result["expert_summary"].get("negative_summary", "No negative summary found."))

    # ✅ 전체 기사 표시
    with st.expander("🔍 Show All Analyzed Articles"):
        for a in result["positive_news"] + result["negative_news"]:
            st.write(f"**{a['title']}**")
            st.write(f"*Sentiment:* {a['sentiment']} ({a['score']}) | *Source:* {a['source']}")
            st.write(f"*Summary:* {a['summary']}")
            st.markdown("---")
