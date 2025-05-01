import streamlit as st
import plotly.express as px
import pandas as pd
from config import INDUSTRY_SUBSECTORS

WISERBOND_COLOR = "#051F5B"

def display_news_section(label, news_list, max_visible=3):
    if not news_list:
        st.markdown(f"_No {label.lower()} news found._")
        return

    sorted_news = sorted(news_list, key=lambda x: x.get("score", 0), reverse=True)
    visible = sorted_news[:max_visible]
    hidden = sorted_news[max_visible:]

    for news in visible:
        st.markdown(f"**Source:** {news['source']}")
        st.markdown(f"**Title:** {news['title']}")
        st.markdown(f"**Summary:** {news['description']}")
        st.write("---")

    if hidden:
        with st.expander(f"View more {label.lower()} news"):
            for news in hidden:
                st.markdown(f"**Source:** {news['source']}")
                st.markdown(f"**Title:** {news['title']}")
                st.markdown(f"**Summary:** {news['description']}")
                st.write("---")


def draw_sentiment_chart(sector_sentiment_scores, selected_industry="All"):
    if selected_industry != "All":
        sectors = list(INDUSTRY_SUBSECTORS.get(selected_industry, {}).keys())
        scores = [sector_sentiment_scores.get(sec, 0.0) for sec in sectors]
    else:
        sectors = list(sector_sentiment_scores.keys())
        scores = list(sector_sentiment_scores.values())

    if not sectors:
        st.write("No sector sentiment scores to visualize.")
        return

    df = pd.DataFrame({
        "Sector": sectors,
        "Sentiment": scores
    })

    fig = px.bar(
        df,
        y="Sector",
        x="Sentiment",
        orientation="h",
        color="Sentiment",
        color_continuous_scale=["#ef6c6c", "#b8b8b8", "#6cadef"],
        range_x=[0, 1],
        title="Sector Sentiment Overview"
    )

    fig.add_vline(
        x=0.5,
        line_dash="dash",
        line_color="gray",
        annotation_text="Neutral",
        annotation_position="top right"
    )

    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)
