
# ui_components.py
import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter

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

def draw_sentiment_chart(articles):
    total = len(articles)
    if total == 0:
        st.write("No articles to visualize.")
        return
    counts = Counter([a['sentiment'] for a in articles])
    labels = ['NEGATIVE', 'NEUTRAL', 'POSITIVE']
    colors = ['#d9534f', '#f7f1f1', '#bfaeff']
    values = [counts.get(label, 0) / total * 100 for label in labels]

    plt.figure(figsize=(8, 1.2))
    plt.barh(['Sentiment'], values, color=colors, edgecolor='black', height=0.4,
             left=[0, values[0], values[0]+values[1]])
    for i, (v, label) in enumerate(zip(values, labels)):
        if v > 0:
            plt.text(sum(values[:i]) + v/2, 0, f"{label.title()} {int(v)}%", va='center', ha='center', fontsize=9)
    plt.axis('off')
    plt.title("Sentiment Breakdown")
    st.pyplot(plt)
