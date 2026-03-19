"""
EUDAIMON LIVE TRACKER - Configuration
24/7 Resource & Stock Signal System
"""

# ═══════════════════════════════════════════════════════════════════════════════
# TRACKED RESOURCES & STOCKS
# ═══════════════════════════════════════════════════════════════════════════════

TRACKED_ASSETS = {
    # ─────────────────────────────────────────────────────────────────────────
    # FERTILIZERS / AGRICULTURE
    # ─────────────────────────────────────────────────────────────────────────
    "NTR": {
        "name": "Nutrien Ltd",
        "category": "Fertilizer",
        "thesis": "Potash bottleneck, food security forced buyer",
        "keywords": ["potash", "fertilizer", "nitrogen", "crop", "agriculture", "food prices"]
    },
    "MOS": {
        "name": "Mosaic Company",
        "category": "Fertilizer",
        "thesis": "Phosphate producer, agriculture infrastructure",
        "keywords": ["phosphate", "fertilizer", "agriculture", "crop yields"]
    },
    "CF": {
        "name": "CF Industries",
        "category": "Fertilizer",
        "thesis": "Nitrogen fertilizer, natural gas derivative play",
        "keywords": ["nitrogen", "ammonia", "fertilizer", "natural gas"]
    },

    # ─────────────────────────────────────────────────────────────────────────
    # URANIUM / NUCLEAR
    # ─────────────────────────────────────────────────────────────────────────
    "LEU": {
        "name": "Centrus Energy",
        "category": "Uranium/Nuclear",
        "thesis": "HALEU monopoly, only US enricher",
        "keywords": ["uranium", "HALEU", "enrichment", "nuclear", "DOE", "reactor"]
    },
    "CCJ": {
        "name": "Cameco Corp",
        "category": "Uranium/Nuclear",
        "thesis": "Largest Western uranium miner, supply deficit",
        "keywords": ["uranium", "mining", "nuclear", "Westinghouse", "reactor"]
    },
    "UEC": {
        "name": "Uranium Energy Corp",
        "category": "Uranium/Nuclear",
        "thesis": "US uranium producer, domestic supply",
        "keywords": ["uranium", "mining", "nuclear", "Texas", "Wyoming"]
    },

    # ─────────────────────────────────────────────────────────────────────────
    # COPPER / INDUSTRIAL METALS
    # ─────────────────────────────────────────────────────────────────────────
    "FCX": {
        "name": "Freeport-McMoRan",
        "category": "Copper",
        "thesis": "Largest copper producer, electrification demand",
        "keywords": ["copper", "mining", "electrification", "EV", "grid", "data center"]
    },
    "SCCO": {
        "name": "Southern Copper",
        "category": "Copper",
        "thesis": "Low-cost copper producer, Peru/Mexico",
        "keywords": ["copper", "mining", "Peru", "Mexico", "electrification"]
    },

    # ─────────────────────────────────────────────────────────────────────────
    # RARE EARTHS / CRITICAL MINERALS
    # ─────────────────────────────────────────────────────────────────────────
    "MP": {
        "name": "MP Materials",
        "category": "Rare Earths",
        "thesis": "Only US rare earth mine, DoD forced buyer",
        "keywords": ["rare earth", "magnet", "EV", "defense", "China", "tariff"]
    },

    # ─────────────────────────────────────────────────────────────────────────
    # PRECIOUS METALS
    # ─────────────────────────────────────────────────────────────────────────
    "GLD": {
        "name": "SPDR Gold Trust",
        "category": "Gold",
        "thesis": "Dollar debasement hedge, central bank buying",
        "keywords": ["gold", "Fed", "inflation", "dollar", "central bank", "reserve"]
    },
    "SLV": {
        "name": "iShares Silver Trust",
        "category": "Silver",
        "thesis": "Industrial + monetary demand, solar/EV",
        "keywords": ["silver", "solar", "industrial", "monetary", "gold ratio"]
    },
    "WPM": {
        "name": "Wheaton Precious Metals",
        "category": "Precious Metals",
        "thesis": "Streaming royalty model, leveraged to metals",
        "keywords": ["gold", "silver", "streaming", "royalty", "mining"]
    },

    # ─────────────────────────────────────────────────────────────────────────
    # DEFENSE / DRONES
    # ─────────────────────────────────────────────────────────────────────────
    "AVAV": {
        "name": "AeroVironment",
        "category": "Defense/Drones",
        "thesis": "Switchblade drones, modern warfare shift",
        "keywords": ["drone", "Switchblade", "Ukraine", "Taiwan", "defense", "military"]
    },
    "KTOS": {
        "name": "Kratos Defense",
        "category": "Defense/Drones",
        "thesis": "Autonomous drones, hypersonics",
        "keywords": ["drone", "autonomous", "hypersonic", "defense", "Air Force"]
    },

    # ─────────────────────────────────────────────────────────────────────────
    # ENERGY / NATURAL GAS
    # ─────────────────────────────────────────────────────────────────────────
    "EQT": {
        "name": "EQT Corporation",
        "category": "Natural Gas",
        "thesis": "Largest US nat gas producer, AI data center demand",
        "keywords": ["natural gas", "LNG", "data center", "power", "Appalachian"]
    },

    # ─────────────────────────────────────────────────────────────────────────
    # DATA CENTER / AI INFRASTRUCTURE
    # ─────────────────────────────────────────────────────────────────────────
    "VRT": {
        "name": "Vertiv Holdings",
        "category": "Data Center",
        "thesis": "Data center cooling, AI power infrastructure",
        "keywords": ["data center", "cooling", "AI", "power", "infrastructure"]
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# SIGNAL THRESHOLDS
# ═══════════════════════════════════════════════════════════════════════════════

SIGNAL_CONFIG = {
    # Technical thresholds
    "rsi_oversold": 30,      # RSI below this = bullish signal
    "rsi_overbought": 70,    # RSI above this = bearish signal
    "rsi_neutral_low": 40,
    "rsi_neutral_high": 60,

    # Price action
    "pullback_threshold": -0.05,    # 5% pullback = potential entry
    "breakout_threshold": 0.03,     # 3% breakout = momentum signal

    # News sentiment
    "sentiment_bullish": 0.6,       # Above 0.6 = bullish news
    "sentiment_bearish": 0.4,       # Below 0.4 = bearish news

    # Volume
    "volume_spike": 1.5,            # 1.5x average = significant
}

# ═══════════════════════════════════════════════════════════════════════════════
# SIGNAL DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════

SIGNAL_MEANINGS = {
    "GREEN": {
        "label": "BUY ZONE",
        "description": "Strong entry opportunity - thesis intact, technicals favorable, sentiment positive",
        "action": "Consider adding position"
    },
    "YELLOW": {
        "label": "HOLD/WATCH",
        "description": "Neutral zone - thesis intact but wait for better entry or confirmation",
        "action": "Monitor closely"
    },
    "RED": {
        "label": "AVOID/CAUTION",
        "description": "Risk elevated - overbought, negative news, or thesis under pressure",
        "action": "Do not add, consider trimming"
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# API CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

API_CONFIG = {
    "refresh_interval": 60,         # Seconds between updates
    "news_refresh": 300,            # Seconds between news checks
    "market_hours_only": False,     # Track 24/7 or market hours only
}

# ═══════════════════════════════════════════════════════════════════════════════
# NEWS SOURCES
# ═══════════════════════════════════════════════════════════════════════════════

NEWS_SOURCES = [
    "reuters",
    "bloomberg",
    "wsj",
    "financial_times",
    "seeking_alpha",
    "zerohedge",
]
