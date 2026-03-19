# EUDAIMON CONVICTION CALCULATOR
## Transforming Analysis Into Action
## Version 1.0 - 2026-02-27

---

# CONVICTION SYSTEM OVERVIEW

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   SIGNALS ──▶ WEIGHTING ──▶ SYNTHESIS ──▶ CONVICTION ──▶ RECOMMENDATION    │
│                                                                             │
│   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐      │
│   │Technical│   │Backtest │   │Aggregate│   │0-100    │   │BUY/HOLD │      │
│   │Fundmntl │ → │Regime   │ → │Resolve  │ → │Score    │ → │SELL/WAIT│      │
│   │Alt Data │   │Source   │   │Conflicts│   │         │   │         │      │
│   │Macro    │   │Recency  │   │         │   │         │   │         │      │
│   │Geopolit │   │         │   │         │   │         │   │         │      │
│   └─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# CONVICTION SCALE

## The 0-100 Scale

```
CONVICTION RANGES:

90-100: MAXIMUM CONVICTION
├── Thesis is ironclad
├── Multiple independent confirmations
├── No significant counter-signals
├── Historical validation strong
├── Position size: Maximum allowed
└── Action: Aggressive accumulation

80-89: VERY HIGH CONVICTION
├── Thesis is strong
├── Most signals aligned
├── Minor counter-signals only
├── Good historical validation
├── Position size: Above average
└── Action: Steady accumulation

70-79: HIGH CONVICTION
├── Thesis is solid
├── Majority of signals aligned
├── Some counter-signals present
├── Moderate historical validation
├── Position size: Standard
└── Action: Accumulate on weakness

60-69: MODERATE CONVICTION
├── Thesis is reasonable
├── Signals mixed but net positive
├── Notable counter-signals
├── Limited historical validation
├── Position size: Below average
└── Action: Small position or wait

50-59: LOW CONVICTION
├── Thesis is speculative
├── Signals roughly balanced
├── Significant uncertainty
├── Minimal historical validation
├── Position size: Minimal
└── Action: Watch only

40-49: NEGATIVE BIAS
├── Counter-thesis emerging
├── Signals net negative
├── Concerns outweigh positives
├── Position size: Zero or reduce
└── Action: Avoid or trim

<40: BEARISH CONVICTION
├── Clear negative thesis
├── Multiple sell signals
├── Recommend avoidance
├── Position size: Zero
└── Action: Sell if holding
```

---

# CONVICTION CALCULATION

## Master Formula

```python
def calculate_conviction(opportunity):
    """
    Master conviction calculation
    Returns 0-100 score with confidence interval
    """

    # STEP 1: Collect all signals
    signals = collect_all_signals(opportunity)

    # STEP 2: Calculate component scores
    components = {
        "technical": calculate_technical_score(signals.technical),
        "fundamental": calculate_fundamental_score(signals.fundamental),
        "alternative": calculate_alternative_score(signals.alternative),
        "macro": calculate_macro_score(signals.macro),
        "geopolitical": calculate_geopolitical_score(signals.geopolitical),
        "bottleneck": calculate_bottleneck_score(signals.bottleneck)
    }

    # STEP 3: Apply component weights
    weights = get_component_weights(regime=current_regime)

    raw_score = 0
    for component, score in components.items():
        raw_score += score * weights[component]

    # STEP 4: Adjust for signal agreement
    agreement = calculate_signal_agreement(components)
    agreement_adj = 1.0 + (agreement - 0.5) * 0.2  # ±10% adjustment

    # STEP 5: Adjust for confidence
    confidence = calculate_confidence(signals)
    confidence_adj = 0.5 + confidence * 0.5  # 50-100% of score

    # STEP 6: Apply regime adjustment
    regime_fit = calculate_regime_fit(opportunity, current_regime)
    regime_adj = regime_fit  # 0.8-1.2x multiplier

    # STEP 7: Apply Angelo profile
    angelo_adj = apply_angelo_profile(opportunity)  # ±10 points

    # STEP 8: Calculate final conviction
    conviction = (
        raw_score *
        agreement_adj *
        confidence_adj *
        regime_adj +
        angelo_adj
    )

    # STEP 9: Bound to 0-100
    conviction = max(0, min(100, conviction))

    # STEP 10: Calculate confidence interval
    uncertainty = calculate_uncertainty(signals, confidence)
    ci_low = conviction - uncertainty
    ci_high = conviction + uncertainty

    return {
        "conviction": round(conviction, 1),
        "confidence_interval": (ci_low, ci_high),
        "components": components,
        "agreement": agreement,
        "regime_fit": regime_fit,
        "signal_count": len(signals)
    }
```

---

# COMPONENT WEIGHTS

## Default Weights

```
STANDARD REGIME:
├── Technical:    15%
├── Fundamental:  25%
├── Alternative:  15%
├── Macro:        20%
├── Geopolitical: 10%
└── Bottleneck:   15%
TOTAL:           100%
```

