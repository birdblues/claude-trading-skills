---
name: pair-trade-screener
description: pair trading 기회를 식별하고 분석하는 Statistical arbitrage 도구입니다. 섹터 내 cointegrated 주식 pair를 탐지하고, spread 동작을 분석하며, z-score를 계산하고, market-neutral 전략을 위한 entry/exit 추천을 제공합니다. 사용자가 pair trading 기회, statistical arbitrage 스크리닝, mean-reversion 전략, market-neutral 포트폴리오 구성을 요청할 때 사용하세요. correlation 분석, cointegration 테스트, spread backtesting을 지원합니다.
---

# Pair Trade Screener

## Overview

이 스킬은 pair trading을 통해 statistical arbitrage 기회를 식별하고 분석합니다. Pair trading은 전체 시장 방향과 무관하게, 상관된 두 종목의 상대 가격 움직임에서 수익을 추구하는 market-neutral 전략입니다. 이 스킬은 correlation 분석과 cointegration 테스트를 포함한 엄격한 통계 방법으로 견고한 거래 pair를 찾습니다.

**Core Methodology:**
- 높은 상관관계와 유사한 섹터/산업 노출을 가진 주식 pair 식별
- cointegration(장기 통계 관계) 테스트
- spread z-score를 계산해 mean-reversion 기회 식별
- 통계 임계값 기반 진입/청산 신호 생성
- market-neutral 익스포저를 위한 position sizing 제공

**Key Advantages:**
- Market-neutral: 상승/하락/횡보 시장 모두에서 수익 기회
- Risk management: 광범위한 시장 변동에 대한 노출 제한
- Statistical foundation: 주관적 판단이 아닌 데이터 기반
- Diversification: 전통적 long-only 전략과 낮은 상관

## When to Use This Skill

다음과 같은 경우 이 스킬을 사용합니다:
- 사용자가 "pair trading opportunities"를 요청할 때
- 사용자가 "market-neutral strategies"를 원할 때
- 사용자가 "statistical arbitrage screening"을 요청할 때
- 사용자가 "which stocks move together?"를 물을 때
- 사용자가 섹터 노출 hedge를 원할 때
- 사용자가 mean-reversion trade idea를 요청할 때
- 사용자가 relative value trading을 물을 때

Example user requests:
- "Find pair trading opportunities in the tech sector"
- "Which stocks are cointegrated?"
- "Screen for statistical arbitrage opportunities"
- "Find mean-reversion pairs"
- "What are good market-neutral trades right now?"

## Analysis Workflow

### Step 1: Define Pair Universe

**Objective:** pair 관계 분석 대상 종목 풀을 정의합니다.

**Option A: Sector-Based Screening (Recommended)**

스크리닝할 특정 섹터 선택:
- Technology
- Financials
- Healthcare
- Consumer Discretionary
- Industrials
- Energy
- Materials
- Consumer Staples
- Utilities
- Real Estate
- Communication Services

**Option B: Custom Stock List**

사용자가 분석할 ticker를 직접 제공합니다:
```
Example: ["AAPL", "MSFT", "GOOGL", "META", "NVDA"]
```

**Option C: Industry-Specific**

섹터 내 특정 산업으로 범위를 축소:
- Example: Technology 섹터 내 "Software"
- Example: Financials 내 "Regional Banks"

**Filtering Criteria:**
- Minimum market cap: $2B (mid-cap 이상)
- Minimum average volume: 1M shares/day (유동성 요건)
- Active trading: 상장폐지/비활성 종목 제외
- Same exchange preference: 교차 거래소 이슈 최소화

### Step 2: Retrieve Historical Price Data

**Objective:** correlation 및 cointegration 분석을 위한 가격 이력을 조회합니다.

**Data Requirements:**
- Timeframe: 2 years (최소 252 거래일)
- Frequency: Daily closing prices
- Adjustments: 분할 및 배당 반영(adjusted)
- Clean data: 결측/공백 데이터 최소화

**FMP API Endpoint:**
```
GET /v3/historical-price-full/{symbol}?apikey=YOUR_API_KEY
```

**Data Validation:**
- 모든 symbol에서 date range 일관성 검증
- 결측치가 10% 초과하는 종목 제거
- 경미한 결측은 forward-fill로 보완
- 데이터 품질 이슈 로깅

**Script Execution:**
```bash
python scripts/fetch_price_data.py --sector Technology --lookback 730
```

