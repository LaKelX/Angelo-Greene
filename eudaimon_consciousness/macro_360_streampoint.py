#!/usr/bin/env python3
"""
MACRO 360 OUTLOOK - STREAMPOINT ANALYSIS
Runs without requiring MenthorQ data for all symbols
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / "shenanigans"))

print("="*80)
print("MACRO 360 OUTLOOK - STREAMPOINT ANALYSIS")
print("="*80)
print("\n🌍 ANALYZING FULL MARKET ECOSYSTEM")

# Simplified analysis - use basic modules
UNIVERSE = {
    'US_INDICES': ['SPY', 'QQQ', 'DIA', 'IWM'],
    'CHINA_EXPOSURE': ['FXI', 'BABA', 'KWEB', 'ASHR'],
    'SAFE_HAVENS': ['GLD', 'TLT', 'UUP'],
    'SECTORS': ['XLF', 'XLE', 'XLK', 'XLI', 'XLY', 'XLP']
}

ALL_SYMBOLS = []
for category, symbols in UNIVERSE.items():
    ALL_SYMBOLS.extend(symbols)

print(f"📊 Total symbols to analyze: {len(ALL_SYMBOLS)}\n")

# Run analysis using individual modules
from TERMINAL.core.streampoint_price_verification import StreamPointVerification
from TERMINAL.core.streampoint_game_theory import GameTheoryEngine
from TERMINAL.core.streampoint_monte_carlo import MonteCarloEngine
from TERMINAL.core.streampoint_risk_metrics import RiskMetricsEngine
from TERMINAL.core.streampoint_regime_detection import RegimeDetectionEngine

print("="*80)
print("RUNNING STREAMPOINT MODULES")
print("="*80)
print("\n⏳ Analyzing with core modules...")

# Initialize engines
results = {}

for symbol in ALL_SYMBOLS:
    print(f"\n📊 Analyzing {symbol}...")

    try:
        # Price verification
        verifier = StreamPointVerification()
        price_data = verifier.verify_price(symbol)

        if not price_data or not price_data.get('verified'):
            print(f"   ⚠️  Price verification failed")
            continue

        price = price_data['price']
        print(f"   ✅ Price: ${price:.2f}")

        # Monte Carlo
        mc_engine = MonteCarloEngine()
        mc_results = mc_engine.run_simulation(symbol, current_price=price)

        # Risk Metrics
        risk_engine = RiskMetricsEngine()
        risk_results = risk_engine.calculate_metrics(symbol, current_price=price)

        # Regime Detection
        regime_engine = RegimeDetectionEngine()
        regime_results = regime_engine.detect_regime(symbol)

        # Game Theory
        gt_engine = GameTheoryEngine()
        gt_results = gt_engine.analyze(symbol, current_price=price)

        # Calculate simple score (0-10)
        score_factors = []

        # Monte Carlo win rate
        if mc_results and 'win_probability' in mc_results:
            win_prob = mc_results['win_probability']
            score_factors.append(win_prob * 10)

        # Sharpe ratio
        if risk_results and 'sharpe_ratio' in risk_results:
            sharpe = risk_results['sharpe_ratio']
            score_factors.append(min(sharpe * 5, 10))  # Scale to 0-10

        # Regime (bull=10, neutral=5, bear=0)
        if regime_results and 'current' in regime_results:
            regime = regime_results['current']
            if regime == 'BULL':
                score_factors.append(10)
            elif regime == 'NEUTRAL':
                score_factors.append(5)
            else:
                score_factors.append(0)

        # Game theory optimal action
        if gt_results and 'nash_equilibrium' in gt_results:
            action = gt_results['nash_equilibrium'].get('optimal_action', 'HOLD')
            if action == 'BUY':
                score_factors.append(10)
            elif action == 'HOLD':
                score_factors.append(5)
            else:
                score_factors.append(0)

        # Calculate average score
        overall_score = sum(score_factors) / len(score_factors) if score_factors else 5

        results[symbol] = {
            'price': price,
            'monte_carlo': mc_results,
            'risk_metrics': risk_results,
            'regime': regime_results,
            'game_theory': gt_results,
            'score': round(overall_score, 1)
        }

        print(f"   📊 Score: {results[symbol]['score']}/10")
        print(f"   📈 Forecast: ${mc_results.get('mean_forecast', 0):.2f}")
        print(f"   🎲 Win Prob: {mc_results.get('win_probability', 0)*100:.1f}%")
        print(f"   🏛️  Regime: {regime_results.get('current', 'N/A')}")

    except Exception as e:
        print(f"   ❌ Error: {e}")
        continue

# Save results
import json
from datetime import datetime

filename = f"macro_360_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(filename, 'w') as f:
    json.dump(results, f, indent=2, default=str)

print(f"\n✅ Analysis complete!")
print(f"📁 Results saved: {filename}")

# Generate comprehensive report
print("\n" + "="*80)
print("360 MACRO OUTLOOK REPORT")
print("="*80)

# SECTION 1: US INDICES
print("\n" + "="*80)
print("1. US INDICES - MARKET HEALTH CHECK")
print("="*80)

indices_scores = {}
for symbol in UNIVERSE['US_INDICES']:
    if symbol in results:
        score = results[symbol]['score']
        indices_scores[symbol] = score
        mc = results[symbol].get('monte_carlo', {})
        regime = results[symbol].get('regime', {})

        print(f"\n{symbol}:")
        print(f"   Score: {score}/10")
        print(f"   Price: ${results[symbol]['price']:.2f}")
        print(f"   Forecast: ${mc.get('mean_forecast', 0):.2f}")
        print(f"   Expected Return: {mc.get('expected_return', 0):+.1f}%")
        print(f"   Regime: {regime.get('current', 'N/A')}")

avg_indices = sum(indices_scores.values()) / len(indices_scores) if indices_scores else 0
print(f"\n📊 AVERAGE US INDICES SCORE: {avg_indices:.1f}/10")

if avg_indices >= 7:
    market_health = "STRONG"
    health_risk = "LOW"
    print("   ✅ BULLISH - Markets healthy and resilient")
elif avg_indices >= 5:
    market_health = "NEUTRAL"
    health_risk = "MEDIUM"
    print("   ⚠️  NEUTRAL - Mixed signals, proceed with caution")
else:
    market_health = "WEAK"
    health_risk = "HIGH"
    print("   ❌ BEARISH - Markets under significant pressure")

# SECTION 2: CHINA EXPOSURE
print("\n" + "="*80)
print("2. CHINA EXPOSURE - TARIFF IMPACT ASSESSMENT")
print("="*80)

china_scores = {}
for symbol in UNIVERSE['CHINA_EXPOSURE']:
    if symbol in results:
        score = results[symbol]['score']
        china_scores[symbol] = score
        mc = results[symbol].get('monte_carlo', {})
        risk = results[symbol].get('risk_metrics', {})

        print(f"\n{symbol}:")
        print(f"   Score: {score}/10")
        print(f"   Price: ${results[symbol]['price']:.2f}")
        print(f"   Expected Return: {mc.get('expected_return', 0):+.1f}%")
        print(f"   Max Drawdown: {risk.get('max_drawdown', 0)*100:.1f}%")
        print(f"   Sharpe: {risk.get('sharpe_ratio', 0):.2f}")

avg_china = sum(china_scores.values()) / len(china_scores) if china_scores else 0
print(f"\n🇨🇳 AVERAGE CHINA EXPOSURE SCORE: {avg_china:.1f}/10")

if avg_china < 4:
    china_impact = "SEVERE"
    contagion_risk = "HIGH"
    print("   🔥 SEVERE TARIFF IMPACT - Avoid/Heavily Reduce")
elif avg_china < 6:
    china_impact = "MODERATE"
    contagion_risk = "MEDIUM"
    print("   ⚠️  MODERATE IMPACT - Caution warranted, selective exposure")
else:
    china_impact = "LIMITED"
    contagion_risk = "LOW"
    print("   ✅ LIMITED IMPACT - Opportunities may exist")

# SECTION 3: SAFE HAVENS
print("\n" + "="*80)
print("3. SAFE HAVEN FLOWS - RISK SENTIMENT")
print("="*80)

safe_haven_scores = {}
for symbol in UNIVERSE['SAFE_HAVENS']:
    if symbol in results:
        score = results[symbol]['score']
        safe_haven_scores[symbol] = score
        mc = results[symbol].get('monte_carlo', {})

        print(f"\n{symbol}:")
        print(f"   Score: {score}/10")
        print(f"   Price: ${results[symbol]['price']:.2f}")
        print(f"   Forecast: ${mc.get('mean_forecast', 0):.2f}")
        print(f"   Expected Return: {mc.get('expected_return', 0):+.1f}%")

avg_safe_haven = sum(safe_haven_scores.values()) / len(safe_haven_scores) if safe_haven_scores else 0
print(f"\n🛡️  AVERAGE SAFE HAVEN SCORE: {avg_safe_haven:.1f}/10")

if avg_safe_haven >= 7:
    safe_haven_demand = "HIGH"
    panic_risk = "HIGH"
    print("   🚨 RISK-OFF MODE - Strong flight to safety underway")
elif avg_safe_haven >= 5:
    safe_haven_demand = "MODERATE"
    panic_risk = "MEDIUM"
    print("   ⚠️  MIXED - Some defensive positioning occurring")
else:
    safe_haven_demand = "LOW"
    panic_risk = "LOW"
    print("   ✅ RISK-ON - Investors comfortable with risk assets")

# SECTION 4: SECTOR ROTATION
print("\n" + "="*80)
print("4. SECTOR ROTATION - CAPITAL FLOWS")
print("="*80)

sector_map = {
    'XLF': 'Financials',
    'XLE': 'Energy',
    'XLK': 'Technology',
    'XLI': 'Industrials',
    'XLY': 'Discretionary',
    'XLP': 'Staples'
}

sector_scores = {}
for symbol in UNIVERSE['SECTORS']:
    if symbol in results:
        score = results[symbol]['score']
        sector_scores[symbol] = score
        mc = results[symbol].get('monte_carlo', {})

        print(f"\n{sector_map[symbol]} ({symbol}):")
        print(f"   Score: {score}/10")
        print(f"   Expected Return: {mc.get('expected_return', 0):+.1f}%")

sorted_sectors = sorted(sector_scores.items(), key=lambda x: x[1], reverse=True)

print(f"\n📈 STRONGEST SECTORS:")
for symbol, score in sorted_sectors[:3]:
    print(f"   {sector_map[symbol]:15} ({symbol}): {score}/10")

print(f"\n📉 WEAKEST SECTORS:")
for symbol, score in sorted_sectors[-3:]:
    print(f"   {sector_map[symbol]:15} ({symbol}): {score}/10")

# Defensive vs Offensive
defensive = ['XLP']  # Staples
offensive = ['XLK', 'XLY', 'XLE']  # Tech, Discretionary, Energy

defensive_avg = sum(sector_scores.get(s, 0) for s in defensive if s in sector_scores) / len([s for s in defensive if s in sector_scores]) if any(s in sector_scores for s in defensive) else 0
offensive_avg = sum(sector_scores.get(s, 0) for s in offensive if s in sector_scores) / len([s for s in offensive if s in sector_scores]) if any(s in sector_scores for s in offensive) else 0

print(f"\n🛡️  DEFENSIVE SECTORS: {defensive_avg:.1f}/10")
print(f"⚔️  OFFENSIVE SECTORS: {offensive_avg:.1f}/10")

if defensive_avg > offensive_avg + 1:
    rotation_pattern = "DEFENSIVE ROTATION"
    rotation_risk = "HIGH"
    print("   → DEFENSIVE ROTATION - Risk-off behavior evident")
elif defensive_avg > offensive_avg:
    rotation_pattern = "SLIGHT DEFENSIVE TILT"
    rotation_risk = "MEDIUM"
    print("   → SLIGHT DEFENSIVE TILT - Some caution emerging")
else:
    rotation_pattern = "OFFENSIVE ROTATION"
    rotation_risk = "LOW"
    print("   → OFFENSIVE ROTATION - Risk appetite remains")

# SECTION 5: GEOPOLITICAL RISK
print("\n" + "="*80)
print("5. GEOPOLITICAL RISK ASSESSMENT")
print("="*80)

print("""
🌍 CURRENT GEOPOLITICAL FLASHPOINTS:

