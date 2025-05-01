import streamlit as st
from datetime import datetime

from core import analyze_topic
from config import TOPIC_SETTINGS, COUNTRY_LIST, INDUSTRY_SUBSECTORS, LANG_TEXT
from ui_components import draw_sentiment_chart, display_news_section

WISERBOND_COLOR = "#051F5B"

# 앱 설정
st.set_page_config(page_title="Wiserbond News Sentiment Report", layout="wide")

# 사이드바 설정
st.sidebar.title("🔍 Select Analysis Settings")
topic_choice = st.sidebar.selectbox("Topic", list(TOPIC_SETTINGS.keys()))
country_choice = st.sidebar.selectbox("Country", COUNTRY_LIST)
industry_choice = st.sidebar.selectbox("Industry", ["All"] + list(INDUSTRY_SUBSECTORS.keys()))
language_choice = st.sidebar.selectbox("Language", list(LANG_TEXT.keys()))
st.session_state["language"] = language_choice

# 실행 버튼
if st.sidebar.button("Run Analysis"):
    with st.spinner("Running sentiment and summary analysis..."):
        result = analyze_topic(topic_choice, country=country_choice, industry=industry_choice, language=language_choice)

    st.session_state["result"] = result
    st.session_state["timestamp"] = datetime.now().strftime("%B %d, %Y %H:%M")
    st.session_state["topic_choice"] = topic_choice
    st.session_state["country_choice"] = country_choice
    st.session_state["industry_choice"] = industry_choice

# 결과 렌더링
if "result" in st.session_state:
    result = st.session_state["result"]
    lang = st.session_state["language"]
    txt = LANG_TEXT[lang]

    executive_summary = result["executive_summary"]
    sentiment_counts = result["sentiment_counts"]
    impact_summary = result["impact_summary"]
    expert_summary = result["expert_summary"]
    sector_sentiment_scores = result["sector_sentiment_scores"]
    pos_news = result["positive_news"]
    neg_news = result["negative_news"]
    timestamp = st.session_state["timestamp"]
    selected_industry = st.session_state["industry_choice"]

    # 스타일 적용
    st.markdown(f"""
    <style>
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

    st.markdown(txt["header"])
    st.write(f"**Date:** {timestamp}")
    st.markdown(
        f"<small>Topic: {st.session_state['topic_choice']} | Country: {st.session_state['country_choice']} | Industry: {selected_industry}</small>",
        unsafe_allow_html=True
    )
    st.write("---")

    # Executive Summary
    st.markdown(txt["executive_summary"])
    st.info(executive_summary)

    # Sector Sentiment Chart
    st.markdown(txt["sentiment_chart"])
    if sector_sentiment_scores:
        draw_sentiment_chart(sector_sentiment_scores, selected_industry)
    else:
        st.warning("No sector sentiment data available.")

    # Sector Impact Breakdown
    st.markdown("## 🏭 Sector Impact Breakdown")
    if impact_summary:
        for item in impact_summary:
            sector = item.get('sector', 'Unknown Sector')
            impact = item.get('impact', 'No summary available')
            source = item.get('source', 'Unknown')
            st.markdown(f"- **{sector}**: {impact} ({source})", unsafe_allow_html=True)
    else:
        st.info("No sector impact summaries available.")

    # Expert Interpretation
    st.markdown(txt["expert_insight"])
    st.markdown(txt["positive_title"])
    st.success(expert_summary.get("positive_summary", "No positive insights found."))
    st.markdown(txt["negative_title"])
    st.warning(expert_summary.get("negative_summary", "No negative insights found."))

    # 뉴스 원문 섹션 (요약된 기사)
    st.markdown("## 📰 Sample Articles (Top-ranked by sentiment score)")
    display_news_section("Positive", pos_news)
    display_news_section("Negative", neg_news)

    # Footer
    st.markdown(txt["footer"], unsafe_allow_html=True)