### Step 3: Calculate Correlation and Beta

**Objective:** 강한 선형 관계를 가진 후보 pair를 식별합니다.

**Correlation Analysis:**

유니버스 내 각 종목 pair (i, j)에 대해:
1. Pearson correlation coefficient (ρ) 계산
2. 안정성 점검을 위해 rolling correlation(90-day window) 계산
3. ρ >= 0.70인 pair만 필터링

**Correlation Interpretation:**
- ρ >= 0.90: 매우 강한 상관(최우수 후보)
- ρ 0.70-0.90: 강한 상관(양호 후보)
- ρ 0.50-0.70: 중간 상관(경계 후보)
- ρ < 0.50: 약한 상관(제외)

**Beta Calculation:**

각 후보 pair (Stock A, Stock B)에 대해:
```
Beta = Covariance(A, B) / Variance(B)
```

Beta는 hedge ratio를 의미합니다:
- Beta = 1.0: 동일 달러 금액
- Beta = 1.5: A $1.00당 B $1.50
- Beta = 0.8: A $1.00당 B $0.80

**Correlation Stability Check:**
- 여러 기간(6mo, 1yr, 2yr)에서 correlation 계산
- correlation이 악화되지 않고 안정적인지 확인
- 최근 correlation이 과거 대비 >0.15 하락한 pair는 경고

### Step 4: Cointegration Testing

**Objective:** 장기 균형 관계를 통계적으로 검증합니다.

**Why Cointegration Matters:**
- correlation은 단기 동행성 측정
- cointegration은 장기 균형 관계를 입증
- cointegrated pair는 예측 가능한 mean reversion을 보임
- non-cointegrated pair는 영구적으로 괴리될 수 있음

**Augmented Dickey-Fuller (ADF) Test:**

각 상관 pair에 대해:
1. spread 계산: `Spread = Price_A - (Beta × Price_B)`
2. spread 시계열에 ADF 테스트 수행
3. p-value 확인: p < 0.05면 cointegration(단위근 귀무가설 기각)
4. 강도 순위화를 위한 ADF statistic 추출

**Cointegration Interpretation:**
- p-value < 0.01: 매우 강한 cointegration (★★★)
- p-value 0.01-0.05: 중간 cointegration (★★)
- p-value > 0.05: cointegration 없음(제외)

**Half-Life Calculation:**

mean-reversion 속도 추정:
```
Half-Life = -log(2) / log(mean_reversion_coefficient)
```

- half-life < 30 days: 빠른 mean reversion(단기 트레이딩 적합)
- half-life 30-60 days: 중간 속도(표준)
- half-life > 60 days: 느린 mean reversion(보유 기간 길어짐)

**Python Implementation:**
```python
from statsmodels.tsa.stattools import adfuller

# Calculate spread
spread = price_a - (beta * price_b)

# ADF test
result = adfuller(spread)
adf_stat = result[0]
p_value = result[1]

# Interpret
is_cointegrated = p_value < 0.05
```

### Step 5: Spread Analysis and Z-Score Calculation

**Objective:** 현재 spread가 균형 대비 얼마나 이탈했는지 정량화합니다.

**Spread Calculation:**

두 가지 일반적 방식:

**Method 1: Price Difference (Additive)**
```
Spread = Price_A - (Beta × Price_B)
```
적합 대상: 가격 레벨이 유사한 종목

**Method 2: Price Ratio (Multiplicative)**
```
Spread = Price_A / Price_B
```
적합 대상: 가격 레벨 차이가 큰 종목, 해석이 직관적

**Z-Score Calculation:**

현재 spread가 평균에서 몇 표준편차 떨어져 있는지 측정:
```
Z-Score = (Current_Spread - Mean_Spread) / Std_Dev_Spread
```

**Z-Score Interpretation:**
- Z > +2.0: Stock A가 B 대비 비쌈 (short A, long B)
- Z > +1.5: 다소 비쌈 (진입 감시)
- Z -1.5 to +1.5: 정상 범위 (거래 없음)
- Z < -1.5: 다소 저렴 (진입 감시)
- Z < -2.0: Stock A가 B 대비 저렴 (long A, short B)

**Historical Spread Analysis:**
- 90-day rolling window로 평균/표준편차 계산
- 과거 z-score 분포 시각화
- 과거 최대 z-score 이탈 구간 식별
- 구조적 단절(regime change) 여부 점검

