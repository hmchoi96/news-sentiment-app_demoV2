# app.py
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from core import analyze_topic
from config import LANG_TEXT, INDUSTRY_KEYWORDS, COUNTRY_LIST
from news_sentiment_tool_demo import TOPIC_SETTINGS
from ui_components import display_news_section, draw_sentiment_chart

# 페이지 설정
st.set_page_config(page_title="Wiserbond News Report", layout="wide")

# --- 사이드바 입력값 설정 ---
st.sidebar.title("🔍 분석 설정")
topic_choice = st.sidebar.selectbox("주제", list(TOPIC_SETTINGS.keys()))
country_choice = st.sidebar.selectbox("국가", COUNTRY_LIST)
industry_choice = st.sidebar.selectbox("산업", ["All"] + list(INDUSTRY_KEYWORDS.keys()))
language_choice = st.sidebar.selectbox("언어 선택", list(LANG_TEXT.keys()))
st.session_state["language"] = language_choice

# 분석 실행
with st.spinner("뉴스를 분석 중입니다..."):
    result = analyze_topic(topic_choice, country_choice, industry_choice, language_choice)

# 결과 변수 추출
summary_text = result["summary"]
sentiment_counts = result["sentiment_counts"]
top_articles = result["top_articles"]
expert_comment = result["expert_comment"]
analysis_date = datetime.now().strftime("%Y년 %m월 %d일 %H:%M")

# --- 보고서 본문 시작 ---

# 스타일 삽입 (폰트/출력 안정화)
st.markdown("""
<style>
body {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0 auto;
    padding: 0 1.5rem;
}
.section-title { font-size:1.3em; font-weight:bold; margin-top:2em; }
@media print {
    .element-container { page-break-inside: avoid; }
}
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown("## Wiserbond News Synthesizer V2 – 감정·요약 보고서")
st.write(f"**분석 기준:** {analysis_date}")
st.write("---")

# 1. 핵심 요약
st.markdown("### 1. 핵심 요약")
st.info(summary_text)

# 2. 감정 흐름 시각화
st.markdown("### 2. 감정 흐름")
fig, ax = plt.subplots(figsize=(5, 1.5))
colors = ['#4caf50', '#ffc107', '#f44336']
ax.bar(sentiment_counts.keys(), sentiment_counts.values(), color=colors)
ax.set_ylabel("기사 수")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
st.pyplot(fig)

# 3. 주요 기사 요약
st.markdown("### 3. 주요 기사 요약")
for idx, art in enumerate(top_articles, 1):
    with st.expander(f"{idx}. {art['title']}"):
        st.write(art["summary"])
        st.markdown(f"[전체 기사 보기]({art['url']})")

# 4. 전문가 해석
st.markdown("### 4. 전문가 해석")
st.success(expert_comment)

# 5. 분석 설정
st.markdown("### 5. 분석 설정")
st.write(f"- **주제:** {topic_choice}")
st.write(f"- **국가:** {country_choice}")
st.write(f"- **산업:** {industry_choice}")
st.write(f"- **언어:** {language_choice}")

# 인쇄 안내
st.markdown("---")
st.markdown("*이 보고서는 전문가용 제출 형식에 맞춰 인쇄 및 PDF 저장 시 레이아웃이 유지되도록 설계되었습니다.*")
