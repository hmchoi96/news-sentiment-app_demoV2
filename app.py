
import streamlit as st
from datetime import datetime

from config import LANG_TEXT, INDUSTRY_KEYWORDS, COUNTRY_LIST
from news_sentiment_tool_demo import TOPIC_SETTINGS
from core import analyze_topic
from ui_components import display_news_section, draw_sentiment_chart

st.set_page_config(page_title="Wiserbond News Sentiment Report", layout="wide")

# Sidebar - User Inputs
st.sidebar.title("🔍 Select Topic")
topic_choice = st.sidebar.selectbox("Choose a topic", list(TOPIC_SETTINGS.keys()))
country_choice = st.sidebar.selectbox("🌍 Country Filter (Optional)", COUNTRY_LIST)
industry_choice = st.sidebar.selectbox("🏭 Select Industry (Optional)", ["All"] + list(INDUSTRY_KEYWORDS.keys()))
language_choice = st.sidebar.selectbox("🌐 Language / 언어 선택", list(LANG_TEXT.keys()))

st.session_state["language"] = language_choice
st.session_state["country"] = country_choice
st.session_state["industry"] = industry_choice
texts = LANG_TEXT[language_choice]

# Run button
if st.sidebar.button("Run Analysis"):
    result = analyze_topic(topic_choice, industry_choice, country_choice)
    st.session_state["topic"] = topic_choice
    st.session_state.update(result)

# UI Header
st.markdown(f"# {texts['header']}")
st.markdown(
    f"**Date:** {datetime.today().strftime('%B %d, %Y')} | **Topic:** {st.session_state.get('topic', 'Not selected')} | **Industry:** {st.session_state.get('industry', 'All')} | **Country:** {st.session_state.get('country', 'Global')}"
)

# Show Results
if "sentiment_counts" in st.session_state:
    positive_news = st.session_state["positive_news"]
    negative_news = st.session_state["negative_news"]
    expert_summary = st.session_state["expert_summary"]

    st.markdown(texts["executive_summary"])
    st.markdown(texts["sentiment_chart"])

    draw_sentiment_chart(positive_news + negative_news)

    st.markdown("## 📰 Key News Highlights")
    st.markdown(texts["positive_title"])
    display_news_section("Positive", positive_news)
    st.markdown("**📰 Sources:** " + ", ".join(st.session_state["positive_sources"]))  # 👈 여기에

    st.markdown(texts["negative_title"])
    display_news_section("Negative", negative_news)
    st.markdown("**📰 Sources:** " + ", ".join(st.session_state["negative_sources"]))  # 👈 여기에


    st.markdown(texts["expert_insight"])
    st.markdown(f"<div style='white-space: pre-wrap'>{expert_summary}</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(texts["footer"], unsafe_allow_html=True)
