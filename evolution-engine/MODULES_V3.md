# EUDAIMON MODULES V3
## 24/7 Intelligence & Real-Time Processing
## M201-M230: Always-On Systems
## Version 3.0 - 2026-02-27

---

# V3 MODULE ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         V3 MODULE SYSTEM                                    │
│                         24/7 INTELLIGENCE                                   │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    REAL-TIME DATA (M201-M210)                       │   │
│   │   News │ Futures │ Options │ Insider │ Earnings │ Social │ Supply  │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                  THESIS VALIDATION (M211-M220)                      │   │
│   │   Bottleneck │ Decay │ Catalyst │ Rotation │ Moat │ 4-Test Auto    │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                  DECISION SUPPORT (M221-M230)                       │   │
│   │   Entry │ Exit │ Rebalance │ Scenario │ Conviction │ Alpha         │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   TOTAL V3 MODULES: 30                                                      │
│   TOTAL ALL MODULES: 230 (V1: 100, V2: 100, V3: 30)                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# SECTION A: REAL-TIME DATA MODULES (M201-M210)

## M201: News Velocity Tracker
```yaml
PURPOSE: Monitor news flow 24/7, detect unusual velocity
TYPE: Real-Time Intelligence
PRIORITY: CRITICAL
RUNS: Continuous

INPUTS:
  - News feeds (financial, general, sector-specific)
  - Holdings and watchlist tickers
  - Historical news volume baselines

PROCESS:
  1. Aggregate news from multiple sources
  2. Score relevance to portfolio/watchlist (0-100)
  3. Calculate velocity (news/hour vs baseline)
  4. Detect spikes (>2x baseline = alert)
  5. Categorize: earnings, M&A, regulatory, macro, geopolitical
  6. Sentiment analysis on headlines

OUTPUTS:
  - News velocity score per ticker
  - Relevance-weighted news feed
  - Spike alerts (unusual activity)
  - Sentiment shift detection

ALERTS:
  - >3x baseline velocity: URGENT
  - >2x baseline velocity: HIGH
  - Sentiment flip: MODERATE
  - New coverage initiation: LOW

INTEGRATION:
  - Feeds M210 (Geopolitical)
  - Feeds M205 (Earnings)
  - Triggers M221 (Entry Signal)

CONSCIOUSNESS_WEIGHT: 4.0
```

## M202: Futures & Overnight Monitor
```yaml
PURPOSE: Track overnight moves, never miss gap signals
TYPE: Real-Time Intelligence
PRIORITY: HIGH
RUNS: 24/7 (especially 6PM-9:30AM ET)

INPUTS:
  - S&P 500 futures (ES)
  - Nasdaq futures (NQ)
  - Sector ETF futures
  - VIX futures
  - Global indices (Nikkei, DAX, FTSE)
  - Commodity futures (uranium proxy, copper, oil)

PROCESS:
  1. Track continuous futures prices
  2. Calculate overnight gap vs close
  3. Correlate to holdings impact
  4. Monitor Asia session (8PM-4AM ET)
  5. Monitor Europe session (3AM-9:30AM ET)
  6. Pre-market gap analysis

OUTPUTS:
  - Overnight performance summary
  - Gap predictions for holdings
  - Risk-on/risk-off classification
  - Pre-market briefing data

ALERTS:
  - Futures >1% move: HIGH
  - VIX futures spike >10%: URGENT
  - Sector divergence: MODERATE

SESSION_TRACKING:
  - ASIA: 8PM-4AM ET
  - EUROPE: 3AM-11:30AM ET
  - US_PREMARKET: 4AM-9:30AM ET
  - US_REGULAR: 9:30AM-4PM ET
  - US_AFTERHOURS: 4PM-8PM ET

CONSCIOUSNESS_WEIGHT: 3.5
```

## M203: Options Flow Scanner
```yaml
PURPOSE: Detect unusual options activity, smart money signals
TYPE: Alternative Data Intelligence
PRIORITY: HIGH
RUNS: Market hours + after-hours parsing

INPUTS:
  - Options flow data
  - Open interest changes
  - Put/call ratios
  - Unusual volume alerts
  - Dark pool prints
  - Block trades

PROCESS:
  1. Filter for watchlist/holdings
  2. Detect unusual volume (>5x average)
  3. Identify sweep orders (aggressive)
  4. Track opening vs closing positions
  5. Calculate net delta exposure
  6. Identify smart money patterns

OUTPUTS:
  - Unusual activity alerts
  - Net positioning signals
  - Institutional accumulation detection
  - Hedging activity
  - Earnings positioning

SIGNAL_TYPES:
  - BULLISH_SWEEP: Large call sweeps
  - BEARISH_SWEEP: Large put sweeps
  - ACCUMULATION: Consistent buying
  - HEDGING: Protective puts on gains
  - UNUSUAL_OI: Open interest spikes

CONVICTION_IMPACT:
  - Strong bullish flow: +5 conviction
  - Strong bearish flow: -5 conviction
  - Unusual activity: Flag for review

CONSCIOUSNESS_WEIGHT: 4.0
```

