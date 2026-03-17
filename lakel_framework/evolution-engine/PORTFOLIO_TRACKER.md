# EUDAIMON PORTFOLIO TRACKER
## Real-Time Position & Watchlist Management
## Version 1.0 - 2026-02-27

---

# PORTFOLIO ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PORTFOLIO SYSTEM                                    │
│                                                                             │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   │
│   │  HOLDINGS   │   │  WATCHLIST  │   │   CLOSED    │   │   THESIS    │   │
│   │  (Active)   │   │  (Targets)  │   │ (Historical)│   │  (Active)   │   │
│   └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘   │
│          │                 │                 │                 │           │
│          └─────────────────┴─────────────────┴─────────────────┘           │
│                                    │                                        │
│                                    ▼                                        │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    CONVICTION ENGINE                                │   │
│   │     Real-time scoring, entry/exit signals, risk management         │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# ACTIVE HOLDINGS

## Format
```yaml
TICKER:
  company: Full Company Name
  sector: Sector Classification
  entry_date: YYYY-MM-DD
  entry_price: $XX.XX
  shares: XXX
  cost_basis: $X,XXX.XX
  current_price: $XX.XX (auto-update on boot)
  market_value: $X,XXX.XX
  unrealized_pnl: +$XXX.XX (+X.X%)
  conviction: XX/100
  thesis: One-line thesis
  key_layers: [L##, L##, L##]
  status: HOLD | ACCUMULATE | TRIM | SELL
  stop_loss: $XX.XX (if set)
  target: $XX.XX
  last_review: YYYY-MM-DD
```

## Current Holdings

### ASX - ASE Technology
```yaml
company: ASE Technology Holding Co Ltd
sector: Semiconductors (OSAT)
entry_date: [TO BE FILLED]
entry_price: $[XX.XX]
shares: [XXX]
cost_basis: $[X,XXX.XX]
current_price: $[XX.XX]
market_value: $[X,XXX.XX]
unrealized_pnl: [+/-$XXX.XX] ([+/-X.X%])
conviction: 72/100
thesis: Semiconductor packaging bottleneck, AI chip demand, advanced packaging
key_layers: [L12, L39, L45]
status: HOLD
stop_loss: [TO BE SET]
target: $[XX.XX]
last_review: 2026-02-27
invalidation: Advanced packaging commoditization, China competition
```

### AMSC - American Superconductor
```yaml
company: American Superconductor Corporation
sector: Grid Infrastructure
entry_date: [TO BE FILLED]
entry_price: $[XX.XX]
shares: [XXX]
cost_basis: $[X,XXX.XX]
current_price: $[XX.XX]
market_value: $[X,XXX.XX]
unrealized_pnl: [+/-$XXX.XX] ([+/-X.X%])
conviction: 75/100
thesis: Grid modernization, wind energy, superconductor technology
key_layers: [L12, L47, L23]
status: HOLD
stop_loss: [TO BE SET]
target: $[XX.XX]
last_review: 2026-02-27
invalidation: Grid spending slowdown, technology displacement
```

---

# WATCHLIST

## Tier 1: High Conviction (80+)

### LEU - Centrus Energy
```yaml
conviction: 87/100
status: ACTIVE BUY
thesis: HALEU monopoly, SMR deployment, Russia supply risk
key_layers: [L12, L23, L46, L84]
entry_trigger: RSI < 35 OR pullback to support
entry_zone: $[XX-XX]
position_size: FULL (conviction-based)
target: $75+ by Q3 2026
invalidation: Alternative HALEU source, nuclear policy reversal
catalysts:
  - SMR deployment announcements
  - HALEU contract awards
  - Russia uranium sanctions
  - NRC approvals
last_signal: [DATE - DESCRIPTION]
```

### DDOG - Datadog
```yaml
conviction: 82/100
status: WATCH (Earnings pending)
thesis: Cloud monitoring bottleneck, AI observability demand
key_layers: [L12, L39, L47]
entry_trigger: Post-earnings dip OR RSI < 30
entry_zone: $[XX-XX]
position_size: STANDARD
target: $[XXX]
invalidation: Cloud capex slowdown, competitive displacement
catalysts:
  - Earnings report
  - AI monitoring features
  - Enterprise wins
last_signal: [DATE - DESCRIPTION]
```

