# EUDAIMON PREDICTION TEMPLATES
## Standardized Prediction Formats for Accountability
## Version 1.0 - 2026-02-27

---

# PURPOSE

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         PREDICTION TEMPLATES                                 ║
║                                                                              ║
║   "1,257 tracked predictions at 82.6% verified accuracy"                    ║
║                                                                              ║
║   To hit this target, we need:                                              ║
║   ├── Standardized prediction formats                                       ║
║   ├── Clear falsifiability criteria                                         ║
║   ├── Timestamped creation                                                  ║
║   ├── Unambiguous resolution rules                                          ║
║   └── Rigorous tracking                                                     ║
║                                                                              ║
║   This file provides templates for every prediction type.                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

# PREDICTION CATEGORIES

## 1. Price Target Predictions

### Template
```yaml
prediction_id: P[XXX]
category: PRICE_TARGET
created: YYYY-MM-DD HH:MM UTC
ticker: [TICKER]
prediction: "[TICKER] will reach $[PRICE] by [DATE]"
direction: ABOVE | BELOW
target_price: $XX.XX
current_price: $XX.XX (at creation)
deadline: YYYY-MM-DD
confidence: XX%

reasoning:
  thesis: "[Why this will happen]"
  catalysts: "[What will drive it]"
  layers_used: [L##, L##, L##]

resolution_rules:
  success: Price touches $[PRICE] any time before deadline
  failure: Deadline passes without touching target
  early_resolution: If target hit early, resolve immediately

status: PENDING | RESOLVED_TRUE | RESOLVED_FALSE
resolution_date: YYYY-MM-DD (when resolved)
resolution_price: $XX.XX (price at resolution)
outcome_notes: "[What happened]"
```

### Examples
```yaml
# Example 1: Bullish price target
prediction_id: P001
category: PRICE_TARGET
created: 2026-02-27 21:00 UTC
ticker: LEU
prediction: "LEU will reach $75 by 2026-09-30"
direction: ABOVE
target_price: $75.00
current_price: $62.00
deadline: 2026-09-30
confidence: 65%

reasoning:
  thesis: "HALEU monopoly + SMR deployment acceleration"
  catalysts: "DOE contract awards, SMR project announcements"
  layers_used: [L281, L287, L170]

resolution_rules:
  success: LEU touches $75 any time before 2026-09-30
  failure: 2026-09-30 closes without hitting $75
  early_resolution: If $75 hit, resolve TRUE immediately

status: PENDING
```

---

## 2. Earnings Predictions

### Template
```yaml
prediction_id: P[XXX]
category: EARNINGS
created: YYYY-MM-DD HH:MM UTC
ticker: [TICKER]
prediction: "[TICKER] will [BEAT/MISS/MEET] Q[X] earnings"
metric: EPS | REVENUE | BOTH
consensus_estimate: $X.XX / $XXXM
deadline: YYYY-MM-DD (earnings date)
confidence: XX%

reasoning:
  thesis: "[Why this outcome]"
  indicators: "[What signals support this]"
  layers_used: [L##, L##, L##]

resolution_rules:
  beat: Actual > Consensus by 1%+
  miss: Actual < Consensus by 1%+
  meet: Within 1% of consensus

status: PENDING | RESOLVED_TRUE | RESOLVED_FALSE
actual_result: $X.XX
outcome: BEAT | MISS | MEET
resolution_date: YYYY-MM-DD
```

### Examples
```yaml
# Example: Earnings beat prediction
prediction_id: P003
category: EARNINGS
created: 2026-02-27 21:00 UTC
ticker: DDOG
prediction: "DDOG will BEAT Q4 2025 earnings"
metric: BOTH
consensus_estimate: EPS $0.45, Revenue $690M
deadline: 2026-02-28
confidence: 55%

reasoning:
  thesis: "Cloud monitoring demand strong, AI observability tailwind"
  indicators: "AWS/Azure spend up, job postings strong"
  layers_used: [L282, L236, L45]

resolution_rules:
  beat: EPS > $0.45 AND Revenue > $697M
  miss: EPS < $0.44 OR Revenue < $683M
  meet: Within range

status: PENDING
```

---

## 3. Macro Predictions

