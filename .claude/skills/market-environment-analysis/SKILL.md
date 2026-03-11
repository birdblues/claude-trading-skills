---
name: market-environment-analysis
description: Comprehensive market environment analysis and reporting tool. Analyzes global markets including US, European, Asian markets, forex, commodities, and economic indicators. Provides risk-on/risk-off assessment, sector analysis, and technical indicator interpretation. Triggers on keywords like market analysis, market environment, global markets, trading environment, market conditions, investment climate, market sentiment, forex analysis, stock market analysis, 相場環境, 市場分析, マーケット状況, 投資環境.
---

# Market Environment Analysis

Comprehensive analysis tool for understanding market conditions and creating professional market reports anytime.

## Core Workflow

### Step 0.5: Supabase Breaking News Context (Optional)

**Prerequisite:** Check if `mcp__supabase__execute_sql` tool is available.
If not available, skip directly to Step 1.

Invoke the `supabase-news-summarizer` agent:

```
Agent tool:
  subagent_type: "supabase-news-summarizer"
  prompt: |
    최근 10일간 Supabase public.news 테이블의 속보를 전량 수집하여
    시장 환경 분석에 특화된 요약을 생성해주세요.

    분석 기간: [현재 날짜 - 10일] ~ [현재 날짜]

    다음을 반환해주세요:
    1. 글로벌 주식시장 주요 이벤트 (미국, 유럽, 아시아)
    2. 외환·원자재 시장 변동 요인
    3. 중앙은행 정책 변화 (FOMC, ECB, BOJ 등)
    4. VIX·변동성 관련 이벤트
    5. 지정학적 리스크 영향
    6. 크로스테마 상호작용
    7. WebSearch 갭 리스트
    8. 블라인드 스팟 경보 (사모/크레딧/시스템 리스크)
```

**Why agent:** 10일간 중요 속보 800+건 × detail 평균 824자 = ~665K자로 메인 컨텍스트에 직접 로드 불가. 에이전트가 자체 컨텍스트 윈도우에서 전량 처리 후 3,000자 이내 압축 요약을 반환.

**Agent output → Step 1 input:**
- Supabase 요약이 있으면 갭 리스트 기반으로 WebSearch 집중
- 내러티브 그룹별 요약을 시장 환경 평가의 기초 컨텍스트로 활용

### 1. Initial Data Collection
Collect latest market data using web_search tool. If Step 0.5 was executed, focus on filling gaps identified in the WebSearch gap list and verifying key Supabase findings. If Step 0.5 was skipped (no Supabase MCP), execute all searches below as primary collection.
1. Major stock indices (S&P 500, NASDAQ, Dow, Nikkei 225, Shanghai Composite, Hang Seng)
2. Forex rates (USD/JPY, EUR/USD, major currency pairs)
3. Commodity prices (WTI crude, Gold, Silver)
4. US Treasury yields (2-year, 10-year, 30-year)
5. VIX index (Fear gauge)
6. Market trading status (open/close/current values)

### 2. Market Environment Assessment
Evaluate the following from collected data:
- **Trend Direction**: Uptrend/Downtrend/Range-bound
- **Risk Sentiment**: Risk-on/Risk-off
- **Volatility Status**: Market anxiety level from VIX
- **Sector Rotation**: Where capital is flowing

### 3. Report Structure

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

## Troubleshooting

### Data Collection Notes
- Check market holidays (holiday calendars)
- Be aware of daylight saving time changes
- Distinguish between flash and final data

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