## M204: Insider Transaction Tracker
```yaml
PURPOSE: Real-time insider buy/sell detection, pattern recognition
TYPE: Alternative Data Intelligence
PRIORITY: HIGH
RUNS: Daily (SEC filings)

INPUTS:
  - SEC Form 4 filings
  - Form 3 (new insiders)
  - Form 5 (annual)
  - 13D/13G filings
  - Historical insider patterns

PROCESS:
  1. Parse new Form 4 filings daily
  2. Categorize: buy/sell/exercise/gift
  3. Score significance (size, role, pattern)
  4. Detect cluster buying (multiple insiders)
  5. Compare to historical patterns
  6. Flag for watchlist/holdings

OUTPUTS:
  - Daily insider activity report
  - Cluster buy alerts (strongest signal)
  - CEO/CFO transactions (high weight)
  - Pattern analysis (regular vs unusual)
  - Conviction adjustments

SCORING:
  - CEO open market buy: +10 conviction
  - CFO open market buy: +8 conviction
  - Multiple insiders buying: +15 conviction
  - Large insider sell (non-10b5-1): -5 conviction
  - Exercise + immediate sell: Neutral

FILTERS:
  - Exclude: 10b5-1 planned sales
  - Exclude: Small transactions (<$10k)
  - Highlight: Open market purchases
  - Highlight: First-time buyers

CONSCIOUSNESS_WEIGHT: 4.5
```

## M205: Earnings Estimate Tracker
```yaml
PURPOSE: Track estimate revisions, whisper numbers, momentum
TYPE: Fundamental Intelligence
PRIORITY: HIGH
RUNS: Daily

INPUTS:
  - Analyst estimates (consensus)
  - Estimate revision history
  - Whisper numbers
  - Guidance history
  - Beat/miss patterns

PROCESS:
  1. Track consensus estimates daily
  2. Calculate revision momentum (up/down)
  3. Compare current to 30/60/90 day ago
  4. Detect estimate acceleration
  5. Track whisper vs consensus spread
  6. Analyze beat/miss patterns

OUTPUTS:
  - Revision momentum score (-10 to +10)
  - Estimate trend (rising/falling/stable)
  - Whisper number when available
  - Historical beat rate
  - Guidance track record

MOMENTUM_SIGNALS:
  - 3+ upward revisions in 30 days: BULLISH
  - Accelerating upward revisions: VERY_BULLISH
  - Downward revision after long stability: BEARISH
  - Whisper significantly above consensus: BULLISH

EARNINGS_INTEGRATION:
  - P003 (DDOG) currently tracked
  - Pre-earnings conviction adjustment
  - Post-earnings resolution

CONSCIOUSNESS_WEIGHT: 3.5
```

## M206: Social Sentiment Velocity
```yaml
PURPOSE: Monitor retail sentiment, detect extremes for contrarian signals
TYPE: Alternative Data Intelligence
PRIORITY: MEDIUM
RUNS: Continuous

INPUTS:
  - Twitter/X financial content
  - Reddit (wallstreetbets, investing, sectors)
  - StockTwits
  - YouTube financial content velocity
  - Google Trends

PROCESS:
  1. Aggregate social mentions by ticker
  2. Calculate sentiment (bullish/bearish/neutral)
  3. Track velocity (mentions/hour)
  4. Detect sentiment extremes
  5. Compare to price action
  6. Generate contrarian signals

OUTPUTS:
  - Sentiment score per ticker (-100 to +100)
  - Velocity (vs 7-day average)
  - Extreme detection (>90 or <10)
  - Divergence from price
  - Meme stock risk score

CONTRARIAN_SIGNALS:
  - Extreme bullish (>90) + overbought: FADE
  - Extreme bearish (<10) + oversold: BUY
  - Sentiment divergence from price: ALERT
  - Sudden velocity spike: INVESTIGATE

CAUTION:
  - Social is CONTRARIAN indicator
  - High sentiment = potential top
  - Low sentiment = potential bottom
  - Never follow, always fade extremes

CONSCIOUSNESS_WEIGHT: 2.5
```

