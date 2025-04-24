import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from core import analyze_topic
from config import LANG_TEXT, INDUSTRY_KEYWORDS, COUNTRY_LIST
from news_sentiment_tool_demo import TOPIC_SETTINGS

# 페이지 설정
st.set_page_config(page_title="Wiserbond News Sentiment Report", layout="wide")

# 사이드바 입력값 설정
st.sidebar.title("🔍 Analysis Settings")
topic_choice = st.sidebar.selectbox("Topic", list(TOPIC_SETTINGS.keys()))
country_choice = st.sidebar.selectbox("Country", COUNTRY_LIST)
industry_choice = st.sidebar.selectbox("Industry", ["All"] + list(INDUSTRY_KEYWORDS.keys()))
language_choice = st.sidebar.selectbox("Language", list(LANG_TEXT.keys()))
st.session_state["language"] = language_choice  # UI용으로만 사용

# 분석 실행 버튼
if st.sidebar.button("Run Analysis"):
    with st.spinner("Running sentiment and summary analysis..."):
        result = analyze_topic(topic_choice, industry_choice, country_choice)

    # 세션에 저장
    st.session_state["result"] = result
    st.session_state["timestamp"] = datetime.now().strftime("%B %d, %Y %H:%M")
    st.session_state["topic_choice"] = topic_choice
    st.session_state["country_choice"] = country_choice
    st.session_state["industry_choice"] = industry_choice

# 분석 결과 표시
if "result" in st.session_state:
    result = st.session_state["result"]
    executive_summary = result["executive_summary"]
    sentiment_counts = result["sentiment_counts"]
    impact_summary = result["impact_summary"]
    expert_summary = result["expert_summary"]
    sector_sentiment_scores = result["sector_sentiment_scores"]
    analysis_date = st.session_state["timestamp"]

    # 스타일 설정
    st.markdown("""
    <style>
    body {
        font-family: 'Segoe UI', sans-serif;
        font-size: 0.95rem;
        line-height: 1.6;
        margin: 0 auto;
        padding: 0 1.5rem;
    }
    .section-title { font-size:1.3em; font-weight:bold; margin-top:2em; }
    @media print {
        .element-container { page-break-inside: avoid; }
    }
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
    st.info(executive_summary)

    # 2. Sentiment Breakdown (더 작고 얇은 바 차트)
    st.markdown("### 2. Sentiment Breakdown")
    filtered_counts = {k: v for k, v in sentiment_counts.items() if k in ["Positive", "Negative"]}
    fig, ax = plt.subplots(figsize=(2.2, 0.9))
    ax.bar(filtered_counts.keys(), filtered_counts.values(), color=['#4caf50', '#f44336'])
    ax.set_ylabel("Articles", fontsize=8)
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    st.pyplot(fig)

    # 3. Sector Impact Breakdown with source
    st.markdown("### 3. Sector Impact Breakdown")
    for item in impact_summary:
        sector = item['sector']
        impact = item['impact']
        source = item.get('source', 'Unknown')
        st.markdown(f"- **{sector}**: {impact} (Source: {source})")

    # 4. Wiserbond Interpretation
    st.markdown("### 4. Wiserbond Interpretation")
    st.success(expert_summary)

    # 5. Sector Sentiment Spectrum Visualization
    st.markdown("### 5. Sector Sentiment Spectrum")
    fig, ax = plt.subplots(figsize=(6, 1.2))

    # 기본 스펙트럼 선
    ax.hlines(0, 0, 1, colors="#ccc", linestyles="solid", linewidth=8)

    # 전체 평균 감정 (■)
    sentiment_map = {"NEGATIVE": 0.0, "NEUTRAL": 0.5, "POSITIVE": 1.0}
    all_scores = [sentiment_map.get(a["sentiment"], 0.5) for a in result["positive_news"] + result["negative_news"]]
    overall_score = sum(all_scores) / len(all_scores)
    ax.plot(overall_score, 0, marker="s", color="black", markersize=8, label="Overall")

    # ▲ 섹터별 위치 표시 (위아래 교차)
    toggle = True
    for sector, score in sector_sentiment_scores.items():
        y = 0.25 if toggle else -0.25
        ax.plot(score, 0, marker="v", color="blue", markersize=6)
        ax.text(score, y, sector, fontsize=8, ha="center", va="bottom" if toggle else "top")
        toggle = not toggle

    # 축 정리
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.4, 0.4)
    ax.set_xticks([0.0, 0.5, 1.0])
    ax.set_xticklabels(["Negative", "Neutral", "Positive"], fontsize=8)
    ax.set_yticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)

    st.pyplot(fig)

    st.markdown("---")
    st.markdown("*This report layout is optimized for professional printing and PDF export.*")
