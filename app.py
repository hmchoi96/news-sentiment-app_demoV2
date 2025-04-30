# app.py
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

from core import analyze_topic
from config import LANG_TEXT, INDUSTRY_KEYWORDS, INDUSTRY_SUBSECTORS, COUNTRY_LIST
from news_sentiment_tool_demo import TOPIC_SETTINGS
from ui_components import display_news_section, draw_sentiment_chart

WISERBOND_COLOR = "#051F5B"

st.set_page_config(page_title="Wiserbond News Sentiment Report", layout="wide")

# ─── 사이드바 ─────────────────────────
st.sidebar.title("🔍 Select Filters")
topic_choice     = st.sidebar.selectbox("Choose Topic", list(TOPIC_SETTINGS.keys()))
country_choice   = st.sidebar.selectbox("Country (Optional)", ["Global"] + COUNTRY_LIST)
industry_choice  = st.sidebar.selectbox("Industry (Optional)", ["All"] + list(INDUSTRY_KEYWORDS.keys()))
language_choice  = st.sidebar.selectbox("Language / 언어 선택", list(LANG_TEXT.keys()))

# 다국어 텍스트 불러오기
texts = LANG_TEXT[language_choice]

# 헤더
st.markdown(texts["header"], unsafe_allow_html=True)
st.markdown(f"**Date:** {datetime.utcnow().strftime('%B %d, %Y %H:%M UTC')}", unsafe_allow_html=True)
st.markdown(texts["executive_summary"], unsafe_allow_html=True)

# 하위 섹터 매핑
if industry_choice != "All":
    subsector_mapping = INDUSTRY_SUBSECTORS.get(industry_choice, {})
else:
    subsector_mapping = None

# ─── 분석 실행 ─────────────────────────
with st.spinner("Analyzing news..."):
    result = analyze_topic(
        topic_choice,
        country=country_choice,
        industry=industry_choice,
        subsector_mapping=subsector_mapping,
        language=language_choice
    )

# 1) 감정 분포 차트
st.markdown(texts["sentiment_chart"], unsafe_allow_html=True)
draw_sentiment_chart(result["sentiment_counts"], WISERBOND_COLOR)

# 2) 긍정 / 부정 뉴스 섹션
st.markdown(texts["positive_title"], unsafe_allow_html=True)
if result["positive_news"]:
    display_news_section(result["positive_news"])
else:
    st.info("No positive news found.")

st.markdown(texts["negative_title"], unsafe_allow_html=True)
if result["negative_news"]:
    display_news_section(result["negative_news"])
else:
    st.info("No negative news found.")

# 3) 섹터별 임팩트 요약
st.markdown("### 🏭 Sector Impact Summary")
if result.get("impact_summary"):
    for imp in result["impact_summary"]:
        st.markdown(f"**{imp['sector']}**: {imp['impact']} (Source: {imp['source']})")
else:
    st.info("No sector impact detected.")

# 4) 전문가 해석
st.markdown(texts["expert_insight"], unsafe_allow_html=True)
st.markdown(f"✅ { result['expert_summary'].get('positive_summary', '') }")
st.markdown(f"❗ { result['expert_summary'].get('negative_summary', '') }")

st.markdown("---")
st.markdown(texts["footer"], unsafe_allow_html=True)