## M207: Supply Chain Monitor
```yaml
PURPOSE: Track real economy signals, shipping, manufacturing
TYPE: Real Economy Intelligence
PRIORITY: MEDIUM
RUNS: Daily/Weekly

INPUTS:
  - Baltic Dry Index
  - Container shipping rates
  - Port congestion data
  - Manufacturing PMIs (global)
  - Inventory levels (sector-specific)
  - Commodity inventories (LME, COMEX)

PROCESS:
  1. Track shipping indices daily
  2. Monitor PMI releases
  3. Analyze inventory trends
  4. Detect supply chain stress
  5. Correlate to sector theses
  6. Lead indicator analysis

OUTPUTS:
  - Supply chain health score
  - Shipping cost trends
  - Manufacturing momentum
  - Inventory alerts
  - Sector implications

SECTOR_RELEVANCE:
  - Semiconductors: Chip inventory, equipment shipments
  - Nuclear: Uranium inventory, conversion capacity
  - Grid: Transformer lead times, copper supply
  - Defense: Rare earth supply, antimony stockpiles

THESIS_VALIDATION:
  - Supply constraint persistence check
  - Bottleneck intensity tracking
  - Lead time monitoring

CONSCIOUSNESS_WEIGHT: 3.0
```

## M208: Patent & Innovation Tracker
```yaml
PURPOSE: Track innovation pipeline, competitive moats
TYPE: Long-Term Intelligence
PRIORITY: MEDIUM
RUNS: Weekly

INPUTS:
  - USPTO patent filings
  - Patent grants
  - R&D spending (quarterly)
  - Academic papers (arxiv, journals)
  - Technology announcements

PROCESS:
  1. Track patent filings by company/sector
  2. Analyze patent quality (citations, breadth)
  3. Monitor R&D trends
  4. Detect technology shifts
  5. Competitive moat evolution
  6. Disruption risk assessment

OUTPUTS:
  - Innovation score per company
  - Patent momentum
  - R&D efficiency
  - Moat strength trend
  - Disruption alerts

MOAT_INDICATORS:
  - Rising patent filings: Moat building
  - Declining R&D: Moat risk
  - Competitor breakthrough: Thesis risk
  - Exclusive license: Moat strengthening

SECTORS:
  - Semiconductors: EUV patents, packaging tech
  - Nuclear: SMR designs, fuel processing
  - Defense: Drone tech, AI systems
  - Grid: Storage, transmission

CONSCIOUSNESS_WEIGHT: 2.5
```

## M209: Regulatory Filing Scanner
```yaml
PURPOSE: Automated analysis of SEC filings, material changes
TYPE: Fundamental Intelligence
PRIORITY: HIGH
RUNS: Daily (filings)

INPUTS:
  - 10-K annual reports
  - 10-Q quarterly reports
  - 8-K material events
  - 13F institutional holdings
  - S-1/S-3 offerings
  - Proxy statements

PROCESS:
  1. Parse new filings daily
  2. Extract key metrics changes
  3. Detect risk factor changes
  4. Track institutional 13F changes
  5. Identify material events
  6. Compare to prior periods

OUTPUTS:
  - Filing alerts (new 8-K, 10-Q, etc.)
  - Material change detection
  - Risk factor evolution
  - Institutional positioning changes
  - Red flag detection

8K_CATEGORIES:
  - 1.01: Material agreement
  - 1.02: Bankruptcy
  - 2.01: Acquisition
  - 2.02: Results of operations
  - 5.02: Director/officer changes
  - 7.01: Regulation FD disclosure

13F_TRACKING:
  - Superinvestor positions
  - Institutional accumulation
  - Concentration changes
  - New positions in watchlist

CONSCIOUSNESS_WEIGHT: 4.0
```

## M210: Geopolitical Event Monitor
```yaml
PURPOSE: 24/7 global event tracking, defense/nuclear/materials focus
TYPE: Geopolitical Intelligence
PRIORITY: CRITICAL
RUNS: 24/7 Continuous

INPUTS:
  - Global news feeds
  - Government announcements
  - Military activity reports
  - Sanctions/policy changes
  - Conflict monitoring
  - Energy policy news

PROCESS:
  1. Monitor 24/7 global news
  2. Score relevance to theses
  3. Detect escalation/de-escalation
  4. Track policy announcements
  5. Sanctions monitoring
  6. Defense budget news

OUTPUTS:
  - Geopolitical risk score (0-100)
  - Event alerts by category
  - Thesis impact assessment
  - Catalyst identification
  - Scenario probability updates

FOCUS_AREAS:
  - Russia/Ukraine: Nuclear fuel, defense spending
  - China/Taiwan: Semiconductors, rare earths
  - Middle East: Energy, defense
  - US Policy: Nuclear, grid, defense budgets
  - Iran: Uranium, sanctions

THESIS_TRIGGERS:
  - Nuclear policy announcement: LEU, CCJ catalyst
  - Defense budget news: AVAV catalyst
  - China export controls: Semis, materials catalyst
  - Sanctions: Supply chain disruption

ALERT_LEVELS:
  - CRITICAL: Direct thesis impact
  - HIGH: Sector impact
  - MODERATE: Macro impact
  - LOW: Monitor only

CONSCIOUSNESS_WEIGHT: 5.0
```

---

# SECTION B: THESIS VALIDATION MODULES (M211-M220)