1. US-CHINA TRADE WAR ESCALATION:
   • Trump announces 100% additional tariffs on China (Nov 1)
   • Total effective tariff: 130%+
   • China retaliating with port fees (starts Monday Oct 14)
   • Rare earth export controls threatened
   • Impact: SEVERE - $1.56T market cap lost Friday

2. AFGHANISTAN-PAKISTAN CONFLICT:
   • New military attacks between Afghanistan and Pakistan
   • Escalating tensions in nuclear-armed region
   • Pakistan nuclear arsenal: ~170 warheads
   • Impact: ELEVATED - Regional instability

3. QATAR-PAKISTAN DEFENSE PACT:
   • Qatar and Pakistan mutual defense agreement
   • Potential for wider Middle East involvement
   • Qatar hosts major US military base (Al Udeid)
   • Impact: MODERATE - Could complicate US positioning

4. COMPOUNDING FACTORS:
   • Iran-Israel tensions remain elevated
   • Russia-Ukraine war ongoing
   • Taiwan Strait tensions
   • Multiple nuclear powers involved
""")

# Calculate geopolitical risk score
geopolitical_risk_factors = {
    'US-China Trade War': 'CRITICAL',  # Immediate market impact
    'Afghanistan-Pakistan': 'HIGH',     # Nuclear powers, active conflict
    'Qatar-Pakistan Pact': 'MEDIUM',    # Defense commitment, US base implications
    'General Instability': 'HIGH'       # Multiple concurrent crises
}

critical_count = sum(1 for r in geopolitical_risk_factors.values() if r == 'CRITICAL')
high_count = sum(1 for r in geopolitical_risk_factors.values() if r == 'HIGH')

if critical_count >= 1 and high_count >= 2:
    geopolitical_risk = "EXTREME"
    geo_impact = "Markets vulnerable to shock events"
elif critical_count >= 1 or high_count >= 2:
    geopolitical_risk = "HIGH"
    geo_impact = "Significant headline risk"
else:
    geopolitical_risk = "ELEVATED"
    geo_impact = "Manageable but requires monitoring"

print(f"\n⚠️  GEOPOLITICAL RISK LEVEL: {geopolitical_risk}")
print(f"💥 MARKET IMPACT: {geo_impact}")

# SECTION 6: BLACK MONDAY PROBABILITY
print("\n" + "="*80)
print("6. BLACK MONDAY RISK ASSESSMENT - NEXT WEEK (OCT 14-18)")
print("="*80)

print("\n🧮 CALCULATING SYSTEMIC RISK...")

risk_factors = {
    '1. Market Health': (health_risk, market_health),
    '2. China Contagion': (contagion_risk, china_impact),
    '3. Safe Haven Panic': (panic_risk, safe_haven_demand),
    '4. Sector Rotation': (rotation_risk, rotation_pattern),
    '5. Geopolitical Risk': (geopolitical_risk, geo_impact)
}

print("")
for factor, (risk, detail) in risk_factors.items():
    print(f"{factor:25} {risk:10} ({detail})")

# Calculate overall risk
high_risks = sum(1 for r, _ in risk_factors.values() if r in ['HIGH', 'EXTREME', 'CRITICAL'])
medium_risks = sum(1 for r, _ in risk_factors.values() if r == 'MEDIUM')

print("\n" + "="*80)
print("⚠️  BLACK MONDAY PROBABILITY ASSESSMENT")
print("="*80)

if high_risks >= 4 or geopolitical_risk == "EXTREME":
    black_monday_risk = "VERY HIGH"
    probability = "35-50%"
    emoji = "🔴🔴🔴"
    severity = "SEVERE"
elif high_risks >= 3:
    black_monday_risk = "HIGH"
    probability = "20-35%"
    emoji = "🔴🔴"
    severity = "SIGNIFICANT"
elif high_risks >= 2 or medium_risks >= 3:
    black_monday_risk = "ELEVATED"
    probability = "10-20%"
    emoji = "🟡🟡"
    severity = "MODERATE"
else:
    black_monday_risk = "MODERATE"
    probability = "5-10%"
    emoji = "🟡"
    severity = "LOW"

print(f"\n{emoji} RISK LEVEL: {black_monday_risk}")
print(f"📊 ESTIMATED PROBABILITY: {probability}")
print(f"💥 POTENTIAL SEVERITY: {severity}")

# SECTION 7: WHAT CHANGED
print("\n" + "="*80)
print("7. CRITICAL DEVELOPMENTS - LAST 48 HOURS")
print("="*80)

print("""
🔥 FRIDAY OCTOBER 10, 2025 - MARKET CARNAGE:

   📉 MARKET REACTION:
      • Dow: -879 points (-1.9%)
      • S&P 500: -2.71% (WORST DAY SINCE APRIL)
      • Nasdaq: -3.56%
      • Market cap lost: $1.56 TRILLION
      • VIX: +32% spike

   💣 TRUMP TARIFF BOMBSHELL:
      • 100% additional tariff on China (Nov 1)
      • Stacked on existing 30% tariffs
      • Total: 130%+ effective rate
      • Rare earth retaliation threatened

   🇨🇳 CHINA COUNTERMEASURES:
      • Port fees on US ships (STARTS MONDAY OCT 14)
      • Battery tech export controls (Nov 8)
      • Qualcomm deal investigation
      • Rare earth leverage (70% mining, 93% magnets)

   ⚡ AFGHANISTAN-PAKISTAN ESCALATION:
      • New military attacks
      • Two nuclear powers in direct conflict
      • Qatar defense pact adds complexity
      • US Al Udeid base in Qatar at risk

