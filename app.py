import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from core import analyze_topic
from config import LANG_TEXT, INDUSTRY_KEYWORDS, COUNTRY_LIST
from news_sentiment_tool_demo import TOPIC_SETTINGS

st.set_page_config(page_title="Wiserbond News Sentiment Report", layout="wide")

st.sidebar.title("🔍 Analysis Settings")
topic_choice = st.sidebar.selectbox("Topic", list(TOPIC_SETTINGS.keys()))
country_choice = st.sidebar.selectbox("Country", COUNTRY_LIST)
industry_choice = st.sidebar.selectbox("Industry", ["All"] + list(INDUSTRY_KEYWORDS.keys()))
language_choice = st.sidebar.selectbox("Language", list(LANG_TEXT.keys()))
st.session_state["language"] = language_choice

with st.spinner("Running sentiment and summary analysis..."):
    result = analyze_topic(topic_choice, industry_choice, country_choice)

executive_summary = result["executive_summary"]
sentiment_counts = result["sentiment_counts"]
impact_summary = result["impact_summary"]
expert_summary = result["expert_summary"]
analysis_date = datetime.now().strftime("%B %d, %Y %H:%M")

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

st.markdown("### 3. Sector Impact Breakdown")
for item in impact_summary:
    st.markdown(f"- **{item['sector']}**: {item['impact']}")

st.markdown("### 4. Wiserbond Interpretation")
st.success(expert_summary)

st.markdown("### 5. Analysis Settings")
st.write(f"- **Topic:** {topic_choice}")
st.write(f"- **Country:** {country_choice}")
st.write(f"- **Industry:** {industry_choice}")
st.write(f"- **Language:** {language_choice}")

st.markdown("---")
st.markdown("*This report layout is optimized for professional printing and PDF export.*")