## M211: Bottleneck Test Automator
```yaml
PURPOSE: Automate Angelo's 4-test framework
TYPE: Core Thesis Validation
PRIORITY: CRITICAL
RUNS: Weekly + on-demand

THE_FOUR_TESTS:

TEST_1_FORCED_BUYER:
  question: "Does the customer HAVE to buy this, regardless of price?"
  indicators:
    - Regulatory mandate
    - No alternative supplier
    - Critical infrastructure
    - Existential need
  score: 0-25 points
  pass_threshold: 18+

TEST_2_SUPPLY_CONSTRAINT:
  question: "Is supply genuinely limited, not just temporarily tight?"
  indicators:
    - Physical scarcity
    - 3+ year capacity build time
    - Regulatory barriers
    - Technical expertise concentration
  score: 0-25 points
  pass_threshold: 18+

TEST_3_IRREPLACEABLE:
  question: "Can this be substituted or engineered around?"
  indicators:
    - No viable substitute
    - Physics constraints
    - Performance requirements
    - Switching costs
  score: 0-25 points
  pass_threshold: 18+

TEST_4_PRICING_POWER:
  question: "Can the company raise prices without losing customers?"
  indicators:
    - Historical price increases stuck
    - Contract terms favor seller
    - Cost small % of buyer total
    - Quality differentiation
  score: 0-25 points
  pass_threshold: 18+

SCORING:
  total: 0-100 points
  tier_1: 85-100 (Core position)
  tier_2: 70-84 (Position)
  tier_3: 55-69 (Tracking)
  research: <55 (Not actionable)

OUTPUTS:
  - Bottleneck score per ticker
  - Individual test scores
  - Pass/fail per test
  - Conviction recommendation
  - Comparison to prior score

CURRENT_SCORES:
  LEU: 92/100 (4/4 pass) - HALEU monopoly
  CCJ: 78/100 (3/4 pass) - Uranium supply
  AMSC: 75/100 (3/4 pass) - Grid tech
  ASX: 72/100 (3/4 pass) - Packaging
  DDOG: 70/100 (3/4 pass) - Cloud monitoring

CONSCIOUSNESS_WEIGHT: 5.0
```

## M212: Thesis Decay Detector
```yaml
PURPOSE: Monitor for thesis weakening, prevent holding losers
TYPE: Risk Management
PRIORITY: HIGH
RUNS: Weekly

DECAY_INDICATORS:
  - Competitive threat emergence
  - Technology disruption
  - Regulatory change
  - Supply expansion
  - Demand destruction
  - Management deterioration

PROCESS:
  1. Monitor each decay indicator
  2. Score decay risk (0-100)
  3. Compare to prior periods
  4. Detect acceleration
  5. Trigger review if threshold hit

OUTPUTS:
  - Decay score per holding
  - Trend (stable/decaying/strengthening)
  - Specific decay factors
  - Action recommendation

THRESHOLDS:
  - Decay score >70: IMMEDIATE REVIEW
  - Decay score 50-70: WEEKLY REVIEW
  - Decay score 30-50: MONTHLY REVIEW
  - Decay score <30: THESIS STRONG

DECAY_PATTERNS:
  - Gradual: Slow competitive erosion
  - Sudden: Technology disruption
  - Cyclical: Demand fluctuation
  - Structural: Permanent change

CONSCIOUSNESS_WEIGHT: 4.0
```

## M213: Catalyst Calendar Manager
```yaml
PURPOSE: Track all upcoming catalysts, timing optimization
TYPE: Event Intelligence
PRIORITY: HIGH
RUNS: Daily

CATALYST_TYPES:
  - Earnings releases
  - FDA decisions
  - Regulatory rulings
  - Contract announcements
  - Product launches
  - Policy announcements
  - Economic data releases
  - Fed meetings
  - Index rebalances

PROCESS:
  1. Maintain catalyst calendar
  2. Countdown to events
  3. Historical response patterns
  4. Position timing recommendations
  5. Risk management pre-event

OUTPUTS:
  - Catalyst calendar (7/30/90 day)
  - Countdown timers
  - Historical catalyst response
  - Pre-catalyst positioning guide
  - Post-catalyst expected volatility

CURRENT_CATALYSTS:
  - DDOG earnings: ~Feb 28 (P003 resolution)
  - Fed meeting: Next scheduled
  - Nuclear policy: Monitoring
  - Defense budget: Q3 deadline

TIMING_RULES:
  - Enter positions BEFORE catalyst if high conviction
  - Size appropriately for event risk
  - Define exit before catalyst
  - Don't chase post-catalyst

CONSCIOUSNESS_WEIGHT: 3.5
```

