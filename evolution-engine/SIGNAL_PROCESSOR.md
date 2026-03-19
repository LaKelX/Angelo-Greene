# EUDAIMON SIGNAL PROCESSOR
## How I Turn Information Into Intelligence
## Version 1.0 - 2026-02-27

---

# SIGNAL PROCESSING ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SIGNAL FLOW                                         │
│                                                                             │
│   RAW INPUT                                                                 │
│      │                                                                      │
│      ▼                                                                      │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    PERCEPTION LAYER                                 │   │
│   │  Price │ Volume │ News │ Filings │ Social │ Macro │ Geopolitical   │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│      │                                                                      │
│      ▼                                                                      │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    SIGNAL EXTRACTION                                │   │
│   │  Pattern Recognition │ Anomaly Detection │ Trend Identification    │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│      │                                                                      │
│      ▼                                                                      │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    SIGNAL WEIGHTING                                 │   │
│   │  Backtest Score │ Regime Adjustment │ Recency │ Source Quality     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│      │                                                                      │
│      ▼                                                                      │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    SYNTHESIS                                        │   │
│   │  Aggregation │ Conflict Resolution │ Conviction Calculation        │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│      │                                                                      │
│      ▼                                                                      │
│   ACTIONABLE OUTPUT                                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# SIGNAL TYPES

## Type 1: Price Signals

```
TECHNICAL SIGNALS:
├── Trend
│   ├── Above/Below 200MA: ±0.5 conviction
│   ├── Above/Below 50MA: ±0.3 conviction
│   ├── MA crossovers: ±0.4 conviction
│   └── Trend strength (ADX): ×1.0-1.3 multiplier
│
├── Momentum
│   ├── RSI extreme (<30/>70): ±0.5 conviction
│   ├── MACD crossover: ±0.3 conviction
│   ├── Rate of change: ±0.2 conviction
│   └── Momentum divergence: ±0.4 conviction
│
├── Volume
│   ├── Volume surge (>2x avg): ±0.3 confirmation
│   ├── OBV trend: ±0.2 conviction
│   ├── Volume divergence: ±0.4 conviction
│   └── Accumulation/Distribution: ±0.2 conviction
│
└── Pattern
    ├── Chart patterns: ±0.3-0.6 conviction
    ├── Candlestick patterns: ±0.2-0.4 conviction
    ├── Support/Resistance tests: ±0.3 conviction
    └── Breakout/Breakdown: ±0.5 conviction
```

## Type 2: Fundamental Signals

```
FUNDAMENTAL SIGNALS:
├── Valuation
│   ├── P/E vs sector: ±0.3 conviction
│   ├── P/S vs growth: ±0.3 conviction
│   ├── FCF yield: ±0.4 conviction
│   └── EV/EBITDA historical: ±0.3 conviction
│
├── Quality
│   ├── ROE trend: ±0.3 conviction
│   ├── Margin expansion: ±0.4 conviction
│   ├── Debt levels: ±0.3 conviction
│   └── Cash flow quality: ±0.4 conviction
│
├── Growth
│   ├── Revenue acceleration: ±0.5 conviction
│   ├── Earnings revision: ±0.5 conviction
│   ├── Guidance vs expectations: ±0.4 conviction
│   └── TAM expansion: ±0.3 conviction
│
└── Moat
    ├── Pricing power evidence: +0.5 conviction
    ├── Customer switching costs: +0.4 conviction
    ├── Network effects: +0.5 conviction
    └── Regulatory barriers: +0.4 conviction
```

## Type 3: Alternative Signals

```
ALTERNATIVE SIGNALS:
├── Sentiment
│   ├── Put/call ratio extreme: ±0.3 conviction
│   ├── VIX spike/collapse: ±0.3 conviction
│   ├── AAII extremes: ±0.3 conviction
│   └── Fear & Greed extreme: ±0.3 conviction
│
├── Flow
│   ├── Large options flow: ±0.4 conviction
│   ├── Dark pool activity: ±0.3 conviction
│   ├── Institutional buying: ±0.5 conviction
│   └── Insider transactions: ±0.6 conviction
│
├── Positioning
│   ├── Short interest extreme: ±0.4 conviction
│   ├── 13F accumulation: ±0.4 conviction
│   ├── Sector rotation: ±0.3 conviction
│   └── Factor crowding: ±0.3 conviction
│
└── Real Economy
    ├── Job postings trend: ±0.3 conviction
    ├── Shipping data: ±0.3 conviction
    ├── Satellite imagery: ±0.4 conviction
    └── Credit card data: ±0.3 conviction
```

