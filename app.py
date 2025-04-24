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

# 분석 결과 표시
if "result" in st.session_state:
    result = st.session_state["result"]
    executive_summary = result["executive_summary"]
    sentiment_counts = result["sentiment_counts"]
    impact_summary = result["impact_summary"]
    expert_summary = result["expert_summary"]
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
    st.write("---")

    # 1. Executive Summary
    st.markdown("### 1. Executive Summary")
    st.info(executive_summary)

    # 2. Sentiment Breakdown
    st.markdown("### 2. Sentiment Breakdown")
    fig, ax = plt.subplots(figsize=(5, 1.5))
    colors = ['#4caf50', '#ffc107', '#f44336']
    ax.bar(sentiment_counts.keys(), sentiment_counts.values(), color=colors)
    ax.set_ylabel("Article Count")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    st.pyplot(fig)

    # 3. Sector Impact Breakdown
    st.markdown("### 3. Sector Impact Breakdown")
    for item in impact_summary:
        st.markdown(f"- **{item['sector']}**: {item['impact']}")

    # 4. Wiserbond Interpretation
    st.markdown("### 4. Wiserbond Interpretation")
    st.success(expert_summary)

    # 5. 분석 조건 요약
    st.markdown("### 5. Analysis Settings")
    st.write(f"- **Topic:** {topic_choice}")
    st.write(f"- **Country:** {country_choice}")
    st.write(f"- **Industry:** {industry_choice}")
    st.write(f"- **Language:** {language_choice}")

    st.markdown("---")
    st.markdown("*This report layout is optimized for professional printing and PDF export.*")
