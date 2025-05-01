import streamlit as st
from datetime import datetime

from core import analyze_topic
from config import TOPIC_SETTINGS, COUNTRY_LIST, INDUSTRY_SUBSECTORS
from ui_components import draw_sentiment_chart, display_news_section
from news_sentiment_tool_demo import get_news, filter_articles

# ✅ 앱 설정
st.set_page_config(page_title="Wiserbond News Sentiment Analyzer", layout="wide")
st.title("📊 Wiserbond News Sentiment Analyzer")

# ✅ 분석 설정
st.sidebar.title("🔍 Select Analysis Settings")
topic_choice = st.sidebar.selectbox("Choose a topic", list(TOPIC_SETTINGS.keys()))
country_choice = st.sidebar.selectbox("Select Country", COUNTRY_LIST)
industry_choice = st.sidebar.selectbox("Select Industry", ["All"] + list(INDUSTRY_SUBSECTORS.keys()))
run_analysis = st.sidebar.button("Run Analysis")

# ✅ 버튼 누른 경우 실행
if run_analysis:
    with st.spinner("🔍 Fetching and analyzing news..."):
        result = analyze_topic(topic_choice, country=country_choice, industry=industry_choice)

    st.session_state["result"] = result
    st.session_state["timestamp"] = datetime.now().strftime("%B %d, %Y %H:%M")
    st.session_state["topic"] = topic_choice
    st.session_state["country"] = country_choice
    st.session_state["industry"] = industry_choice

# ✅ 결과 출력
if "result" in st.session_state:
    result = st.session_state["result"]
    st.markdown(f"### 🕒 Analysis Date: {st.session_state['timestamp']}")
    st.markdown(f"**Topic:** {st.session_state['topic']}  |  **Country:** {st.session_state['country']}  |  **Industry:** {st.session_state['industry']}")
    st.write("---")

    st.markdown("### 1. Executive Summary")
    st.info(result["executive_summary"])

    st.markdown("### 2. Sector Sentiment Breakdown")
    draw_sentiment_chart(result["sector_sentiment_scores"], st.session_state["industry"])

    st.markdown("### 3. Sector Impact Breakdown")
    for item in result["impact_summary"]:
        st.markdown(f"- **{item['sector']}**: {item['impact']} ({item['source']})")

    st.markdown("### 4. Wiserbond Interpretation")
    st.success("✅ Positive Insight: " + result["expert_summary"].get("positive_summary", "None"))
    st.warning("❗ Negative Insight: " + result["expert_summary"].get("negative_summary", "None"))

    with st.expander("🔍 Show All Analyzed Articles"):
        display_news_section("All Articles", result["positive_news"] + result["negative_news"])