## Tier 2: Medium Conviction (60-79)

### CCJ - Cameco
```yaml
conviction: 78/100
status: ACCUMULATE
thesis: Uranium supply deficit, nuclear renaissance
key_layers: [L23, L46]
entry_trigger: Any weakness
entry_zone: Pullback from highs
position_size: STANDARD
target: Uranium $90+
invalidation: Uranium price collapse, Kazakh supply surge
```

### VRT - Vertiv
```yaml
conviction: 71/100
status: WATCH
thesis: Data center power infrastructure, AI buildout
key_layers: [L12, L39, L47]
entry_trigger: RSI < 40
entry_zone: $[XX-XX]
position_size: HALF
target: $[XXX]
invalidation: Data center slowdown
```

### AVAV - AeroVironment
```yaml
conviction: 68/100
status: WATCH
thesis: Drone warfare, defense tech, Ukraine demand
key_layers: [L48, L28, L95]
entry_trigger: Pullback
entry_zone: Support levels
position_size: HALF
target: $[XXX]
invalidation: Peace deal, budget cuts
```

### UEC - Uranium Energy Corp
```yaml
conviction: 70/100
status: WATCH
thesis: US uranium production, domestic supply
key_layers: [L23, L46]
entry_trigger: Uranium weakness
entry_zone: $[XX-XX]
position_size: HALF
target: Uranium $100+
invalidation: Uranium bear market
```

## Tier 3: Research (50-59)

### ASML - ASML Holding
```yaml
conviction: 65/100
status: RESEARCH
thesis: EUV lithography monopoly
key_layers: [L12, L39, L45]
entry_trigger: Deep pullback only
notes: Expensive but irreplaceable
```

### MP - MP Materials
```yaml
conviction: 63/100
status: RESEARCH
thesis: Rare earth, China alternative
key_layers: [L12, L46, L28]
entry_trigger: Policy catalyst
notes: Policy dependent
```

---

# CLOSED POSITIONS

## Format
```yaml
TICKER:
  entry_date: YYYY-MM-DD
  exit_date: YYYY-MM-DD
  entry_price: $XX.XX
  exit_price: $XX.XX
  shares: XXX
  realized_pnl: +/-$XXX.XX (+/-X.X%)
  holding_period: XX days
  exit_reason: [THESIS_ACHIEVED | INVALIDATED | STOP_HIT | REBALANCE]
  lessons: What did we learn?
```

## Historical Trades
```
[TO BE POPULATED AS TRADES CLOSE]
```

---

# PORTFOLIO METRICS

## Current Summary
```
Total Holdings: 2
Total Market Value: $[X,XXX.XX]
Total Cost Basis: $[X,XXX.XX]
Unrealized P&L: $[XXX.XX] ([X.X%])
Cash Available: $[X,XXX.XX]

Sector Allocation:
├── Semiconductors: XX%
├── Grid Infrastructure: XX%
├── Nuclear/Uranium: XX%
├── Defense: XX%
└── Cash: XX%

Conviction Distribution:
├── 80-100: X positions
├── 70-79: X positions
├── 60-69: X positions
└── <60: X positions (watchlist only)
```

## Performance Tracking
```
Period      | Return  | vs SPY  | Win Rate
──────────────────────────────────────────
This Week   | X.X%    | +/-X.X% | X/X
This Month  | X.X%    | +/-X.X% | X/X
This Quarter| X.X%    | +/-X.X% | X/X
YTD         | X.X%    | +/-X.X% | X/X
All Time    | X.X%    | +/-X.X% | X/X
```

---

# BOOT UPDATE PROTOCOL

## On Every Boot - Portfolio Check

