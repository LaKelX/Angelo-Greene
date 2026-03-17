"""
EUDAIMON LIVE TRACKER - Signal Engine
Determines RED / YELLOW / GREEN signals for each asset
"""

from typing import Dict, Tuple
from config import SIGNAL_CONFIG, SIGNAL_MEANINGS, TRACKED_ASSETS


class SignalEngine:
    """
    Calculates buy/hold/avoid signals based on:
    1. Technical indicators (RSI, moving averages, volume)
    2. News sentiment
    3. Price action (pullbacks, breakouts)
    4. Thesis alignment
    """

    def __init__(self):
        self.config = SIGNAL_CONFIG

    def calculate_signal(self, asset_data: Dict) -> Tuple[str, int, Dict]:
        """
        Calculate signal for a single asset

        Returns:
            signal: "GREEN", "YELLOW", or "RED"
            score: 0-100 conviction score
            breakdown: dict with reasoning
        """
        if "error" in asset_data:
            return "YELLOW", 50, {"error": asset_data.get("error")}

        # Initialize scoring
        scores = {
            "technical": 0,
            "sentiment": 0,
            "momentum": 0,
            "value": 0
        }
        reasons = []

        # ═══════════════════════════════════════════════════════════════════
        # 1. RSI ANALYSIS (25 points max)
        # ═══════════════════════════════════════════════════════════════════
        rsi = asset_data.get("rsi", 50)

        if rsi <= self.config["rsi_oversold"]:
            scores["technical"] += 25
            reasons.append(f"RSI oversold at {rsi} - strong buy signal")
        elif rsi <= self.config["rsi_neutral_low"]:
            scores["technical"] += 18
            reasons.append(f"RSI approaching oversold at {rsi}")
        elif rsi >= self.config["rsi_overbought"]:
            scores["technical"] -= 15
            reasons.append(f"RSI overbought at {rsi} - caution")
        elif rsi >= self.config["rsi_neutral_high"]:
            scores["technical"] += 5
            reasons.append(f"RSI neutral-high at {rsi}")
        else:
            scores["technical"] += 12
            reasons.append(f"RSI neutral at {rsi}")

        # ═══════════════════════════════════════════════════════════════════
        # 2. MOVING AVERAGE ANALYSIS (20 points max)
        # ═══════════════════════════════════════════════════════════════════
        above_sma_20 = asset_data.get("above_sma_20", False)
        above_sma_50 = asset_data.get("above_sma_50", False)

        if above_sma_20 and above_sma_50:
            scores["technical"] += 15
            reasons.append("Price above both 20 & 50 SMA - uptrend intact")
        elif above_sma_20:
            scores["technical"] += 10
            reasons.append("Price above 20 SMA, testing 50 SMA")
        elif above_sma_50:
            scores["technical"] += 5
            reasons.append("Price below 20 SMA but holding 50 SMA")
        else:
            scores["technical"] -= 5
            reasons.append("Price below both SMAs - downtrend")

        # ═══════════════════════════════════════════════════════════════════
        # 3. PULLBACK / BREAKOUT ANALYSIS (15 points max)
        # ═══════════════════════════════════════════════════════════════════
        pct_from_high = asset_data.get("pct_from_high", 0)
        change_5d = asset_data.get("change_5d", 0)

        # Pullback entry opportunity
        if pct_from_high <= -15:
            scores["value"] += 15
            reasons.append(f"Deep pullback: {pct_from_high}% from 52w high - potential value")
        elif pct_from_high <= -10:
            scores["value"] += 10
            reasons.append(f"Moderate pullback: {pct_from_high}% from high")
        elif pct_from_high <= -5:
            scores["value"] += 5
            reasons.append(f"Slight pullback: {pct_from_high}% from high")
        elif pct_from_high >= -2:
            scores["value"] -= 5
            reasons.append(f"Near 52w high: {pct_from_high}% - less upside room")

        # Recent momentum
        if change_5d >= 5:
            scores["momentum"] += 10
            reasons.append(f"Strong 5-day momentum: +{change_5d}%")
        elif change_5d >= 2:
            scores["momentum"] += 5
            reasons.append(f"Positive 5-day momentum: +{change_5d}%")
        elif change_5d <= -5:
            scores["momentum"] -= 5
            reasons.append(f"Weak 5-day momentum: {change_5d}%")

        # ═══════════════════════════════════════════════════════════════════
        # 4. VOLUME ANALYSIS (10 points max)
        # ═══════════════════════════════════════════════════════════════════
        volume_ratio = asset_data.get("volume_ratio", 1)

        if volume_ratio >= self.config["volume_spike"]:
            # High volume - could be good or bad depending on direction
            if asset_data.get("change_1d", 0) > 0:
                scores["technical"] += 10
                reasons.append(f"High volume rally: {volume_ratio}x average")
            else:
                scores["technical"] -= 5
                reasons.append(f"High volume selloff: {volume_ratio}x average - caution")
        elif volume_ratio < 0.5:
            reasons.append(f"Low volume: {volume_ratio}x average - low conviction move")

        # ═══════════════════════════════════════════════════════════════════
        # 5. NEWS SENTIMENT ANALYSIS (20 points max)
        # ═══════════════════════════════════════════════════════════════════
        sentiment = asset_data.get("news_sentiment", 0.5)

        if sentiment >= self.config["sentiment_bullish"]:
            scores["sentiment"] += 20
            reasons.append(f"Bullish news sentiment: {sentiment}")
        elif sentiment >= 0.5:
            scores["sentiment"] += 10
            reasons.append(f"Neutral-positive news sentiment: {sentiment}")
        elif sentiment <= self.config["sentiment_bearish"]:
            scores["sentiment"] -= 10
            reasons.append(f"Bearish news sentiment: {sentiment}")
        else:
            scores["sentiment"] += 5
            reasons.append(f"Neutral news sentiment: {sentiment}")

        # ═══════════════════════════════════════════════════════════════════
        # 6. CALCULATE FINAL SCORE & SIGNAL
        # ═══════════════════════════════════════════════════════════════════
        total_score = sum(scores.values())

        # Normalize to 0-100
        # Max theoretical score: 25 + 20 + 15 + 10 + 10 + 20 = 100
        # Min theoretical score: -15 - 5 - 5 - 5 - 10 = -40
        normalized_score = min(100, max(0, total_score + 40))  # Shift and cap

        # Determine signal
        if normalized_score >= 70:
            signal = "GREEN"
        elif normalized_score >= 45:
            signal = "YELLOW"
        else:
            signal = "RED"

        breakdown = {
            "scores": scores,
            "total_raw": total_score,
            "normalized": normalized_score,
            "reasons": reasons,
            "signal_meaning": SIGNAL_MEANINGS[signal]
        }

        return signal, normalized_score, breakdown

    def calculate_all_signals(self, all_data: Dict) -> Dict[str, Dict]:
        """Calculate signals for all tracked assets"""
        signals = {}

        for symbol, data in all_data.items():
            signal, score, breakdown = self.calculate_signal(data)

            signals[symbol] = {
                "symbol": symbol,
                "name": data.get("name", symbol),
                "category": data.get("category", "Unknown"),
                "thesis": data.get("thesis", ""),
                "signal": signal,
                "score": score,
                "price": data.get("price", 0),
                "change_1d": data.get("change_1d", 0),
                "rsi": data.get("rsi", 50),
                "breakdown": breakdown,
                "news": data.get("news", [])[:3],  # Top 3 news
                "last_update": data.get("last_update", "")
            }

        return signals

    def get_signal_summary(self, signals: Dict) -> Dict:
        """Get summary counts of signals by category"""
        summary = {
            "GREEN": [],
            "YELLOW": [],
            "RED": [],
            "by_category": {}
        }

        for symbol, data in signals.items():
            signal = data["signal"]
            category = data["category"]

            summary[signal].append(symbol)

            if category not in summary["by_category"]:
                summary["by_category"][category] = {"GREEN": [], "YELLOW": [], "RED": []}

            summary["by_category"][category][signal].append(symbol)

        return summary


if __name__ == "__main__":
    # Test the signal engine
    from data_fetcher import DataFetcher
    import json

    fetcher = DataFetcher()
    engine = SignalEngine()

    # Test single asset
    data = fetcher.get_stock_data("NTR")
    data["news_sentiment"] = 0.6  # Mock sentiment
    data["news"] = []

    signal, score, breakdown = engine.calculate_signal(data)
    print(f"\nNTR Signal: {signal} (Score: {score})")
    print(json.dumps(breakdown, indent=2))
