import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

from core import analyze_topic
from config import LANG_TEXT, INDUSTRY_KEYWORDS, COUNTRY_LIST
from news_sentiment_tool_demo import TOPIC_SETTINGS
from ui_components import display_news_section, draw_sentiment_chart

WISERBOND_COLOR = "#051F5B"

# 페이지 설정
st.set_page_config(page_title="Wiserbond News Sentiment Report", layout="wide")

# 사이드바 입력값 설정
st.sidebar.title("🔍 Analysis Settings")
topic_choice = st.sidebar.selectbox("Topic", list(TOPIC_SETTINGS.keys()))
country_choice = st.sidebar.selectbox("Country", COUNTRY_LIST)
industry_choice = st.sidebar.selectbox("Industry", ["All"] + list(INDUSTRY_KEYWORDS.keys()))
language_choice = st.sidebar.selectbox("Language", list(LANG_TEXT.keys()))
st.session_state["language"] = language_choice

# 분석 실행
if st.sidebar.button("Run Analysis"):
    with st.spinner("Running sentiment and summary analysis..."):
        # 수정: 파라미터 순서 (topic, country, industry, language)
        result = analyze_topic(topic_choice, country=country_choice, industry=industry_choice, language=language_choice)

    # 세션에 저장
    st.session_state["result"] = result
    st.session_state["timestamp"] = datetime.now().strftime("%B %d, %Y %H:%M")
    st.session_state["topic_choice"] = topic_choice
    st.session_state["country_choice"] = country_choice
    st.session_state["industry_choice"] = industry_choice

# 결과 표시
if "result" in st.session_state:
    result = st.session_state["result"]
    executive_summary = result["executive_summary"]
    sentiment_counts = result["sentiment_counts"]
    impact_summary = result["impact_summary"]
    expert_summary = result["expert_summary"]
    sector_sentiment_scores = result["sector_sentiment_scores"]
    analysis_date = st.session_state["timestamp"]

    # 스타일
    st.markdown(f"""
    <style>
    body {{
        font-family: 'Segoe UI', sans-serif;
        font-size: 0.95rem;
        line-height: 1.6;
        margin: 0 auto;
        padding: 0 1.5rem;
    }}
    h2, h3 {{
        color: {WISERBOND_COLOR};
    }}
    @media print {{
        .element-container {{ page-break-inside: avoid; }}
    }}
    </style>
    """, unsafe_allow_html=True)

    # 보고서 헤더
    st.markdown("## 📊 Wiserbond News Synthesizer V2 – Sentiment & Summary Report")
    st.write(f"**Date:** {analysis_date}")
    st.markdown(
        f"<small>Topic: {st.session_state['topic_choice']} | Country: {st.session_state['country_choice']} | Industry: {st.session_state['industry_choice']}</small>",
        unsafe_allow_html=True
    )
    st.write("---")

    # 1. Executive Summary
    st.markdown("### 1. Executive Summary")
    st.info(executive_summary)

    # 2. Sector Sentiment Spectrum (Bar Chart)
    st.markdown("### 2. Sector Sentiment Spectrum")
    if sector_sentiment_scores:
        col1, col2, col3 = st.columns([1, 8, 1])
        with col2:
            draw_sentiment_chart(sector_sentiment_scores)

    else:
        st.warning("No sector sentiment data available.")

    # 3. Sector Impact Breakdown
    st.markdown("### 3. Sector Impact Breakdown")
    if impact_summary:
        for item in impact_summary:
            sector = item.get('sector', 'Unknown Sector')
            impact = item.get('impact', 'No summary available')
            source = item.get('source', 'Unknown')
            st.markdown(f"- **{sector}**: {impact} ({source})", unsafe_allow_html=True)
    else:
        st.info("No sector impact summaries available.")

    # 4. Wiserbond Interpretation
# 4. Wiserbond Interpretation
    st.markdown("### 4. Wiserbond Interpretation")
    if expert_summary:
        st.markdown("✅ **Positive Insight**")
        st.success(expert_summary.get('positive_summary', 'No positive insights found.'))
    
        st.markdown("❗ **Negative Insight**")
        st.warning(expert_summary.get('negative_summary', 'No negative insights found.'))
    else:
        st.info("No expert interpretation available.")


    st.markdown("---")
    st.markdown("*This report layout is optimized for professional printing and PDF export.*")