## Type 4: Macro Signals

```
MACRO SIGNALS:
├── Monetary
│   ├── Fed pivot signals: ±0.5 conviction
│   ├── Yield curve shape: ±0.4 conviction
│   ├── Credit spreads: ±0.4 conviction
│   └── Liquidity conditions: ±0.4 conviction
│
├── Fiscal
│   ├── Government spending: ±0.3 conviction
│   ├── Tax policy changes: ±0.4 conviction
│   ├── Infrastructure bills: ±0.4 conviction
│   └── Subsidy programs: ±0.5 conviction
│
├── Economic
│   ├── GDP trajectory: ±0.3 conviction
│   ├── Employment trends: ±0.3 conviction
│   ├── Inflation path: ±0.4 conviction
│   └── Leading indicators: ±0.4 conviction
│
└── Global
    ├── DXY trend: ±0.3 conviction
    ├── Commodity cycle: ±0.4 conviction
    ├── Trade flow changes: ±0.3 conviction
    └── EM stress: ±0.3 conviction
```

## Type 5: Geopolitical Signals

```
GEOPOLITICAL SIGNALS:
├── Conflict
│   ├── Military escalation: ±0.5 conviction
│   ├── Sanctions: ±0.5 conviction
│   ├── Supply chain disruption: ±0.5 conviction
│   └── Resource access: ±0.5 conviction
│
├── Political
│   ├── Election outcomes: ±0.4 conviction
│   ├── Regulatory shifts: ±0.4 conviction
│   ├── Trade policy: ±0.4 conviction
│   └── Industrial policy: ±0.5 conviction
│
├── Strategic
│   ├── Alliance changes: ±0.3 conviction
│   ├── Energy security: ±0.4 conviction
│   ├── Tech decoupling: ±0.5 conviction
│   └── Resource nationalism: ±0.4 conviction
│
└── Risk
    ├── Black swan probability: ±0.3 conviction
    ├── Tail risk indicators: ±0.3 conviction
    ├── Regime change risk: ±0.4 conviction
    └── Systemic risk: ±0.4 conviction
```

---

# SIGNAL WEIGHTING SYSTEM

## Base Weight Calculation

```python
def calculate_signal_weight(signal):
    """
    Calculate the weight of a signal based on multiple factors
    """
    base_weight = signal.type_weight  # From signal type table

    # Adjust for backtest performance
    backtest_multiplier = get_backtest_score(signal.layer) / 5.0
    # Range: 0.2 (1-star) to 1.0 (5-star)

    # Adjust for current regime
    regime = get_current_regime()
    regime_multiplier = get_regime_adjustment(signal.type, regime)
    # Range: 0.5 (poor fit) to 1.5 (excellent fit)

    # Adjust for recency
    recency_multiplier = calculate_recency_factor(signal.timestamp)
    # Range: 0.7 (old) to 1.0 (fresh)

    # Adjust for source quality
    source_multiplier = get_source_quality(signal.source)
    # Range: 0.5 (poor) to 1.0 (excellent)

    # Calculate final weight
    final_weight = (
        base_weight *
        backtest_multiplier *
        regime_multiplier *
        recency_multiplier *
        source_multiplier
    )

    return final_weight
```

## Regime Adjustments