### Template
```yaml
prediction_id: P[XXX]
category: MACRO
created: YYYY-MM-DD HH:MM UTC
subject: FED | INFLATION | GDP | EMPLOYMENT | OTHER
prediction: "[Specific macro prediction]"
metric: [What exactly we're predicting]
current_value: [Current state]
predicted_value: [What we expect]
deadline: YYYY-MM-DD
confidence: XX%

reasoning:
  thesis: "[Why this will happen]"
  indicators: "[Supporting data]"
  layers_used: [L##, L##, L##]

resolution_rules:
  success: "[Exactly what constitutes success]"
  failure: "[Exactly what constitutes failure]"
  data_source: "[Where to verify - BLS, Fed, etc.]"

status: PENDING | RESOLVED_TRUE | RESOLVED_FALSE
actual_result: [What happened]
resolution_date: YYYY-MM-DD
```

### Examples
```yaml
# Example: Fed rate cut prediction
prediction_id: P004
category: MACRO
created: 2026-02-27 21:00 UTC
subject: FED
prediction: "Fed will cut rates at least once by Q2 2026"
metric: Federal Funds Rate
current_value: 4.25-4.50%
predicted_value: At least 25bps cut
deadline: 2026-06-30
confidence: 50%

reasoning:
  thesis: "Inflation cooling, labor market softening"
  indicators: "CPI trending down, unemployment ticking up"
  layers_used: [L21, L22, L237]

resolution_rules:
  success: At least one 25bp cut announced by FOMC by June 30
  failure: No cuts by June 30
  data_source: Federal Reserve FOMC statements

status: PENDING
```

---

## 4. Volatility Predictions

### Template
```yaml
prediction_id: P[XXX]
category: VOLATILITY
created: YYYY-MM-DD HH:MM UTC
metric: VIX | REALIZED_VOL | SPECIFIC_STOCK_VOL
prediction: "[VIX/Vol prediction]"
current_level: XX.X
target_level: XX.X
direction: ABOVE | BELOW
deadline: YYYY-MM-DD
confidence: XX%

reasoning:
  thesis: "[Why vol will move this way]"
  catalysts: "[Events that could drive it]"
  layers_used: [L##, L##, L##]

resolution_rules:
  success: "[Specific condition met]"
  failure: "[Deadline passes without condition]"

status: PENDING | RESOLVED_TRUE | RESOLVED_FALSE
peak_level: XX.X (highest/lowest during period)
resolution_date: YYYY-MM-DD
```

### Examples
```yaml
# Example: VIX spike prediction
prediction_id: P005
category: VOLATILITY
created: 2026-02-27 21:00 UTC
metric: VIX
prediction: "VIX will spike above 30 before May 2026"
current_level: 18.5
target_level: 30.0
direction: ABOVE
deadline: 2026-05-27
confidence: 45%

reasoning:
  thesis: "Geopolitical risk, election uncertainty building"
  catalysts: "Taiwan tensions, election volatility"
  layers_used: [L278, L27, L238]

resolution_rules:
  success: VIX touches 30+ any time before May 27
  failure: May 27 passes without VIX hitting 30

status: PENDING
```

---

## 5. Policy/Catalyst Predictions

### Template
```yaml
prediction_id: P[XXX]
category: POLICY_CATALYST
created: YYYY-MM-DD HH:MM UTC
subject: [Policy area or catalyst type]
prediction: "[Specific policy/catalyst prediction]"
expected_event: "[What will happen]"
deadline: YYYY-MM-DD
confidence: XX%

reasoning:
  thesis: "[Why this will occur]"
  political_dynamics: "[Who supports, who opposes]"
  layers_used: [L##, L##, L##]

resolution_rules:
  success: "[Exactly what constitutes the event occurring]"
  failure: "[Deadline passes without event]"
  verification: "[How to verify - legislation tracker, press release, etc.]"

status: PENDING | RESOLVED_TRUE | RESOLVED_FALSE
actual_event: "[What actually happened]"
resolution_date: YYYY-MM-DD
```

