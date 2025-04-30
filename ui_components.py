import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter

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
    """
    선택된 산업군 기준으로 섹터만 시각화. 
    해당 섹터가 없더라도 모두 0점으로 보여줌 (산업별 기준 적용).
    """
    from config import INDUSTRY_SUBSECTORS

    if selected_industry != "All":
        sectors = list(INDUSTRY_SUBSECTORS.get(selected_industry, {}).keys())
        scores = [sector_sentiment_scores.get(sec, 0.0) for sec in sectors]
    else:
        sectors = list(sector_sentiment_scores.keys())
        scores = list(sector_sentiment_scores.values())

    if not sectors:
        st.write("No sector sentiment scores to visualize.")
        return

    overall_score = sum(scores) / len(scores) if scores else 0.5
    colors = ['#ef6c6c' if s < 0.4 else '#6cadef' if s > 0.6 else '#b8b8b8' for s in scores]

    fig, ax = plt.subplots(figsize=(6, 2.4), dpi=100)
    ax.barh(sectors, scores, height=0.5, color=colors, alpha=0.8)
    ax.axvline(x=0.5, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=overall_score, color=WISERBOND_COLOR, linestyle='-', linewidth=2, label='Overall Sentiment')

    ax.set_xlim(0, 1)
    ax.set_xticks([0, 0.5, 1])
    ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(frameon=False, loc='lower right')
    plt.tight_layout()
    st.pyplot(fig)
