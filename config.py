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

COUNTRY_LIST = ["Global", "United States", "Canada", "Japan", "China", "Germany", "India", "South Korea"]

INDUSTRY_SUBSECTORS = {
    "Supply Chain": {
        "Freight Shipping": ["Freight", "Shipping", "Container", "Marine", "Ocean Transport"],
        "Rail Transportation": ["Rail", "Train Freight", "Cargo Rail", "Railroad Logistics"],
        "Trucking & Haulage": ["Trucking", "Haulage", "Trailer", "Ground Transport"],
        "Air Cargo": ["Air Cargo", "Air Freight", "Logistics Airline", "Cargo Flight"],
        "Third-Party Logistics": ["Logistics", "3PL", "Distribution Partner", "Supply Chain Service"]
    },
    "Manufacturing": {
        "Automotive": ["Automotive", "Vehicle", "EV", "Battery", "Auto Parts"],
        "Aerospace": ["Aerospace", "Defence", "Aircraft", "Aviation Manufacturing"],
        "Electronics": ["Electronics", "Semiconductors", "Consumer Tech", "Circuit"],
        "Machinery": ["Industrial Machinery", "Factory Equipment", "Assembly Machine"],
        "Textiles": ["Textile", "Fabric", "Apparel Production", "Garment"]
    },
    "Finance": {
        "Retail Banking": ["Bank", "Deposit", "Savings", "Branch Banking"],
        "Insurance": ["Insurance", "Underwriting", "Claims", "Premiums"],
        "Asset Management": ["Investment", "Fund", "Portfolio", "Asset Manager"],
        "Fintech": ["Fintech", "Digital Bank", "Mobile Payment", "Robo-Advisor"],
        "Capital Markets": ["Stock", "Bond", "Equity", "IPO", "Market Volatility"]
    },
    "Energy": {
        "Oil and Gas": ["Oil", "Gas", "Exploration", "Drilling", "Pipeline"],
        "Renewable Energy": ["Solar", "Wind", "Hydro", "Clean Energy"],
        "Utilities": ["Electricity", "Natural Gas", "Power Grid", "Utility Pricing"],
        "Nuclear": ["Nuclear", "Reactor", "Uranium", "Fission Energy"],
        "Energy Storage": ["Battery Storage", "Energy Storage", "Grid Backup", "Lithium"]
    },
    "Technology": {
        "Semiconductors": ["Semiconductor", "Chip", "Fab", "Wafer", "Foundry"],
        "Cloud Computing": ["Cloud", "Infrastructure", "AWS", "Azure", "Serverless"],
        "AI & ML": ["AI", "Machine Learning", "Deep Learning", "NLP"],
        "Consumer Electronics": ["Smartphone", "Tablet", "Laptop", "Smartwatch"],
        "Cybersecurity": ["Cybersecurity", "Ransomware", "Firewall", "Infosec"]
    },
    "Retail": {
        "E-Commerce": ["Ecommerce", "Online Shopping", "Checkout", "Digital Cart"],
        "Apparel": ["Fashion", "Apparel", "Clothing Store", "Retail Brand"],
        "Grocery Chains": ["Grocery", "Supermarket", "Food Retail", "Discount Store"],
        "Luxury Goods": ["Luxury", "Designer", "High-End", "Premium Brand"],
        "Home Improvement": ["Home Improvement", "DIY", "Hardware Store", "Furniture Retail"]
    },
    "Healthcare": {
        "Pharmaceuticals": ["Pharma", "Drug", "Prescription", "FDA Approval"],
        "Medical Devices": ["Device", "Implant", "Surgical Tool", "Diagnostic Equipment"],
        "Biotech": ["Biotech", "Genetic", "Clinical Trial", "Biological Therapy"],
        "Health Insurance": ["Health Insurance", "Premium", "Coverage", "Co-Pay"],
        "Hospitals": ["Hospital", "Clinic", "Inpatient", "Medical Care"]
    },
    "Construction": {
        "Residential": ["Residential", "Housing", "Real Estate", "Home Building"],
        "Commercial": ["Office Building", "Commercial Project", "Retail Construction"],
        "Infrastructure": ["Road", "Bridge", "Tunnel", "Public Works"],
        "Materials": ["Cement", "Steel", "Lumber", "Construction Supply"],
        "Engineering Services": ["Civil Engineering", "Project Management", "Site Plan"]
    },
    "Agriculture": {
        "Farming": ["Farm", "Crop", "Harvest", "Planting"],
        "Livestock": ["Livestock", "Cattle", "Meat", "Poultry"],
        "AgriTech": ["Agritech", "Precision Agriculture", "Smart Farming", "Drone"],
        "Food Processing": ["Food Processing", "Packaging", "Food Plant", "Dairy"],
        "Fertilizers": ["Fertilizer", "Ammonia", "Soil Nutrients", "Nitrogen"]
    },
    "Transportation": {
        "Airlines": ["Airline", "Flight", "Airfare", "Carrier"],
        "Public Transit": ["Bus", "Subway", "Metro", "Commuter"],
        "Shipping Lines": ["Shipping Line", "Vessel", "Freighter", "Shipping Route"],
        "Rail Services": ["Rail", "Train", "Cargo Rail", "Track"],
        "Mobility Platforms": ["Rideshare", "Uber", "Lyft", "Mobility App"]
    }
}

