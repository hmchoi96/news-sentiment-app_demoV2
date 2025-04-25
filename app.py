# 결과 표시
if "result" in st.session_state:
    result = st.session_state["result"]
    executive_summary = result["executive_summary"]
    sentiment_counts = result["sentiment_counts"]
    impact_summary = result["impact_summary"]
    expert_summary = result["expert_summary"]
    analysis_date = st.session_state["timestamp"]

    # ✅ Subsector 점수 우선 사용
    subsector_scores = result.get("subsector_sentiment_scores", {})
    use_subsectors = bool(subsector_scores)

    st.markdown(f"## Wiserbond News Synthesizer V2 – Sentiment & Summary Report")
    st.write(f"**Date:** {analysis_date}")
    st.markdown(
        f"<small>Topic: {st.session_state['topic_choice']} | Country: {st.session_state['country_choice']} | Industry: {st.session_state['industry_choice']}</small>",
        unsafe_allow_html=True
    )
    st.write("---")

    # 1. Executive Summary
    st.markdown("### 1. Executive Summary")
    st.info(executive_summary)

    # 2. Sentiment Spectrum (Subsector or Sector)
    st.markdown("### 2. Sentiment Spectrum")
    col1, col2, col3 = st.columns([1, 8, 1])
    with col2:
        data_source = subsector_scores if use_subsectors else result["sector_sentiment_scores"]
        labels = list(data_source.keys())
        scores = list(data_source.values())
        overall_score = sum(scores) / len(scores) if scores else 0.5

        colors = ['#ef6c6c' if s < 0.4 else '#6cadef' if s > 0.6 else '#b8b8b8' for s in scores]

        fig, ax = plt.subplots(figsize=(6, 2.4 + len(labels) * 0.15), dpi=100)
        ax.barh(labels, scores, height=0.5, color=colors, alpha=0.8)

        ax.axvline(x=0.5, color='gray', linestyle='--', alpha=0.5)
        ax.axvline(x=overall_score, color=WISERBOND_COLOR, linestyle='-', linewidth=2, label='Overall Sentiment')

        ax.set_xlim(0, 1)
        ax.set_xticks([0, 0.5, 1])
        ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend(frameon=False, loc='upper right')
        plt.tight_layout()
        st.pyplot(fig)

    # 3. Sector Impact Breakdown
    st.markdown("### 3. Sector Impact Breakdown")
    for item in impact_summary:
        sector = item['sector']
        impact = item['impact']
        source = item.get('source', 'Unknown')
        st.markdown(f"- **{sector}**: {impact} ({source})", unsafe_allow_html=True)

    # 4. Wiserbond Interpretation
    st.markdown("### 4. Wiserbond Interpretation")
    st.success(expert_summary)

    st.markdown("---")
    st.markdown("*This report layout is optimized for professional printing and PDF export.*")