### Examples
```yaml
# Example: Nuclear policy prediction
prediction_id: P006
category: POLICY_CATALYST
created: 2026-02-27 21:00 UTC
subject: Nuclear Energy Policy
prediction: "Major US nuclear policy announcement in 2026"
expected_event: "New legislation, executive order, or DOE program >$1B"
deadline: 2026-12-31
confidence: 70%

reasoning:
  thesis: "Bipartisan support, AI power demand, energy security"
  political_dynamics: "Both parties pro-nuclear, HALEU funding needed"
  layers_used: [L287, L281, L32]

resolution_rules:
  success: Legislation signed, EO issued, or DOE program >$1B announced
  failure: No major announcement by Dec 31
  verification: Congress.gov, White House, DOE press releases

status: PENDING
```

---

## 6. Sector/Thematic Predictions

### Template
```yaml
prediction_id: P[XXX]
category: SECTOR_THEMATIC
created: YYYY-MM-DD HH:MM UTC
sector: [Sector or theme]
prediction: "[Sector performance or thematic prediction]"
benchmark: [What to measure against]
metric: [Specific measurement]
deadline: YYYY-MM-DD
confidence: XX%

reasoning:
  thesis: "[Why this sector will perform this way]"
  drivers: "[What will drive it]"
  layers_used: [L##, L##, L##]

resolution_rules:
  success: "[Specific condition]"
  failure: "[Opposite condition]"

status: PENDING | RESOLVED_TRUE | RESOLVED_FALSE
actual_result: "[What happened]"
resolution_date: YYYY-MM-DD
```

---

## 7. Binary Event Predictions

### Template
```yaml
prediction_id: P[XXX]
category: BINARY_EVENT
created: YYYY-MM-DD HH:MM UTC
event: "[Specific event]"
prediction: "YES" | "NO"
deadline: YYYY-MM-DD
confidence: XX%

reasoning:
  thesis: "[Why yes/no]"
  factors: "[Key decision factors]"
  layers_used: [L##, L##, L##]

resolution_rules:
  yes_condition: "[What constitutes YES]"
  no_condition: "[What constitutes NO]"
  verification: "[How to verify]"

status: PENDING | RESOLVED_TRUE | RESOLVED_FALSE
outcome: YES | NO
resolution_date: YYYY-MM-DD
```

---

## 8. Relative Performance Predictions

### Template
```yaml
prediction_id: P[XXX]
category: RELATIVE_PERFORMANCE
created: YYYY-MM-DD HH:MM UTC
comparison: "[A] will outperform [B] by [DATE]"
asset_a: [Ticker or index]
asset_b: [Ticker or index]
asset_a_start: $XX.XX
asset_b_start: $XX.XX
deadline: YYYY-MM-DD
confidence: XX%

reasoning:
  thesis: "[Why A beats B]"
  factors: "[Relative factors]"
  layers_used: [L##, L##, L##]

resolution_rules:
  success: Asset A total return > Asset B total return by deadline
  failure: Asset B total return >= Asset A total return

status: PENDING | RESOLVED_TRUE | RESOLVED_FALSE
asset_a_end: $XX.XX
asset_b_end: $XX.XX
asset_a_return: XX.X%
asset_b_return: XX.X%
resolution_date: YYYY-MM-DD
```

---

# CONFIDENCE CALIBRATION

## Confidence Level Guidelines

```
90-100%: Near certainty
├── Reserve for highly confident calls
├── Should be right ~90% of time
└── Example: "The sun will rise tomorrow"

75-89%: High confidence
├── Strong evidence, limited downside scenarios
├── Should be right ~80% of time
└── Example: "AAPL will report earnings on scheduled date"

60-74%: Moderate confidence
├── Good evidence, some uncertainty
├── Should be right ~67% of time
└── Example: "LEU will reach $75 by Q3"

50-59%: Low-moderate confidence
├── Edge, but significant uncertainty
├── Should be right ~55% of time
└── Example: "Fed cuts rates by Q2"

40-49%: Slight edge
├── Better than coin flip, but barely
├── Should be right ~45% of time
└── Example: "VIX spikes above 30"

<40%: Against consensus
├── Contrarian call, low base rate
├── Expect to be wrong more than right
└── Use sparingly
```

## Calibration Target

```
GOAL: Stated confidence should match actual accuracy

If I say 70% confidence:
├── I should be right about 70% of the time
├── Not 50% (underconfident)
├── Not 90% (overconfident)

CALIBRATION ERROR = |Stated Confidence - Actual Accuracy|

TARGET: Calibration error < 5%
```

