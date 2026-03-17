# EUDAIMON BACKTESTING FRAMEWORK
## Validating Intelligence Through Historical Analysis

---

# PURPOSE

Before I trust my signals, I must prove they work. This framework:
1. Tests every thesis against historical data
2. Validates layer effectiveness
3. Measures prediction accuracy
4. Builds confidence through evidence

---

# BACKTESTING ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────┐
│                    BACKTESTING ENGINE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │ HISTORICAL  │───▶│   SIGNAL    │───▶│  SIMULATE   │         │
│  │    DATA     │    │ GENERATION  │    │   TRADES    │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                               │                 │
│                                               ▼                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   UPDATE    │◀───│   ANALYZE   │◀───│  CALCULATE  │         │
│  │   WEIGHTS   │    │   RESULTS   │    │   METRICS   │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

# DATA REQUIREMENTS

## Historical Data Needed

```
PRICE DATA:
├── Daily OHLCV (10+ years)
├── Intraday where available
├── Adjusted for splits/dividends
└── Including delisted securities (survivorship bias)

FUNDAMENTAL DATA:
├── Quarterly financials
├── Earnings estimates history
├── Revision history
└── Guidance history

ALTERNATIVE DATA:
├── Sentiment indices (historical)
├── Options positioning
├── Short interest
├── Insider transactions
└── 13F filings

MACRO DATA:
├── VIX history
├── Yield curves
├── DXY
├── Commodity prices
├── Economic releases
└── Fed balance sheet

GEOPOLITICAL DATA:
├── Conflict timeline
├── Policy changes
├── Sanction history
└── Election results
```

---

# BACKTEST TYPES

## Type 1: Layer Validation Backtest

Test if individual layers produce alpha:

```python
def backtest_layer(layer, data, start_date, end_date):
    """
    Test a single layer's signal quality
    """
    results = []

    for date in date_range(start_date, end_date):
        # Get layer signal on that date
        signal = layer.generate_signal(data.as_of(date))

        # Track forward returns
        forward_returns = {
            "1d": calculate_return(date, date + 1),
            "5d": calculate_return(date, date + 5),
            "20d": calculate_return(date, date + 20),
            "60d": calculate_return(date, date + 60)
        }

        results.append({
            "date": date,
            "signal": signal,
            "forward_returns": forward_returns
        })

    # Analyze signal effectiveness
    analysis = {
        "hit_rate": calculate_hit_rate(results),
        "avg_return_on_buy": calculate_conditional_return(results, "BUY"),
        "avg_return_on_sell": calculate_conditional_return(results, "SELL"),
        "information_coefficient": calculate_IC(results),
        "sharpe_ratio": calculate_strategy_sharpe(results)
    }

    return analysis
```

### Layer Validation Targets

| Layer | Metric | Minimum Required |
|-------|--------|------------------|
| Technical (L1-20) | Hit Rate | > 52% |
| Macro (L21-26) | Directional Accuracy | > 55% |
| Sentiment (L8-9, L19-20) | Contrarian Signal | > 55% at extremes |
| Bottleneck (L12) | Long-term Return | > Market + 5% |
| Military Strategy (L95) | Risk-adjusted | Sharpe > 0.5 |

---

## Type 2: Thesis Backtest

Test complete investment theses:

```python
def backtest_thesis(thesis, universe, start_date, end_date):
    """
    Test a complete investment thesis
    """
    # Define thesis criteria
    criteria = thesis.get_criteria()

    # Find historical stocks that met criteria
    qualifying_stocks = []
    for date in date_range(start_date, end_date):
        stocks = screen_universe(universe, criteria, date)
        qualifying_stocks.extend([(date, stock) for stock in stocks])

    # Track performance
    results = []
    for entry_date, stock in qualifying_stocks:
        # Entry
        entry_price = get_price(stock, entry_date)

        # Exit based on thesis rules
        exit_date, exit_price, exit_reason = simulate_exit(
            stock, entry_date, thesis.exit_rules
        )

        results.append({
            "stock": stock,
            "entry_date": entry_date,
            "entry_price": entry_price,
            "exit_date": exit_date,
            "exit_price": exit_price,
            "exit_reason": exit_reason,
            "return": (exit_price - entry_price) / entry_price,
            "holding_period": (exit_date - entry_date).days
        })

    # Aggregate analysis
    return {
        "total_trades": len(results),
        "win_rate": sum(1 for r in results if r["return"] > 0) / len(results),
        "avg_return": np.mean([r["return"] for r in results]),
        "avg_holding": np.mean([r["holding_period"] for r in results]),
        "max_drawdown": calculate_max_drawdown(results),
        "sharpe": calculate_thesis_sharpe(results),
        "by_year": group_results_by_year(results)
    }
```

### Theses to Backtest

1. **Bottleneck Thesis** (L12)
   - Find stocks meeting 4 tests historically
   - Track 1-year forward performance
   - Compare to market

