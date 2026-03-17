#!/usr/bin/env python3
"""Quick Macro Analysis - Get the key metrics fast"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path.home() / "shenanigans"))

from TERMINAL.core.streampoint_price_verification import StreamPointVerification
from TERMINAL.core.streampoint_monte_carlo import MonteCarloEngine

symbols = {
    'US_INDICES': ['SPY', 'QQQ', 'DIA', 'IWM'],
    'CHINA': ['FXI', 'BABA', 'KWEB', 'ASHR'],
    'SAFE_HAVENS': ['GLD', 'TLT', 'UUP'],
    'SECTORS': ['XLF', 'XLE', 'XLK', 'XLI', 'XLY', 'XLP']
}

print('='*80)
print('MACRO 360 - STREAMPOINT QUICK ANALYSIS')
print('='*80)
print()

results = {}

for category, sym_list in symbols.items():
    print(f'\n{category}:')
    print('-'*80)

    for sym in sym_list:
        try:
            verifier = StreamPointVerification()
            price_data = verifier.verify_price(sym)

            if price_data and price_data.get('verified'):
                price = price_data['price']

                mc_engine = MonteCarloEngine()
                mc = mc_engine.run_simulation(sym, current_price=price)

                win_prob = mc.get('win_probability', 0.5) if mc else 0.5
                expected_ret = mc.get('expected_return', 0) if mc else 0

                score = round(win_prob * 10, 1)

                results[sym] = {
                    'category': category,
                    'price': price,
                    'win_prob': win_prob,
                    'expected_return': expected_ret,
                    'score': score
                }

                print(f'{sym:6} ${price:7.2f}  Score: {score}/10  Expected: {expected_ret:+.1f}%  Win: {win_prob*100:.1f}%')
        except Exception as e:
            print(f'{sym:6} ERROR: {str(e)[:60]}')

# Calculate category averages
print('\n' + '='*80)
print('CATEGORY SCORES')
print('='*80)

for category in symbols.keys():
    cat_results = [v for k,v in results.items() if v['category'] == category]
    if cat_results:
        avg_score = sum(r['score'] for r in cat_results) / len(cat_results)
        avg_return = sum(r['expected_return'] for r in cat_results) / len(cat_results)
        print(f'\n{category:20} {avg_score:.1f}/10  Avg Expected Return: {avg_return:+.1f}%')

        if avg_score < 4:
            risk = "HIGH RISK - AVOID"
        elif avg_score < 6:
            risk = "MODERATE RISK - CAUTION"
        else:
            risk = "LOW RISK - FAVORABLE"
        print(f'                     {risk}')

# BLACK MONDAY ASSESSMENT
print('\n' + '='*80)
print('BLACK MONDAY RISK ASSESSMENT')
print('='*80)

us_indices = [v for k,v in results.items() if k in ['SPY', 'QQQ', 'DIA', 'IWM']]
china_exp = [v for k,v in results.items() if k in ['FXI', 'BABA', 'KWEB', 'ASHR']]
safe_havens = [v for k,v in results.items() if k in ['GLD', 'TLT', 'UUP']]

us_avg = sum(r['score'] for r in us_indices) / len(us_indices) if us_indices else 5
china_avg = sum(r['score'] for r in china_exp) / len(china_exp) if china_exp else 5
safe_avg = sum(r['score'] for r in safe_havens) / len(safe_havens) if safe_havens else 5

print(f'\nMarket Health (US Indices): {us_avg:.1f}/10')
print(f'China Contagion Risk: {10 - china_avg:.1f}/10 (lower China score = higher risk)')
print(f'Safe Haven Demand: {safe_avg:.1f}/10')

# Geopolitical risk (manual based on news)
geo_risk = "EXTREME"  # US-China trade war + Afghanistan-Pakistan
print(f'Geopolitical Risk: {geo_risk}')

# Calculate overall risk
risk_score = 0

if us_avg < 5:
    risk_score += 2  # Market health poor
elif us_avg < 7:
    risk_score += 1

if china_avg < 4:
    risk_score += 2  # China severe
elif china_avg < 6:
    risk_score += 1

if safe_avg > 7:
    risk_score += 2  # Flight to safety
elif safe_avg > 5:
    risk_score += 1

if geo_risk == "EXTREME":
    risk_score += 2

print(f'\nOverall Risk Score: {risk_score}/8')

if risk_score >= 6:
    black_monday_risk = "VERY HIGH"
    probability = "35-50%"
    action = "REDUCE EXPOSURE NOW - RAISE 40-50% CASH"
elif risk_score >= 4:
    black_monday_risk = "HIGH"
    probability = "20-35%"
    action = "REDUCE EXPOSURE - RAISE 30-40% CASH"
elif risk_score >= 2:
    black_monday_risk = "ELEVATED"
    probability = "10-20%"
    action = "REVIEW POSITIONS - RAISE 20-30% CASH"
else:
    black_monday_risk = "MODERATE"
    probability = "5-10%"
    action = "MAINTAIN DISCIPLINE - NORMAL CASH LEVELS"

print(f'\nBLACK MONDAY RISK: {black_monday_risk}')
print(f'Estimated Probability: {probability}')
print(f'\nRECOMMENDED ACTION: {action}')

print('\n' + '='*80)
print('KEY TAKEAWAYS')
print('='*80)

print(f'''
1. US MARKET HEALTH: {"WEAK" if us_avg < 5 else "NEUTRAL" if us_avg < 7 else "STRONG"}
   - Score: {us_avg:.1f}/10

2. CHINA EXPOSURE: {"TOXIC - EXIT" if china_avg < 4 else "RISKY - REDUCE" if china_avg < 6 else "MANAGEABLE"}
   - Score: {china_avg:.1f}/10
   - Friday's tariff announcement creates severe risk
   - Port fees start MONDAY (Oct 14)

3. SAFE HAVEN FLOWS: {"PANIC MODE" if safe_avg > 7 else "ELEVATED" if safe_avg > 5 else "NORMAL"}
   - Score: {safe_avg:.1f}/10
   - Gold/Bonds strength = fear indicator

4. GEOPOLITICAL RISK: {geo_risk}
   - US-China trade war (130% tariffs)
   - Afghanistan-Pakistan conflict (nuclear powers)
   - Qatar-Pakistan defense pact
   - Multiple crises compounding

5. NEXT WEEK OUTLOOK:
   - Watch Asia markets Sunday night (critical)
   - Monday could gap down significantly
   - China port fees take effect Monday
   - High volatility expected

BOTTOM LINE: {"This is a DANGEROUS setup. Reduce risk NOW." if risk_score >= 5 else "Elevated caution warranted. Prepare defensively." if risk_score >= 3 else "Manageable but monitor closely."}
''')

print('='*80)