SECTOR_KEYWORDS = {
    "Freight Shipping": ["Shipping", "Freight", "Container", "Marine", "Cargo Vessel", "Port Congestion"],
    "Rail Transportation": ["Rail", "Railway", "Cargo Rail", "Train Freight", "Rail Logistics"],
    "Trucking & Haulage": ["Trucking", "Haulage", "Trailer", "Truck Transport", "Highway Freight"],
    "Air Cargo": ["Air Cargo", "Air Freight", "Cargo Airline", "Logistics Flight", "Air Shipment"],
    "Third-Party Logistics": ["3PL", "Third-Party Logistics", "Distribution Partner", "Outsourced Logistics", "Fulfillment Service"],

    "Automotive": ["Automotive", "Car", "EV", "Battery", "Tesla", "Auto Parts", "Vehicle Production"],
    "Aerospace": ["Aerospace", "Defense Aircraft", "Military Jet", "Aviation Manufacturing", "Boeing", "Airbus"],
    "Electronics": ["Electronics", "Semiconductors", "Consumer Devices", "Circuit", "Display Panel"],
    "Machinery": ["Machinery", "Industrial Equipment", "Assembly Line", "CNC", "Manufacturing Equipment"],
    "Textiles": ["Textile", "Apparel", "Fabric", "Garment", "Fashion Manufacturing"],

    "Retail Banking": ["Bank", "Retail Banking", "Branch", "Deposit", "Savings", "Mortgage"],
    "Insurance": ["Insurance", "Claim", "Premium", "Underwriting", "Policyholder"],
    "Asset Management": ["Asset Management", "Investment Fund", "Portfolio", "Mutual Fund", "ETF"],
    "Fintech": ["Fintech", "Mobile Payment", "Digital Bank", "Robo Advisor", "Online Lending"],
    "Capital Markets": ["Equity", "Bond", "Stock Exchange", "IPO", "Volatility", "Securities"],

    "Oil and Gas": ["Oil", "Gas", "Drilling", "Exploration", "Pipeline", "OPEC"],
    "Renewable Energy": ["Renewable", "Solar", "Wind", "Green Energy", "Hydro"],
    "Utilities": ["Utility", "Electricity", "Grid", "Energy Pricing", "Natural Gas"],
    "Nuclear": ["Nuclear", "Uranium", "Reactor", "Atomic Energy", "Fission"],
    "Energy Storage": ["Battery Storage", "Energy Storage", "Grid Backup", "Lithium"],

    "Semiconductors": ["Semiconductor", "Chip", "TSMC", "Foundry", "Wafer", "Advanced Packaging"],
    "Cloud Computing": ["Cloud", "AWS", "Azure", "Cloud Infrastructure", "Serverless", "SaaS"],
    "AI & ML": ["AI", "Machine Learning", "Deep Learning", "NLP", "Generative AI"],
    "Consumer Electronics": ["Smartphone", "Tablet", "Laptop", "Smartwatch", "Consumer Devices"],
    "Cybersecurity": ["Cybersecurity", "Firewall", "Ransomware", "Infosec", "Threat Detection"],

    "E-Commerce": ["Ecommerce", "Online Store", "Checkout", "Digital Cart", "Delivery Time"],
    "Apparel": ["Apparel", "Fashion Brand", "Retail Clothing", "Garment", "Textile"],
    "Grocery Chains": ["Grocery", "Supermarket", "Discount Store", "Food Retail", "Checkout Queue"],
    "Luxury Goods": ["Luxury", "Designer", "High-End Brand", "Premium Goods", "Luxury Retail"],
    "Home Improvement": ["Home Improvement", "DIY", "Hardware Store", "Home Renovation", "Furniture Retail"],

    "Pharmaceuticals": ["Pharmaceutical", "Drug", "Prescription", "FDA", "Pill", "Medicine"],
    "Medical Devices": ["Medical Device", "Implant", "Surgical Tool", "Health Equipment", "Diagnostic"],
    "Biotech": ["Biotech", "Gene Therapy", "Clinical Trial", "Biological Drug", "FDA Approval"],
    "Health Insurance": ["Health Insurance", "Co-Pay", "Coverage", "Medical Plan", "Claim"],
    "Hospitals": ["Hospital", "Clinic", "Inpatient", "Healthcare Center", "Medical Facility"],

    "Residential": ["Residential", "Housing", "Home Construction", "Real Estate", "Mortgage"],
    "Commercial": ["Office Building", "Commercial Construction", "Business Park", "Tenant Lease", "Mixed-use"],
    "Infrastructure": ["Infrastructure", "Bridge", "Tunnel", "Public Project", "Government Contract"],
    "Materials": ["Cement", "Steel", "Building Materials", "Lumber", "Construction Supply"],
    "Engineering Services": ["Civil Engineering", "Project Management", "Blueprint", "Site Survey"],

    "Farming": ["Farming", "Crop", "Agriculture", "Harvest", "Farm Equipment"],
    "Livestock": ["Livestock", "Cattle", "Meat Production", "Dairy", "Poultry"],
    "AgriTech": ["AgriTech", "Smart Farming", "Precision Agriculture", "Ag Drone", "Yield Forecast"],
    "Food Processing": ["Food Processing", "Packaging Plant", "Processed Foods", "Supply Chain Food"],
    "Fertilizers": ["Fertilizer", "Soil Nutrients", "Nitrogen", "Ammonia", "Crop Boost"],

    "Airlines": ["Airline", "Flight", "Airfare", "Carrier", "Travel Booking"],
    "Public Transit": ["Subway", "Bus", "Metro", "Public Transit", "Urban Rail"],
    "Shipping Lines": ["Shipping Line", "Freighter", "Vessel", "Sea Route", "Ocean Trade"],
    "Rail Services": ["Train", "Passenger Rail", "Freight Rail", "Rail Service", "Commuter Train"],
    "Mobility Platforms": ["Rideshare", "Mobility App", "Uber", "Lyft", "Shared Transport"]
}
