import requests
from transformers import pipeline
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# ✅ API Key
NEWS_API_KEY = '0e28b7f94fc04e6b9d130092886cabc6'

# ✅ Keyword Setting
TOPIC_SETTINGS = {
    "tariff": {
        "search_term": "tariff",
        "keywords": [
            "tariff", "tariffs", "duties", "customs", "import", "export", "trade",
            "sanction", "levy", "protectionism", "trade war", "tariff hike",
            "border tax", "retaliatory", "quota"
        ]
    },
    "trump": {
        "search_term": "Donald Trump",
        "keywords": [
            "trump", "donald", "republican", "president", "white house",
            "gop", "maga", "trump administration", "former president",
            "2024 election", "trump rally", "indictment", "mar-a-lago"
        ]
    },
    "inflation": {
        "search_term": "inflation",
        "keywords": [
            "inflation", "price index", "cpi", "ppi", "consumer price", "core inflation",
            "cost of living", "rising prices", "inflationary pressure",
            "interest rates", "wage growth", "monetary tightening", "headline inflation",
            "economic overheating", "sticky inflation", "disinflation"
        ]
    },
    "fed": {
        "search_term": "fed",
        "keywords": [
            "federal reserve", "interest rate", "rate hike", "rate cut", "jerome powell",
            "fed", "fomc", "central bank", "tightening", "pause", "pivot", "monetary policy"
        ]
    },
    "unemployment": {
        "search_term": "employment",
        "keywords": [
            "unemployment", "employment", "jobless", "nonfarm payroll", "labor market", "jobs report",
            "layoffs", "job cuts", "hiring freeze", "job growth", "employment rate"
        ]
    }
}

FROM_DATE = (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')


def get_news(search_term, industry_keywords=None, max_pages=4, page_size=100):
    all_articles = []
    base_url = "https://newsapi.org/v2/everything"
    queries = [search_term]
    if industry_keywords:
        queries += [f"{search_term} AND {kw}" for kw in industry_keywords]

    for q in queries:
        for page in range(1, max_pages + 1):
            params = {
                "q": q,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": page_size,
                "page": page,
                "from": FROM_DATE,
                "domains": "reuters.com,bloomberg.com,cnn.com,wsj.com,ft.com,nytimes.com",
                "apiKey": NEWS_API_KEY
            }
            try:
                response = requests.get(base_url, params=params)
                data = response.json()
                if 'articles' in data:
                    all_articles.extend(data['articles'])
                if len(data.get("articles", [])) < page_size:
                    break
            except Exception as e:
                print(f"Error fetching query '{q}':", e)
    return all_articles


def contains_keywords(text, keywords):
    text = (text or "").lower()
    return sum(k in text for k in keywords) >= 1


def filter_articles(articles, keywords, max_filtered=50):
    seen_sources = set()
    filtered = []
    for a in articles:
        source = a['source']['name']
        title = a['title']
        desc = a['description']
        if not title or not desc:
            continue
        combined = f"{title} {desc}"
        if contains_keywords(combined, keywords) and source not in seen_sources:
            filtered.append(a)
            seen_sources.add(source)
        if len(filtered) >= max_filtered:
            break
    return filtered


def run_sentiment_analysis(articles):
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", framework="pt")
    results = []
    for a in articles:
        text = f"{a['title']}. {a['description'] or ''}"
        sentiment = sentiment_pipeline(text)[0]
        results.append({
            "source": a['source']['name'],
            "title": a['title'],
            "description": a['description'],
            "sentiment": sentiment['label'],
            "score": round(sentiment['score'], 2)
        })
    return results


def summarize_by_sentiment(articles, sentiment_label, keywords):
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    texts = [
        f"{a['description']} (Title: {a['title']})"
        for a in articles
        if a['sentiment'] == sentiment_label and a['description'] and contains_keywords(f"{a['description']} {a['title']}", keywords)
    ]

    if len(texts) < 1:
        return "No matching articles found for summarization."

    chunks = []
    word_limit = 500
    current_chunk = []
    total_words = 0

    for t in texts:
        w_count = len(t.split())
        if total_words + w_count > word_limit:
            break
        current_chunk.append(t)
        total_words += w_count

    truncated = " ".join(current_chunk)
    try:
        summary = summarizer(truncated, max_length=200, min_length=60, do_sample=False)[0]['summary_text']
        return summary
    except Exception as e:
        return "Summarization failed due to model input error."


def draw_sentiment_chart(articles):
    total = len(articles)
    if total == 0:
        print("No articles to visualize.")
        return
    from collections import Counter
    counts = Counter([a['sentiment'] for a in articles])
    labels = ['NEGATIVE', 'NEUTRAL', 'POSITIVE']
    colors = ['#d9534f', '#f7f1f1', '#bfaeff']
    values = [counts.get(label, 0) / total * 100 for label in labels]
    plt.figure(figsize=(8, 1.2))
    plt.barh(['Sentiment'], values, color=colors, edgecolor='black', height=0.4, left=[0, values[0], values[0]+values[1]])
    for i, (v, label) in enumerate(zip(values, labels)):
        if v > 0:
            plt.text(sum(values[:i]) + v/2, 0, f"{label.title()} {int(v)}%", va='center', ha='center', fontsize=9)
    plt.axis('off')
    plt.title("Sentiment Breakdown")
    plt.show()


def run_analysis():
    while True:
        topic = input("📝 Enter a keyword (Available: tariff, trump, inflation, fed, unemployment): ").strip().lower()
        if topic not in TOPIC_SETTINGS:
            print(f"❌ '{topic}' is not available. Please try again.")
            continue
        setting = TOPIC_SETTINGS[topic]
        search_term = setting['search_term']
        filter_keywords = setting['keywords']
        raw = get_news(search_term, industry_keywords=filter_keywords)
        filtered = filter_articles(raw, filter_keywords)
        analyzed = run_sentiment_analysis(filtered)
        pos_summary = summarize_by_sentiment(analyzed, 'POSITIVE', filter_keywords)
        neg_summary = summarize_by_sentiment(analyzed, 'NEGATIVE', filter_keywords)
        print(f"\n📅 News Summary for the Period: {FROM_DATE} to {datetime.today().strftime('%Y-%m-%d')}")
        print(f"📊 Analyzed {len(analyzed)} articles from {len(set(a['source'] for a in analyzed))} news sources.\n")
        print("🤖 AI Summary:")
        print(f"❗ Negative News: {neg_summary}")
        print(f"✅ Positive News: {pos_summary}")
        draw_sentiment_chart(analyzed)
        again = input("\n🔁 Would you like to analyze another topic? (yes / no): ").strip().lower()
        if again in ['no', 'n']:
            print("👋 Analysis finished. Have a great day!")
            break

# execute
if __name__ == "__main__":
    run_analysis()