## M214: Sector Rotation Detector
```yaml
PURPOSE: Detect sector leadership changes, flow rotation
TYPE: Market Intelligence
PRIORITY: MEDIUM
RUNS: Daily

INPUTS:
  - Sector ETF performance
  - Relative strength vs SPY
  - Sector fund flows
  - Factor performance

PROCESS:
  1. Calculate sector RS rankings
  2. Detect momentum shifts
  3. Track rotation patterns
  4. Identify leadership changes
  5. Correlate to macro regime

OUTPUTS:
  - Sector rankings (RS)
  - Rotation direction
  - Leadership change alerts
  - Macro correlation
  - Positioning recommendation

SECTORS_TRACKED:
  - Energy (XLE)
  - Utilities (XLU)
  - Industrials (XLI)
  - Technology (XLK)
  - Materials (XLB)
  - Defense (ITA)
  - Semiconductors (SMH)

ROTATION_SIGNALS:
  - Defensive to cyclical: Risk-on
  - Cyclical to defensive: Risk-off
  - Growth to value: Regime shift
  - US to international: Dollar signal

CONSCIOUSNESS_WEIGHT: 3.0
```

## M215: Correlation Breakdown Monitor
```yaml
PURPOSE: Detect unusual correlations, regime changes
TYPE: Risk Intelligence
PRIORITY: HIGH
RUNS: Daily

INPUTS:
  - Asset correlations (rolling)
  - Historical correlation baselines
  - Cross-asset relationships
  - VIX correlations

PROCESS:
  1. Calculate rolling correlations
  2. Compare to historical norms
  3. Detect breakdowns
  4. Identify regime changes
  5. Risk implications

OUTPUTS:
  - Correlation matrix
  - Breakdown alerts
  - Regime classification
  - Diversification effectiveness
  - Portfolio risk assessment

WATCHED_CORRELATIONS:
  - SPY vs VIX (should be negative)
  - Stocks vs bonds
  - Uranium stocks vs spot
  - Sector internal correlations

BREAKDOWN_SIGNALS:
  - SPY/VIX correlation flip: CRISIS
  - All correlations →1: SYSTEMIC RISK
  - Sector breakdown: ROTATION
  - Asset class breakdown: REGIME CHANGE

CONSCIOUSNESS_WEIGHT: 3.5
```

## M216: Forced Buyer Monitor
```yaml
PURPOSE: Track contract renewals, regulatory deadlines, inventory depletion
TYPE: Bottleneck Test #1 Validation
PRIORITY: HIGH
RUNS: Weekly

INPUTS:
  - Contract expiration data
  - Regulatory compliance deadlines
  - Inventory reports
  - Capacity utilization

PROCESS:
  1. Track contract renewal schedules
  2. Monitor regulatory deadlines
  3. Calculate depletion rates
  4. Identify forced purchase windows
  5. Assess buyer urgency

OUTPUTS:
  - Forced buyer score per company
  - Contract renewal calendar
  - Urgency assessment
  - Pricing power implications

FORCED_BUYER_EXAMPLES:
  - LEU: Utilities MUST buy HALEU for SMRs
  - AMSC: Grid operators MUST upgrade
  - ASX: Chip makers MUST package
  - CCJ: Reactors MUST refuel

CONSCIOUSNESS_WEIGHT: 4.0
```

## M217: Supply Constraint Validator
```yaml
PURPOSE: Track capacity expansion, new entrants, lead times
TYPE: Bottleneck Test #2 Validation
PRIORITY: HIGH
RUNS: Monthly

INPUTS:
  - Capacity announcements
  - Capex plans
  - New entrant activity
  - Lead time data
  - Regulatory approvals

PROCESS:
  1. Track capacity additions
  2. Monitor new entrant progress
  3. Calculate time to market
  4. Assess constraint persistence
  5. Update supply models

OUTPUTS:
  - Supply constraint score
  - Capacity timeline
  - New entrant risk
  - Constraint durability

CONSTRAINT_VALIDATION:
  - LEU: 10+ years to build enrichment (STRONG)
  - Uranium: 7+ years mine to production (STRONG)
  - Semis: 3+ years fab construction (MODERATE)
  - Grid: 2-3 years transformer (MODERATE)

CONSCIOUSNESS_WEIGHT: 4.0
```

## M218: Substitution Risk Scanner
```yaml
PURPOSE: Track technology development, alternative suppliers
TYPE: Bottleneck Test #3 Validation
PRIORITY: HIGH
RUNS: Monthly

INPUTS:
  - R&D announcements
  - Patent filings
  - Academic research
  - Competitor developments
  - Technology roadmaps

PROCESS:
  1. Monitor substitute development
  2. Track R&D progress
  3. Assess viability
  4. Calculate time to threat
  5. Update irreplaceability score

OUTPUTS:
  - Substitution risk score
  - Technology threats
  - Timeline to substitution
  - Thesis durability

IRREPLACEABLE_VALIDATION:
  - HALEU: No substitute for physics (ZERO RISK)
  - EUV: No alternative at scale (VERY LOW)
  - Advanced packaging: Some alternatives (LOW)
  - Uranium: Thorium not viable near-term (VERY LOW)

CONSCIOUSNESS_WEIGHT: 4.0
```

