import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
WISERBOND_COLOR = "#051F5B"

def display_news_section(label, news_list, max_visible=3):
    if not news_list:
        st.markdown(f"_No {label.lower()} found._")
        return

    sorted_news = sorted(news_list, key=lambda x: x.get("score",0), reverse=True)
    visible, hidden = sorted_news[:max_visible], sorted_news[max_visible:]

    st.markdown(f"**{label}**")
    for n in visible:
        st.markdown(
            f"- **[{n['title']}]({n['url']})**  \n"
            f"  Source: {n['source']} | Score: {n['score']}  \n"
            f"  {n.get('description','')}"
        )

    if hidden:
        with st.expander(f"Show {len(hidden)} more"):
            for n in hidden:
                st.markdown(
                    f"- **[{n['title']}]({n['url']})**  \n"
                    f"  Source: {n['source']} | Score: {n['score']}  \n"
                    f"  {n.get('description','')}"
                )

def draw_sentiment_chart(scores: dict):
    if not scores:
        st.markdown("_No sentiment data available._")
        return
    sectors, values = list(scores.keys()), list(scores.values())
    overall = sum(values)/len(values) if values else 0.5

    fig, ax = plt.subplots()
    ax.barh(sectors, values, color=WISERBOND_COLOR, alpha=0.8)
    ax.axvline(0.5, linestyle="--", alpha=0.5)
    ax.axvline(overall, color=WISERBOND_COLOR, linewidth=2, label="Overall")
    ax.set_xlim(0,1)
    ax.xaxis.set_major_locator(FixedLocator([0,0.5,1]))
    ax.set_xlabel("Sentiment (0=Neg, 1=Pos)")
    ax.legend(frameon=False)
    plt.tight_layout()
    st.pyplot(fig)
