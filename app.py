import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
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
    
    # 2. Sector Sentiment Spectrum (Gradient Bar with Sector Points)
    st.markdown("### 4. Sector Sentiment Spectrum")

    sentiment_map = {"NEGATIVE": 0.0, "NEUTRAL": 0.5, "POSITIVE": 1.0}
    all_scores = [sentiment_map.get(a["sentiment"], 0.5) for a in result["positive_news"] + result["negative_news"]]
    overall_score = sum(all_scores) / len(all_scores)

    fig, ax = plt.subplots(figsize=(7, 1.5), dpi=120)
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    ax.imshow(gradient, aspect='auto', cmap=cm.coolwarm, extent=[0, 1, -0.18, 0.18], alpha=0.25)
    ax.hlines(0, 0, 1, colors="#bbb", linestyles="solid", linewidth=10, zorder=0)
    ax.plot(overall_score, 0, marker="s", color="black", markersize=14, label="Overall", zorder=2)

    sector_colors = cm.Blues(np.linspace(0.5, 0.95, len(sector_sentiment_scores)))
    for i, (sector, score) in enumerate(sector_sentiment_scores.items()):
        ax.plot(score, 0, marker="o", color=sector_colors[i], markersize=10, zorder=3)
        y_offset = 0.24 if i % 2 == 0 else -0.28
        ax.text(score, y_offset, sector, fontsize=9, ha="center", va="bottom" if y_offset > 0 else "top",
                fontweight="medium", color=sector_colors[i])

    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.4, 0.4)
    ax.set_xticks([0.0, 0.5, 1.0])
    ax.set_xticklabels(["Negative", "Neutral", "Positive"], fontsize=10, fontweight="bold")
    ax.set_yticks([])
    for spine in ["top", "right", "left", "bottom"]:
        ax.spines[spine].set_visible(False)

    ax.legend(["Overall Sentiment"], loc="upper right", frameon=False, fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)
    # 3. Sector Impact Breakdown with source
    st.markdown("### 2. Sector Impact Breakdown")
    for item in impact_summary:
        sector = item['sector']
        impact = item['impact']
        source = item.get('source', 'Unknown')
        st.markdown(f"- **{sector}**: {impact} (Source: {source})")

    # 4. Wiserbond Interpretation
    st.markdown("### 3. Wiserbond Interpretation")
    st.success(expert_summary)

   

    st.markdown("---")
    st.markdown("*This report layout is optimized for professional printing and PDF export.*")