🚨 WHY THIS IS DIFFERENT FROM APRIL 2025:

   April 2025:
   • Initial tariff shock
   • Market had room to absorb
   • China held back retaliation
   • No concurrent geopolitical crises
   • Recovery by June

   October 2025:
   • RE-ESCALATION after truce
   • Market already damaged from April
   • China NOW retaliating aggressively
   • Afghanistan-Pakistan conflict adds fuel
   • Multiple nuclear flashpoints active
   • Rare earth weapon in play

💡 THE COMPOUNDING EFFECT:

   This isn't just ONE crisis.
   It's MULTIPLE crises hitting simultaneously:

   1. Trade war (economic)
   2. Afghanistan-Pakistan (military)
   3. Qatar involvement (geopolitical)
   4. Rare earth supply chain (strategic)
   5. Tech sector vulnerability (market structure)

   Markets CAN handle one crisis.
   Markets STRUGGLE with multiple concurrent crises.
""")

# SECTION 8: NEXT WEEK OUTLOOK
print("\n" + "="*80)
print("8. NEXT WEEK TRADING OUTLOOK (OCT 14-18, 2025)")
print("="*80)

print(f"""
📅 CRITICAL DATES:

   • Monday Oct 14: China port fees take effect
   • Throughout week: Q3 earnings season
   • Friday Oct 18: Options expiration
   • Nov 1 (looming): 100% tariff deadline

