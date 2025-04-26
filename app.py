import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from core import analyze_topic
from config import LANG_TEXT, INDUSTRY_KEYWORDS, COUNTRY_LIST
from news_sentiment_tool_demo import TOPIC_SETTINGS

st.set_page_config(page_title="Wiserbond News Sentiment Report", layout="wide")

# Sidebar
st.sidebar.title("🔍 Analysis Settings")
topic_choice = st.sidebar.selectbox("Topic", list(TOPIC_SETTINGS.keys()))
country_choice = st.sidebar.selectbox("Country", COUNTRY_LIST)
industry_choice = st.sidebar.selectbox("Industry", ["All"] + list(INDUSTRY_KEYWORDS.keys()))
language_choice = st.sidebar.selectbox("Language", list(LANG_TEXT.keys()))
st.session_state["language"] = language_choice

# Run analysis
if st.sidebar.button("Run Analysis"):
    with st.spinner("Running sentiment and summary analysis..."):
        result = analyze_topic(topic_choice, industry_choice, country_choice)

    st.session_state["result"] = result
    st.session_state["timestamp"] = datetime.now().strftime("%B %d, %Y %H:%M")
    st.session_state["topic_choice"] = topic_choice
    st.session_state["country_choice"] = country_choice
    st.session_state["industry_choice"] = industry_choice

# Show result
if "result" in st.session_state:
    result = st.session_state["result"]
    executive_summary = result["executive_summary"]
    sentiment_counts = result["sentiment_counts"]
    impact_summary = result["impact_summary"]
    expert_summary = result["expert_summary"]
    analysis_date = st.session_state["timestamp"]

    st.markdown("## Wiserbond News Synthesizer V2 – Sentiment & Summary Report")
    st.write(f"**Date:** {analysis_date}")
    st.write("---")

    st.markdown("### 1. Executive Summary")
    st.info(executive_summary)

    st.markdown("### 2. Sentiment Breakdown")
    fig, ax = plt.subplots(figsize=(5, 1.5))
    colors = ['#4caf50', '#ffc107', '#f44336']
    ax.bar(sentiment_counts.keys(), sentiment_counts.values(), color=colors)
    ax.set_ylabel("Article Count")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    st.pyplot(fig)

    # 📊 2-1. Sector Sentiment Spectrum Chart
    if "sector_sentiment_scores" in result:
        st.markdown("### 2. Sector Sentiment Spectrum")

        sector_scores = result["sector_sentiment_scores"]
        overall_sentiment = sum(sector_scores.values()) / len(sector_scores) if sector_scores else 0

        sector_names = list(sector_scores.keys())
        scores = list(sector_scores.values())
        colors = [
            "#D3D3D3" if s == 0 else
            "#ADD8E6" if s > 0 else
            "#F08080" for s in scores
        ]

        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.barh(sector_names, scores, color=colors)
        ax.axvline(0, color="gray", linestyle="--", linewidth=1)
        ax.axvline(overall_sentiment, color="#051F5B", linewidth=2, label="Overall Sentiment")
        ax.set_xlim(-1, 1)
        ax.set_xlabel("Sentiment")
        ax.set_title("2. Sector Sentiment Spectrum")
        ax.legend()
        ax.invert_yaxis()
        st.pyplot(fig)

    st.markdown("### 3. Sector Impact Breakdown")
    for item in impact_summary:
        st.markdown(f"- **{item['sector']}**: {item['impact']}")

    st.markdown("### 4. Wiserbond Interpretation")
    st.success(expert_summary)

    st.markdown("### 5. Analysis Settings")
    st.write(f"- **Topic:** {st.session_state['topic_choice']}")
    st.write(f"- **Country:** {st.session_state['country_choice']}")
    st.write(f"- **Industry:** {st.session_state['industry_choice']}")
    st.write(f"- **Language:** {language_choice}")

    st.markdown("---")
    st.markdown("*This report layout is optimized for professional printing and PDF export.*")
