import streamlit as st
import numpy as np
from datetime import datetime

from core import analyze_topic
from config import TOPIC_SETTINGS, LANG_TEXT, COUNTRY_LIST, INDUSTRY_SUBSECTORS
from ui_components import display_news_section, draw_sentiment_chart

WISERBOND_COLOR = "#051F5B"

st.set_page_config(page_title="Wiserbond News Sentiment Report", layout="wide")

st.sidebar.title("🔍 Analysis Settings")
topic_choice = st.sidebar.selectbox("Topic", list(TOPIC_SETTINGS.keys()))
country_choice = st.sidebar.selectbox("Country", COUNTRY_LIST)
industry_choice = st.sidebar.selectbox("Industry", ["All"] + list(INDUSTRY_SUBSECTORS.keys()))
language_choice = st.sidebar.selectbox("Language", list(LANG_TEXT.keys()))
st.session_state["language"] = language_choice

if st.sidebar.button("Run Analysis"):
    try:
        with st.spinner("Running sentiment and summary analysis..."):
            result = analyze_topic(topic_choice, country=country_choice, industry=industry_choice, language=language_choice)

        st.session_state["result"] = result
        st.session_state["timestamp"] = datetime.now().strftime("%B %d, %Y %H:%M")
        st.session_state["topic_choice"] = topic_choice
        st.session_state["country_choice"] = country_choice
        st.session_state["industry_choice"] = industry_choice

    except Exception as e:
        st.error(f"❌ 오류 발생: {e}")

if "result" in st.session_state:
    result = st.session_state["result"]
    executive_summary = result["executive_summary"]
    sentiment_counts = result["sentiment_counts"]
    impact_summary = result["impact_summary"]
    expert_summary = result["expert_summary"]
    sector_sentiment_scores = result["sector_sentiment_scores"]
    analysis_date = st.session_state["timestamp"]
    selected_industry = st.session_state["industry_choice"]

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
        body {{ zoom: 90%; width: 100%; }}
        .element-container {{ page-break-inside: avoid; }}
        h2 {{ font-size: 20pt; margin-top: 30px; }}
        h3 {{ font-size: 16pt; margin-top: 20px; }}
        p, li, span, div {{ font-size: 10pt; }}
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("## 📊 Wiserbond News Synthesizer V2 – Sentiment & Summary Report")
    st.write(f"**Date:** {analysis_date}")
    st.markdown(
        f"<small>Topic: {st.session_state['topic_choice']} | Country: {st.session_state['country_choice']} | Industry: {selected_industry}</small>",
        unsafe_allow_html=True
    )
    st.write("---")

    st.markdown("### 1. Executive Summary")
    st.info(executive_summary)

    st.markdown("### 2. Sector Sentiment Spectrum")
    if sector_sentiment_scores:
        col1, col2, col3 = st.columns([1, 8, 1])
        with col2:
            draw_sentiment_chart(sector_sentiment_scores, selected_industry)
    else:
        st.warning("No sector sentiment data available.")

    st.markdown("### 3. Sector Impact Breakdown")
    if impact_summary:
        for item in impact_summary:
            sector = item.get('sector', 'Unknown Sector')
            impact = item.get('impact', 'No summary available')
            source = item.get('source', 'Unknown')
            article_count = item.get('article_count', 'n')
            st.markdown(f"- **{sector}**: {impact} ({source}, {article_count}개 기사 기반)", unsafe_allow_html=True)
    else:
        st.info("No sector impact summaries available.")


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