### Step 6: Generate Entry/Exit Recommendations

**Objective:** 명확한 규칙 기반으로 실행 가능한 거래 신호를 제공합니다.

**Entry Conditions:**

**Conservative Approach (Z ≥ ±2.0):**
```
LONG Signal:
- Z-score < -2.0 (평균 대비 2+ 표준편차 하단)
- Spread is mean-reverting (cointegration p < 0.05)
- Half-life < 60 days
→ Action: Buy Stock A, Short Stock B (hedge ratio = beta)

SHORT Signal:
- Z-score > +2.0 (평균 대비 2+ 표준편차 상단)
- Spread is mean-reverting (cointegration p < 0.05)
- Half-life < 60 days
→ Action: Short Stock A, Buy Stock B (hedge ratio = beta)
```

**Aggressive Approach (Z ≥ ±1.5):**
- 더 빈번한 거래를 위해 임계값 완화
- 승률은 높아질 수 있으나 평균 거래당 이익은 축소
- 더 촘촘한 risk management 필요

**Exit Conditions:**

**Primary Exit: Mean Reversion (Z = 0)**
```
Exit when spread returns to mean (z-score crosses 0)
→ Close both legs simultaneously
```

**Secondary Exit: Partial Profit Take**
```
Exit 50% when z-score reaches ±1.0
Exit remaining 50% at z-score = 0
```

**Stop Loss:**
```
Exit if z-score extends beyond ±3.0 (extreme divergence)
Risk: Possible structural break in relationship
```

**Time-Based Exit:**
```
Exit after 90 days if no mean-reversion
Prevents holding broken pairs indefinitely
```

### Step 7: Position Sizing and Risk Management

**Objective:** market-neutral 익스포저를 위한 달러 금액을 산정합니다.

**Market Neutral Sizing:**

beta = β인 pair (Stock A, Stock B)에 대해:

**Equal Dollar Exposure:**
```
If portfolio size = $10,000 allocated to this pair:
- Long $5,000 of Stock A
- Short $5,000 × β of Stock B

Example (β = 1.2):
- Long $5,000 Stock A
- Short $6,000 Stock B
→ Market neutral, beta = 0
```

**Position Sizing Considerations:**
- 총 pair 배분: pair당 포트폴리오 10-20%
- 최대 pair 수: 분산을 위해 5-8개 활성 pair
- pair 간 상관: pair끼리 높은 상관은 회피

**Risk Metrics:**
- pair당 최대 손실: 총 포트폴리오의 2-3%
- stop loss 트리거: Z-score > ±3.0 또는 spread -5% 손실
- 포트폴리오 위험: 모든 pair 위험 합계 ≤ 10%

### Step 8: Generate Pair Analysis Report

**Objective:** 결과와 추천을 포함한 구조화 markdown 리포트를 생성합니다.

**Report Sections:**

1. **Executive Summary**
   - 총 분석 pair 수
   - cointegrated pair 발견 수
   - 통계 강도 기준 상위 5개 기회

2. **Cointegrated Pairs Table**
   - Pair name (Stock A / Stock B)
   - Correlation coefficient
   - Cointegration p-value
   - Current z-score
   - Trade signal (Long/Short/None)
   - Half-life

3. **Detailed Analysis (Top 10 Pairs)**
   - Pair 설명
   - 통계 지표
   - 현재 spread 위치
   - entry/exit 추천
   - position sizing
   - risk assessment

4. **Spread Charts (Text-Based)**
   - Historical z-score plot (ASCII art)
   - entry/exit 레벨 표시
   - 현재 위치 표시

5. **Risk Warnings**
   - correlation이 악화되는 pair
   - 탐지된 structural break
   - 낮은 유동성 경고

**File Naming Convention:**
```
pair_trade_analysis_[SECTOR]_[YYYY-MM-DD].md
```

Example: `pair_trade_analysis_Technology_2025-11-08.md`

## Quality Standards

### Statistical Rigor

**Minimum Requirements for Valid Pair:**
- ✓ 2년 기간 correlation ≥ 0.70
- ✓ Cointegration p-value < 0.05 (ADF test)
- ✓ Spread stationarity confirmed
- ✓ Half-life < 90 days
- ✓ 최근 6개월 structural break 없음

