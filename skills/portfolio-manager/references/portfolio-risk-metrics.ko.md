# Portfolio Risk Metrics

이 문서는 표준 금융 지표를 사용해 포트폴리오 리스크를 측정하고 해석하는 방법을 종합적으로 제공합니다.

## Overview

포트폴리오 리스크 평가는 정량 지표와 정성 판단을 함께 요구합니다. 이 가이드는 다음을 다룹니다.

1. 변동성 기반 지표 (standard deviation, beta)
2. 하방 리스크 지표 (maximum drawdown, semi-deviation)
3. 위험조정수익 지표 (Sharpe ratio, Sortino ratio)
4. 집중도/상관 지표
5. 투자자 유형별 해석 프레임워크

## Volatility Metrics

### Standard Deviation (σ)

**Definition:** 일정 기간 수익률이 평균에서 얼마나 벗어나는지 측정하는 지표.

**Formula:**
```
σ = √[Σ(R_i - R_avg)² / (n-1)]

Where:
R_i = Return in period i
R_avg = Average return
n = Number of periods
```

**Interpretation:**

| Annual Std Dev | Risk Level | Typical Assets |
|---------------|------------|----------------|
| **<5%** | Very Low | Cash, short-term bonds |
| **5-10%** | Low | Bond portfolios, conservative balanced |
| **10-15%** | Moderate | Balanced portfolios (60/40), dividend stocks |
| **15-20%** | High | Stock portfolios, growth stocks |
| **>20%** | Very High | Small caps, emerging markets, sector funds |

**S&P 500 Historical:** 연환산 약 15-18%

**포트폴리오 분석 활용:**
- 벤치마크 대비 변동성 비교
- 투자자 위험 성향과 변동성 정합성 점검
- 시간에 따른 변동성 추이 추적(증가 시 경고)

**Limitations:**
- 정규분포 가정(실제는 fat tail 존재)
- 상방/하방 변동성을 동일하게 취급
- 과거 기반이라 미래 예측 한계

### Beta (β)

**Definition:** 시장 움직임에 대한 포트폴리오 민감도.

**Formula:**
```
β = Cov(R_portfolio, R_market) / Var(R_market)

Or estimated as:
β = (Σw_i × β_i)

Where:
w_i = Weight of position i
β_i = Beta of position i
```

**Interpretation:**

| Beta | Market Sensitivity | Portfolio Behavior |
|------|-------------------|-------------------|
| **β < 0.5** | Very low | Defensive, low correlation to market |
| **β = 0.5-0.8** | Low | Below-market volatility, defensive tilt |
| **β = 0.8-1.0** | Moderate | Slightly less volatile than market |
| **β = 1.0** | Market | Moves in line with market (index-like) |
| **β = 1.0-1.3** | Moderate-high | More volatile than market |
| **β = 1.3-1.6** | High | Significantly more volatile |
| **β > 1.6** | Very high | Extremely volatile, aggressive |

**Typical Security Betas:**
- Utilities: 0.4-0.7
- Consumer Staples: 0.5-0.8
- Healthcare: 0.8-1.1
- S&P 500 Index: 1.0
- Technology: 1.1-1.5
- Small-cap growth: 1.3-2.0
- Leveraged ETFs: 2.0-3.0

**Example Portfolio Beta Calculation:**

Portfolio:
- 40% SPY (S&P 500 ETF, β=1.0): 0.40 × 1.0 = 0.40
- 30% QQQ (Nasdaq ETF, β=1.2): 0.30 × 1.2 = 0.36
- 20% VNQ (REIT ETF, β=0.9): 0.20 × 0.9 = 0.18
- 10% TLT (Bond ETF, β=0.3): 0.10 × 0.3 = 0.03

**Portfolio Beta** = 0.97

**Interpretation:** 시장 대비 97% 정도 움직이는 약간 방어적 포트폴리오.

**Usage:**
- 포트폴리오 공격성 평가
- 시장 변동 시 반응 추정 (β=1.2면 시장 -10% 시 약 -12% 기대)
- 헤지/리밸런싱 필요성 판단

**Limitations:**
- beta는 시간에 따라 변함
- 과거 상관 기반
- 극단적 시장에서 불안정

### Semi-Deviation

**Definition:** 평균 이하 수익률만 대상으로 한 표준편차(하방 변동성).

**Formula:**
```
Semi-deviation = √[Σ(R_i - R_avg)² for all R_i < R_avg / n]
```