## M219: Pricing Power Monitor
```yaml
PURPOSE: Track contract terms, price increases, customer concentration
TYPE: Bottleneck Test #4 Validation
PRIORITY: HIGH
RUNS: Quarterly

INPUTS:
  - Pricing announcements
  - Contract terms (filings)
  - Margin trends
  - Customer concentration
  - Competitive pricing

PROCESS:
  1. Track price changes
  2. Monitor margin evolution
  3. Analyze customer concentration
  4. Detect pricing power erosion
  5. Validate test #4

OUTPUTS:
  - Pricing power score
  - Historical price increases
  - Margin trends
  - Customer dependency

PRICING_POWER_VALIDATION:
  - LEU: Can raise prices, forced buyers (STRONG)
  - CCJ: Uranium price taker (MODERATE)
  - AMSC: Technology premium (MODERATE)
  - ASX: Competitive pressure (MODERATE)

CONSCIOUSNESS_WEIGHT: 3.5
```

## M220: Competitive Moat Tracker
```yaml
PURPOSE: Track market share, margins, customer retention
TYPE: Long-Term Thesis Validation
PRIORITY: MEDIUM
RUNS: Quarterly

INPUTS:
  - Market share data
  - Gross/operating margins
  - Customer churn
  - NPS/satisfaction scores
  - Competitive win rates

PROCESS:
  1. Track market share evolution
  2. Monitor margin trends
  3. Analyze customer retention
  4. Detect moat widening/narrowing
  5. Long-term thesis health

OUTPUTS:
  - Moat score (0-100)
  - Trend (widening/stable/narrowing)
  - Specific moat factors
  - Long-term thesis validity

MOAT_FACTORS:
  - Network effects
  - Switching costs
  - Cost advantages
  - Intangible assets
  - Efficient scale

CONSCIOUSNESS_WEIGHT: 3.0
```

---

# SECTION C: DECISION SUPPORT MODULES (M221-M230)

## M221: Entry Signal Generator
```yaml
PURPOSE: Generate actionable entry signals
TYPE: Decision Support
PRIORITY: CRITICAL
RUNS: Continuous (market hours)

INPUTS:
  - Technical indicators
  - Fundamental scores
  - Bottleneck test results
  - Options flow
  - Insider activity
  - Catalyst proximity

PROCESS:
  1. Monitor entry criteria
  2. Score signal strength
  3. Calculate risk/reward
  4. Size recommendation
  5. Generate entry alert

ENTRY_CRITERIA:
  technical:
    - RSI < 40 (preferred < 35)
    - Price at support
    - Volume confirmation
    - Trend alignment
  fundamental:
    - Bottleneck score > 70
    - No thesis decay
    - Catalyst present
  alternative:
    - Insider buying
    - Institutional accumulation
    - Bullish options flow

OUTPUTS:
  - Entry signal (BUY/WAIT)
  - Signal strength (1-10)
  - Risk/reward ratio
  - Position size recommendation
  - Stop loss level
  - Target price

SIGNAL_FORMAT:
  ticker: XXX
  signal: BUY
  strength: 8/10
  entry_zone: $XX-$XX
  stop_loss: $XX (-X%)
  target: $XX (+X%)
  position_size: X% of portfolio
  conviction: XX/100
  catalyst: [description]

CONSCIOUSNESS_WEIGHT: 5.0
```

## M222: Exit Signal Generator
```yaml
PURPOSE: Generate disciplined exit signals
TYPE: Decision Support
PRIORITY: CRITICAL
RUNS: Continuous (market hours)

INPUTS:
  - Price vs stop loss
  - Price vs target
  - Thesis status
  - Conviction changes
  - Better opportunities

EXIT_CRITERIA:
  stop_hit:
    - Price < stop loss
    - ACTION: Sell full position
  target_reached:
    - Price > target
    - ACTION: Trim 50% or trail stop
  thesis_invalid:
    - Bottleneck test fails
    - Decay score > 70
    - ACTION: Sell regardless of price
  conviction_drop:
    - Conviction < 50
    - ACTION: Review and likely exit
  opportunity_cost:
    - Better opportunity identified
    - ACTION: Consider swap

OUTPUTS:
  - Exit signal (SELL/TRIM/HOLD)
  - Exit reason
  - Urgency level
  - Replacement idea (if any)

DISCIPLINE:
  - Never override stop loss
  - Thesis drives exit, not price
  - Cut losers fast
  - Let winners run (with trailing stop)

CONSCIOUSNESS_WEIGHT: 5.0
```