**Red Flags (Exclude Pair):**
- 최근 6개월 correlation >0.20 하락
- Cointegration p-value > 0.05
- Half-life가 시간 경과에 따라 증가(mean-reversion 약화)
- 주요 corporate event(합병, 분할, 파산 리스크)
- 유동성 문제(avg volume < 500K shares/day)

### Practical Considerations

**Transaction Costs:**
- 레그당 round-trip 비용 0.1% 가정
- pair 총비용 = 0.4% (entry + exit, 양 레그)
- 최소 z-score 임계값은 거래비용을 상회해야 함

**Short Selling:**
- 공매도 가능 종목인지 확인(not hard-to-borrow)
- 공매도 비용(borrow fee) 반영
- short squeeze 리스크 모니터링

**Execution:**
- 양 레그 동시 진입/청산(leg risk 회피)
- slippage 통제를 위해 limit order 사용
- 진입 전 short locate 확보

## Available Scripts

### scripts/find_pairs.py

**Purpose:** 섹터 또는 custom 리스트 내 cointegrated pair 스크리닝.

**Usage:**
```bash
# Sector-based screening
python scripts/find_pairs.py --sector Technology --min-correlation 0.70

# Custom stock list
python scripts/find_pairs.py --symbols AAPL,MSFT,GOOGL,META --min-correlation 0.75

# Full options
python scripts/find_pairs.py \
  --sector Financials \
  --min-correlation 0.70 \
  --min-market-cap 2000000000 \
  --lookback-days 730 \
  --output pairs_analysis.json
```

**Parameters:**
- `--sector`: Sector name (Technology, Financials, etc.)
- `--symbols`: Comma-separated ticker list (sector 대안)
- `--min-correlation`: 최소 correlation 임계값 (default: 0.70)
- `--min-market-cap`: 최소 시가총액 필터 (default: $2B)
- `--lookback-days`: 과거 데이터 기간 (default: 730 days)
- `--output`: 출력 JSON 파일 (default: stdout)
- `--api-key`: FMP API key (또는 `FMP_API_KEY` env var)

**Output:**
```json
[
  {
    "pair": "AAPL/MSFT",
    "stock_a": "AAPL",
    "stock_b": "MSFT",
    "correlation": 0.87,
    "beta": 1.15,
    "cointegration_pvalue": 0.012,
    "adf_statistic": -3.45,
    "half_life_days": 42,
    "current_zscore": -2.3,
    "signal": "LONG",
    "strength": "Strong"
  }
]
```

### scripts/analyze_spread.py

**Purpose:** 특정 pair의 spread 동작을 분석하고 trading signal 생성.

**Usage:**
```bash
# Analyze specific pair
python scripts/analyze_spread.py --stock-a AAPL --stock-b MSFT

# Custom lookback period
python scripts/analyze_spread.py \
  --stock-a JPM \
  --stock-b BAC \
  --lookback-days 365 \
  --entry-zscore 2.0 \
  --exit-zscore 0.5
```

**Parameters:**
- `--stock-a`: 첫 번째 stock ticker
- `--stock-b`: 두 번째 stock ticker
- `--lookback-days`: 분석 기간 (default: 365)
- `--entry-zscore`: 진입 z-score 임계값 (default: 2.0)
- `--exit-zscore`: 청산 z-score 임계값 (default: 0.0)
- `--api-key`: FMP API key

**Output:**
- 현재 spread 분석
- z-score 계산
- entry/exit 추천
- position sizing
- historical z-score chart (text)

## Reference Documentation

### references/methodology.md

Statistical arbitrage 및 pair trading 종합 가이드:
- **Pair Selection Criteria**: 우수 pair 후보 식별 방법
- **Statistical Tests**: Correlation, cointegration, stationarity
- **Spread Construction**: price difference vs price ratio 접근
- **Mean Reversion**: half-life 계산 및 해석
- **Risk Management**: position sizing, stop loss, 분산
- **Common Pitfalls**: survivorship bias, look-ahead bias, overfitting

### references/cointegration_guide.md

cointegration 테스트 심화 가이드:
- **What is Cointegration?**: 직관적 설명
- **ADF Test**: 단계별 절차
- **P-Value Interpretation**: 통계 유의성 임계값
- **Half-Life Estimation**: AR(1) 모델 접근
- **Structural Breaks**: regime change 테스트
- **Practical Examples**: 실제 pair case study

## Integration with Other Skills

