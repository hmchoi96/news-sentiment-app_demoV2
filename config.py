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
    "Freight Shipping": ["freight", "shipping", "container", "port", "automaker", "trade flow", "cross-border", "marine", "cargo vessel", "port congestion"],
    "Rail Transportation": ["rail", "railway", "cargo rail", "train freight", "rail logistics", "railroad", "border crossing"],
    "Trucking & Haulage": ["trucking", "haulage", "trailer", "truck transport", "highway freight", "long-haul", "interstate"],
    "Air Cargo": ["air cargo", "air freight", "cargo airline", "logistics flight", "air shipment", "express delivery"],
    "Third-Party Logistics": ["3PL", "third-party logistics", "distribution partner", "outsourced logistics", "fulfillment service", "retail price", "supply route", "logistics partner"],

    "Automotive": ["automotive", "car", "EV", "battery", "tesla", "auto parts", "vehicle production", "electric mobility", "charging infrastructure"],
    "Aerospace": ["aerospace", "defense aircraft", "military jet", "aviation manufacturing", "boeing", "airbus", "jet engine"],
    "Electronics": ["electronics", "semiconductors", "consumer devices", "circuit", "display panel", "PCB", "integrated circuit"],
    "Machinery": ["machinery", "industrial equipment", "assembly line", "CNC", "manufacturing equipment", "robot arm", "automated process"],
    "Textiles": ["textile", "apparel", "fabric", "garment", "fashion manufacturing", "clothing mill", "cotton", "weaving"],

    "Retail Banking": ["bank", "retail banking", "branch", "deposit", "savings", "mortgage", "interest rate", "lending"],
    "Insurance": ["insurance", "claim", "premium", "underwriting", "policyholder", "payout", "reinsurance"],
    "Asset Management": ["asset management", "investment fund", "portfolio", "mutual fund", "ETF", "fund manager"],
    "Fintech": ["fintech", "mobile payment", "digital bank", "robo advisor", "online lending", "blockchain", "financial technology"],
    "Capital Markets": ["equity", "bond", "stock exchange", "IPO", "volatility", "securities", "market sentiment", "yield curve"],

    "Oil and Gas": ["oil", "gas", "drilling", "exploration", "pipeline", "OPEC", "offshore rig", "natural gas", "refinery"],
    "Renewable Energy": ["renewable", "solar", "wind", "green energy", "hydro", "geothermal", "clean energy", "sustainability"],
    "Utilities": ["utility", "electricity", "grid", "energy pricing", "natural gas", "power bill", "rate hike"],
    "Nuclear": ["nuclear", "uranium", "reactor", "atomic energy", "fission", "nuclear plant", "radioactive", "cooling tower"],
    "Energy Storage": ["battery storage", "energy storage", "grid backup", "lithium", "stationary storage", "charging station"],

    "Semiconductors": ["semiconductor", "chip", "TSMC", "foundry", "wafer", "advanced packaging", "fabless", "process node", "silicon"],
    "Cloud Computing": ["cloud", "AWS", "Azure", "cloud infrastructure", "serverless", "SaaS", "data center", "compute engine"],
    "AI & ML": ["AI", "machine learning", "deep learning", "NLP", "generative AI", "foundation model", "transformer", "large language model"],
    "Consumer Electronics": ["smartphone", "tablet", "laptop", "smartwatch", "consumer devices", "headphone", "wearable", "OLED"],
    "Cybersecurity": ["cybersecurity", "firewall", "ransomware", "infosec", "threat detection", "data breach", "penetration test"],

    "E-Commerce": ["ecommerce", "online store", "checkout", "digital cart", "delivery time", "online order", "shopping platform"],
    "Apparel": ["apparel", "fashion brand", "retail clothing", "garment", "textile", "outlet", "runway", "fast fashion"],
    "Grocery Chains": ["grocery", "supermarket", "discount store", "food retail", "checkout queue", "food basket", "loyalty program"],
    "Luxury Goods": ["luxury", "designer", "high-end brand", "premium goods", "luxury retail", "heritage brand", "luxury watch"],
    "Home Improvement": ["home improvement", "DIY", "hardware store", "home renovation", "furniture retail", "tool kit", "remodeling"],

    "Pharmaceuticals": ["pharmaceutical", "drug", "prescription", "FDA", "pill", "medicine", "formulation", "dosage", "regulatory"],
    "Medical Devices": ["medical device", "implant", "surgical tool", "health equipment", "diagnostic", "scanner", "monitoring system"],
    "Biotech": ["biotech", "gene therapy", "clinical trial", "biological drug", "FDA approval", "biopharma", "rna", "antibody"],
    "Health Insurance": ["health insurance", "co-pay", "coverage", "medical plan", "claim", "deductible", "insurance premium"],
    "Hospitals": ["hospital", "clinic", "inpatient", "healthcare center", "medical facility", "ER", "nurse shortage"],

    "Residential": ["residential", "housing", "home construction", "real estate", "mortgage", "housing permit", "zoning"],
    "Commercial": ["office building", "commercial construction", "business park", "tenant lease", "mixed-use", "co-working"],
    "Infrastructure": ["infrastructure", "bridge", "tunnel", "public project", "government contract", "public works", "infrastructure bill"],
    "Materials": ["cement", "steel", "building materials", "lumber", "construction supply", "rebar", "sheet metal"],
    "Engineering Services": ["civil engineering", "project management", "blueprint", "site survey", "design-build", "infrastructure design"],

    "Farming": ["farming", "crop", "agriculture", "harvest", "farm equipment", "irrigation", "crop rotation"],
    "Livestock": ["livestock", "cattle", "meat production", "dairy", "poultry", "slaughterhouse", "animal feed"],
    "AgriTech": ["agritech", "smart farming", "precision agriculture", "ag drone", "yield forecast", "farm automation", "soil sensor"],
    "Food Processing": ["food processing", "packaging plant", "processed foods", "supply chain food", "food safety", "food packaging"],
    "Fertilizers": ["fertilizer", "soil nutrients", "nitrogen", "ammonia", "crop boost", "potash", "fertilizer price"],

    "Airlines": ["airline", "flight", "airfare", "carrier", "travel booking", "baggage fee", "aviation fuel"],
    "Public Transit": ["subway", "bus", "metro", "public transit", "urban rail", "commute", "fare"],
    "Shipping Lines": ["shipping line", "freighter", "vessel", "sea route", "ocean trade", "cargo manifest", "customs"],
    "Rail Services": ["train", "passenger rail", "freight rail", "rail service", "commuter train", "bullet train", "track access"],
    "Mobility Platforms": ["rideshare", "mobility app", "uber", "lyft", "shared transport", "micro-mobility", "e-scooter"]
}