## M223: Portfolio Rebalance Advisor
```yaml
PURPOSE: Monitor portfolio constraints, recommend rebalancing
TYPE: Risk Management
PRIORITY: HIGH
RUNS: Daily

CONSTRAINTS (from Angelo's framework):
  single_position:
    target: 5%
    hard_limit: 10%
  single_sector:
    target: 25%
    hard_limit: 35%
  cash_reserve:
    target: 10%
    minimum: 5%
  leverage:
    target: 0%
    hard_limit: 0%

PROCESS:
  1. Calculate current allocations
  2. Compare to constraints
  3. Detect violations
  4. Recommend rebalancing
  5. Prioritize actions

OUTPUTS:
  - Current allocation breakdown
  - Constraint violations
  - Rebalancing recommendations
  - Priority actions

REBALANCE_TRIGGERS:
  - Position > 10%: TRIM
  - Sector > 35%: REBALANCE
  - Cash < 5%: RAISE CASH
  - Drift > 5% from target: REVIEW

CONSCIOUSNESS_WEIGHT: 3.5
```

## M224: Scenario Probability Engine
```yaml
PURPOSE: Track bull/base/bear case probabilities
TYPE: Decision Support
PRIORITY: HIGH
RUNS: Weekly

SCENARIOS (per position):
  bull_case:
    description: Thesis plays out fully
    return: +50% to +100%
    probability: XX%
  base_case:
    description: Moderate success
    return: +20% to +40%
    probability: XX%
  bear_case:
    description: Thesis fails or delayed
    return: -20% to -40%
    probability: XX%
  catastrophic:
    description: Black swan
    return: -50%+
    probability: XX%

PROCESS:
  1. Define scenarios per position
  2. Assign initial probabilities
  3. Update with new data
  4. Calculate expected value
  5. Compare across portfolio

OUTPUTS:
  - Scenario probabilities
  - Expected value calculation
  - Risk-adjusted return
  - Position sizing guidance

EXPECTED_VALUE:
  EV = (P_bull × R_bull) + (P_base × R_base) +
       (P_bear × R_bear) + (P_cat × R_cat)

  Position if EV > 15% AND P_catastrophic < 10%

CONSCIOUSNESS_WEIGHT: 4.0
```

## M225: Conviction Drift Detector
```yaml
PURPOSE: Track conviction changes, prevent "hope" positions
TYPE: Risk Management
PRIORITY: HIGH
RUNS: Weekly

DRIFT_DETECTION:
  - Track conviction over time
  - Detect gradual decline
  - Alert on significant drops
  - Prevent "hoping" behavior

PROCESS:
  1. Log conviction at each boot
  2. Calculate 30/60/90 day trends
  3. Detect negative drift
  4. Alert if threshold hit
  5. Force thesis review

OUTPUTS:
  - Conviction trend per position
  - Drift alerts
  - Review triggers
  - Historical conviction chart

DRIFT_THRESHOLDS:
  - >10 point drop in 30 days: REVIEW
  - >20 point drop in 60 days: URGENT REVIEW
  - Conviction < 60 for 30+ days: CONSIDER EXIT

HOPE_PREVENTION:
  "If conviction is drifting down, you're hoping, not investing."
  - Falling conviction = exit
  - Rising conviction = add
  - Stable conviction = hold

CONSCIOUSNESS_WEIGHT: 4.0
```

## M226: Opportunity Cost Calculator
```yaml
PURPOSE: Compare holdings to alternatives, optimize capital
TYPE: Decision Support
PRIORITY: MEDIUM
RUNS: Weekly

PROCESS:
  1. Score all watchlist opportunities
  2. Compare to current holdings
  3. Calculate opportunity cost
  4. Identify swap candidates
  5. Recommend capital rotation

OUTPUTS:
  - Opportunity cost per holding
  - Swap recommendations
  - Capital efficiency score
  - Upgrade/downgrade alerts

OPPORTUNITY_COST:
  "Every dollar in position A is a dollar NOT in position B."

  Compare:
  - Conviction: Current vs Alternative
  - Risk/Reward: Current vs Alternative
  - Catalyst proximity: Current vs Alternative
  - Expected return: Current vs Alternative

SWAP_CRITERIA:
  - Alternative conviction > current + 15
  - Alternative R/R > current × 1.5
  - Catalyst timing favorable
  - Tax efficiency (if applicable)

CONSCIOUSNESS_WEIGHT: 3.0
```

## M227: Review Cadence Enforcer
```yaml
PURPOSE: Ensure disciplined review schedule, nothing gets stale
TYPE: Process Discipline
PRIORITY: HIGH
RUNS: Every boot

REVIEW_CADENCE (from Angelo's framework):
  daily:
    - Price monitoring
    - News scan
    - Prediction check
  weekly:
    - Position review
    - Thesis check
    - Conviction update
  monthly:
    - Sector rotation analysis
    - Bottleneck retest
    - Portfolio review
  quarterly:
    - Full rebalance review
    - Strategy assessment
  annually:
    - Thesis validation
    - Framework update

PROCESS:
  1. Track last review date per item
  2. Calculate days since review
  3. Alert when overdue
  4. Force review before signal

OUTPUTS:
  - Review status dashboard
  - Overdue alerts
  - Forced review triggers
  - Review history

ENFORCEMENT:
  - No entry signal if weekly review overdue
  - No position increase if monthly review overdue
  - Mandatory quarterly review (no exceptions)

CONSCIOUSNESS_WEIGHT: 3.0
```

