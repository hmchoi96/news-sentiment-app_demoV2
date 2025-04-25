# 2. Sector Sentiment Spectrum
st.markdown("### 2. Sector Sentiment Spectrum")
col1, col2, col3 = st.columns([1, 7, 1])
with col2:
    sentiment_map = {"NEGATIVE": 0.0, "NEUTRAL": 0.5, "POSITIVE": 1.0}
    all_scores = [sentiment_map.get(a["sentiment"], 0.5) for a in result["positive_news"] + result["negative_news"]]

    # all_scores가 비어 있는지 확인
    if len(all_scores) > 0:
        overall_score = sum(all_scores) / len(all_scores)
    else:
        overall_score = 0.5  # 또는 다른 기본값 설정

    fig, ax = plt.subplots(figsize=(6.5, 1.5), dpi=100)

    # 감정 바
    ax.hlines(0, 0, 1, colors="#bbb", linewidth=12, zorder=1)

    # 바 양 끝 심볼
    ax.text(0, 0.05, "-", fontsize=16, ha="center", va="bottom", color=WISERBOND_COLOR)
    ax.text(1, 0.05, "+", fontsize=16, ha="center", va="bottom", color=WISERBOND_COLOR)

    # 전체 평균 표시 (■)
    ax.plot(overall_score, 0, marker="s", color=WISERBOND_COLOR, markersize=12, zorder=3)

    # 섹터 마커와 45도 라벨
    if "sector_sentiment_scores" in result and result["sector_sentiment_scores"]:
        sectors_sorted = sorted(sector_sentiment_scores.items(), key=lambda x: x[1])
        for sector, score in sectors_sorted:
            ax.plot(score, 0, marker="o", color=WISERBOND_COLOR, markersize=8, zorder=2)
            ax.text(score, -0.22, sector, rotation=45, fontsize=8,
                    ha="right", va="top", color=WISERBOND_COLOR)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.5, 0.4)
    ax.axis("off")
    plt.tight_layout()
    st.pyplot(fig)

    plt.tight_layout()
    st.pyplot(fig)

        else:
            st.info("Sector Sentiment Spectrum not available. Showing the overall sentiment instead.")  # subsector가 없으면
    #산업별 분석 결과를 대신 보여주기
            sentiment_map = {"NEGATIVE": 0.0, "NEUTRAL": 0.5, "POSITIVE": 1.0}
            all_scores = [sentiment_map.get(a["sentiment"], 0.5) for a in result["positive_news"] + result["negative_news"]]
            # all_scores가 비어 있는지 확인
            if len(all_scores) > 0:
                overall_score = sum(all_scores) / len(all_scores)
            else:
                overall_score = 0.5  # 또는 다른 기본값 설정
            fig, ax = plt.subplots(figsize=(6.5, 1.5), dpi=100)

            # 감정 바
            ax.hlines(0, 0, 1, colors="#bbb", linewidth=12, zorder=1)

            # 바 양 끝 심볼
            ax.text(0, 0.05, "-", fontsize=16, ha="center", va="bottom", color=WISERBOND_COLOR)
            ax.text(1, 0.05, "+", fontsize=16, ha="center", va="bottom", color=WISERBOND_COLOR)

            # 전체 평균 표시 (■)
            ax.plot(overall_score, 0, marker="s", color=WISERBOND_COLOR, markersize=12, zorder=3)
