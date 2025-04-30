from news_sentiment_tool_demo import (
    get_news, filter_articles,
    run_sentiment_analysis, summarize_by_sentiment,
    TOPIC_SETTINGS
)
from config import (
    INDUSTRY_KEYWORDS, INDUSTRY_SUBSECTORS,
    SECTOR_KEYWORDS
)
from collections import Counter
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

def detect_impacted_sectors(articles):
    """기사별 언급된 섹터 카운트 요약"""
    mentions = []
    for a in articles:
        text = f"{a['title']} {a.get('description','')}".lower()
        for sec, kws in SECTOR_KEYWORDS.items():
            if any(k.lower() in text for k in kws):
                mentions.append(sec)
    counts = Counter(mentions)
    return [{"sector": s, "impact": f"{counts[s]} mentions"} for s in counts]

def compute_sector_sentiment_scores(analyzed, mapping):
    """
    키워드 매핑(mapping) 기반으로 부문별 평점 계산
    평균 점수를 [-1,1] -> [0,1]로 정규화
    """
    totals = {k: 0.0 for k in mapping}
    counts = {k: 0 for k in mapping}
    for a in analyzed:
        text = f"{a['title']} {a.get('description','')}".lower()
        for sec, kws in mapping.items():
            if any(k.lower() in text for k in kws):
                counts[sec] += 1
                score = a["score"] if a["sentiment"] == "POSITIVE" else -a["score"] if a["sentiment"] == "NEGATIVE" else 0
                totals[sec] += score
    final = {}
    for sec in totals:
        if counts[sec]:
            avg = totals[sec] / counts[sec]
            final[sec] = round((avg + 1) / 2, 2)
        else:
            final[sec] = 0.5
    return final

def analyze_topic(topic, country="Global", industry="All", language="English"):
    settings = TOPIC_SETTINGS.get(topic, {})
    keywords = settings.get("keywords", [])
    search_term = settings.get("search_term", topic)

    raw = get_news(search_term)
    filtered = filter_articles(raw, keywords)
    analyzed = run_sentiment_analysis(filtered)

    sentiment_counts = Counter(a["sentiment"] for a in analyzed)
    pos_news = [a for a in analyzed if a["sentiment"] == "POSITIVE"]
    neg_news = [a for a in analyzed if a["sentiment"] == "NEGATIVE"]

    # Executive summary: 상위 3개 단어 추출
    words = []
    for a in filtered:
        words += [w.lower().strip(".,") for w in a.get("title","").split()]
    top3 = [w for w,_ in Counter(words).most_common(3)]
    executive_summary = f"Top terms: {', '.join(top3)}."

    impact_summary = detect_impacted_sectors(filtered)

    # 섹터 또는 서브섹터 감정 점수
    if industry != "All" and industry in INDUSTRY_SUBSECTORS:
        mapping = INDUSTRY_SUBSECTORS[industry]
    else:
        mapping = SECTOR_KEYWORDS
    sector_sentiment_scores = compute_sector_sentiment_scores(analyzed, mapping)

    # 전문가 요약
    pos_summary = summarize_by_sentiment(analyzed, "POSITIVE", keywords)
    neg_summary = summarize_by_sentiment(analyzed, "NEGATIVE", keywords)
    expert_summary = {"positive_summary": pos_summary, "negative_summary": neg_summary}

    return {
        "sentiment_counts": sentiment_counts,
        "positive_news": pos_news,
        "negative_news": neg_news,
        "executive_summary": executive_summary,
        "impact_summary": impact_summary,
        "sector_sentiment_scores": sector_sentiment_scores,
        "expert_summary": expert_summary,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