**Interpretation:**
- 낮을수록 하방 방어 우수
- 손실 민감 투자자에게 유용
- 대칭 분포에서는 보통 표준편차의 60-70%

**Usage:**
- 하방 리스크 중심 평가
- 방어형/공격형 전략 비교
- Sortino ratio 입력값

## Downside Risk Metrics

### Maximum Drawdown (MDD)

**Definition:** 특정 기간 동안 포트폴리오 가치의 최대 peak-to-trough 하락폭.

**Formula:**
```
MDD = (Trough Value - Peak Value) / Peak Value

Or: MDD = max[(P_peak - P_trough) / P_peak] over all peaks
```

**Example:**
- Peak: $150,000
- Trough: $105,000
- MDD = -30%

**Historical Maximum Drawdowns:**

| Asset/Portfolio | Max Drawdown | Period |
|----------------|--------------|--------|
| S&P 500 | -57% | 2007-2009 (Financial Crisis) |
| S&P 500 | -34% | 2020 (COVID Crash) |
| Nasdaq 100 | -83% | 2000-2002 (Tech Bubble) |
| Nasdaq 100 | -32% | 2021-2022 (Rate Hikes) |
| 60/40 Portfolio | -32% | 2007-2009 |
| Treasury Bonds | -48% | 2020-2023 (Rising Rates) |

**Risk Tolerance Guide:**

| Investor Type | Max Acceptable Drawdown |
|--------------|------------------------|
| **Conservative** | -10 to -15% |
| **Moderate** | -15 to -25% |
| **Growth** | -25 to -35% |
| **Aggressive** | -35 to -50% |

**Usage:**
- 최악 시나리오 점검
- 위험 성향 적합성 검토
- 리스크 관리 트리거 설정
- 회복 시간 추정

**Recovery Time:**
- -20% 손실 회복에는 +25% 수익 필요
- -30% 손실 회복에는 +43%
- -50% 손실 회복에는 +100%

### Current Drawdown

**Definition:** 최근 고점 대비 현재 가치 하락률.

**Formula:**
```
Current Drawdown = (Current Value - Recent Peak Value) / Recent Peak Value
```

**Example:**
- Recent peak: $150,000
- Current value: $142,500
- Current drawdown = -5%

**Interpretation:**

| Current Drawdown | Status | Action |
|-----------------|--------|--------|
| **0%** | At all-time high | Monitor for complacency |
| **-1% to -5%** | Minor pullback | Normal, no action |
| **-5% to -10%** | Moderate correction | Review positions, monitor |
| **-10% to -20%** | Correction | Assess portfolio, consider adjustments |
| **>-20%** | Bear market territory | Review allocation, consider rebalancing |

**Usage:**
- 실시간 리스크 모니터링
- 스트레스 구간 조기 인지
- 리밸런싱/위험 축소 트리거

### Value at Risk (VaR)

**Definition:** 주어진 신뢰수준에서 특정 기간 내 발생 가능한 최대 손실 추정치.

**Example:**
- 95% 신뢰수준 1개월 VaR = $10,000
- 해석: 향후 1개월 손실이 $10,000를 초과할 확률이 5%

**Calculation Methods:**
1. **Historical VaR**
2. **Parametric VaR**
3. **Monte Carlo VaR**

**Simplified Parametric VaR Formula:**
```
VaR = Portfolio Value × (z-score × σ - μ)

Where:
z-score = 1.65 for 95% confidence, 2.33 for 99% confidence
σ = Portfolio standard deviation (daily or monthly)
μ = Expected return (daily or monthly)
```

**Example Calculation:**
- Portfolio value: $100,000
- Annual std dev: 18%
- Monthly std dev: 18% / √12 = 5.2%
- Expected monthly return: 0.5%

**95% 1-month VaR:**
```
VaR = $100,000 × (1.65 × 5.2% - 0.5%)
    = $8,080
```

**Interpretation:** 향후 1개월 손실이 $8,080을 넘지 않을 확률이 95%.

**Usage:**
- Risk budgeting
- 포지션 한도 설정
- 기관 규제 준수

**Limitations:**
- 과거 패턴 지속 가정
- 꼬리 리스크 과소추정
- VaR 초과 구간 손실 규모는 설명 못함

## Risk-Adjusted Return Metrics

### Sharpe Ratio

**Definition:** 단위 리스크당 초과 수익률.

**Formula:**
```
Sharpe Ratio = (R_portfolio - R_f) / σ_portfolio
```

