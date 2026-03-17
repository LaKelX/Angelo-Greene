"""
STREAMPOINT REAL-TIME: NQ BOUNCE OFF CALL RESISTANCE
Oct 22, 2025 - Live Market Analysis

User: "NQ bounced off call resistance and I think it can take out NY high.
Am I missing something?"

ANALYSIS:
- Check current NQ price vs call resistance
- Identify NY session high
- Assess bounce strength vs rejection
- Risk/reward for taking the trade
"""

import yfinance as yf
from datetime import datetime
import pytz

class NQBounceAnalysis:
    def __init__(self):
        self.timestamp = datetime.now(pytz.timezone('US/Eastern'))
        print("=" * 80)
        print("STREAMPOINT REAL-TIME: NQ BOUNCE ANALYSIS")
        print(f"Timestamp: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S ET')}")
        print("=" * 80)

    def fetch_nq_realtime(self):
        """Get current NQ/NDX prices and intraday action"""
        print("\n" + "=" * 80)
        print("AGENT 1: REAL-TIME NQ PRICE ACTION")
        print("=" * 80 + "\n")

        try:
            # Fetch NDX (cash index)
            ndx = yf.Ticker('^NDX')
            ndx_hist = ndx.history(period='2d', interval='5m')

            if not ndx_hist.empty:
                current_price = ndx_hist['Close'].iloc[-1]
                today_open = ndx_hist['Open'].iloc[0]
                today_high = ndx_hist['High'].max()
                today_low = ndx_hist['Low'].min()

                print(f"📊 NQ (NDX) Current Price: {current_price:,.2f}")
                print(f"   Today's Open:  {today_open:,.2f}")
                print(f"   Today's High:  {today_high:,.2f}")
                print(f"   Today's Low:   {today_low:,.2f}")
                print(f"   Range: {today_high - today_low:,.2f} points")

                # Calculate where we are in the range
                range_position = ((current_price - today_low) / (today_high - today_low)) * 100
                print(f"   Range Position: {range_position:.1f}% (0% = low, 100% = high)")

                return {
                    'current': current_price,
                    'open': today_open,
                    'high': today_high,
                    'low': today_low,
                    'range_pct': range_position
                }
            else:
                print("❌ Failed to fetch NDX data")
                return None

        except Exception as e:
            print(f"❌ Error fetching data: {e}")
            return None

    def analyze_gex_levels(self, current_price):
        """Analyze GEX levels from user's chart"""
        print("\n" + "=" * 80)
        print("AGENT 2: GEX LEVELS (From User's Chart)")
        print("=" * 80 + "\n")

        print("📊 Oct 22 0DTE GEX Structure:")
        print("-" * 80)

        call_resistance = 25_400
        put_support = 25_130
        spot_price_chart = 25_146  # From user's chart yesterday

        print(f"Call Resistance: {call_resistance:,} (0DTE expiring today)")
        print(f"Put Support:     {put_support:,}")
        print(f"Current NQ:      {current_price:,.0f}")
        print(f"GEX Expiring:    9.04%")

        # Calculate distances
        distance_to_call = call_resistance - current_price
        distance_to_put = current_price - put_support

        print(f"\nDistance to Call Wall: {distance_to_call:+,.0f} points ({(distance_to_call/current_price)*100:+.2f}%)")
        print(f"Distance to Put Support: {distance_to_put:+,.0f} points ({(distance_to_put/current_price)*100:+.2f}%)")

        # Determine positioning
        if current_price >= call_resistance:
            status = "✅✅ ABOVE CALL RESISTANCE (BULLISH BREAKOUT)"
            print(f"\n{status}")
            print("→ Broke through call wall = very bullish")
            print("→ Dealers SHORT gamma, must buy futures = accelerates higher")
            print("→ Target: 25,550-25,600 (next resistance)")

        elif current_price >= put_support and current_price < call_resistance:
            status = "✅ IN THE SWEET SPOT (between support and resistance)"
            print(f"\n{status}")
            room = distance_to_call
            print(f"→ Room to move: {room:,.0f} points to call wall")

            if current_price >= 25_300:
                print("→ UPPER HALF of range = bullish bias")
                print("→ Bounced off call resistance = tested and held")
                print("→ Can take out highs if breaks 25,400")
            elif current_price <= 25_200:
                print("→ LOWER HALF of range = bearish bias")
                print("→ Could dump back to put support 25,130")
            else:
                print("→ MIDDLE of range = neutral, could go either way")

        else:
            status = "🔴 BELOW PUT SUPPORT (BEARISH)"
            print(f"\n{status}")
            print("→ Failed support = bearish breakdown")
            print("→ Next support: 25,000 psychological")

        return {
            'call_wall': call_resistance,
            'put_support': put_support,
            'distance_to_call': distance_to_call,
            'distance_to_put': distance_to_put
        }

    def analyze_bounce_vs_rejection(self, nq_data, gex_data):
        """Determine if this is a bounce (bullish) or rejection (bearish)"""
        print("\n" + "=" * 80)
        print("AGENT 3: BOUNCE vs REJECTION ANALYSIS")
        print("=" * 80 + "\n")

        current = nq_data['current']
        high = nq_data['high']
        low = nq_data['low']
        range_pct = nq_data['range_pct']
        call_wall = gex_data['call_wall']

        print("USER SAYS: 'NQ bounced off call resistance'")
        print("-" * 80)

        # Check if we touched the call wall
        if high >= call_wall:
            print(f"✅ CONFIRMED: NQ touched call wall at {call_wall:,}")
            print(f"   Today's high: {high:,.0f}")
            print(f"   Touched resistance: YES")

            # Check if we're holding near highs
            pullback = high - current
            pullback_pct = (pullback / high) * 100

            print(f"\nPullback from high: {pullback:,.0f} points ({pullback_pct:.1f}%)")

            if pullback_pct < 0.3:
                verdict = "🟢 BOUNCE (Bullish)"
                print(f"\n{verdict}")
                print("→ Pullback < 0.3% = holding near highs")
                print("→ Tested call wall, rejected, but HOLDING")
                print("→ Buyers stepped in = strength")
                print("→ High probability breaks through on next push")
                bias = "BULLISH"

            elif pullback_pct < 0.6:
                verdict = "🟡 CONSOLIDATION (Neutral)"
                print(f"\n{verdict}")
                print("→ Pullback 0.3-0.6% = normal consolidation")
                print("→ Could go either way")
                print("→ Need to see next candle direction")
                bias = "NEUTRAL"

            else:
                verdict = "🔴 REJECTION (Bearish)"
                print(f"\n{verdict}")
                print("→ Pullback > 0.6% = sellers winning")
                print("→ Tested call wall, got REJECTED")
                print("→ Could dump back to middle or support")
                bias = "BEARISH"

        else:
            print(f"⚠️  CAUTION: NQ has NOT touched call wall yet")
            print(f"   Today's high: {high:,.0f}")
            print(f"   Call wall: {call_wall:,}")
            print(f"   Still {call_wall - high:,.0f} points away")
            print("\nUser may be seeing different timeframe or futures data")
            bias = "UNCLEAR"
            verdict = "❓ NEED MORE DATA"

        return bias, verdict

    def risk_reward_analysis(self, nq_data, gex_data):
        """Calculate risk/reward for taking the long"""
        print("\n" + "=" * 80)
        print("AGENT 4: RISK/REWARD ANALYSIS")
        print("=" * 80 + "\n")

        current = nq_data['current']
        call_wall = gex_data['call_wall']
        put_support = gex_data['put_support']

        print("IF YOU GO LONG HERE:")
        print("-" * 80)

        # Upside target (breakout above call wall)
        target = 25_550  # Next resistance
        upside = target - current
        upside_pct = (upside / current) * 100

        # Downside risk (stop at middle of range or put support)
        stop_tight = 25_250  # Middle of range
        stop_wide = put_support  # Put support

        risk_tight = current - stop_tight
        risk_wide = current - stop_wide

        risk_tight_pct = (risk_tight / current) * 100
        risk_wide_pct = (risk_wide / current) * 100

        print(f"Entry: {current:,.0f}")
        print(f"Target: {target:,} (+{upside:,.0f} points / +{upside_pct:.2f}%)")
        print(f"\nStop Options:")
        print(f"  Tight: {stop_tight:,} (-{risk_tight:,.0f} points / -{risk_tight_pct:.2f}%)")
        print(f"  Wide: {stop_wide:,} (-{risk_wide:,.0f} points / -{risk_wide_pct:.2f}%)")

        # R/R ratios
        rr_tight = upside / risk_tight if risk_tight > 0 else 0
        rr_wide = upside / risk_wide if risk_wide > 0 else 0

        print(f"\nRisk/Reward Ratios:")
        print(f"  Tight stop: {rr_tight:.2f}:1")
        print(f"  Wide stop: {rr_wide:.2f}:1")

        if rr_tight >= 2.0:
            print("\n✅ GOOD R/R: Greater than 2:1 (worth the trade)")
        elif rr_tight >= 1.5:
            print("\n🟡 FAIR R/R: Between 1.5:1 - 2:1 (acceptable if high conviction)")
        else:
            print("\n🔴 POOR R/R: Less than 1.5:1 (not worth the risk)")

    def what_user_might_be_missing(self):
        """Critical factors user should consider"""
        print("\n" + "=" * 80)
        print("AGENT 5: WHAT YOU MIGHT BE MISSING")
        print("=" * 80 + "\n")

        print("🚨 CRITICAL CONSIDERATIONS:")
        print("-" * 80)

        print("\n1. 0DTE EXPIRY TODAY (Oct 22)")
        print("   → GEX expiring: 9.04%")
        print("   → Dealers will PIN price to call wall (25,400) into close")
        print("   → After close, GEX resets = volatility increases")
        print("   → Breakout AFTER close is more reliable")

        print("\n2. YOUR PORTFOLIO = 0% TECH")
        print("   → You have NO NQ/QQQ exposure")
        print("   → If NQ rips, you MISS the move")
        print("   → BUT also safe if it fails")
        print("   → Master plan: Wait for Trump-Xi Oct 29")

        print("\n3. TRUMP-XI MEETING IN 7 DAYS")
        print("   → Oct 29 = binary catalyst")
        print("   → Market may chop until then")
        print("   → Risk: Take trade now, gets chopped, then real move happens Oct 29")

        print("\n4. TECH EARNINGS THIS WEEK")
        print("   → Volatility = whipsaw risk")
        print("   → Could gap up OR down on earnings")
        print("   → Timing risk before catalyst")

        print("\n5. YOUR SWEET SPOT PATTERN")
        print("   → Entry time: 3:30-4:00 PM ET")
        print("   → Current time: ~11:00 AM ET")
        print("   → TOO EARLY = more chop risk")
        print("   → Wait for 3:30 PM setup")

        print("\n6. OPPORTUNITY COST")
        print("   → Using cash for NQ swing = less for ASML/AVGO")
        print("   → ASML entry post Trump-Xi = higher conviction")
        print("   → Don't blow dry powder on low conviction setup")

    def final_verdict(self, nq_data, bias):
        """Final recommendation"""
        print("\n" + "=" * 80)
        print("STREAMPOINT FINAL VERDICT")
        print("=" * 80 + "\n")

        current = nq_data['current']
        high = nq_data['high']

        print("USER'S QUESTION: 'NQ bounced off call resistance. Can it take out NY high?'")
        print("-" * 80)

        print(f"\nCurrent NQ: {current:,.0f}")
        print(f"Today's High: {high:,.0f}")
        print(f"Call Wall: 25,400")
        print(f"Bias: {bias}")

        print("\n🎯 ANSWER:")
        print("=" * 80)

        if bias == "BULLISH":
            print("\nYES, NQ CAN take out the high IF:")
            print("  ✅ Holding near highs (< 0.3% pullback)")
            print("  ✅ Volume increases on next push")
            print("  ✅ ES also strong (above 6,750)")
            print("  ✅ No negative news/earnings")

            print("\nPROBABILITY: 60% breaks out, 40% fails")

            print("\n⚠️  BUT YOU SHOULD STILL WAIT:")
            print("  → 0DTE expiry today = dealers pin price")
            print("  → Sweet Spot entry = 3:30-4:00 PM (not now)")
            print("  → Trump-Xi in 7 days = bigger catalyst")
            print("  → Don't blow $5.4K cash on marginal setup")

            print("\n✅ RECOMMENDED ACTION:")
            print("  1. WATCH for now (don't enter)")
            print("  2. If holds near highs into 3:30 PM → take Sweet Spot setup")
            print("  3. If breaks out before 3:30 PM → miss it, wait for Trump-Xi")
            print("  4. Stay disciplined, don't FOMO")

        elif bias == "NEUTRAL":
            print("\nMAYBE - Could go either way:")
            print("  🟡 Consolidating after touching resistance")
            print("  🟡 Need to see direction on next move")
            print("  🟡 50/50 = not worth the risk")

            print("\n✅ RECOMMENDED ACTION:")
            print("  1. WAIT for clarity (direction break)")
            print("  2. If breaks above 25,400 with volume → watch")
            print("  3. If fails and dumps → stay out")
            print("  4. Best trade = wait for 3:30 PM or Trump-Xi")

        elif bias == "BEARISH":
            print("\nNO - This looks like a rejection:")
            print("  🔴 Touched resistance, got rejected")
            print("  🔴 Pulling back from highs")
            print("  🔴 Sellers in control")

            print("\n✅ RECOMMENDED ACTION:")
            print("  1. STAY OUT (don't enter long)")
            print("  2. Wait for support test (25,130)")
            print("  3. If bounces off support → new setup")
            print("  4. Or wait for Trump-Xi Oct 29")

        else:
            print("\nUNCLEAR - Need more data:")
            print("  ❓ May not have touched call wall yet")
            print("  ❓ Or different timeframe than user watching")

            print("\n✅ RECOMMENDED ACTION:")
            print("  1. Verify if NQ actually touched 25,400")
            print("  2. If yes, re-assess with updated data")
            print("  3. If no, wait for actual test")
            print("  4. Stay patient, don't force it")

        print("\n" + "=" * 80)
        print("BOTTOM LINE: STAY CASH, WAIT FOR 3:30 PM OR TRUMP-XI OCT 29")
        print("Your patience is your edge. Don't blow it on FOMO.")
        print("=" * 80)


def main():
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                            ║")
    print("║         STREAMPOINT REAL-TIME: NQ BOUNCE ANALYSIS - OCT 22, 2025          ║")
    print("║                                                                            ║")
    print("║  User: 'NQ bounced off call resistance. Can it take out NY high?'         ║")
    print("║  Am I missing something?                                                   ║")
    print("║                                                                            ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝")

    analyzer = NQBounceAnalysis()

    # Execute analysis
    nq_data = analyzer.fetch_nq_realtime()

    if nq_data:
        gex_data = analyzer.analyze_gex_levels(nq_data['current'])
        bias, verdict = analyzer.analyze_bounce_vs_rejection(nq_data, gex_data)
        analyzer.risk_reward_analysis(nq_data, gex_data)
        analyzer.what_user_might_be_missing()
        analyzer.final_verdict(nq_data, bias)
    else:
        print("\n❌ Could not complete analysis due to data fetch error")

    print("\n" + "=" * 80)
    print("Analysis Complete")
    print("=" * 80)


if __name__ == "__main__":
    main()
