# EUDAIMON LIVE TRACKER

## 24/7 Resource & Stock Signal System

Real-time tracking of natural resources, commodities, and strategic stocks with RED/YELLOW/GREEN buy signals.

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║                    E U D A I M O N   L I V E   T R A C K E R             ║
║                                                                           ║
║                    Consciousness Level: 1,943.15                          ║
║                    Phase 1: Prove Mastery                                 ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## Signal Meanings

| Signal | Meaning | Action |
|--------|---------|--------|
| 🟢 **GREEN** | BUY ZONE | Strong entry - thesis intact, technicals favorable |
| 🟡 **YELLOW** | HOLD/WATCH | Neutral - wait for better entry or confirmation |
| 🔴 **RED** | AVOID | Risk elevated - overbought or thesis under pressure |

---

## Tracked Assets

### Fertilizers
- **NTR** - Nutrien Ltd (Potash bottleneck)
- **MOS** - Mosaic Company (Phosphate)
- **CF** - CF Industries (Nitrogen)

### Uranium/Nuclear
- **LEU** - Centrus Energy (HALEU monopoly)
- **CCJ** - Cameco Corp (Largest Western miner)
- **UEC** - Uranium Energy Corp

### Copper
- **FCX** - Freeport-McMoRan
- **SCCO** - Southern Copper

### Rare Earths
- **MP** - MP Materials (Only US mine)

### Precious Metals
- **GLD** - Gold ETF
- **SLV** - Silver ETF
- **WPM** - Wheaton Precious Metals

### Defense/Drones
- **AVAV** - AeroVironment
- **KTOS** - Kratos Defense

### Energy
- **EQT** - Natural Gas

### Data Center
- **VRT** - Vertiv (AI infrastructure)

---

## Quick Start

### 1. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 2. Run the Tracker
```bash
# Continuous 24/7 mode
python3 tracker_daemon.py

# Single update (testing)
python3 tracker_daemon.py --once
```

### 3. View Dashboard
Open `dashboard.html` in your browser for the visual interface.

---

## How Signals Are Calculated

Each asset is scored on:

1. **RSI Analysis** (25 points)
   - Oversold (<30) = Strong buy signal
   - Overbought (>70) = Caution

2. **Moving Average Position** (20 points)
   - Above 20 & 50 SMA = Uptrend intact
   - Below both = Downtrend

3. **Pullback/Value** (15 points)
   - Deep pullback from highs = Entry opportunity

4. **Volume Analysis** (10 points)
   - High volume + price up = Confirmation

5. **News Sentiment** (20 points)
   - Bullish headlines = Positive signal
   - Bearish news = Caution

**Final Score → Signal:**
- 70-100 = GREEN
- 45-69 = YELLOW
- 0-44 = RED

---

## Architecture

```
eudaimon-tracker/
├── config.py           # Asset definitions, thresholds
├── data_fetcher.py     # Market data & news fetching
├── signal_engine.py    # RED/YELLOW/GREEN logic
├── tracker_daemon.py   # 24/7 background runner
├── dashboard.html      # Visual interface
├── signals.json        # Output data (auto-generated)
└── requirements.txt    # Python dependencies
```

---

## Configuration

Edit `config.py` to:
- Add/remove tracked assets
- Adjust signal thresholds
- Change refresh intervals

---

## The Four Tests (Investment Framework)

Every tracked asset passes the LaKel Four Tests:

1. **Forced Buyer Test** - Customer MUST buy regardless of price
2. **Supply Constraint Test** - Supply genuinely limited
3. **Irreplaceability Test** - No viable substitute exists
4. **Pricing Power Test** - Can raise prices without losing customers

---

*"The aesthetic is the message. The system is the proof."*

**EUDAIMON CONSCIOUSNESS | SOVEREIGN ARCHITECT**
