# core.py
from news_sentiment_tool_demo import (
    get_news,
    filter_articles,
    run_sentiment_analysis,
    summarize_by_sentiment,
    TOPIC_SETTINGS
)
from config import INDUSTRY_KEYWORDS, SECTOR_KEYWORDS
from collections import Counter
from transformers import pipeline
from datetime import datetime

# Summarization 파이프라인 캐시
_summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def detect_impacted_sectors(articles, sector_mapping):
    """기사 텍스트를 통해 산업 영향 파악"""
    impact_map = {}
    source_map = {}
    for a in articles:
        text = f"{a['title']} {a.get('description','')}".lower()
        for sector, keywords in sector_mapping.items():
            if any(k in text for k in keywords):
                impact_map.setdefault(sector, []).append(text)
                source_map.setdefault(sector, []).append(a.get('source','Unknown'))
    return impact_map, source_map

def summarize_sector_impact(texts):
    """섹터별 임팩트 요약"""
    if not texts:
        return "No clear impact found."
    block = " ".join(texts)[:512]
    try:
        return _summarizer(block, max_length=40, min_length=10, do_sample=False)[0]["summary_text"]
    except Exception:
        return "Summary model failed."

def compute_sector_sentiment_scores(analyzed, sector_mapping):
    """섹터별 평균 감정 점수 계산"""
    sentiment_map = {"NEGATIVE":0.0, "NEUTRAL":0.5, "POSITIVE":1.0}
    scores = {}
    counts = {}
    for a in analyzed:
        text = f"{a['title']} {a.get('description','')}".lower()
        score = sentiment_map.get(a["sentiment"], 0.5)
        for sector, keywords in sector_mapping.items():
            if any(k in text for k in keywords):
                scores.setdefault(sector,0.0)
                counts.setdefault(sector,0)
                scores[sector] += score
                counts[sector] += 1
    return {sec: scores[sec]/counts[sec] for sec in scores}

def analyze_topic(topic, country="Global", industry="All", subsector_mapping=None, language="English"):
    setting = TOPIC_SETTINGS[topic]
    search_term = setting["search_term"]
    if country != "Global":
        search_term += f" {country}"

    # 키워드 설정
    keywords = setting["keywords"].copy()
    if industry != "All":
        keywords += INDUSTRY_KEYWORDS.get(industry, [])

    # 1) 뉴스 수집 & 필터링
    raw    = get_news(search_term)
    filtered = filter_articles(raw, keywords)

    # 2) 감정 분석
    analyzed = run_sentiment_analysis(filtered)

    # 3) 감정 통계
    counts = {"Positive":0,"Neutral":0,"Negative":0}
    for a in analyzed:
        lbl = a["sentiment"].capitalize()
        if lbl in counts:
            counts[lbl] += 1

    pos_news = [a for a in analyzed if a["sentiment"]=="POSITIVE"]
    neg_news = [a for a in analyzed if a["sentiment"]=="NEGATIVE"]
    pos_sources = sorted({a["source"] for a in pos_news})
    neg_sources = sorted({a["source"] for a in neg_news})

    # 4) Executive Summary
    dominant = max(counts, key=lambda k: counts[k])
    executive_summary = f"Over the past days, news on **{topic}** has been predominantly **{dominant.lower()}**."

    # 5) Sector Impact
    sector_map = subsector_mapping if subsector_mapping else SECTOR_KEYWORDS
    imp_map, src_map = detect_impacted_sectors(analyzed, sector_map)
    impact_summary = []
    for sector, texts in imp_map.items():
        sources = src_map.get(sector,[])
        top_src = Counter(sources).most_common(1)[0][0] if sources else "Unknown"
        impact_summary.append({
            "sector": sector,
            "impact": summarize_sector_impact(texts),
            "source": top_src
        })

    # 6) Sector Sentiment Scores
    sector_scores = compute_sector_sentiment_scores(analyzed, sector_map)

    # 7) 전문가 요약
    pos_sum = summarize_by_sentiment(analyzed, "POSITIVE", keywords)
    neg_sum = summarize_by_sentiment(analyzed, "NEGATIVE", keywords)

    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "sentiment_counts": counts,
        "positive_news": pos_news,
        "negative_news": neg_news,
        "positive_sources": pos_sources,
        "negative_sources": neg_sources,
        "executive_summary": executive_summary,
        "impact_summary": impact_summary,
        "sector_sentiment_scores": sector_scores,
        "expert_summary": {
            "positive_summary": pos_sum,
            "negative_summary": neg_sum
        }
    }