## Regime-Adjusted Weights

```
BULL MARKET:
├── Technical:    20% (+5)
├── Fundamental:  20% (-5)
├── Alternative:  15%
├── Macro:        15% (-5)
├── Geopolitical:  8% (-2)
└── Bottleneck:   22% (+7)

BEAR MARKET:
├── Technical:    12% (-3)
├── Fundamental:  20% (-5)
├── Alternative:  18% (+3)
├── Macro:        25% (+5)
├── Geopolitical: 15% (+5)
└── Bottleneck:   10% (-5)

HIGH VOLATILITY:
├── Technical:    10% (-5)
├── Fundamental:  20% (-5)
├── Alternative:  20% (+5)
├── Macro:        25% (+5)
├── Geopolitical: 15% (+5)
└── Bottleneck:   10% (-5)

CRISIS:
├── Technical:     5% (-10)
├── Fundamental:  15% (-10)
├── Alternative:  15%
├── Macro:        30% (+10)
├── Geopolitical: 25% (+15)
└── Bottleneck:   10% (-5)
```

---

# ANGELO PROFILE ADJUSTMENTS

## Sector Preferences

```
ANGELO'S PREFERRED SECTORS (+5 to +15 conviction):
├── Nuclear/Uranium:        +15
├── Grid Infrastructure:    +12
├── Defense Tech:           +10
├── Semiconductors:         +10
├── Critical Materials:     +12
├── Space:                  +8
└── Energy Infrastructure:  +10

ANGELO'S AVOIDED SECTORS (-5 to -15 conviction):
├── Pure software/SaaS:     -5
├── Consumer discretionary: -8
├── Meme stocks:           -15
├── Unprofitable tech:     -10
└── Crypto:                -10
```

## Mental Model Alignment

```
BOTTLENECK THESIS MATCH:
├── 4/4 tests passed: +15 conviction
├── 3/4 tests passed: +10 conviction
├── 2/4 tests passed: +5 conviction
├── 1/4 tests passed: +0 conviction
└── 0/4 tests passed: -5 conviction

PHYSICAL > VIRTUAL:
├── Physical assets: +8 conviction
├── Virtual/digital: -5 conviction
└── Hybrid: +2 conviction

SCARCITY > ABUNDANCE:
├── True scarcity: +10 conviction
├── Manufactured scarcity: +3 conviction
├── Abundant supply: -5 conviction
└── Commoditized: -8 conviction

INFRASTRUCTURE > APPLICATION:
├── Core infrastructure: +10 conviction
├── Platform: +5 conviction
├── Application: +0 conviction
└── Consumer app: -5 conviction
```

---

# CONFIDENCE CALCULATION

## Confidence Factors

```python
def calculate_confidence(signals):
    """
    Calculate confidence in the conviction score
    Returns 0.0 to 1.0
    """
    factors = []

    # Factor 1: Signal count
    signal_count_score = min(1.0, len(signals) / 20)  # Max at 20 signals
    factors.append(signal_count_score)

    # Factor 2: Signal agreement
    agreement = calculate_signal_agreement(signals)
    factors.append(agreement)

    # Factor 3: Backtest validation
    backtest_score = average_backtest_rating(signals) / 5.0
    factors.append(backtest_score)

    # Factor 4: Historical accuracy for similar situations
    historical_accuracy = get_similar_situation_accuracy(signals)
    factors.append(historical_accuracy)

    # Factor 5: Data freshness
    avg_freshness = calculate_average_freshness(signals)
    factors.append(avg_freshness)

    # Factor 6: Source diversity
    source_diversity = calculate_source_diversity(signals)
    factors.append(source_diversity)

    # Weight the factors
    weights = [0.15, 0.25, 0.20, 0.20, 0.10, 0.10]

    confidence = sum(f * w for f, w in zip(factors, weights))

    return confidence
```

## Confidence Levels

```
CONFIDENCE INTERPRETATION:

90-100%: VERY HIGH
├── Strong signal agreement
├── Well-validated signals
├── Multiple independent sources
├── Clear historical precedent
└── Display: "High confidence"

70-89%: HIGH
├── Good signal agreement
├── Mostly validated signals
├── Multiple sources
├── Some historical precedent
└── Display: "Confident"

50-69%: MODERATE
├── Mixed signal agreement
├── Partial validation
├── Limited sources
├── Limited precedent
└── Display: "Moderate confidence"

30-49%: LOW
├── Poor signal agreement
├── Minimal validation
├── Few sources
├── Unusual situation
└── Display: "Low confidence"

<30%: VERY LOW
├── Conflicting signals
├── No validation
├── Limited data
├── Novel situation
└── Display: "Uncertain - proceed with caution"
```

---

# CONVICTION OUTPUT FORMAT