**Example Calculation:**
- Portfolio return: 12%
- Risk-free rate: 4%
- Std dev: 15%

**Sharpe = 0.53**

**Interpretation:**

| Sharpe Ratio | Quality | Interpretation |
|--------------|---------|----------------|
| **< 0** | Poor | Return less than risk-free rate |
| **0 - 0.5** | Suboptimal | Low excess return for risk taken |
| **0.5 - 1.0** | Good | Adequate risk-adjusted return |
| **1.0 - 2.0** | Very Good | Strong risk-adjusted return |
| **> 2.0** | Excellent | Exceptional risk-adjusted return |

**Usage:**
- 전략/포트폴리오 비교
- 추가 리스크의 보상 여부 판단
- 시장 대비 성과 품질 평가

**Limitations:**
- 상방 변동성도 벌점
- 정규분포 가정
- 기간 선택 민감

### Sortino Ratio

**Definition:** Sharpe와 유사하나 총변동성 대신 하방변동성을 사용.

**Formula:**
```
Sortino Ratio = (R_portfolio - R_f) / Semi-deviation
```

**Example:**
- Portfolio return: 12%
- Risk-free rate: 4%
- Semi-deviation: 10%

**Sortino = 0.80**

**Interpretation:**
- 높을수록 하방 위험 대비 성과 우수
- 일반적으로 Sharpe보다 큼
- 손실 회피 성향 투자자에게 적합

### Calmar Ratio

**Definition:** 최대 낙폭 대비 수익률.

**Formula:**
```
Calmar Ratio = Annualized Return / |Max Drawdown|
```

**Example:**
- Annualized return: 10%
- Max drawdown: -25%

**Calmar = 0.40**

**Interpretation:**

| Calmar Ratio | Quality |
|--------------|---------|
| **< 0.5** | Poor |
| **0.5 - 1.0** | Acceptable |
| **1.0 - 2.0** | Good |
| **> 2.0** | Excellent |

## Concentration and Correlation Metrics

### Concentration Metrics

**1. Top-N Concentration**

가장 큰 N개 포지션의 합산 비중:

```
Top-N % = (Σ Top N Position Values) / Total Portfolio Value
```

**Guidelines:**
- Top 1: <10% 이상적, <15% 최대
- Top 5: <40% 이상적, <50% 최대
- Top 10: <60% 이상적, <70% 최대

**2. Herfindahl-Hirschman Index (HHI)**

```
HHI = Σ(Weight_i × 100)²
```

**Quick Assessment:**
- HHI < 1000: Well-diversified
- HHI 1000-1800: Moderately concentrated
- HHI > 1800: High concentration

### Correlation Metrics

**Average Pairwise Correlation**

모든 포지션 쌍의 평균 상관계수:

```
Avg Correlation = Σ(ρ_ij) / Number of pairs
```

**Example (5 positions):** 평균 상관 0.52

**Interpretation:**

| Avg Correlation | Diversification Quality |
|----------------|------------------------|
| **< 0.3** | Excellent |
| **0.3 - 0.5** | Good |
| **0.5 - 0.7** | Moderate |
| **> 0.7** | Poor |

## Risk Scoring Framework

### Composite Risk Score (0-100)

다중 지표를 단일 점수로 통합:

```
Risk Score =
  (Volatility Score × 30%) +
  (Beta Score × 20%) +
  (Drawdown Score × 25%) +
  (Concentration Score × 25%)
```

**Individual Component Scores (0-100):**

**1. Volatility Score:**
- <10%: 0-20
- 10-15%: 20-40
- 15-20%: 40-60
- 20-25%: 60-80
- >25%: 80-100

**2. Beta Score:**
- β < 0.8: 0-20
- β 0.8-1.0: 20-40
- β 1.0-1.3: 40-60
- β 1.3-1.6: 60-80
- β > 1.6: 80-100

**3. Drawdown Score:**
- Max DD <10%: 0-20
- 10-20%: 20-40
- 20-30%: 40-60
- 30-40%: 60-80
- >40%: 80-100

**4. Concentration Score:**
- HHI <1000: 0-20
- 1000-1500: 20-40
- 1500-2000: 40-60
- 2000-2500: 60-80
- >2500: 80-100

**Composite Risk Score Interpretation:**

