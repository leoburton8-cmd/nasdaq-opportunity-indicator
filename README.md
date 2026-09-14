# 📊 NASDAQ Opportunity Indicator

**Real-time momentum indicator** tracking big opportunities and optimal entry points across NASDAQ's most liquid components.

[![GitHub stars](https://img.shields.io/github/stars/leoburton8-cmd/nasdaq-opportunity-indicator?style=social)](https://github.com/leoburton8-cmd/nasdaq-opportunity-indicator/stargazers)
[![License](https://img.shields.io/github/license/leoburton8-cmd/nasdaq-opportunity-indicator)](LICENSE)

## ✨ Features

- **🎯 Real-Time Signals**: Live momentum scores (0-100) for NASDAQ components
- **📈 Entry Zone Detection**: Automatic support/resistance calculation
- **🔊 Volume Surge Alerts**: Identifies unusual volume activity
- **⚡ Opportunity Ratings**: EXCEPTIONAL / HIGH / MODERATE / LOW
- **📊 Dashboard View**: Clean summary of top 5 opportunities
- **📥 CSV Export**: Export all signals for further analysis
- **🔔 Signal Types**: STRONG BUY / BUY / HOLD / SELL / STRONG SELL

## 🎯 What It Tracks

| Component | Purpose |
|-----------|---------|
| **QQQ** | NASDAQ 100 ETF - overall market direction |
| **AAPL, MSFT, NVDA** | Top 3 by market cap - market leaders |
| **GOOGL, META, AMZN** | Mega-cap tech - sentiment drivers |
| **TSLA, AMD** | High beta - momentum indicators |
| **NDX** | NASDAQ 100 Index - benchmark |

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/leoburton8-cmd/nasdaq-opportunity-indicator.git
cd nasdaq-opportunity-indicator
```

### 2. Install Dependencies

```bash
pip install requests
```

### 3. Configure API Key

Edit `indicator.py` line ~190:

```python
API_KEY = "YOUR_PERPLEXITY_API_KEY_HERE"
```

Get your key: https://www.perplexity.ai/settings/api

### 4. Run Indicator

```bash
python indicator.py
```

## 📊 Example Output

```
🔍 NASDAQ Opportunity Indicator
======================================================================
Timestamp: 2026-09-14 17:07:51

Scanning 10 NASDAQ components...

🟢 MSFT  | Score:  78.5 | Price: $  507.68 | Change:   2.43% | Vol: ELEVATED | Signal: BUY
🟢 GOOGL | Score:  76.2 | Price: $  346.81 | Change:   2.45% | Vol: NORMAL   | Signal: BUY
🟢 META  | Score:  74.8 | Price: $  663.58 | Change:   2.40% | Vol: NORMAL   | Signal: BUY
⚪ AAPL  | Score:  52.3 | Price: $  334.37 | Change:   0.63% | Vol: NORMAL   | Signal: HOLD
🔴 AMD   | Score:  28.1 | Price: $  493.54 | Change:  -4.38% | Vol: SURGE    | Signal: SELL

======================================================================
📊 NASDAQ OPPORTUNITY DASHBOARD
======================================================================

🎯 TOP 5 OPPORTUNITIES

Rank  Ticker   Score    Price        Change     Signal          Rating
----------------------------------------------------------------------
1     MSFT     78.5     $507.68      2.43%      BUY             ⭐ HIGH
2     GOOGL    76.2     $346.81      2.45%      BUY             ⭐ HIGH
3     META     74.8     $663.58      2.40%      BUY             📊 MODERATE
4     AAPL     52.3     $334.37      0.63%      HOLD            ⚠️ LOW
5     TSLA     48.6     $362.61      -0.78%     HOLD            ⚠️ LOW

======================================================================
📈 DETAILED ANALYSIS - TOP PICK
======================================================================

Ticker: MSFT
Signal: 🟢 BUY
Momentum Score: 78.5/100
Opportunity: ⭐ HIGH

Current Price: $507.68
Daily Change: 2.43%
Volume: 11,926,127 (ELEVATED)

🎯 ENTRY STRATEGY:
  Entry Zone: $495.50 - $505.60
  Stop Loss: $482.30
  Take Profit 1: $517.83
  Take Profit 2: $533.06
  Take Profit 3: $558.45
  Risk/Reward: 2.85:1

📊 KEY LEVELS:
  Support: $495.34, $485.72, $482.30
  Resistance: $508.80, $515.54, $533.06
```

## 🎯 Signal Calculation

### Momentum Score (0-100)

| Factor | Weight | Description |
|--------|--------|-------------|
| Day Range Position | ±15 | Where price sits in today's range |
| Year Range Position | ±10 | Where price sits in 52-week range |
| Daily Change | ±20 | Percentage move today |
| Volume Surge | +10 | Volume > 2x average |

### Signal Types

- **🟢 STRONG BUY** (75-100): Exceptional momentum, high conviction
- **🟡 BUY** (60-74): Good momentum, favorable setup
- **⚪ HOLD** (40-59): Neutral, wait for better entry
- **🟠 SELL** (25-39): Weak momentum, consider exiting
- **🔴 STRONG SELL** (0-24): Strong downward pressure

### Opportunity Ratings

- **🔥 EXCEPTIONAL** (90+): Rare setups, high probability
- **⭐ HIGH** (75-89): Quality opportunities
- **📊 MODERATE** (60-74): Tradeable with caution
- **⚠️ LOW** (<60): Skip or very small size

## 📁 Output Files

- `nasdaq_signals.csv` - All signals with entry/exit levels
- Console dashboard - Real-time summary

## 🛠️ Customization

### Add More Tickers

Edit `indicator.py` line ~28:

```python
self.tickers = [
    'QQQ', 'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'META', 
    'TSLA', 'AMZN', 'AMD', 'NDX',
    # Add your tickers here:
    'NFLX', 'AVGO', 'COST'
]
```

### Adjust Scoring

Edit `calculate_momentum_score()` function to weight factors differently.

### Change Entry Logic

Edit `detect_entry_zone()` to match your preferred entry strategy.

## ⚠️ Disclaimer

**For educational purposes only. Not financial advice.**

- Always do your own research
- Use proper risk management
- Never risk more than you can afford to lose
- Past performance ≠ future results

## 📝 License

MIT License - free to use and modify.

## 🔗 Connect

- **GitHub:** [@leoburton8-cmd](https://github.com/leoburton8-cmd)
- **Issues:** [Report bugs](https://github.com/leoburton8-cmd/nasdaq-opportunity-indicator/issues)

---

**Built for traders** | Last updated: September 2026