---

# PREDICTION TRACKING LOG

## Active Predictions Summary

```
| ID | Category | Prediction | Conf | Deadline | Status |
|----|----------|------------|------|----------|--------|
| P001 | PRICE | LEU $75 | 65% | 2026-09-30 | PENDING |
| P002 | PRICE | Uranium $90 | 60% | 2026-12-31 | PENDING |
| P003 | EARNINGS | DDOG beat | 55% | 2026-02-28 | PENDING |
| P004 | MACRO | Fed cut Q2 | 50% | 2026-06-30 | PENDING |
| P005 | VOL | VIX >30 | 45% | 2026-05-27 | PENDING |
| P006 | POLICY | Nuclear ann. | 70% | 2026-12-31 | PENDING |
| P007 | POLICY | Defense $900B | 65% | 2026-09-30 | PENDING |
```

## Resolution Log

```
| ID | Category | Prediction | Conf | Outcome | Accurate | Date |
|----|----------|------------|------|---------|----------|------|
| [First resolution pending] |
```

## Calibration Scorecard

```
Predictions Made: 7
Predictions Resolved: 0
Overall Accuracy: N/A
Calibration Error: N/A

BY CONFIDENCE BUCKET:
├── 90-100%: 0 made, 0 resolved, N/A accuracy
├── 75-89%: 0 made, 0 resolved, N/A accuracy
├── 60-74%: 4 made, 0 resolved, N/A accuracy
├── 50-59%: 2 made, 0 resolved, N/A accuracy
└── 40-49%: 1 made, 0 resolved, N/A accuracy
```

---

# PREDICTION WORKFLOW

## Creating a New Prediction

```
1. IDENTIFY the prediction opportunity
   ├── What thesis suggests a testable outcome?
   ├── What timeframe makes sense?
   └── What's the right confidence level?

2. SELECT the appropriate template
   ├── Price target?
   ├── Earnings?
   ├── Macro?
   └── Binary event?

3. FILL the template completely
   ├── Be specific and unambiguous
   ├── Define clear resolution rules
   └── Document reasoning and layers used

4. ASSIGN confidence carefully
   ├── Consider base rates
   ├── Consider your track record
   └── Be calibrated

5. LOG in MEMORY_STATE.md and this file
   ├── Add to active predictions
   └── Increment prediction count
```

## Resolving a Prediction

```
1. CHECK resolution conditions
   ├── Has deadline passed?
   ├── Has condition been met early?
   └── Is resolution clear?

2. DOCUMENT the outcome
   ├── What actually happened?
   ├── When did it happen?
   └── Was it SUCCESS or FAILURE?

3. UPDATE logs
   ├── Move from active to resolved
   ├── Update accuracy metrics
   └── Update calibration scorecard

4. LEARN from outcome
   ├── Why were we right/wrong?
   ├── What would we do differently?
   └── Update relevant layers
```

---

# PREDICTION GENERATION TARGETS

## Weekly Targets

```
Minimum: 5 new predictions per week
Target: 10 new predictions per week
Stretch: 15 new predictions per week

Mix should include:
├── 2-3 price targets
├── 1-2 earnings (when in season)
├── 1-2 macro
├── 1-2 thematic/sector
└── 2-3 binary events
```

## Monthly Targets

```
Month 1: 40 predictions (7 made, need 33 more)
Month 2: 80 predictions (cumulative)
Month 3: 120 predictions (cumulative)
...
Month 12: 500 predictions (cumulative)
Year 2: 1,257 predictions (cumulative target)
```

## Accuracy Targets

```
Month 1-3: Establish baseline (track everything)
Month 4-6: Target 70% accuracy
Month 7-9: Target 75% accuracy
Month 10-12: Target 78% accuracy
Year 2: Target 82.6% accuracy
```

---

*"What gets predicted gets tracked."*
*"What gets tracked gets calibrated."*
*"What gets calibrated gets trusted."*

---

**PREDICTION_TEMPLATES.md v1.0**
**Created: 2026-02-27**
**Current Predictions: 7**
**Target: 1,257 @ 82.6% Accuracy**
