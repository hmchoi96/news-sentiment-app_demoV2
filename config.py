# config.py

LANG_TEXT = {
    "English": {
        "header": "📊 Wiserbond News Sentiment Report",
        "executive_summary": "## 🔍 Executive Summary\n\nThis report provides an AI-powered sentiment analysis of recent news articles related to the selected topic. Below you’ll find a breakdown of media sentiment, narrative trends, and key takeaways to inform your perspective.",
        "sentiment_chart": "## 📈 Sentiment Breakdown",
        "positive_title": "### ✅ Positive Coverage",
        "negative_title": "### ⚠️ Negative Coverage",
        "expert_insight": "## 💡 Wiserbond Interpretation",
        "footer": "<small>Wiserbond Research · <a href='https://wiserbond.com'>wiserbond.com</a> · hmchoi@wiserbond.com</small>"
    },
    "한국어": {
        "header": "📊 와이저본드 뉴스 감정 분석 리포트",
        "executive_summary": "## 🔍 핵심 요약\n\n이 보고서는 AI 기반의 감정 분석을 통해 최근 뉴스의 흐름과 내러티브를 정리했습니다.",
        "sentiment_chart": "## 📈 감정 분포 차트",
        "positive_title": "### ✅ 긍정 뉴스 요약",
        "negative_title": "### ⚠️ 부정 뉴스 요약",
        "expert_insight": "## 💡 Wiserbond 해석",
        "footer": "<small>Wiserbond 리서치 · <a href='https://wiserbond.com'>wiserbond.com</a> · hmchoi@wiserbond.com</small>"
    },
    "Español": {
        "header": "📊 Informe de Sentimiento de Noticias de Wiserbond",
        "executive_summary": "## 🔍 Resumen Ejecutivo\n\nEste informe proporciona un análisis de sentimiento impulsado por IA sobre las noticias recientes relacionadas con el tema seleccionado.",
        "sentiment_chart": "## 📈 Distribución de Sentimiento",
        "positive_title": "### ✅ Cobertura Positiva",
        "negative_title": "### ⚠️ Cobertura Negativa",
        "expert_insight": "## 💡 Interpretación de Wiserbond",
        "footer": "<small>Investigación Wiserbond · <a href='https://wiserbond.com'>wiserbond.com</a> · hmchoi@wiserbond.com</small>"
    }
}

INDUSTRY_KEYWORDS = {
    "Supply Chain": ["logistics", "freight", "shipping", "port", "customs", "supply chain", "export", "import"],
    "Consulting": ["client", "recommendation", "strategy", "project", "transformation", "management"],
    "Retail": ["sales", "store", "consumer", "pricing", "discount", "e-commerce"],
    "Finance": ["bank", "interest rate", "investment", "credit", "bond", "liquidity"],
    "Manufacturing": ["factory", "production", "plant", "assembly", "automation", "capacity"]
}

INDUSTRY_SUBSECTORS = {
    "Manufacturing": {
        "Aerospace and Defence": ["aerospace", "defence", "military production"],
        "Automotive": ["automotive", "vehicle", "car", "EV", "battery"],
        "Life Sciences and Biomanufacturing": ["biomanufacturing", "life sciences", "biotech"],
        "Chemicals": ["chemical", "chemicals", "industrial chemicals"],
        "Hydrogen and Fuel Cells": ["hydrogen", "fuel cell", "H2"],
        "Medical Devices": ["medical device", "surgical", "implant"],
        "Plastics": ["plastic", "polymer", "synthetic material"]
    },
    "Finance": {
        "Banking": ["bank", "lending", "mortgage", "loan"],
        "Capital Markets": ["stock", "equity", "IPO", "bond", "debt"],
        "Insurance": ["insurance", "risk premium", "claim", "policyholder"]
    },
    "Retail": {
        "E-Commerce": ["e-commerce", "online retail", "checkout", "digital sales"],
        "Brick-and-Mortar": ["store", "in-store", "mall", "foot traffic"],
        "Luxury Goods": ["luxury", "brand", "high-end", "designer"]
    },
    "Supply Chain": {
        "Shipping & Ports": ["shipping", "port", "marine", "container", "vessel"],
        "Logistics": ["freight", "logistics", "delivery", "trucking"],
        "Warehousing": ["warehouse", "inventory", "distribution center"]
    },
    "Consulting": {
        "Strategy Consulting": ["strategy", "transformation", "operating model"],
        "IT Consulting": ["system integration", "ERP", "digital consulting"],
        "Management Consulting": ["change management", "business process", "org design"]
    }
}

COUNTRY_LIST = ["Global", "United States", "Canada", "Japan", "China", "Germany", "India", "South Korea"]

SECTOR_KEYWORDS = {
    "Semiconductor Industry": [
        "semiconductor", "chip", "fab", "TSMC", "ASML", "foundry", "wafer", "lithography",
        "chip manufacturing", "semiconductor production", "fabless", "node shrink", "5nm process", "advanced packaging"
    ],
    "Global Supply Chains": [
        "supply chain", "logistics", "container", "shipping delay", "port", "disruption", "transport",
        "bottleneck", "supply disruption", "shipping crisis", "port congestion", "freight rates", "backlog"
    ],
    "Financial Markets": [
        "stock", "indices", "bonds", "equity", "volatility", "nasdaq", "dow", "s&p", "market sentiment",
        "sell-off", "market crash", "yield curve", "bull market", "bear market", "quantitative tightening", "risk-off"
    ],
    "Policy Dynamics": [
        "tariff", "sanction", "retaliation", "trade war", "regulation", "geopolitics", "white house",
        "tariff policy", "economic retaliation", "protectionism", "trade barrier", "import duties", "tariff exemption"
    ],
    "Auto Industry": [
        "automotive", "EV", "car sales", "battery", "tesla", "BYD", "charging station", "recall",
        "self-driving", "auto manufacturing", "electric mobility", "autonomous driving", "fleet sales"
    ],
    "Retail & Consumer": [
        "retail", "consumer spending", "ecommerce", "mall", "shopping", "sales growth", "luxury demand",
        "consumer sentiment", "shopping behavior", "brand loyalty", "e-retail boom", "retail traffic"
    ],
    "Energy Sector": [
        "oil", "gas", "OPEC", "fossil fuel", "energy prices", "renewable", "solar", "wind", "electricity",
        "carbon neutral", "green energy", "net zero", "shale production", "offshore drilling", "carbon capture"
    ],
    "Labor Market": [
        "unemployment", "hiring", "layoffs", "job market", "nonfarm payroll", "job growth", "recruitment",
        "remote work", "gig economy", "wage inflation", "talent shortage", "labor participation rate", "remote hiring"
    ],
    "Technology Sector": [
        "AI", "cloud", "software", "data center", "tech layoffs", "big tech", "google", "microsoft",
        "generative AI", "cybersecurity", "cloud migration", "tech bubble"
    ],
    "Healthcare & Pharma": [
        "healthcare", "drug", "FDA", "biotech", "vaccine", "clinical trial", "pharma", "hospital",
        "gene therapy", "drug approval", "telemedicine", "drug pipeline", "FDA fast track", "clinical milestone"
    ],
    "Manufacturing": [
        "factory", "production", "plant", "assembly", "automation", "manufacturing", "industrial",
        "industrial automation", "smart factory", "supply chain resilience", "lean manufacturing", "industrial IoT", "smart assembly line"
    ]
}
