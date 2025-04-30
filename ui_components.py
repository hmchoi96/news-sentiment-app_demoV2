# ui_components.py
import streamlit as st
import matplotlib.pyplot as plt

def display_news_section(news_list, max_visible=3):
    """뉴스 리스트와 AI 요약 표시"""
    sorted_news = sorted(news_list, key=lambda x: x.get("score",0), reverse=True)
    visible = sorted_news[:max_visible]
    hidden  = sorted_news[max_visible:]

    for idx, art in enumerate(visible,1):
        st.markdown(f"**{idx}. {art['title']}**")
        st.write(art.get("description",""))
        st.markdown(f"*Source: {art.get('source','Unknown')}*")
        if art.get("ai_summary"):
            st.markdown(f"*AI Summary:* {art['ai_summary']}")
        st.markdown("---")

    if hidden:
        if st.button(f"Show {len(hidden)} more"):
            for art in hidden:
                st.markdown(f"**• {art['title']}**")
                st.write(art.get("description",""))
                st.markdown(f"*Source: {art.get('source','Unknown')}*")
                if art.get("ai_summary"):
                    st.markdown(f"*AI Summary:* {art['ai_summary']}")
                st.markdown("---")

def draw_sentiment_chart(counts, color):
    """감정 분포 차트 그리기"""
    labels = list(counts.keys())
    values = [counts[lbl] for lbl in labels]
    fig, ax = plt.subplots()
    ax.bar(labels, values, color=color)
    ax.set_ylabel("Count")
    ax.set_title("Sentiment Distribution")
    st.pyplot(fig)