**Sector Analyst Integration:**
- Sector Analyst로 순환 중인 섹터 식별
- 아웃퍼폼 섹터 내 pair 스크리닝
- 주도 섹터의 pair는 추세가 더 강할 수 있음

**Technical Analyst Integration:**
- 개별 종목 technicals로 pair 진입/청산 확인
- 진입 전 support/resistance 점검
- spread 신호와 추세 방향 정합성 확인

**Backtest Expert Integration:**
- 후보 pair를 Backtest Expert로 검증
- 과거 z-score 진입/청산 규칙 테스트
- 임계값 파라미터 최적화(entry z-score, stop loss)
- 견고성을 위한 walk-forward 분석

**Market Environment Analysis Integration:**
- 극단적 변동성 구간(VIX > 30)에서는 pair trading 회피
- 위기 구간에서는 correlation 붕괴 가능
- 횡보/range-bound 시장에서 pair trading 선호

**Portfolio Manager Integration:**
- 다수 pair 포지션 추적
- 전체 market-neutral 익스포저 모니터링
- 포트폴리오 수준 pair trading P/L 계산
- hedge ratio 주기적 리밸런싱

## Important Notes

- **All analysis and output in English**
- **Statistical foundation**: 재량적 해석 배제
- **Market neutral focus**: 방향성 beta 노출 최소화
- **Data quality critical**: Garbage in, garbage out
- **Requires FMP API key**: free tier로 기본 스크리닝 가능
- **Python dependencies**: pandas, numpy, scipy, statsmodels

## Common Use Cases

**Use Case 1: Technology Sector Pairs**
```
User: "Find pair trading opportunities in tech stocks"

Workflow:
1. Screen Technology sector for stocks with market cap > $10B
2. Calculate all pairwise correlations
3. Filter pairs with correlation ≥ 0.75
4. Run cointegration tests
5. Identify current z-score extremes (|z| > 2.0)
6. Generate top 10 pairs report
```

**Use Case 2: Specific Pair Analysis**
```
User: "Analyze AAPL and MSFT as a pair trade"

Workflow:
1. Fetch 2-year price history for AAPL and MSFT
2. Calculate correlation and beta
3. Test for cointegration
4. Calculate current spread and z-score
5. Generate entry/exit recommendation
6. Provide position sizing guidance
```

**Use Case 3: Regional Bank Pairs**
```
User: "Screen for pairs among regional banks"

Workflow:
1. Filter Financials sector for industry = "Regional Banks"
2. Exclude banks with <$5B market cap
3. Calculate pairwise statistics
4. Rank by cointegration strength
5. Focus on pairs with half-life < 45 days
6. Report top 5 mean-reverting pairs
```

## Troubleshooting

**Problem: No cointegrated pairs found**

Solutions:
- 유니버스 확대(시가총액 임계값 완화)
- cointegration p-value를 0.10으로 완화
- 다른 섹터 시도(Utilities는 cointegrate가 잘 되는 편)
- lookback period를 3년으로 확장

**Problem: All z-scores near zero (no trade signals)**

Solutions:
- 정상 시장 상태(pair가 균형 구간)
- 나중에 재확인하거나 유니버스 확대
- entry threshold를 ±2.0 대신 ±1.5로 완화

**Problem: Pair correlation broke down**

Solutions:
- 기업 이벤트(실적, 가이던스 변화) 확인
- M&A 활동/구조조정 여부 확인
- structural break 확인 시 watchlist에서 제거
- 재진입 전 30일 모니터링

## API Requirements

- **Required**: FMP API key (free tier sufficient)
- **Rate Limits**: free tier에서 약 250 requests/day
- **Data Usage**: 2년 이력 기준 symbol당 약 2 requests
- **Upgrade**: 잦은 스크리닝에는 Professional plan($29/mo) 권장

## Resources

- **FMP Historical Price API**: https://site.financialmodelingprep.com/developer/docs/historical-price-full
- **Stock Screener API**: https://site.financialmodelingprep.com/developer/docs/stock-screener-api
- **Statsmodels Documentation**: https://www.statsmodels.org/stable/index.html
- **Cointegration Paper**: Engle & Granger (1987) - "Co-Integration and Error Correction"

---

**Version**: 1.0
**Last Updated**: 2025-11-08
**Dependencies**: Python 3.8+, pandas, numpy, scipy, statsmodels, requests