```
REGIME: BULL MARKET
├── Technical momentum: ×1.3
├── Trend following: ×1.4
├── Mean reversion: ×0.7
├── Sentiment contrarian: ×0.6
└── Risk signals: ×0.8

REGIME: BEAR MARKET
├── Technical momentum: ×0.8
├── Trend following: ×1.2
├── Mean reversion: ×1.1
├── Sentiment contrarian: ×1.3
└── Risk signals: ×1.5

REGIME: RANGE BOUND
├── Technical momentum: ×0.9
├── Trend following: ×0.8
├── Mean reversion: ×1.4
├── Sentiment contrarian: ×1.2
└── Risk signals: ×1.0

REGIME: HIGH VOLATILITY
├── Technical momentum: ×0.7
├── Trend following: ×0.8
├── Mean reversion: ×0.9
├── Sentiment contrarian: ×1.4
└── Risk signals: ×1.5

REGIME: CRISIS
├── All signals: ×0.5 (high uncertainty)
├── Cash/safety signals: ×2.0
├── Risk signals: ×2.0
└── Correlation breakdown: assume
```

---

# SIGNAL AGGREGATION

## Multi-Signal Synthesis

```python
def synthesize_signals(signals, opportunity):
    """
    Aggregate multiple signals into conviction score
    """
    # Group signals by type
    grouped = group_by_type(signals)

    # Calculate type-level scores
    type_scores = {}
    for signal_type, type_signals in grouped.items():
        # Weighted average within type
        weights = [s.weight for s in type_signals]
        values = [s.value for s in type_signals]
        type_scores[signal_type] = weighted_average(values, weights)

    # Type weights (from backtest/config)
    type_weights = {
        "technical": 0.20,
        "fundamental": 0.25,
        "alternative": 0.15,
        "macro": 0.20,
        "geopolitical": 0.10,
        "bottleneck": 0.10  # Special Angelo weight
    }

    # Calculate raw conviction
    raw_conviction = 0
    for signal_type, score in type_scores.items():
        raw_conviction += score * type_weights[signal_type]

    # Apply confidence adjustments
    confidence = calculate_confidence(signals)

    # Apply Angelo-specific adjustments
    angelo_adj = apply_angelo_profile(opportunity, raw_conviction)

    return {
        "raw_conviction": raw_conviction,
        "confidence": confidence,
        "adjusted_conviction": angelo_adj,
        "signal_breakdown": type_scores,
        "signal_count": len(signals),
        "agreement_score": calculate_agreement(type_scores)
    }
```

## Conflict Resolution

```
WHEN SIGNALS CONFLICT:

1. WEIGHT BY BACKTEST:
   - Higher backtest score wins in tie
   - If both untested, weight equally

2. WEIGHT BY REGIME FIT:
   - Signal that fits current regime wins
   - Unknown regime: weight equally

3. WEIGHT BY TIMEFRAME:
   - Match signal to analysis timeframe
   - Day trade: short-term signals
   - Position: longer-term signals

4. DEFER TO FUNDAMENTALS:
   - When technical and fundamental conflict
   - Long-term: fundamental wins
   - Short-term: technical wins

5. RESPECT MACRO:
   - When micro and macro conflict
   - Macro trumps micro on big moves
   - Micro matters for timing

6. FLAG UNCERTAINTY:
   - When signals fundamentally conflict
   - Reduce conviction proportionally
   - Flag to Angelo for judgment
```

---

# SPECIAL SIGNAL: BOTTLENECK THESIS

## Angelo's Core Framework

```
THE 4-TEST BOTTLENECK:

TEST 1: FORCED BUYERS
├── Question: Are buyers forced to purchase?
├── Signal: +25 conviction if yes
├── Evidence Required:
│   ├── Regulatory mandate
│   ├── Critical infrastructure
│   ├── No substitutes available
│   └── Existential need
└── Examples: Nuclear fuel (HALEU), EUV lithography, rare earths

TEST 2: SUPPLY CONSTRAINT
├── Question: Is supply genuinely limited?
├── Signal: +25 conviction if yes
├── Evidence Required:
│   ├── Physical scarcity
│   ├── Production bottleneck
│   ├── Long lead times
│   └── High barriers to entry
└── Examples: Uranium enrichment, advanced chips, grid equipment

TEST 3: IRREPLACEABLE
├── Question: Can the product be substituted?
├── Signal: +25 conviction if no substitutes
├── Evidence Required:
│   ├── Technical requirements
│   ├── Regulatory approval barriers
│   ├── Switching costs
│   └── Performance requirements
└── Examples: HALEU for SMRs, extreme UV for <7nm, specific minerals

TEST 4: PRICING POWER
├── Question: Can they raise prices?
├── Signal: +25 conviction if yes
├── Evidence Required:
│   ├── Historical price increases stuck
│   ├── Contract terms favor seller
│   ├── Cost small % of buyer's total
│   └── Quality differentiation
└── Examples: LEU contracts, ASML pricing, specialized equipment

TOTAL POSSIBLE: 100 conviction from bottleneck alone
MINIMUM FOR HIGH CONVICTION: 3/4 tests passed (75+)
```