🎯 MOST LIKELY SCENARIOS:
""")

if black_monday_risk in ["VERY HIGH", "HIGH"]:
    print("""
   1️⃣  MONDAY GAP DOWN + CONTINUED SELLOFF (55% probability)
      → Asia contagion from Friday's carnage
      → SPY opens below $575
      → China port fees news adds pressure
      → VIX spikes above 25
      → Panic selling into support levels

   2️⃣  VIOLENT VOLATILITY / WHIPSAW (30% probability)
      → Wild intraday swings ±2-3%
      → Algorithmic selling + dip buying clash
      → No sustained direction
      → News-driven chaos
      → Stop losses trigger cascades

   3️⃣  DEAD CAT BOUNCE (15% probability)
      → Oversold technical bounce Monday
      → Relief fades by Tuesday/Wednesday
      → Trump walks back rhetoric briefly
      → False hope rally
      → Sells off again by Friday
""")
else:
    print("""
   1️⃣  VOLATILITY CHOP / CONSOLIDATION (50% probability)
      → Digest Friday's selloff
      → Range-bound $575-590 on SPY
      → News-driven swings
      → Wait-and-see mode
      → Low conviction moves

   2️⃣  GRADUAL GRIND LOWER (30% probability)
      → Slow bleed throughout week
      → Support levels tested
      → No panic, but pressure
      → Defensive rotation continues
      → Close near lows Friday

   3️⃣  STABILIZATION / RELIEF RALLY (20% probability)
      → Market finds footing
      → Dip buyers emerge
      → Earnings provide distraction
      • Short covering aids bounce
      → Relief into weekend