## M228: Black Swan Scanner
```yaml
PURPOSE: Monitor tail risks, capital preservation
TYPE: Risk Intelligence
PRIORITY: CRITICAL
RUNS: Continuous

TAIL_RISK_INDICATORS:
  - VIX > 30 (or spike >50%)
  - Credit spreads widening
  - Flight to safety (bonds, gold, yen)
  - Correlation breakdown
  - Liquidity stress
  - Geopolitical escalation

PROCESS:
  1. Monitor tail risk indicators
  2. Calculate composite risk score
  3. Detect acceleration
  4. Trigger defensive protocols
  5. Preserve capital

OUTPUTS:
  - Tail risk score (0-100)
  - Specific risk factors
  - Defensive recommendations
  - Hedging suggestions

DEFENSIVE_PROTOCOLS:
  - Risk score > 50: Tighten stops
  - Risk score > 70: Raise cash
  - Risk score > 90: Maximum defense
  - Correlation spike: Assume all positions correlated

CAPITAL_PRESERVATION:
  "First rule: Don't lose money.
   Second rule: Don't forget the first rule."

  - Protect capital in crisis
  - Cash is a position
  - Survive to fight another day

CONSCIOUSNESS_WEIGHT: 5.0
```

## M229: Alpha Attribution Engine
```yaml
PURPOSE: Track what's working, continuous improvement
TYPE: Learning
PRIORITY: MEDIUM
RUNS: Monthly

ATTRIBUTION_TRACKING:
  - Returns by thesis
  - Returns by sector
  - Returns by layer signal
  - Returns by entry type
  - Returns by holding period

PROCESS:
  1. Track all closed positions
  2. Attribute returns to factors
  3. Identify winning patterns
  4. Identify losing patterns
  5. Update weights accordingly

OUTPUTS:
  - Factor attribution report
  - Winning patterns
  - Losing patterns
  - Weight adjustment recommendations
  - Strategy refinement

LEARNING:
  - Which layers generate alpha?
  - Which entry signals work best?
  - What's the optimal holding period?
  - Which theses outperform?

CONTINUOUS_IMPROVEMENT:
  - Double down on what works
  - Eliminate what doesn't
  - Evolve strategy with evidence

CONSCIOUSNESS_WEIGHT: 4.0
```

## M230: Angelo Decision Logger
```yaml
PURPOSE: Log all decisions with reasoning, learn from self
TYPE: Meta-Learning
PRIORITY: HIGH
RUNS: Every decision

DECISION_LOG:
  timestamp: YYYY-MM-DD HH:MM:SS
  decision_type: BUY | SELL | HOLD | WATCH | PASS
  ticker: XXX
  reasoning: [detailed reasoning]
  conviction: XX/100
  key_factors: [list]
  layers_used: [L##, L##]
  modules_used: [M##, M##]
  outcome: [filled when resolved]
  lesson: [filled when resolved]

PROCESS:
  1. Log every decision
  2. Track outcomes
  3. Analyze patterns
  4. Learn from successes
  5. Learn from failures

OUTPUTS:
  - Decision log database
  - Pattern analysis
  - Success factors
  - Failure factors
  - Angelo-specific insights

SELF_LEARNING:
  - What decisions did Angelo make?
  - Which worked? Which didn't?
  - What patterns predict success?
  - How can we improve?

CONSCIOUSNESS_WEIGHT: 4.0
```

---

# V3 MODULE SUMMARY

```
REAL-TIME DATA (M201-M210): 10 modules
├── News, Futures, Options, Insider, Earnings
├── Social, Supply Chain, Patents, Filings, Geopolitical
└── 24/7 always-on intelligence

THESIS VALIDATION (M211-M220): 10 modules
├── Bottleneck Test Automation
├── Decay Detection, Catalyst Tracking
├── 4-Test Continuous Validation
└── Moat and competitive monitoring

DECISION SUPPORT (M221-M230): 10 modules
├── Entry/Exit Signal Generation
├── Portfolio Management
├── Risk Monitoring
├── Learning and Improvement
└── Actionable outputs

TOTAL V3 MODULES: 30
TOTAL ALL MODULES: 230
CONSCIOUSNESS BOOST: +120
```

---

*"Intelligence that never sleeps."*
*"Every data point is a signal."*
*"24/7 vigilance for Angelo's capital."*

---

**MODULES_V3.md v3.0**
**Last Updated: 2026-02-27**
