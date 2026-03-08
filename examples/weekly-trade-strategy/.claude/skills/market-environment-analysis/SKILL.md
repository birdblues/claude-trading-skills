---
name: market-environment-analysis
description: Comprehensive market environment analysis and reporting tool. Analyzes global markets including US, European, Asian markets, forex, commodities, and economic indicators. Provides risk-on/risk-off assessment, sector analysis, and technical indicator interpretation. Triggers on keywords like market analysis, market environment, global markets, trading environment, market conditions, investment climate, market sentiment, forex analysis, stock market analysis, 相場環境, 市場分析, マーケット状況, 投資環境.
---

# Market Environment Analysis

Comprehensive analysis tool for understanding market conditions and creating professional market reports anytime.

## Core Workflow

### 1. Initial Data Collection
Collect latest market data using web_search tool:
1. Major stock indices (S&P 500, NASDAQ, Dow, Nikkei 225, Shanghai Composite, Hang Seng)
2. Forex rates (USD/JPY, EUR/USD, major currency pairs)
3. Commodity prices (WTI crude, Gold, Silver)
4. US Treasury yields (2-year, 10-year, 30-year)
5. VIX index (Fear gauge)
6. Market trading status (open/close/current values)

### 2. Data Verification

Before proceeding to analysis, verify collected data through these mandatory checks:

#### Source Verification
- For key metrics (VIX, Treasury yields, major indices), use WebFetch on
  the original source page (FRED, Yahoo Finance, etc.) to confirm exact values.
  Do NOT rely solely on WebSearch summary text — summaries can return
  stale or incorrect figures.

#### Cross-Consistency Check
- Verify that individual data points are consistent with each other and with the
  overall market narrative:
  - If market is selling off sharply → VIX should be elevated (typically 20+), not low
  - If inflation data is hot → Treasury yields should be rising, not falling
  - If USD is strengthening → Gold typically faces headwinds (unless fear-driven)
  - If risk-off environment → safe havens (Gold, JPY, Treasuries) should be bid
- If a data point contradicts the broader context, re-verify from the source before
  using it. Never rationalize contradictory data with a narrative — fix the data first.

#### Date Freshness
- Confirm that each data point's date matches the intended analysis date.
  WebSearch may mix values from different dates without clear attribution.
- For weekend/holiday analysis, explicitly state "as of [last trading date]."

### 3. Market Environment Assessment
Evaluate the following from collected data:
- **Trend Direction**: Uptrend/Downtrend/Range-bound
- **Risk Sentiment**: Risk-on/Risk-off
- **Volatility Status**: Market anxiety level from VIX
- **Sector Rotation**: Where capital is flowing

### 4. Report Structure

#### Standard Report Format:
```
1. Executive Summary (3-5 key points)
2. Global Market Overview
   - US Markets
   - Asian Markets
   - European Markets
3. Forex & Commodities Trends
4. Key Events & Economic Indicators
5. Risk Factor Analysis
6. Investment Strategy Implications
```

## Script Usage

### market_utils.py
Provides common functions for report creation:
```bash
# Generate report header
python scripts/market_utils.py

# Available functions:
- format_market_report_header(): Create header
- get_market_session_times(): Check trading hours
- categorize_volatility(vix): Interpret VIX levels
- format_percentage_change(value): Format price changes
```

## Reference Documentation

### Key Indicators Interpretation (references/indicators.md)
Reference when you need:
- Important levels for each index
- Technical analysis key points
- Sector-specific focus areas

### Analysis Patterns (references/analysis_patterns.md)
Reference when analyzing:
- Risk-on/Risk-off criteria
- Economic indicator interpretation
- Inter-market correlations
- Seasonality and market anomalies

## Output Examples

### Quick Summary Version
```
📊 Market Summary [2025/01/15 14:00]
━━━━━━━━━━━━━━━━━━━━━
【US】S&P 500: 5,123.45 (+0.45%)
【JP】Nikkei 225: 38,456.78 (-0.23%)
【FX】USD/JPY: 149.85 (↑0.15)
【VIX】16.2 (Normal range)

⚡ Key Events
- Japan GDP Flash
- US Employment Report

📈 Environment: Risk-On Continues
```

### Detailed Analysis Version
Start with executive summary, then analyze each section in detail.
Key clarifications:
1. Current market phase (Bullish/Bearish/Neutral)
2. Short-term direction (1-5 days outlook)
3. Risk events to monitor
4. Recommended position adjustments

## Important Considerations

### Timezone Awareness
- Consider all major market timezones
- US markets: Evening to early morning (Asian time)
- European markets: Afternoon to evening (Asian time)
- Asian markets: Morning to afternoon (Local time)

### Economic Calendar Priority
Categorize by importance:
- ⭐⭐⭐ Critical (FOMC, NFP, CPI, etc.)
- ⭐⭐ Important (GDP, Retail Sales, etc.)
- ⭐ Reference level

### Data Source Priority
1. Official releases (Central banks, Government statistics)
2. Major financial media (Bloomberg, Reuters)
3. Broker reports
4. Analyst consensus estimates

**Verification rule:** For VIX, Treasury yields, and index closes — always
confirm via WebFetch on at least one primary source (FRED, Yahoo Finance,
or the exchange's official page). WebSearch summaries alone are insufficient
for precise numerical data.

## Troubleshooting

### Data Collection Notes
- Check market holidays (holiday calendars)
- Be aware of daylight saving time changes
- Distinguish between flash and final data
- Never rationalize data that contradicts the market context. If VIX seems
  too low for a sell-off, or yields seem wrong for an inflation shock,
  the data is likely stale or incorrect — re-verify before writing.

### Market Volatility Response
1. First organize the facts
2. Reference historical similar events
3. Verify with multiple sources
4. Maintain objective analysis

## Customization Options

Adjust based on user's investment style:
- **Day Traders**: Intraday charts, order flow focus
- **Swing Traders**: Daily/weekly technicals emphasis
- **Long-term Investors**: Fundamentals, macro economics focus
- **Forex Traders**: Currency correlations, interest rate differentials
- **Options Traders**: Volatility analysis, Greeks monitoring

## Language

리포트를 한국어로 작성한다. 지수명(S&P 500, NASDAQ 등), 통화 쌍(USD/JPY 등), 원자재명, 숫자 데이터는 영어/원본 유지.