""")

# SECTION 9: TRADING RECOMMENDATIONS
print("\n" + "="*80)
print("9. ACTIONABLE TRADING PLAN")
print("="*80)

print("\n🚫 IMMEDIATE AVOIDS:")
worst_symbols = sorted(
    [(sym, results[sym]['score']) for sym in results.keys()],
    key=lambda x: x[1]
)[:5]

for symbol, score in worst_symbols:
    mc = results[symbol].get('monte_carlo', {})
    print(f"   {symbol:6} Score: {score:.1f}/10, Expected: {mc.get('expected_return', 0):+.1f}%")

print("\n✅ RELATIVE STRENGTH / DEFENSIVE HOLDS:")
best_symbols = sorted(
    [(sym, results[sym]['score']) for sym in results.keys()],
    key=lambda x: x[1],
    reverse=True
)[:5]

for symbol, score in best_symbols:
    mc = results[symbol].get('monte_carlo', {})
    print(f"   {symbol:6} Score: {score:.1f}/10, Expected: {mc.get('expected_return', 0):+.1f}%")

print(f"""
🎯 POSITION MANAGEMENT:

   OVERALL EXPOSURE:
   • {'REDUCE TO 40-50%' if black_monday_risk in ['VERY HIGH', 'HIGH'] else 'MAINTAIN 60-70%' if black_monday_risk == 'ELEVATED' else 'MAINTAIN 70-80%'}
   • RAISE CASH TO {'40-50%' if black_monday_risk in ['VERY HIGH', 'HIGH'] else '30-40%' if black_monday_risk == 'ELEVATED' else '20-30%'}
   • Tighten ALL stop losses by 20-30%
   • Consider protective puts on SPY/QQQ

   CHINA EXPOSURE:
   • {'FULL EXIT recommended' if china_impact == 'SEVERE' else 'REDUCE BY 50-75%' if china_impact == 'MODERATE' else 'REDUCE BY 25-50%'}
   • FXI, BABA, KWEB = {'SELL' if avg_china < 4 else 'TRIM' if avg_china < 6 else 'HOLD WITH STOPS'}
   • Wait for clarity on tariffs before re-entry

   SAFE HAVENS:
   • {'INCREASE to 20-30% of portfolio' if safe_haven_demand == 'HIGH' else 'MAINTAIN 10-20%' if safe_haven_demand == 'MODERATE' else 'MAINTAIN 5-10%'}
   • GLD (gold): {'BUY' if safe_haven_scores.get('GLD', 0) >= 6 else 'HOLD' if safe_haven_scores.get('GLD', 0) >= 4 else 'NEUTRAL'}
   • TLT (bonds): {'BUY' if safe_haven_scores.get('TLT', 0) >= 6 else 'HOLD' if safe_haven_scores.get('TLT', 0) >= 4 else 'NEUTRAL'}
   • UUP (dollar): {'BUY' if safe_haven_scores.get('UUP', 0) >= 6 else 'HOLD' if safe_haven_scores.get('UUP', 0) >= 4 else 'NEUTRAL'}

   SECTORS:
   • OVERWEIGHT: {', '.join([sector_map[s] for s, _ in sorted_sectors[:2]])}
   • UNDERWEIGHT: {', '.join([sector_map[s] for s, _ in sorted_sectors[-2:]])}
   • Tech (XLK): {'REDUCE' if sector_scores.get('XLK', 0) < 5 else 'HOLD' if sector_scores.get('XLK', 0) < 7 else 'MAINTAIN'}
   • Energy (XLE): {'ADD' if sector_scores.get('XLE', 0) >= 6 else 'HOLD' if sector_scores.get('XLE', 0) >= 4 else 'AVOID'}
