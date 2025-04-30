import streamlit as st
from config import LANG_TEXT, COUNTRY_LIST, INDUSTRY_KEYWORDS
from news_sentiment_tool_demo import TOPIC_SETTINGS
from core import analyze_topic
from ui_components import display_news_section, draw_sentiment_chart

st.set_page_config(page_title="Wiserbond News Sentiment Report", layout="wide")

# 사이드바
st.sidebar.title("🔍 Analysis Settings")
topic_choice = st.sidebar.selectbox("Topic", list(TOPIC_SETTINGS.keys()))
country_choice = st.sidebar.selectbox("Country", ["Global"] + COUNTRY_LIST)
industry_choice = st.sidebar.selectbox("Industry", ["All"] + list(INDUSTRY_KEYWORDS.keys()))
language_choice = st.sidebar.selectbox("Language", list(LANG_TEXT.keys()))

if st.sidebar.button("Run Analysis"):
    result = analyze_topic(
        topic_choice,
        country=country_choice,
        industry=industry_choice,
        language=language_choice
    )
    texts = LANG_TEXT[language_choice]

    st.markdown(texts["header"])
    st.markdown(
        f"<small>Date: {result['timestamp']} | "
        f"Topic: {topic_choice} | Country: {country_choice} | Industry: {industry_choice}</small>",
        unsafe_allow_html=True
    )
    st.markdown(f"**{result['executive_summary']}**")

    # 1. Sentiment Distribution
    st.markdown(texts["sentiment_chart"])
    draw_sentiment_chart(result["sector_sentiment_scores"])

    # 2. Positive vs Negative Coverage
    st.markdown(texts["positive_title"])
    display_news_section("Positive News", result["positive_news"])
    st.markdown(texts["negative_title"])
    display_news_section("Negative News", result["negative_news"])

    # 3. Sector Impact
    if result["impact_summary"]:
        st.markdown("### Sector Impact")
        for item in result["impact_summary"]:
            st.markdown(f"- **{item['sector']}**: {item['impact']}")

    # 4. Expert Insights
    st.markdown(texts["expert_insight"])
    st.success(result["expert_summary"]["positive_summary"])
    st.warning(result["expert_summary"]["negative_summary"])

    st.markdown(texts["footer"], unsafe_allow_html=True)
else:
    st.markdown("### Configure parameters and click **Run Analysis**")
