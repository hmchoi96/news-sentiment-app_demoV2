if st.sidebar.button("Run Analysis"):
    with st.spinner("Running sentiment and summary analysis..."):
        result = analyze_topic(topic_choice, industry_choice, country_choice)

    # Store result
    st.session_state["result"] = result
    st.session_state["timestamp"] = datetime.now().strftime("%B %d, %Y %H:%M")

# 결과가 있을 경우에만 화면 출력
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

    st.markdown("### 3. Sector Impact Breakdown")
    for item in impact_summary:
        st.markdown(f"- **{item['sector']}**: {item['impact']}")

    st.markdown("### 4. Wiserbond Interpretation")
    st.success(expert_summary)