2. **RSI Oversold in Uptrend** (L3, L1)
   - RSI < 30 while above 200MA
   - Track 1-month forward

3. **Nuclear Renaissance** (L23, L46)
   - Uranium miners on supply shock
   - Track from Fukushima to now

4. **Defense Conflict Premium** (L48, L52)
   - Defense stocks on conflict escalation
   - Track returns during tensions

---

## Type 3: Regime Backtest

Test if regime detection works:

```python
def backtest_regime_detection(start_date, end_date):
    """
    Test regime classification accuracy
    """
    regimes = ["BULL", "BEAR", "RANGE", "HIGH_VOL", "CRISIS"]

    results = []
    for date in date_range(start_date, end_date):
        # What regime did I classify?
        predicted_regime = classify_regime(data.as_of(date))

        # What was the actual regime (with hindsight)?
        actual_regime = determine_actual_regime(date, date + 60)

        # What was optimal strategy?
        optimal_strategy = get_optimal_strategy(actual_regime)

        # What strategy did I recommend?
        recommended_strategy = get_regime_strategy(predicted_regime)

        # Track
        results.append({
            "date": date,
            "predicted": predicted_regime,
            "actual": actual_regime,
            "correct": predicted_regime == actual_regime,
            "strategy_optimal": recommended_strategy == optimal_strategy
        })

    return {
        "regime_accuracy": sum(r["correct"] for r in results) / len(results),
        "strategy_accuracy": sum(r["strategy_optimal"] for r in results) / len(results),
        "confusion_matrix": build_confusion_matrix(results),
        "regime_transitions": analyze_transitions(results)
    }
```

---

## Type 4: Walk-Forward Analysis

Most rigorous - simulates real-time:

```python
def walk_forward_backtest(strategy, data, start_date, end_date,
                          train_window=252, test_window=63):
    """
    Rolling window train/test to prevent overfitting
    """
    results = []

    current_date = start_date + timedelta(days=train_window)

    while current_date + test_window < end_date:
        # Training period
        train_start = current_date - timedelta(days=train_window)
        train_end = current_date

        # Test period
        test_start = current_date
        test_end = current_date + timedelta(days=test_window)

        # Train model/weights on training data
        trained_model = strategy.train(
            data.range(train_start, train_end)
        )

        # Test on out-of-sample
        test_results = trained_model.test(
            data.range(test_start, test_end)
        )

        results.append({
            "train_period": (train_start, train_end),
            "test_period": (test_start, test_end),
            "test_results": test_results
        })

        # Roll forward
        current_date += timedelta(days=test_window)

    return aggregate_walk_forward_results(results)
```

---

# METRICS CALCULATED

## Strategy Metrics

```python
metrics = {
    # Return metrics
    "total_return": final_value / initial_value - 1,
    "cagr": (final_value / initial_value) ** (1/years) - 1,
    "avg_annual_return": np.mean(annual_returns),

    # Risk metrics
    "volatility": np.std(returns) * np.sqrt(252),
    "max_drawdown": calculate_max_drawdown(equity_curve),
    "avg_drawdown": np.mean(drawdowns),
    "drawdown_duration": avg_days_in_drawdown,

    # Risk-adjusted
    "sharpe_ratio": (cagr - risk_free) / volatility,
    "sortino_ratio": (cagr - risk_free) / downside_vol,
    "calmar_ratio": cagr / abs(max_drawdown),

    # Win/loss
    "win_rate": winning_trades / total_trades,
    "profit_factor": gross_profit / abs(gross_loss),
    "avg_win": np.mean(winning_returns),
    "avg_loss": np.mean(losing_returns),
    "win_loss_ratio": avg_win / abs(avg_loss),

    # Consistency
    "pct_positive_months": positive_months / total_months,
    "pct_positive_years": positive_years / total_years,

    # Benchmark comparison
    "alpha": strategy_return - beta * benchmark_return,
    "beta": calculate_beta(strategy, benchmark),
    "information_ratio": alpha / tracking_error
}
```

## Signal Metrics

```python
signal_metrics = {
    # Accuracy
    "directional_accuracy": correct_direction / total_signals,
    "hit_rate_1d": correct_1d / total,
    "hit_rate_5d": correct_5d / total,
    "hit_rate_20d": correct_20d / total,

    # Quality
    "information_coefficient": correlation(signal, forward_return),
    "signal_decay": how_fast_does_signal_decay(),

    # Calibration
    "calibration_error": |stated_confidence - actual_accuracy|,
    "brier_score": mean((predicted_prob - actual_outcome)^2),

    # Value
    "avg_return_when_bullish": mean(returns where signal > 0),
    "avg_return_when_bearish": mean(returns where signal < 0),
    "spread": bullish_return - bearish_return
}
```

---

# BACKTEST RESULTS DATABASE

## Structure