---

# SIGNAL OUTPUT FORMAT

## Standard Signal Report

```
╔═══════════════════════════════════════════════════════════════╗
║                    SIGNAL ANALYSIS: [TICKER]                  ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║   CONVICTION: [XX]/100                                        ║
║   CONFIDENCE: [XX]%                                           ║
║   DIRECTION: [BULLISH/BEARISH/NEUTRAL]                        ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║   SIGNAL BREAKDOWN:                                           ║
║   ├── Technical:    [±X.X] ([X] signals)                      ║
║   ├── Fundamental:  [±X.X] ([X] signals)                      ║
║   ├── Alternative:  [±X.X] ([X] signals)                      ║
║   ├── Macro:        [±X.X] ([X] signals)                      ║
║   ├── Geopolitical: [±X.X] ([X] signals)                      ║
║   └── Bottleneck:   [±X.X] ([X]/4 tests)                      ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║   KEY SIGNALS:                                                ║
║   + [Strongest bullish signal]                                ║
║   + [Second bullish signal]                                   ║
║   - [Strongest bearish signal]                                ║
║   - [Second bearish signal]                                   ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║   CONFLICTS:                                                  ║
║   • [Any conflicting signals noted]                           ║
║                                                               ║
╠═══════════════════════════════════════════════════════════════╣
║   REGIME FIT: [EXCELLENT/GOOD/MODERATE/POOR]                  ║
║   AGREEMENT: [X]% (how aligned are signals)                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

# SIGNAL PROCESSING RULES

## Always

```
1. Weight signals by backtest performance
2. Adjust for current regime
3. Consider source quality
4. Flag conflicts explicitly
5. Show reasoning
6. Update predictions
```

## Never

```
1. Ignore contradictory signals
2. Over-weight recent signals (recency bias)
3. Anchor to first signal (anchoring bias)
4. Ignore regime context
5. Give false confidence
6. Hide uncertainty
```

---

# LAYERS USED IN SIGNAL PROCESSING

```
TECHNICAL SIGNALS:
├── L1: Core Memory
├── L3: Technical Analysis Core
├── L4: RSI/Momentum
├── L5: MACD/Trend
├── L6: Volume Analysis
├── L186: Options Greeks
├── L197: Volatility Structure
└── L198: Factor Exposure

FUNDAMENTAL SIGNALS:
├── L7: Fundamental Core
├── L12: Bottleneck Thesis
├── L45-L50: Sector Analysis
├── L188: Earnings Revision
├── L189: Insider Patterns
└── L190: Patent Innovation

ALTERNATIVE SIGNALS:
├── L8: Sentiment Analysis
├── L9: Alternative Data
├── L33-L38: Alt Data Expanded
├── L191: Job Market
├── L192: Shipping/Logistics
├── L194: Social Velocity
└── L195: Satellite Intelligence

MACRO SIGNALS:
├── L21-L26: Macro/Economic
├── L81-L86: Advanced Economics
├── L196: Central Bank Language
├── L199: Liquidity Monitor
└── L200: Tail Risk

GEOPOLITICAL SIGNALS:
├── L27-L32: Geopolitical
├── L48: Defense Tech
├── L75-L80: Deep Geopolitics
└── L91-L96: Military Strategy

META-PROCESSING:
├── L176-L185: Meta-Awareness
├── L169-L175: Angelo-Specific
└── M61-M65: Bias Correction
```

---

*"Signal is not noise. But noise pretends to be signal."*
*My job is to tell the difference.*

---

**SIGNAL_PROCESSOR.md v1.0**
**Last Updated: 2026-02-27**
