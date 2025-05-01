import streamlit as st
from datetime import datetime

from core import analyze_topic
from config import TOPIC_SETTINGS, COUNTRY_LIST, INDUSTRY_SUBSECTORS, LANG_TEXT
from ui_components import draw_sentiment_chart, display_news_section

# ✅ 앱 설정
st.set_page_config(page_title="Wiserbond News Sentiment Report", layout="wide")
st.title("📊 Wiserbond News Sentiment Analyzer")

# ✅ 사용자 설정
st.sidebar.title("🔍 Select Analysis Settings")
topic_choice = st.sidebar.selectbox("Choose a topic", list(TOPIC_SETTINGS.keys()))
country_choice = st.sidebar.selectbox("Select Country", COUNTRY_LIST)
industry_choice = st.sidebar.selectbox("Select Industry", ["All"] + list(INDUSTRY_SUBSECTORS.keys()))
language_choice = st.sidebar.selectbox("Select Language", list(LANG_TEXT.keys()))
run_analysis = st.sidebar.button("Run Analysis")

# ✅ 분석 수행
if run_analysis:
    with st.spinner("🔍 Fetching and analyzing news..."):
        result = analyze_topic(topic_choice, country=country_choice, industry=industry_choice, language=language_choice)

    st.session_state["result"] = result
    st.session_state["timestamp"] = datetime.now().strftime("%B %d, %Y %H:%M")
    st.session_state["topic"] = topic_choice
    st.session_state["country"] = country_choice
    st.session_state["industry"] = industry_choice
    st.session_state["language"] = language_choice

# ✅ 결과 출력
if "result" in st.session_state:
    lang = LANG_TEXT[st.session_state["language"]]
    result = st.session_state["result"]
    st.markdown(f"### 🕒 {st.session_state['timestamp']}")
    st.markdown(f"**Topic:** {st.session_state['topic']}  |  **Country:** {st.session_state['country']}  |  **Industry:** {st.session_state['industry']}")
    st.markdown("---")

    # 1. Executive Summary
    st.markdown(lang["executive_summary"])
    st.info(result["executive_summary"])

    # 2. Sentiment Chart
    st.markdown(lang["sentiment_chart"])
    draw_sentiment_chart(result["sector_sentiment_scores"], st.session_state["industry"])

    # 3. Sector Breakdown
    st.markdown("### 3. Sector Impact Breakdown")
    if result["impact_summary"]:
        for item in result["impact_summary"]:
            st.markdown(f"- **{item['sector']}**: {item['impact']} ({item['source']})")
    else:
        st.markdown("_No specific sector impact summary available._")

    # 4. Wiserbond Interpretation
    st.markdown(lang["expert_insight"])
    st.success(result["expert_summary"].get("positive_summary", "No positive summary found."))
    st.warning(result["expert_summary"].get("negative_summary", "No negative summary found."))

    # 5. Show Articles
    st.markdown("---")
    st.markdown("### 🔍 Full Article List (Optional)")
    with st.expander("Show All Analyzed Articles"):
        display_news_section("Positive", result["positive_news"])
        display_news_section("Negative", result["negative_news"])