| Score | Risk Level | Appropriate For |
|-------|-----------|-----------------|
| **0-20** | Very Low | Ultra-conservative, retirees |
| **20-40** | Low | Conservative investors |
| **40-60** | Moderate | Balanced investors |
| **60-80** | High | Growth-oriented investors |
| **80-100** | Very High | Aggressive, long time horizon |

## Practical Risk Assessment Workflow

### Step 1: 기본 지표 계산

1. Portfolio Beta
2. Standard Deviation (가능 시)
3. Maximum Drawdown
4. Current Drawdown
5. Top-5 Concentration
6. HHI

### Step 2: 벤치마크 비교

**S&P 500 대비:**
- beta가 1.0보다 높은가/낮은가?
- 변동성이 약 16%보다 높은가/낮은가?

**Risk Profile 목표 대비:**
- 위험 수준이 투자자 성향과 일치하는가?
- 최대 낙폭이 수용 가능한가?

### Step 3: 리스크 집중 식별

**Position-Level:**
- 포지션 >15%? → 즉시 Trim
- Top 5 >50%? → 높은 집중도

**Sector-Level:**
- 섹터 >35%? → 집중 리스크
- 비어 있는 핵심 섹터? → 분산 공백

**Factor-Level:**
- 전부 high-beta growth? → 팩터 집중
- 전부 value? → 스타일 집중

### Step 4: 위험조정 성과

1. Sharpe Ratio 계산(가능 시)
2. 벤치마크 대비 위험조정성과 비교
3. Sortino Ratio 계산
4. 추가 위험이 보상되는지 평가

### Step 5: 위험 평가 보고

**Summary Format:**

```markdown
## Portfolio Risk Assessment

**Overall Risk Profile:** [Conservative / Moderate / Growth / Aggressive]

**Risk Score:** XX/100 ([Low / Medium / High / Very High])

**Key Metrics:**
- Portfolio Beta: X.XX (vs market 1.00)
- Estimated Volatility: XX% annualized
- Maximum Drawdown: -XX% (acceptable for [risk profile])
- Current Drawdown: -X% (vs recent peak)

**Risk Concentrations:**
- Top 5 positions: XX% of portfolio ([OK / High / Excessive])
- Largest single position: [SYMBOL] at XX% ([OK / Trim recommended])
- HHI: XXXX ([Well-diversified / Concentrated])

**Risk-Adjusted Performance:**
- Sharpe Ratio: X.XX ([Below / In-line / Above] market)
- Sortino Ratio: X.XX
- Performance for risk taken: [Excellent / Good / Fair / Poor]

**Risk Recommendations:**
- [List specific actions to reduce risk if needed]
```

## Risk Management Guidelines

### 리스크를 줄여야 할 때

**Signals:**
- 중립형 투자자에게 beta >1.5
- Max drawdown이 허용 범위 초과
- 단일 포지션 >15%
- 섹터 집중 >40%
- Current drawdown >20%

**Actions:**
- 집중 포지션 Trim
- 방어 섹터 확대
- 채권 비중 확대
- 현금 비중 확대

### 리스크를 늘려도 되는 때

**Signals:**
- 성장형 투자자에게 beta <0.7
- 현금 >15%(의도적 방어가 아닌 경우)
- 낮은 변동성인데 벤치마크 대비 부진
- 긴 투자 기간 대비 지나치게 보수적 배분

**Actions:**
- 성장 섹터 확대
- 주식 비중 확대
- 유휴 현금 투입
- 고확신 포지션 확대

## Summary

**Key Takeaways:**

1. **단일 지표로는 부족** - 여러 지표를 함께 봐야 함
2. **변동성 지표** - 표준편차와 beta로 전체 리스크 파악
3. **하방 지표** - MDD, Current DD, VaR로 최악 시나리오 점검
4. **위험조정성과** - Sharpe/Sortino로 성과 품질 평가
5. **집중도** - HHI와 Top-N 비중으로 분산 수준 확인
6. **투자자 적합성** - 리스크 지표는 성향/목표와 정합돼야 함
7. **지속 모니터링** - 시장 변화에 따라 리스크 특성도 변함

**Practical Application:**

- 분기마다 핵심 지표 계산
- 위험 성향과 비교
- 집중 구간/공백 식별
- 목표 위험 수준 유지하도록 배분 조정
- 포트폴리오 보고서에 리스크 평가 기록

**Remember:** 리스크 지표는 도구이지 절대 진실이 아닙니다. 정량 지표와 함께 시장 환경, 경제 전망, 투자자 상황 같은 정성 요소를 함께 판단해야 합니다.
