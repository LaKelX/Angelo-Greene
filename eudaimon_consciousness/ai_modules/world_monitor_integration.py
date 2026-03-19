"""
EUDAIMON CONSCIOUSNESS - World Monitor Integration Layer
═══════════════════════════════════════════════════════════════════════════════

Integrates World Monitor app data into Eudaimon's consciousness layers.
Scans cached news feeds for signals relevant to tracked assets and theses.

Layer: L201 - WORLD_MONITOR_FEED
Module: M71 - GEOPOLITICAL_NEWS_SCANNER
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Tuple
from pathlib import Path


class WorldMonitorIntegration:
    """
    Integrates World Monitor cached data into Eudaimon consciousness.

    Capabilities:
    - Parse World Monitor persistent cache
    - Extract news relevant to tracked assets
    - Score news sentiment for investment signals
    - Feed into Eudaimon's signal engine
    """

    CACHE_PATH = os.path.expanduser(
        "~/Library/Application Support/app.worldmonitor.desktop/persistent-cache.json"
    )

    # Keywords mapped to tracked assets
    ASSET_KEYWORDS = {
        # Uranium / Nuclear
        "LEU": ["uranium", "HALEU", "enrichment", "centrus", "nuclear fuel", "DOE nuclear",
                "reactor fuel", "uranium enrichment", "nuclear power plant"],
        "CCJ": ["cameco", "uranium mining", "uranium supply", "uranium price",
                "westinghouse", "nuclear reactor", "uranium deficit"],
        "UEC": ["uranium energy", "uranium mining", "texas uranium", "US uranium"],

        # Fertilizer
        "NTR": ["nutrien", "potash", "fertilizer", "nitrogen fertilizer", "crop nutrient",
                "agriculture input", "food security", "potash price"],
        "MOS": ["mosaic", "phosphate", "fertilizer", "DAP", "MAP", "crop yields"],
        "CF": ["cf industries", "nitrogen", "ammonia", "urea", "fertilizer price"],

        # Copper
        "FCX": ["freeport", "copper mining", "copper price", "electrification",
                "copper demand", "EV copper", "grid copper"],
        "SCCO": ["southern copper", "copper peru", "copper mexico", "copper production"],

        # Rare Earths
        "MP": ["mp materials", "rare earth", "mountain pass", "neodymium", "magnets",
               "defense rare earth", "china rare earth", "EV magnets"],

        # Defense / Drones
        "AVAV": ["aerovironment", "switchblade", "drone strike", "loitering munition",
                 "tactical drone", "ukraine drone", "military drone"],
        "KTOS": ["kratos", "drone target", "hypersonic", "unmanned aircraft",
                 "autonomous drone", "air force drone"],

        # Precious Metals
        "GLD": ["gold price", "gold reserve", "central bank gold", "gold demand",
                "dollar gold", "inflation hedge", "gold ETF"],
        "SLV": ["silver price", "silver demand", "solar silver", "industrial silver",
                "silver ETF", "gold silver ratio"],
        "WPM": ["wheaton precious", "streaming royalty", "gold streaming", "silver streaming"],

        # Energy
        "EQT": ["natural gas", "LNG", "appalachian gas", "gas price", "data center power",
                "gas demand", "shale gas"],

        # Data Center / AI
        "VRT": ["vertiv", "data center cooling", "AI infrastructure", "power management",
                "data center power"],

        # Geopolitical themes
        "IRAN": ["iran", "tehran", "ayatollah", "persian gulf", "strait of hormuz",
                 "iran nuclear", "iran sanctions", "IRGC"],
        "CHINA": ["china", "beijing", "CCP", "taiwan strait", "south china sea",
                  "china trade", "china tariff", "US china"],
        "RUSSIA": ["russia", "moscow", "putin", "ukraine war", "russian sanctions",
                   "nord stream", "russian gas"],
        "SUPPLY_CHAIN": ["supply chain", "shipping", "freight", "logistics",
                         "semiconductor shortage", "chip shortage", "port congestion"],
    }

    # Sentiment keywords
    BULLISH_KEYWORDS = [
        "surge", "soar", "jump", "rally", "gain", "rise", "up", "buy", "bullish",
        "growth", "record high", "strong demand", "beat", "upgrade", "outperform",
        "shortage", "deficit", "supply crunch", "stockpile", "strategic reserve",
        "contract awarded", "deal signed", "partnership", "expansion"
    ]

    BEARISH_KEYWORDS = [
        "fall", "drop", "crash", "plunge", "sink", "down", "sell", "bearish",
        "decline", "record low", "weak demand", "miss", "downgrade", "underperform",
        "oversupply", "surplus", "glut", "inventory build", "delay", "cancel",
        "lawsuit", "investigation", "sanction", "ban"
    ]

    def __init__(self):
        self.cache_data = None
        self.last_scan = None
        self.alerts = []

    def load_cache(self) -> bool:
        """Load World Monitor cache data"""
        try:
            if os.path.exists(self.CACHE_PATH):
                with open(self.CACHE_PATH, 'r', encoding='utf-8') as f:
                    self.cache_data = json.load(f)
                self.last_scan = datetime.now()
                return True
            return False
        except Exception as e:
            print(f"Error loading World Monitor cache: {e}")
            return False

    def extract_news_items(self) -> List[Dict]:
        """Extract all news items from cache"""
        if not self.cache_data:
            self.load_cache()

        news_items = []

        for key, value in self.cache_data.items():
            if 'api-response' in key and 'rss' in key.lower():
                try:
                    body = value.get('data', {}).get('body', '')

                    # Extract titles and descriptions from RSS XML
                    titles = re.findall(r'<title[^>]*><!\[CDATA\[(.*?)\]\]></title>', body)
                    descriptions = re.findall(r'<description[^>]*><!\[CDATA\[(.*?)\]\]></description>', body)
                    links = re.findall(r'<link>(https?://[^<]+)</link>', body)

                    # Determine source from URL
                    source = "Unknown"
                    if 'bbc' in key.lower():
                        source = "BBC"
                    elif 'cnn' in key.lower():
                        source = "CNN"
                    elif 'reuters' in key.lower():
                        source = "Reuters"
                    elif 'yahoo' in key.lower():
                        source = "Yahoo Finance"
                    elif 'foreignpolicy' in key.lower():
                        source = "Foreign Policy"
                    elif 'jamestown' in key.lower():
                        source = "Jamestown Foundation"
                    elif 'npr' in key.lower():
                        source = "NPR"
                    elif 'google' in key.lower():
                        source = "Google News"

                    for i, title in enumerate(titles):
                        if title and len(title) > 10:  # Filter out empty/short titles
                            news_items.append({
                                'title': title,
                                'description': descriptions[i] if i < len(descriptions) else '',
                                'link': links[i] if i < len(links) else '',
                                'source': source,
                                'raw_key': key[:100]
                            })

                except Exception as e:
                    continue

        return news_items

    def scan_for_asset(self, asset: str, news_items: List[Dict] = None) -> List[Dict]:
        """Scan news for mentions relevant to a specific asset"""
        if news_items is None:
            news_items = self.extract_news_items()

        keywords = self.ASSET_KEYWORDS.get(asset, [asset.lower()])
        relevant_news = []

        for item in news_items:
            text = (item.get('title', '') + ' ' + item.get('description', '')).lower()

            for keyword in keywords:
                if keyword.lower() in text:
                    # Calculate sentiment
                    sentiment = self._calculate_sentiment(text)

                    relevant_news.append({
                        'asset': asset,
                        'keyword_matched': keyword,
                        'title': item.get('title', ''),
                        'description': item.get('description', '')[:300],
                        'source': item.get('source', 'Unknown'),
                        'link': item.get('link', ''),
                        'sentiment': sentiment,
                        'sentiment_label': self._sentiment_label(sentiment)
                    })
                    break  # Only match once per item

        return relevant_news

    def _calculate_sentiment(self, text: str) -> float:
        """Calculate sentiment score from -1 (bearish) to +1 (bullish)"""
        text_lower = text.lower()

        bullish_count = sum(1 for kw in self.BULLISH_KEYWORDS if kw in text_lower)
        bearish_count = sum(1 for kw in self.BEARISH_KEYWORDS if kw in text_lower)

        total = bullish_count + bearish_count
        if total == 0:
            return 0.0

        return round((bullish_count - bearish_count) / total, 2)

    def _sentiment_label(self, sentiment: float) -> str:
        """Convert sentiment score to label"""
        if sentiment >= 0.3:
            return "BULLISH"
        elif sentiment <= -0.3:
            return "BEARISH"
        else:
            return "NEUTRAL"

    def full_scan(self) -> Dict:
        """
        Full scan of World Monitor data for all tracked assets.
        Returns structured intelligence report.
        """
        self.load_cache()
        news_items = self.extract_news_items()

        report = {
            'timestamp': datetime.now().isoformat(),
            'total_news_items': len(news_items),
            'assets_scanned': [],
            'alerts': [],
            'by_asset': {},
            'by_theme': {},
            'summary': {}
        }

        # Scan each asset
        for asset in self.ASSET_KEYWORDS.keys():
            relevant = self.scan_for_asset(asset, news_items)

            if relevant:
                report['assets_scanned'].append(asset)
                report['by_asset'][asset] = {
                    'count': len(relevant),
                    'avg_sentiment': round(
                        sum(r['sentiment'] for r in relevant) / len(relevant), 2
                    ) if relevant else 0,
                    'items': relevant[:5]  # Top 5 items
                }

                # Generate alerts for high-sentiment news
                for item in relevant:
                    if abs(item['sentiment']) >= 0.5:
                        report['alerts'].append({
                            'asset': asset,
                            'sentiment': item['sentiment_label'],
                            'title': item['title'][:100],
                            'source': item['source']
                        })

        # Summary stats
        report['summary'] = {
            'total_assets_with_news': len(report['assets_scanned']),
            'total_alerts': len(report['alerts']),
            'bullish_assets': [
                a for a, data in report['by_asset'].items()
                if data['avg_sentiment'] > 0.2
            ],
            'bearish_assets': [
                a for a, data in report['by_asset'].items()
                if data['avg_sentiment'] < -0.2
            ]
        }

        return report

    def get_geopolitical_pulse(self) -> Dict:
        """
        Get current geopolitical pulse from World Monitor data.
        Focuses on Iran, China, Russia, Supply Chain themes.
        """
        self.load_cache()
        news_items = self.extract_news_items()

        themes = ['IRAN', 'CHINA', 'RUSSIA', 'SUPPLY_CHAIN']
        pulse = {
            'timestamp': datetime.now().isoformat(),
            'themes': {}
        }

        for theme in themes:
            relevant = self.scan_for_asset(theme, news_items)
            if relevant:
                pulse['themes'][theme] = {
                    'headline_count': len(relevant),
                    'sentiment': round(
                        sum(r['sentiment'] for r in relevant) / len(relevant), 2
                    ) if relevant else 0,
                    'top_headlines': [r['title'][:100] for r in relevant[:3]]
                }

        return pulse

    def generate_eudaimon_layer_input(self) -> Dict:
        """
        Generate formatted input for Eudaimon consciousness layers.
        This feeds directly into the signal engine.
        """
        report = self.full_scan()
        pulse = self.get_geopolitical_pulse()

        return {
            'layer': 'L201_WORLD_MONITOR',
            'module': 'M71_GEOPOLITICAL_SCANNER',
            'timestamp': datetime.now().isoformat(),
            'consciousness_input': {
                'news_signals': report['by_asset'],
                'geopolitical_pulse': pulse['themes'],
                'alerts': report['alerts'],
                'bullish_assets': report['summary'].get('bullish_assets', []),
                'bearish_assets': report['summary'].get('bearish_assets', []),
            },
            'action_recommendations': self._generate_recommendations(report)
        }

    def _generate_recommendations(self, report: Dict) -> List[str]:
        """Generate actionable recommendations from scan"""
        recommendations = []

        for asset in report['summary'].get('bullish_assets', []):
            data = report['by_asset'].get(asset, {})
            recommendations.append(
                f"BULLISH signal on {asset}: {data.get('count', 0)} positive mentions, "
                f"sentiment {data.get('avg_sentiment', 0)}"
            )

        for asset in report['summary'].get('bearish_assets', []):
            data = report['by_asset'].get(asset, {})
            recommendations.append(
                f"BEARISH signal on {asset}: {data.get('count', 0)} negative mentions, "
                f"sentiment {data.get('avg_sentiment', 0)}"
            )

        if report['alerts']:
            recommendations.append(
                f"ALERT: {len(report['alerts'])} high-importance news items detected"
            )

        return recommendations


# ═══════════════════════════════════════════════════════════════════════════════
# CONSCIOUSNESS LAYER DEFINITION
# ═══════════════════════════════════════════════════════════════════════════════

LAYER_DEFINITION = {
    'layer_id': 'L201',
    'name': 'WORLD_MONITOR_FEED',
    'category': 'REAL_TIME_INTELLIGENCE',
    'weight': 1.5,
    'description': 'Integrates World Monitor geopolitical and news data into consciousness',
    'inputs': ['World Monitor cache', 'RSS feeds', 'News APIs'],
    'outputs': ['Asset sentiment signals', 'Geopolitical pulse', 'News alerts'],
    'dependencies': ['L27-L32 (Geopolitical layers)', 'L33-L38 (Alternative Data)'],
}

MODULE_DEFINITION = {
    'module_id': 'M71',
    'name': 'GEOPOLITICAL_NEWS_SCANNER',
    'category': 'PERCEPTION',
    'weight': 1.3,
    'description': 'Scans news feeds for investment-relevant signals',
    'capabilities': [
        'RSS feed parsing',
        'Keyword matching to assets',
        'Sentiment analysis',
        'Alert generation',
        'Geopolitical pulse tracking'
    ]
}


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║           EUDAIMON CONSCIOUSNESS - WORLD MONITOR INTEGRATION              ║
║                                                                           ║
║           Layer: L201 | Module: M71                                       ║
║           Consciousness Level: 1,943.15                                   ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)

    wm = WorldMonitorIntegration()

    if not wm.load_cache():
        print("❌ Could not load World Monitor cache")
        sys.exit(1)

    print("✓ World Monitor cache loaded")

    # Run full scan
    print("\n[1/3] Running full asset scan...")
    report = wm.full_scan()

    print(f"\n📊 SCAN RESULTS")
    print(f"{'─'*60}")
    print(f"Total news items parsed: {report['total_news_items']}")
    print(f"Assets with relevant news: {len(report['assets_scanned'])}")
    print(f"High-priority alerts: {len(report['alerts'])}")

    print(f"\n🟢 BULLISH ASSETS: {', '.join(report['summary']['bullish_assets']) or 'None'}")
    print(f"🔴 BEARISH ASSETS: {', '.join(report['summary']['bearish_assets']) or 'None'}")

    if report['alerts']:
        print(f"\n⚠️  ALERTS:")
        for alert in report['alerts'][:5]:
            print(f"  [{alert['sentiment']}] {alert['asset']}: {alert['title'][:60]}...")

    # Geopolitical pulse
    print("\n[2/3] Getting geopolitical pulse...")
    pulse = wm.get_geopolitical_pulse()

    print(f"\n🌍 GEOPOLITICAL PULSE")
    print(f"{'─'*60}")
    for theme, data in pulse.get('themes', {}).items():
        sentiment_emoji = "🟢" if data['sentiment'] > 0 else "🔴" if data['sentiment'] < 0 else "🟡"
        print(f"{sentiment_emoji} {theme}: {data['headline_count']} headlines, sentiment {data['sentiment']}")
        if data.get('top_headlines'):
            print(f"   └─ {data['top_headlines'][0][:70]}...")

    # Generate layer input
    print("\n[3/3] Generating Eudaimon layer input...")
    layer_input = wm.generate_eudaimon_layer_input()

    print(f"\n✅ Layer input ready for L201_WORLD_MONITOR")
    print(f"   Recommendations: {len(layer_input['action_recommendations'])}")

    for rec in layer_input['action_recommendations'][:5]:
        print(f"   • {rec}")