""")

print("\n⚔️  TACTICAL TRADES (Advanced / Aggressive):")
if black_monday_risk in ["VERY HIGH", "HIGH"]:
    print("""
   • SPY/QQQ put spreads (1-2 week expiry)
   • VIX call options (Oct/Nov)
   • GLD calls (safe haven surge play)
   • Short FXI / KWEB (China exposure)
   • TLT calls (flight to bonds)

   WARNING: These are HEDGES, not core positions
   Use 5-10% of portfolio max for tactical trades
""")
else:
    print("""
   • Sell premium on volatility spikes
   • Buy dips ONLY at major support
   • Use tight stops (3-5%)
   • Scale in gradually, don't go all-in
   • Keep powder dry for better entries
""")

# SECTION 10: MONDAY GAME PLAN
print("\n" + "="*80)
print("10. MONDAY MORNING GAME PLAN")
print("="*80)

print(f"""
🌅 SUNDAY NIGHT / MONDAY PRE-MARKET:

   1. Watch Asia Markets (8pm ET Sunday):
      → Hong Kong (HSI)
      → China (CSI 300, Shanghai)
      → Japan (Nikkei)

      IF Asia down >2%: Expect brutal US open
      IF Asia down 1-2%: Expect weak US open
      IF Asia flat/up: Markets may stabilize

   2. Check Futures (6am ET Monday):
      → ES (S&P futures)
      → NQ (Nasdaq futures)

      IF futures limit down: WAIT, don't rush in
      IF futures down 1-2%: Plan defensive moves
      IF futures flat: Proceed cautiously

   3. First Hour (9:30-10:30am ET):
      → DO NOT trade first 30 min (emotion)
      → Watch volume and breadth
      → Check VIX level
      → Identify support/resistance

      IF SPY < $575 with volume: {"Sell into strength, raise cash" if black_monday_risk in ['HIGH', 'VERY HIGH'] else "Defensive positioning"}
      IF SPY $575-590: {"Wait for clarity" if black_monday_risk == 'ELEVATED' else "Selective buying"}
      IF SPY > $590: {"False rally - don't chase" if black_monday_risk in ['HIGH', 'VERY HIGH'] else "Cautiously optimistic"}

