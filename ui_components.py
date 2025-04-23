
# ui_components.py
import streamlit as st

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
