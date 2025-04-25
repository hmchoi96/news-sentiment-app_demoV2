# app.py
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from core import analyze_topic
from config import LANG_TEXT, INDUSTRY_KEYWORDS, COUNTRY_LIST
from news_sentiment_tool_demo import TOPIC_SETTINGS

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
        result = analyze_topic(topic_choice, industry_choice, country_choice)

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
    analysis_date = st.session_state["timestamp"]

    # sector_sentiment_scores가 result에 있는지 확인
    if "sector_sentiment_scores" in result:
        sector_sentiment_scores = result["sector_sentiment_scores"]
    else:
        sector_sentiment_scores = {}

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
    st.markdown("## Wiserbond News Synthesizer V2 – Sentiment & Summary Report")
    st.write(f"**Date:** {analysis_date}")
    st.markdown(
        f"<small>Topic: {st.session_state['topic_choice']} | Country: {st.session_state['country_choice']} | Industry: {st.session_state['industry_choice']}</small>",
        unsafe_allow_html=True
    )
    st.write("---")

    # 1. Executive Summary
    st.markdown("### 1. Executive Summary")
    if executive_summary:
        st.info(executive_summary)
    else:
        st.warning("Executive summary not available. Please try again with different settings.")

    # 2. Sector Sentiment Spectrum
    st.markdown("### 2. Sector Sentiment Spectrum")
    col1, col2, col3 = st.columns([1, 7, 1])
    with col2:
        sentiment_map = {"NEGATIVE": 0.0, "NEUTRAL": 0.5, "POSITIVE": 1.0}
        all_scores = [sentiment_map.get(a["sentiment"], 0.5) for a in result["positive_news"] + result["negative_news"]]

        # all_scores가 비어 있는지 확인
        if len(all_scores) > 0:
            overall_score = sum(all_scores) / len(all_scores)
        else:
            overall_score = 0.5  # 또는 다른 기본값 설정

        fig, ax = plt.subplots(figsize=(6.5, 1.5), dpi=100)

        # 감정 바
        ax.hlines(0, 0, 1, colors="#bbb", linewidth=12, zorder=1)

        # 바 양 끝 심볼
        ax.text(0, 0.05, "-", fontsize=16, ha="center", va="bottom", color=WISERBOND_COLOR)
        ax.text(1, 0.05, "+", fontsize=16, ha="center", va="bottom", color=WISERBOND_COLOR)

        # 전체 평균 표시 (■)
        ax.plot(overall_score, 0, marker="s", color=WISERBOND_COLOR, markersize=12, zorder=3)

        # 섹터 마커와 45도 라벨
        if "sector_sentiment_scores" in result and result["sector_sentiment_scores"]:
            sectors_sorted = sorted(sector_sentiment_scores.items(), key=lambda x: x[1])
            for sector, score in sectors_sorted:
                ax.plot(score, 0, marker="o", color=WISERBOND_COLOR, markersize=8, zorder=2)
                ax.text(score, -0.22, sector, rotation=45, fontsize=8,
                        ha="right", va="top", color=WISERBOND_COLOR)

        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.5, 0.4)
        ax.axis("off")
        plt.tight_layout()
        st.pyplot(fig)

    else:
        st.info("Sector Sentiment Spectrum not available. Showing the overall sentiment instead.")  # subsector가 없으면
        #산업별 분석 결과를 대신 보여주기
        sentiment_map = {"NEGATIVE": 0.0, "NEUTRAL": 0.5, "POSITIVE": 1.0}
        all_scores = [sentiment_map.get(a["sentiment"], 0.5) for a in result["positive_news"] + result["negative_news"]]
        # all_scores가 비어 있는지 확인
        if len(all_scores) > 0:
            overall_score = sum(all_scores) / len(all_scores)
        else:
            overall_score = 0.5  # 또는 다른 기본값 설정
        fig, ax = plt.subplots(figsize=(6.5, 1.5), dpi=100)

        # 감정 바
        ax.hlines(0, 0, 1, colors="#bbb", linewidth=12, zorder=1)

        # 바 양 끝 심볼
        ax.text(0, 0.05, "-", fontsize=16, ha="center", va="bottom", color=WISERBOND_COLOR)
        ax.text(1, 0.05, "+", fontsize=16, ha="center", va="bottom", color=WISERBOND_COLOR)

        # 전체 평균 표시 (■)
        ax.plot(overall_score, 0, marker="s", color=WISERBOND_COLOR, markersize=12, zorder=3)

        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.5, 0.4)
        ax.axis("off")
        plt.tight_layout()
        st.pyplot(fig)

    # 3. Sector Impact Breakdown
    st.markdown("### 3. Sector Impact Breakdown")
    if impact_summary:
        for item in impact_summary:
            sector = item['sector']
            impact = item['impact']
            source = item.get('source', 'Unknown')
            st.markdown(f"- **{sector}**: {impact} ({source})", unsafe_allow_html=True)
    else:
        st.info("Sector Impact Breakdown not available. Insufficient data.")

    # 4. Wiserbond Interpretation
    st.markdown("### 4. Wiserbond Interpretation")
    if expert_summary:
        st.success(expert_summary)
    else:
        st.info("Wiserbond Interpretation not available. Please try again with different settings.")

    st.markdown("---")
    st.markdown("*This report layout is optimized for professional printing and PDF export.*")