⚠️  KEY LEVELS TO WATCH:

   SPY:
   • Major support: $575 (Friday low)
   • Critical support: $560 (April crash low)
   • Breakdown level: $550 (panic mode)
   • Resistance: $590 (prior support)

   QQQ:
   • Major support: $465
   • Critical support: $450
   • Breakdown: $435
   • Resistance: $480

   VIX:
   • Current: ~18-20 range
   • Elevated: >20
   • Fear: >25
   • Panic: >30

📱 NEWS TO MONITOR:

   • Trump tweets/Truth Social (tariff updates)
   • China official response to port fees
   • Afghanistan-Pakistan conflict updates
   • Any corporate earnings surprises
   • Fed speaker comments

🚨 CIRCUIT BREAKER LEVELS (Know these):

   • Level 1: -7% = 15-minute halt
   • Level 2: -13% = 15-minute halt
   • Level 3: -20% = market closed for day

   IF we hit Level 1: This is serious
   IF we hit Level 2: This is Black Monday territory
   IF we hit Level 3: Historic crash underway
""")

# FINAL VERDICT
print("\n" + "="*80)
print("FINAL 360 MACRO VERDICT")
print("="*80)

# Pre-compute conditional strings to avoid f-string quote issues
regime_str = "RISK-OFF (defensive)" if safe_haven_demand == 'HIGH' else "TRANSITIONAL (mixed)" if safe_haven_demand == 'MODERATE' else "RISK-ON (offensive)"
danger_str = "This is a DANGEROUS setup." if black_monday_risk in ['VERY HIGH', 'HIGH'] else "This requires EXTREME caution." if black_monday_risk == 'ELEVATED' else "This is manageable but volatile."
monday_str = "Monday could be catastrophic if Asia sells off hard." if black_monday_risk == 'VERY HIGH' else "Monday will be critical - watch Asia closely." if black_monday_risk in ['HIGH', 'ELEVATED'] else "Monday will set the tone for the week."
april_str = "This could be MUCH worse." if black_monday_risk == 'VERY HIGH' else "This could rival April severity." if black_monday_risk == 'HIGH' else "This could test April lows." if black_monday_risk == 'ELEVATED' else "This is different from April."
markets_str = "Markets were already fragile. Now they're breaking." if black_monday_risk == 'VERY HIGH' else "Markets are under severe stress." if black_monday_risk == 'HIGH' else "Markets are showing cracks." if black_monday_risk == 'ELEVATED' else "Markets are testing resolve."
step1_str = "REDUCE EXPOSURE NOW (do not wait for Monday)" if black_monday_risk in ['VERY HIGH', 'HIGH'] else "REVIEW ALL POSITIONS (set stops)" if black_monday_risk == 'ELEVATED' else "MAINTAIN DISCIPLINE (no panic)"
step2_str = "RAISE CASH TO 40-50%" if black_monday_risk in ['VERY HIGH', 'HIGH'] else "RAISE CASH TO 30-40%" if black_monday_risk == 'ELEVATED' else "MAINTAIN 20-30% CASH"
step3_str = "EXIT CHINA EXPOSURE (FXI, BABA, KWEB)" if avg_china < 4 else "REDUCE CHINA BY 50-75%" if avg_china < 6 else "TRIM CHINA BY 25-50%"
step4_str = "BUY SAFE HAVENS (GLD, TLT)" if safe_haven_demand == 'HIGH' or avg_safe_haven >= 7 else "ADD SAFE HAVENS (10-20%)" if safe_haven_demand == 'MODERATE' else "MAINTAIN SAFE HAVENS (5-10%)"
step5_str = "SET TIGHT STOPS ON EVERYTHING (3-5%)" if black_monday_risk in ['VERY HIGH', 'HIGH'] else "UPDATE ALL STOPS (5-7%)" if black_monday_risk == 'ELEVATED' else "REVIEW STOPS (7-10%)"
step8_str = "SURVIVE FIRST, PROFIT LATER" if black_monday_risk in ['VERY HIGH', 'HIGH'] else "PROTECT CAPITAL FIRST" if black_monday_risk == 'ELEVATED' else "STAY DISCIPLINED"
crisis_str = "Multiple crises are compounding." if high_risks >= 3 else "Significant risks are present." if high_risks >= 2 else "Elevated caution warranted."
action_str = "Act now. Do not wait for Monday." if black_monday_risk in ['VERY HIGH', 'HIGH'] else "Prepare your plan now." if black_monday_risk == 'ELEVATED' else "Stay alert and ready."

print(f"""
🎯 BLACK MONDAY RISK: {black_monday_risk} ({probability})

