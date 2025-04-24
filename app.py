# app.py
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from core import analyze_topic
from config import LANG_TEXT, INDUSTRY_KEYWORDS, COUNTRY_LIST
from news_sentiment_tool_demo import TOPIC_SETTINGS

# Page Setup
st.set_page_config(page_title="Wiserbond News Sentiment Report", layout="wide")

# Sidebar - Input Controls
st.sidebar.title("🔍 Analysis Settings")
topic_choice = st.sidebar.selectbox("Topic", list(TOPIC_SETTINGS.keys()))
country_choice = st.sidebar.selectbox("Country", COUNTRY_LIST)
industry_choice = st.sidebar.selectbox("Industry", ["All"] + list(INDUSTRY_KEYWORDS.keys()))
language_choice = st.sidebar.selectbox("Language", list(LANG_TEXT.keys()))
st.session_state["language"] = language_choice  # UI only

# Run analysis
with st.spinner("Running sentiment and summary analysis..."):
    result = analyze_topic(topic_choice, industry_choice, country_choice)

# Extract result variables
summary_text = result["summary"]
sentiment_counts = result["sentiment_counts"]
top_articles = result["top_articles"]
expert_comment = result["expert_comment"]
analysis_date = datetime.now().strftime("%B %d, %Y %H:%M")

# Style for print compatibility
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

# Report Header
st.markdown("## Wiserbond News Synthesizer V2 – Sentiment & Summary Report")
st.write(f"**Date:** {analysis_date}")
st.write("---")

# Section 1 - Executive Summary
st.markdown("### 1. Executive Summary")
st.info(summary_text)

# Section 2 - Sentiment Breakdown
st.markdown("### 2. Sentiment Breakdown")
fig, ax = plt.subplots(figsize=(5, 1.5))
colors = ['#4caf50', '#ffc107', '#f44336']  # Green, Yellow, Red
ax.bar(sentiment_counts.keys(), sentiment_counts.values(), color=colors)
ax.set_ylabel("Article Count")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
st.pyplot(fig)

# Section 3 - Top News Summaries
st.markdown("### 3. Top News Highlights")
for idx, art in enumerate(top_articles, 1):
    with st.expander(f"{idx}. {art['title']}"):
        st.write(art["summary"])
        st.markdown(f"[Read full article]({art['url']})")

# Section 4 - Expert Interpretation
st.markdown("### 4. Expert Insight")
st.success(expert_comment)

# Section 5 - Analysis Settings
st.markdown("### 5. Analysis Details")
st.write(f"- **Topic:** {topic_choice}")
st.write(f"- **Country:** {country_choice}")
st.write(f"- **Industry:** {industry_choice}")
st.write(f"- **Language:** {language_choice}")

# Footer
st.markdown("---")
st.markdown("*This report layout is optimized for professional printing and PDF export.*")