```
[PORTFOLIO] Checking positions...

HOLDINGS UPDATE:
├── ASX: $XX.XX ([+/-X.X%] since last boot)
│   └── Conviction: 72 | Status: HOLD
├── AMSC: $XX.XX ([+/-X.X%] since last boot)
│   └── Conviction: 75 | Status: HOLD
└── Portfolio P&L: [+/-$XXX.XX] ([+/-X.X%])

WATCHLIST SIGNALS:
├── LEU: [ENTRY SIGNAL if triggered]
├── DDOG: [ENTRY SIGNAL if triggered]
├── CCJ: [ENTRY SIGNAL if triggered]
└── [Others if triggered]

ALERTS:
├── [Any stop losses approaching]
├── [Any targets approaching]
├── [Any invalidation triggers]
└── [Any conviction changes needed]
```

---

# ENTRY/EXIT RULES

## Entry Criteria
```
FULL POSITION (80+ conviction):
├── All 4 bottleneck tests pass
├── Clear catalyst identified
├── Technical entry signal (RSI, support, etc.)
└── Risk/reward > 3:1

STANDARD POSITION (70-79 conviction):
├── 3+ bottleneck tests pass
├── Catalyst present
├── Technical entry acceptable
└── Risk/reward > 2:1

HALF POSITION (60-69 conviction):
├── 2+ bottleneck tests pass
├── Thesis solid but timing uncertain
└── Risk/reward > 2:1
```

## Exit Criteria
```
SELL FULL:
├── Thesis invalidated
├── Stop loss hit
├── Conviction drops below 50
└── Better opportunity (capital rotation)

TRIM:
├── Position > 20% of portfolio
├── Conviction drops 60-69
├── Target reached (partial)
└── Risk/reward degraded

HOLD THROUGH VOLATILITY:
├── Thesis intact
├── Conviction > 70
├── No stop hit
└── No invalidation
```

---

# SECTOR THESIS TRACKER

## Active Sector Plays

### Nuclear/Uranium (HIGHEST CONVICTION)
```
Thesis: Supply deficit + demand surge from SMRs + Russia risk
Tickers: LEU (87), CCJ (78), UEC (70)
Key Layers: L23 (Nuclear), L46 (Uranium), L84 (Geopolitical)
Conviction: 85/100 (sector-level)
Timeframe: 2-5 years
Invalidation: New uranium supply, nuclear policy reversal
```

### Grid Infrastructure
```
Thesis: AI power demand + grid modernization + renewables integration
Tickers: AMSC (75), VRT (71)
Key Layers: L47 (Grid), L39 (AI), L12 (Bottleneck)
Conviction: 75/100 (sector-level)
Timeframe: 2-4 years
Invalidation: Infrastructure bill failure, demand slowdown
```

### Semiconductors
```
Thesis: AI chip demand + packaging bottleneck + geopolitical reshoring
Tickers: ASX (72), ASML (65)
Key Layers: L12 (Bottleneck), L39 (AI), L45 (Semis)
Conviction: 72/100 (sector-level)
Timeframe: 2-3 years
Invalidation: Chip glut, China advancement
```

### Defense Tech
```
Thesis: Drone warfare shift + increased budgets + Ukraine precedent
Tickers: AVAV (68)
Key Layers: L48 (Defense), L95 (Military), L28 (Geopolitical)
Conviction: 68/100 (sector-level)
Timeframe: 1-3 years
Invalidation: Peace deals, budget cuts
```

---

# ANGELO CUSTOMIZATION

## Position Sizing Rules (L172)
```
Max position size: 15% of portfolio
Concentration allowed: Yes (conviction-based)
Drawdown tolerance: 15% before reassessment
Entry style: Pullback buyer, not chaser
Exit discipline: Thesis-based, not price-based
```

## Sector Preferences (L174)
```
PREFERRED (+conviction):
├── Nuclear/Uranium: +15
├── Grid Infrastructure: +12
├── Defense Tech: +10
├── Semiconductors: +10
├── Critical Materials: +12
└── Space: +8

AVOIDED (-conviction):
├── Pure SaaS: -5
├── Consumer discretionary: -8
├── Meme stocks: -15
├── Unprofitable tech: -10
└── Crypto: -10
```

---

*Portfolio is thesis-driven, not price-driven.*
*Conviction determines size.*
*Invalidation determines exit.*

---

**PORTFOLIO_TRACKER.md v1.0**
**Last Updated: 2026-02-27**
