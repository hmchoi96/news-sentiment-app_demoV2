import streamlit as st
from datetime import datetime

from core import analyze_topic
from config import TOPIC_SETTINGS, COUNTRY_LIST, INDUSTRY_SUBSECTORS, LANG_TEXT
from ui_components import draw_sentiment_chart, display_news_section

# 앱 기본 설정
st.set_page_config(page_title="Wiserbond News Sentiment Report", layout="wide")
st.title("📊 Wiserbond News Sentiment Analyzer")

# 사이드바 - 사용자 입력
st.sidebar.title("🔍 Select Analysis Settings")
topic_choice = st.sidebar.selectbox("Choose a topic", list(TOPIC_SETTINGS.keys()))
country_choice = st.sidebar.selectbox("Select Country", COUNTRY_LIST)
industry_choice = st.sidebar.selectbox("Select Industry", ["All"] + list(INDUSTRY_SUBSECTORS.keys()))
language_choice = st.sidebar.selectbox("Language", list(LANG_TEXT.keys()))
st.session_state["language"] = language_choice

if st.sidebar.button("Run Analysis"):
    with st.spinner("Running sentiment and summary analysis..."):
        result = analyze_topic(topic_choice, country=country_choice, industry=industry_choice, language=language_choice)

    st.session_state["result"] = result
    st.session_state["timestamp"] = datetime.now().strftime("%B %d, %Y %H:%M")
    st.session_state["topic"] = topic_choice
    st.session_state["country"] = country_choice
    st.session_state["industry"] = industry_choice

# 결과 출력
if "result" in st.session_state:
    result = st.session_state["result"]
    selected_industry = st.session_state["industry"]
    lang = st.session_state["language"]
    texts = LANG_TEXT[lang]

    st.markdown(f"## {texts['header']}")
    st.write(f"**Date:** {st.session_state['timestamp']}")
    st.markdown(f"<small>Topic: {st.session_state['topic']} | Country: {st.session_state['country']} | Industry: {selected_industry}</small>", unsafe_allow_html=True)
    st.write("---")

    st.markdown(texts["executive_summary"])
    st.info(result["executive_summary"])

    st.markdown(texts["sentiment_chart"])
    draw_sentiment_chart(result["sector_sentiment_scores"], selected_industry)

    st.markdown("## 🧭 Sector Impact Breakdown")
    for item in result["impact_summary"]:
        st.markdown(f"- **{item['sector']}**: {item['impact']} ({item['source']})")

    st.markdown(texts["expert_insight"])
    st.markdown(texts["positive_title"])
    st.success(result["expert_summary"].get("positive_summary", "No positive summary found."))

    st.markdown(texts["negative_title"])
    st.warning(result["expert_summary"].get("negative_summary", "No negative summary found."))

    st.markdown("---")
    st.markdown(texts["footer"], unsafe_allow_html=True)
