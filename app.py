import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from core import analyze_topic
from config import LANG_TEXT, COUNTRY_LIST, INDUSTRY_SUBSECTORS
from news_sentiment_tool_demo import TOPIC_SETTINGS
from ui_components import display_news_section, draw_sentiment_chart

# 💡 브랜드 컬러 적용
WISERBOND_COLOR = "#051F5B"
st.set_page_config(page_title="Wiserbond News Sentiment Report", layout="wide")

# ================================
# Sidebar - User Inputs
# ================================
st.sidebar.title("🔍 Analysis Settings")
topic_choice = st.sidebar.selectbox("Choose a topic", list(TOPIC_SETTINGS.keys()))
country_choice = st.sidebar.selectbox("🌍 Country Filter (Optional)", COUNTRY_LIST)
industry_choice = st.sidebar.selectbox("🏭 Select Industry (Optional)", ["All"] + list(INDUSTRY_SUBSECTORS.keys()))
language_choice = st.sidebar.selectbox("🌐 Language / 언어 선택", list(LANG_TEXT.keys()))
st.session_state["language"] = language_choice

# ================================
# Header
# ================================
st.markdown(f"# {LANG_TEXT[language_choice]['header']}")
st.markdown(
    f"**Date:** {datetime.today().strftime('%B %d, %Y')} | **Topic:** {topic_choice} | **Country:** {country_choice} | **Industry:** {industry_choice}"
)
st.markdown("<small>This is demo version, please understand it may take a few seconds to analyze news.</small>", unsafe_allow_html=True)

# ================================
# Main Analysis Process
# ================================
with st.spinner("🔎 Analyzing news articles... Please wait."):
    result = analyze_topic(topic_choice, country_choice, industry_choice)

# ================================
# Sentiment Chart
# ================================
st.markdown(LANG_TEXT[language_choice]["sentiment_chart"])
draw_sentiment_chart(result["sentiment_counts"], WISERBOND_COLOR)

# ================================
# News Summary Sections
# ================================
display_news_section("positive", result["positive_articles"], language_choice)
display_news_section("negative", result["negative_articles"], language_choice)

# ================================
# Expert Interpretation
# ================================
st.markdown(LANG_TEXT[language_choice]["expert_insight"])
st.markdown(result["expert_summary"])

# ================================
# Footer
# ================================
st.markdown(LANG_TEXT[language_choice]["footer"], unsafe_allow_html=True)