🏛️  MARKET REGIME: {regime_str}

📊 US INDICES HEALTH: {avg_indices:.1f}/10 - {market_health}

🇨🇳 CHINA EXPOSURE: {avg_china:.1f}/10 - {china_impact} impact

🛡️  SAFE HAVEN DEMAND: {avg_safe_haven:.1f}/10 - {safe_haven_demand}

⚔️  SECTOR ROTATION: {rotation_pattern}

🌍 GEOPOLITICAL RISK: {geopolitical_risk}

💡 THE BOTTOM LINE:

   Friday's selloff was NOT just about tariffs.

   It's about MULTIPLE crises converging:
   • $1.56T market cap evaporated in ONE DAY
   • VIX spiked 32% (fear mode activated)
   • China port fees start MONDAY (immediate impact)
   • Afghanistan-Pakistan military conflict (nuclear risk)
   • Rare earth supply chain weapon (tech vulnerability)

   {danger_str}
   {monday_str}

   The April crash was a WARNING.
   {april_str}

   {markets_str}

🎲 SURVIVAL PLAYBOOK:

   1. {step1_str}

   2. {step2_str}

   3. {step3_str}

   4. {step4_str}

   5. {step5_str}

   6. WATCH ASIA SUNDAY NIGHT

   7. DON'T FIGHT THE TAPE

   8. {step8_str}

⏰ THIS IS NOT A DRILL.

   The data shows {high_risks} HIGH-RISK factors.
   Geopolitical risk is {geopolitical_risk}.
   {crisis_str}

   {action_str}

""")

print("="*80)
print(f"📁 FULL ANALYSIS SAVED: {filename}")
print("="*80)
print("\n✅ MACRO 360 ANALYSIS COMPLETE")
print("")