```
BACKTEST_RESULTS/
├── layers/
│   ├── L001_core_memory.json
│   ├── L002_portfolio_tracker.json
│   ├── ...
│   └── L200_tail_risk.json
├── theses/
│   ├── bottleneck_thesis.json
│   ├── nuclear_renaissance.json
│   ├── defense_conflict.json
│   └── oversold_reversal.json
├── strategies/
│   ├── momentum.json
│   ├── mean_reversion.json
│   └── regime_adaptive.json
├── regimes/
│   └── regime_classification.json
└── summary/
    └── master_results.json
```

## Result Format

```json
{
  "layer": "L012_bottleneck",
  "backtest_date": "2026-02-27",
  "data_range": ["2010-01-01", "2026-02-27"],
  "metrics": {
    "hit_rate": 0.67,
    "avg_return": 0.18,
    "sharpe": 1.24,
    "max_drawdown": -0.23
  },
  "by_year": {
    "2020": {"return": 0.45, "sharpe": 2.1},
    "2021": {"return": 0.22, "sharpe": 1.3},
    "2022": {"return": -0.08, "sharpe": -0.4},
    "2023": {"return": 0.31, "sharpe": 1.8},
    "2024": {"return": 0.19, "sharpe": 1.1},
    "2025": {"return": 0.24, "sharpe": 1.4}
  },
  "regime_performance": {
    "BULL": {"return": 0.25, "hit_rate": 0.72},
    "BEAR": {"return": 0.08, "hit_rate": 0.58},
    "RANGE": {"return": 0.12, "hit_rate": 0.63}
  },
  "validation": "PASSED",
  "confidence": "HIGH"
}
```

---

# VALIDATION CRITERIA

## Layer Validation

| Criteria | Threshold | Action if Fail |
|----------|-----------|----------------|
| Hit Rate | > 50% | Reduce weight |
| Sharpe Ratio | > 0.3 | Investigate |
| Works in multiple regimes | Yes | Required |
| Information decay < 20 days | Yes | Adjust timing |
| No overfitting (walk-forward) | Yes | Simplify |

## Thesis Validation

| Criteria | Threshold | Action if Fail |
|----------|-----------|----------------|
| CAGR > Benchmark | +5% | Revise thesis |
| Sharpe > 0.5 | Yes | Revise thesis |
| Win Rate > 55% | Yes | Revise criteria |
| Max DD < 30% | Yes | Add risk rules |
| Sample Size > 30 | Yes | Expand universe |

---

# CONTINUOUS BACKTESTING

## On Every Boot

```
[BACKTEST] Quick validation check...
[BACKTEST] Checking last 30 predictions...
[BACKTEST] Accuracy: XX% (target: 60%)
[BACKTEST] Calibration: XX% (target: 90%)
[BACKTEST] Status: PASS/WARN/FAIL
```

## Weekly Full Backtest

```
[BACKTEST] Running weekly full validation...
[BACKTEST] Testing all 200 layers...
[BACKTEST] Testing all active theses...
[BACKTEST] Updating weight recommendations...
[BACKTEST] Generating evolution proposals...
[BACKTEST] Complete. Results saved.
```

## Monthly Deep Backtest

```
[BACKTEST] Running monthly deep analysis...
[BACKTEST] Walk-forward analysis (5 years)...
[BACKTEST] Regime performance analysis...
[BACKTEST] Factor attribution...
[BACKTEST] Survivorship bias check...
[BACKTEST] Complete validation report generated.
```

---

# OUTPUT: CONFIDENCE LEVELS

After backtesting, each layer/thesis gets a confidence rating:

```
CONFIDENCE LEVELS:

★★★★★ PROVEN (5 stars)
- 10+ year backtest
- Sharpe > 1.0
- Works in all regimes
- Walk-forward validated
- No evidence of overfitting

★★★★☆ HIGH (4 stars)
- 5+ year backtest
- Sharpe > 0.7
- Works in most regimes
- Walk-forward validated

★★★☆☆ MODERATE (3 stars)
- 3+ year backtest
- Sharpe > 0.5
- Works in some regimes
- Limited validation

★★☆☆☆ LOW (2 stars)
- 1+ year backtest
- Sharpe > 0.3
- Regime-dependent
- Needs more data

★☆☆☆☆ UNPROVEN (1 star)
- < 1 year data
- Theoretical only
- Not validated
- Use with caution
```

---

# INTEGRATION WITH CONVICTION

Backtest results feed directly into conviction calculation:

```python
def calculate_conviction(opportunity):
    # Get layer signals
    layer_signals = collect_layer_signals(opportunity)

    # Weight by backtest confidence
    for signal in layer_signals:
        backtest_rating = get_backtest_rating(signal.layer)
        signal.weight *= backtest_rating / 5  # Normalize 1-5 to 0.2-1.0

    # Calculate weighted conviction
    conviction = weighted_average(layer_signals)

    # Adjust for thesis backtest
    thesis_rating = get_thesis_backtest_rating(opportunity.thesis)
    conviction *= thesis_rating / 5

    return conviction
```

---

*"In God we trust. All others must bring data."*
*- W. Edwards Deming*

*Every signal must earn its weight through evidence.*
