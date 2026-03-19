"""
EUDAIMON LIVE TRACKER - Data Fetcher
Fetches real-time prices, technical indicators, and news
"""

import yfinance as yf
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import time
from config import TRACKED_ASSETS, API_CONFIG, NEWS_SOURCES


class DataFetcher:
    """Fetches market data and news for tracked assets"""

    def __init__(self):
        self.cache = {}
        self.last_update = {}

    def get_stock_data(self, symbol: str) -> Dict:
        """
        Fetch current price, technicals, and basic data for a symbol
        """
        try:
            ticker = yf.Ticker(symbol)

            # Get current data
            info = ticker.info
            hist = ticker.history(period="3mo")

            if hist.empty:
                return {"error": f"No data for {symbol}"}

            # Current price
            current_price = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price

            # Calculate RSI (14-period)
            rsi = self._calculate_rsi(hist['Close'], 14)

            # Calculate moving averages
            sma_20 = hist['Close'].tail(20).mean()
            sma_50 = hist['Close'].tail(50).mean() if len(hist) >= 50 else sma_20

            # Volume analysis
            avg_volume = hist['Volume'].tail(20).mean()
            current_volume = hist['Volume'].iloc[-1]
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1

            # Price changes
            change_1d = ((current_price - prev_close) / prev_close) * 100
            change_5d = ((current_price - hist['Close'].iloc[-5]) / hist['Close'].iloc[-5]) * 100 if len(hist) >= 5 else 0
            change_1m = ((current_price - hist['Close'].iloc[-21]) / hist['Close'].iloc[-21]) * 100 if len(hist) >= 21 else 0

            # 52-week high/low
            high_52w = hist['High'].max()
            low_52w = hist['Low'].min()
            pct_from_high = ((current_price - high_52w) / high_52w) * 100

            return {
                "symbol": symbol,
                "price": round(current_price, 2),
                "change_1d": round(change_1d, 2),
                "change_5d": round(change_5d, 2),
                "change_1m": round(change_1m, 2),
                "rsi": round(rsi, 1),
                "sma_20": round(sma_20, 2),
                "sma_50": round(sma_50, 2),
                "above_sma_20": current_price > sma_20,
                "above_sma_50": current_price > sma_50,
                "volume_ratio": round(volume_ratio, 2),
                "high_52w": round(high_52w, 2),
                "low_52w": round(low_52w, 2),
                "pct_from_high": round(pct_from_high, 1),
                "market_cap": info.get("marketCap", 0),
                "sector": info.get("sector", "Unknown"),
                "last_update": datetime.now().isoformat()
            }

        except Exception as e:
            return {"symbol": symbol, "error": str(e)}

    def _calculate_rsi(self, prices, period: int = 14) -> float:
        """Calculate RSI indicator"""
        if len(prices) < period + 1:
            return 50.0  # Default neutral

        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return rsi.iloc[-1] if not rsi.empty else 50.0

    def get_news(self, symbol: str, keywords: List[str]) -> List[Dict]:
        """
        Fetch recent news for a symbol/keywords
        Uses free RSS feeds and news APIs
        """
        news_items = []

        try:
            # Use yfinance news
            ticker = yf.Ticker(symbol)
            yf_news = ticker.news

            if yf_news:
                for article in yf_news[:5]:  # Last 5 articles
                    news_items.append({
                        "title": article.get("title", ""),
                        "publisher": article.get("publisher", ""),
                        "link": article.get("link", ""),
                        "timestamp": datetime.fromtimestamp(
                            article.get("providerPublishTime", time.time())
                        ).isoformat(),
                        "sentiment": self._analyze_sentiment(article.get("title", ""))
                    })

        except Exception as e:
            pass  # Silent fail, return empty news

        return news_items

    def _analyze_sentiment(self, text: str) -> float:
        """
        Basic sentiment analysis on news headline
        Returns: 0.0 (bearish) to 1.0 (bullish)
        """
        if not text:
            return 0.5

        text_lower = text.lower()

        # Bullish keywords
        bullish = ["surge", "soar", "jump", "rally", "gain", "rise", "up", "buy",
                   "bullish", "growth", "record", "high", "strong", "beat",
                   "upgrade", "outperform", "opportunity", "demand", "shortage"]

        # Bearish keywords
        bearish = ["fall", "drop", "crash", "plunge", "sink", "down", "sell",
                   "bearish", "decline", "low", "weak", "miss", "downgrade",
                   "underperform", "risk", "fear", "concern", "warning", "cut"]

        bullish_count = sum(1 for word in bullish if word in text_lower)
        bearish_count = sum(1 for word in bearish if word in text_lower)

        total = bullish_count + bearish_count
        if total == 0:
            return 0.5

        return round(bullish_count / total, 2)

    def get_all_data(self) -> Dict[str, Dict]:
        """Fetch data for all tracked assets"""
        all_data = {}

        for symbol, asset_info in TRACKED_ASSETS.items():
            print(f"Fetching data for {symbol}...")

            # Get stock data
            stock_data = self.get_stock_data(symbol)

            # Get news
            news = self.get_news(symbol, asset_info.get("keywords", []))

            # Combine
            all_data[symbol] = {
                **asset_info,
                **stock_data,
                "news": news,
                "news_sentiment": self._aggregate_news_sentiment(news)
            }

        return all_data

    def _aggregate_news_sentiment(self, news: List[Dict]) -> float:
        """Calculate average sentiment from news articles"""
        if not news:
            return 0.5

        sentiments = [article.get("sentiment", 0.5) for article in news]
        return round(sum(sentiments) / len(sentiments), 2)


if __name__ == "__main__":
    # Test the fetcher
    fetcher = DataFetcher()
    data = fetcher.get_stock_data("NTR")
    print(json.dumps(data, indent=2))