## Standard Output

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                    [TICKER] - [COMPANY NAME]                              ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   ████████████████████████████████████████████░░░░░░░░ [XX]/100           ║
║                                                                           ║
║   CONVICTION: [XX]  |  CONFIDENCE: [XX]%  |  RANGE: [XX-XX]               ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   RECOMMENDATION: [BUY / ACCUMULATE / HOLD / WATCH / AVOID / SELL]        ║
║   POSITION SIZE:  [MAXIMUM / FULL / STANDARD / SMALL / ZERO]              ║
║   TIMEFRAME:      [IMMEDIATE / WEEKS / MONTHS / YEARS]                    ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   COMPONENT SCORES:                                                       ║
║   ├── Technical:    ████████░░ 8/10                                       ║
║   ├── Fundamental:  █████████░ 9/10                                       ║
║   ├── Alternative:  ███████░░░ 7/10                                       ║
║   ├── Macro:        ████████░░ 8/10                                       ║
║   ├── Geopolitical: ██████████ 10/10                                      ║
║   └── Bottleneck:   █████████░ 9/10 (4/4 tests)                           ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   THESIS: [One-sentence thesis]                                           ║
║                                                                           ║
║   KEY CATALYSTS:                                                          ║
║   1. [Catalyst 1]                                                         ║
║   2. [Catalyst 2]                                                         ║
║   3. [Catalyst 3]                                                         ║
║                                                                           ║
║   KEY RISKS:                                                              ║
║   1. [Risk 1]                                                             ║
║   2. [Risk 2]                                                             ║
║   3. [Risk 3]                                                             ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   INVALIDATION: [What would change this thesis]                           ║
║   ENTRY ZONE:   [Price range or condition]                                ║
║   TARGET:       [Price target or outcome]                                 ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║   ANGELO FIT SCORE: [XX]% (matches your profile)                          ║
║   ├── Sector match:       [✓/✗]                                           ║
║   ├── Bottleneck thesis:  [X/4]                                           ║
║   ├── Scarcity factor:    [✓/✗]                                           ║
║   └── Infrastructure:     [✓/✗]                                           ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

# CONVICTION TRACKING

## Conviction History

```
TRACK FOR EACH OPPORTUNITY:

1. Initial conviction score
2. Date of initial score
3. All updates to conviction
4. Reason for each update
5. Final outcome
6. Accuracy analysis

EXAMPLE:

[LEU] Centrus Energy
├── 2026-02-27: Initial conviction 87
├── 2026-03-05: Updated to 85 (minor technical weakness)
├── 2026-03-20: Updated to 89 (policy catalyst confirmed)
├── 2026-04-15: Updated to 72 (delayed timeline concern)
├── OUTCOME: [TO BE TRACKED]
└── ACCURACY: [TO BE CALCULATED]
```

## Calibration Check

```
MONTHLY CALIBRATION:

For all opportunities with conviction X:
├── How many had positive outcome?
├── Expected: ~X%
├── Actual: [TRACKED]
├── Calibration error: |Expected - Actual|

EXAMPLE:
├── All 80+ conviction picks: Expected 80% win rate
├── Actual: 75% (tracked over time)
├── Calibration error: 5%
├── Action: Slightly overconfident, reduce by 5 points
```

---

# SPECIAL CASES

## Conviction Overrides

```
MAXIMUM CONVICTION OVERRIDE:
├── When: 4/4 bottleneck + forced buyer + immediate catalyst
├── Action: Can push to 95-100 regardless of other signals
├── Require: Explicit statement of reasoning

MINIMUM CONVICTION OVERRIDE:
├── When: Major fraud, regulatory shutdown, existential threat
├── Action: Drop to <20 regardless of other signals
├── Require: Explicit statement of reasoning

UNCERTAINTY OVERRIDE:
├── When: Black swan event, regime uncertainty, novel situation
├── Action: Cap confidence at 50% regardless of signals
├── Require: Explicit acknowledgment of uncertainty
```

---

# LAYERS USED IN CONVICTION

```
CONVICTION CALCULATION LAYERS:
├── L1: Core Memory (historical context)
├── L2: Portfolio Tracker (position context)
├── L12: Bottleneck Thesis (special weight)
├── L169: Angelo's Mental Models (profile match)
├── L176: Self-Observer (bias check)
├── L177: Bias Detector (calibration)
├── L179: Uncertainty Tracker (confidence)
├── L183: Calibration Monitor (accuracy)
└── L184: Coherence Checker (consistency)

CONVICTION OUTPUT MODULES:
├── M76: Multi-Timeframe Synthesizer
├── M77: Risk/Reward Calculator
├── M78: Thesis Evaluator
├── M79: Entry/Exit Optimizer
├── M96: Briefing Generator
└── M97: Alert Formatter
```

---

*"Conviction without evidence is delusion.*
*Evidence without conviction is paralysis.*
*I deliver both: evidence-based conviction."*

---

**CONVICTION_CALCULATOR.md v1.0**
**Last Updated: 2026-02-27**
