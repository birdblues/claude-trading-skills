# Statistical Arbitrage and Pair Trading Methodology

## Table of Contents

1. [Introduction to Pair Trading](#introduction-to-pair-trading)
2. [Theoretical Foundation](#theoretical-foundation)
3. [Pair Selection Process](#pair-selection-process)
4. [Statistical Tests](#statistical-tests)
5. [Spread Construction and Analysis](#spread-construction-and-analysis)
6. [Entry and Exit Rules](#entry-and-exit-rules)
7. [Risk Management](#risk-management)
8. [Common Pitfalls](#common-pitfalls)
9. [Advanced Topics](#advanced-topics)

---

## Introduction to Pair Trading

### What is Pair Trading?

Pair trading은 상관관계가 높은 두 종목을 동시에 매수/매도하는 market-neutral 전략입니다. 두 주식의 관계가 과거 균형에서 일시적으로 이탈했을 때, 다시 수렴(convergence)하는 과정에서 수익을 추구합니다.

**Key Characteristics:**
- **Market Neutral**: 한 종목 long, 다른 종목 short → net beta ≈ 0
- **Mean Reverting**: 균형 대비 일시적 이탈의 복귀에 의존
- **Statistical Foundation**: 재량 판단이 아닌 수학적 관계 기반
- **Relative Value**: 절대 방향이 아닌 상대 성과에서 수익 창출

### Historical Context

Pair trading은 1980년대 Morgan Stanley에서 **Gerry Bamberger**가 개척하고 **Nunzio Tartaglia**가 발전시켰습니다. 이 퀀트 팀은 과거 함께 움직였던 주식 pair를 찾아 일시적 괴리에서 수익을 냈습니다.

**Evolution:**
- 1980s: 수동 pair 선택, 단순 spread 추적
- 1990s: 통계 모델(cointegration, Kalman filter)
- 2000s: 고빈도 pair trading, algorithmic execution
- 2010s+: machine learning, regime detection, multi-asset pairs

### Why Pair Trading Works

**Economic Rationale:**
1. **Sector/Industry Linkages**: 같은 섹터 기업은 공통 동인(수요, 규제, 원가)을 공유
2. **Temporary Mispricing**: 정보 비대칭, 행동 편향, 기술적 수급이 일시적 가격 괴리 유발
3. **Mean Reversion**: 차익거래 및 펀더멘털 요인이 가격을 균형으로 복귀시킴
4. **Supply Chain Relationships**: 공급업체-수요업체 종목이 함께 움직이는 경우가 많음

**Statistical Rationale:**
- cointegration은 장기 균형 관계를 보장
- 단기 괴리는 통계적으로 예측 가능
- z-score 프레임워크가 객관적 진입/청산 규칙 제공

---

## Theoretical Foundation

### Cointegration vs Correlation

**Correlation:**
- 수익률의 단기 동행성 측정
- 범위: -1 to +1
- 시간에 따라 불안정할 수 있음
- mean reversion을 보장하지 않음

**Cointegration:**
- 가격 레벨 간 장기 균형 관계 측정
- spread의 stationarity(mean-reversion) 보장
- pair trading의 더 안정적 기반
- 가격이 무기한 벌어지지 않음을 시사

**Mathematical Definition:**

두 시계열 `P_A(t)` 와 `P_B(t)` 가 아래를 만족하면 cointegrated입니다:
```
Spread(t) = P_A(t) - β * P_B(t)
```
여기서 β는 cointegration coefficient입니다.

### Stationarity

시계열이 **stationary** 이려면:
1. 평균이 시간에 대해 일정
2. 분산이 시간에 대해 일정
3. 자기상관이 절대 시점이 아닌 시차에만 의존

**Why Stationarity Matters for Pair Trading:**
- non-stationary spread → 가격이 영구 괴리 가능 → mean reversion 없음
- stationary spread → 평균 회귀 → 수익 기회 생성
- cointegration이 spread stationarity를 보장

### Mean Reversion

spread는 **Ornstein-Uhlenbeck (OU) process**를 따른다고 가정할 수 있습니다:
```
dS(t) = θ(μ - S(t))dt + σdW(t)
```

Where:
- `S(t)`: t 시점 spread
- `θ`: mean reversion speed(클수록 빠름)
- `μ`: spread의 장기 평균
- `σ`: spread 변동성
- `dW(t)`: Brownian motion(랜덤 노이즈)

**Half-Life:**

spread가 평균으로 절반 복귀하는 시간:
```
Half-Life = ln(2) / θ
```

**Interpretation:**
- Half-life = 10 days: 매우 빠른 복귀(데이 트레이딩 적합)
- Half-life = 30 days: 표준 속도(일반적인 pair trade)
- Half-life = 60+ days: 느린 복귀(긴 보유 필요)

---

## Pair Selection Process

### Step 1: Universe Definition

**Sector-Based Approach (Recommended):**
- 같은 섹터 종목 중심으로 분석(예: Technology, Financials)
- 공통 동인으로 cointegration 가능성 증가
- 예시:
  - Tech: AAPL/MSFT, GOOGL/META, NVDA/AMD
  - Financials: JPM/BAC, GS/MS, WFC/USB
  - Energy: XOM/CVX, COP/EOG

**Industry-Specific Approach:**
- 특정 산업으로 좁힘(예: Tech 내 Software, Financials 내 Regional Banks)
- 펀더멘털 연결성이 더 강함
- pair 수는 줄지만 품질 향상

**Custom Approach:**
- 사용자 지정 종목 리스트
- 가설 기반 테스트 가능(공급망 pair, 경쟁사 pair 등)

**Filtering Criteria:**
- Market cap ≥ $2B (유동성/안정성)
- Average volume ≥ 1M shares/day (집행 가능성)
- Same exchange 우선(NYSE/NYSE, NASDAQ/NASDAQ)
- 최근 IPO(<2년) 및 distressed stocks 제외

### Step 2: Correlation Screening

**Calculate Pearson Correlation:**
```python
import pandas as pd
import numpy as np

# Returns-based correlation
correlation = returns_A.corr(returns_B)

# Price-based correlation (for reference)
price_correlation = prices_A.corr(prices_B)
```

**Thresholds:**
- **Excellent (ρ ≥ 0.85)**: 매우 강한 동행성, 최우수 후보
- **Good (ρ 0.70-0.85)**: 강한 관계, 수용 가능
- **Marginal (ρ 0.50-0.70)**: 중간 수준, 강한 cointegration 필요
- **Poor (ρ < 0.50)**: 약함, cointegrated 가능성 낮음

**Correlation Stability:**

여러 기간에서 correlation 안정성 테스트:
```python
# 6-month rolling correlation
rolling_corr = returns_A.rolling(126).corr(returns_B)

# Stability metric: std deviation of rolling correlation
stability = rolling_corr.std()

# Prefer pairs with low stability (<0.10)
```

**Red Flags:**
- 최근 구간 correlation 급락
- correlation 변동성 과도(급격한 점프)
- correlation이 0에 접근하거나 음수 전환

### Step 3: Beta Estimation (Hedge Ratio)

**Ordinary Least Squares (OLS) Regression:**
```python
from scipy import stats

# Regress Price_A on Price_B
slope, intercept, r_value, p_value, std_err = stats.linregress(prices_B, prices_A)

beta = slope  # Hedge ratio
```

**Interpretation:**
- Beta = 1.0: 동일 달러 hedge ($1 long A, $1 short B)
- Beta = 1.5: $1 long A, $1.50 short B
- Beta = 0.8: $1 long A, $0.80 short B

**Alternative Methods:**
- **Total Least Squares (TLS)**: 양 변수 오차 반영
- **Kalman Filter**: 시간가변 beta(고급)
- **Rolling OLS**: 시간 적응형 beta

### Step 4: Cointegration Testing

**Augmented Dickey-Fuller (ADF) Test:**

귀무가설: "Spread has unit root (non-stationary)"

```python
from statsmodels.tsa.stattools import adfuller

# Calculate spread
spread = prices_A - (beta * prices_B)

# ADF test
result = adfuller(spread, maxlag=1, regression='c')
adf_statistic = result[0]
p_value = result[1]
critical_values = result[4]

# Interpret
is_cointegrated = p_value < 0.05
```

**Interpretation:**
- **p < 0.01**: 매우 강한 cointegration (99% 신뢰수준에서 기각)
- **p 0.01-0.05**: 중간 cointegration (95% 신뢰수준에서 기각)
- **p > 0.05**: cointegration 없음(기각 실패)

**Critical Values:**
- ADF stat < critical value (1%) → 매우 강한 증거
- ADF stat < critical value (5%) → 중간 증거
- ADF stat > critical value (10%) → 약한 증거

**Alternative Cointegration Tests:**
- **Engle-Granger Two-Step**: ADF와 유사
- **Johansen Test**: 다변량 cointegration(종목 3개 이상)
- **Phillips-Ouliaris Test**: structural break에 상대적으로 강건

---

## Statistical Tests

### Stationarity Tests

**Augmented Dickey-Fuller (ADF):**
- 가장 널리 쓰이는 stationarity 테스트
- 시계열 단위근 여부 테스트
- 귀무가설: 시계열은 단위근 존재(non-stationary)

**Kwiatkowski-Phillips-Schmidt-Shin (KPSS):**
- ADF 보완 테스트
- 귀무가설: 시계열이 stationary
- 두 테스트를 함께 사용해 강건성 확보:
  - ADF 기각 + KPSS 기각 실패 → Stationary
  - ADF 기각 실패 + KPSS 기각 → Non-stationary

**Phillips-Perron (PP) Test:**
- ADF의 비모수 대안
- 이분산/직렬상관에 더 강건

### Half-Life Estimation

**AR(1) Model Approach:**

spread를 1차 자기회귀로 모델링:
```
S(t) = α + φ * S(t-1) + ε(t)
```

Where:
- φ: 자기상관 계수
- Mean reversion speed: θ = -ln(φ)
- Half-life: HL = ln(2) / θ

**Python Implementation:**
```python
from statsmodels.tsa.ar_model import AutoReg

# Fit AR(1) model
model = AutoReg(spread, lags=1)
result = model.fit()
phi = result.params[1]

# Calculate half-life
theta = -np.log(phi)
half_life = np.log(2) / theta
```

**Interpretation:**
- HL < 20 days: 매우 빠른 mean reversion
- HL 20-40 days: 빠른 mean reversion(pair trading 이상적)
- HL 40-60 days: 중간 mean reversion
- HL > 60 days: 느린 mean reversion(매력도 낮음)

### Structural Break Detection

**Chow Test:**

알려진 날짜(예: 주요 기업 이벤트)에서 structural break 테스트:
```python
from statsmodels.stats.diagnostic import breaks_cusumolsresid

# Test for breaks
stat, pvalue = breaks_cusumolsresid(ols_residuals)

# Interpret
has_structural_break = pvalue < 0.05
```

**CUSUM Test:**
- 미지의 break point 탐지
- 잔차 누적합 플롯 사용
- 급격한 변화는 structural break 신호

**Practical Implication:**
- structural break 탐지 시 → cointegration 관계 재추정
- break가 지속되면 → 해당 pair 폐기(관계 붕괴)

---

## Spread Construction and Analysis

### Spread Definitions

**Price Difference (Additive):**
```
Spread(t) = P_A(t) - β * P_B(t)
```

**Advantages:**
- 해석이 단순
- cointegration 하에서 stationary

**Disadvantages:**
- 단위가 가격 레벨에 의존
- 가격 수준 차이가 큰 종목에는 부적합

**Price Ratio (Multiplicative):**
```
Spread(t) = P_A(t) / P_B(t)
```

**Advantages:**
- 단위 없음(ratio)
- 가격 레벨 차이가 큰 종목에 유리
- 퍼센트 관점 해석 용이

**Disadvantages:**
- stationarity 확보를 위해 log 변환이 자주 필요
- 통계 처리 복잡도 증가

**Log Price Ratio:**
```
Spread(t) = ln(P_A(t)) - ln(P_B(t))
```

**Advantages:**
- stationarity 확보에 유리
- returns 유사 해석 가능
- 0 중심 대칭성

### Z-Score Calculation

**Definition:**
```
Z(t) = [Spread(t) - μ] / σ
```

Where:
- μ: lookback 기간 spread 평균
- σ: lookback 기간 spread 표준편차

**Lookback Period:**
- **90 days (short-term)**: 최근 변화에 민감, 노이즈 큼
- **180 days (medium-term)**: 균형적 접근(권장)
- **252 days (long-term)**: 파라미터 안정적, 적응은 느림

**Rolling vs Expanding Window:**

**Rolling Window:**
```python
rolling_mean = spread.rolling(90).mean()
rolling_std = spread.rolling(90).std()
zscore = (spread - rolling_mean) / rolling_std
```
- 변화하는 spread dynamics에 적응
- 장기 추세를 놓칠 수 있음

**Expanding Window:**
```python
expanding_mean = spread.expanding().mean()
expanding_std = spread.expanding().std()
zscore = (spread - expanding_mean) / expanding_std
```
- 전체 이력 데이터 사용
- 더 안정적이지만 적응성 낮음

### Spread Distribution Analysis

**Normality Test:**
```python
from scipy.stats import normaltest

# Test if spread is normally distributed
stat, pvalue = normaltest(spread)
is_normal = pvalue > 0.05
```

**If spread is NOT normal:**
- z-score 대신 percentile 기반 임계값 사용
- 예: z > 2.0 대신 95th percentile에서 진입

**Skewness and Kurtosis:**
- Skewness ≠ 0: 비대칭 분포(임계값 조정 필요)
- Kurtosis > 3: fat tail(극단값 빈도 높음)

---

## Entry and Exit Rules

### Entry Conditions

**Conservative Strategy (Z ≥ ±2.0):**

**LONG Spread (Long A, Short B):**
```
Conditions:
1. Z-score < -2.0 (spread 2+ std devs below mean)
2. Cointegration p-value < 0.05
3. Correlation > 0.70
4. Half-life < 60 days
5. No structural breaks in recent 6 months

Action:
- Buy Stock A: $5,000
- Sell Stock B: $5,000 × β
```

**SHORT Spread (Short A, Long B):**
```
Conditions:
1. Z-score > +2.0 (spread 2+ std devs above mean)
2. [Same conditions 2-5 as above]

Action:
- Sell Stock A: $5,000
- Buy Stock B: $5,000 × β
```

**Aggressive Strategy (Z ≥ ±1.5):**
- 임계값 완화 → 거래 빈도 증가
- 승률 상승 가능하지만 기대수익은 작아질 수 있음
- 더 적극적인 모니터링 필요

**Very Aggressive (Z ≥ ±1.0):**
- 매우 잦은 거래
- transaction costs 영향이 커짐
- 저수수료/리베이트 환경에서만 실효성

### Exit Conditions

**Primary Exit: Mean Reversion**
```
Exit when Z-score crosses zero
→ Spread has reverted to mean
→ Close both legs simultaneously
```

**Partial Profit Taking:**
```
Stage 1: Exit 50% at Z-score = ±1.0
Stage 2: Exit remaining 50% at Z-score = 0
```

**Stop Loss:**
```
Hard Stop: Z-score > ±3.0
- Spread has diverged to extreme levels
- Possible structural break
→ Exit immediately to limit losses

Drawdown Stop: Total P/L < -5%
- Trade not working as expected
→ Exit to preserve capital
```

**Time-Based Exit:**
```
Maximum Holding Period: 90 days (or 3× half-life)
- If no mean reversion after expected timeframe
→ Exit to free up capital for better opportunities
```

### Signal Confirmation

**Additional Filters (Optional):**

**Volume Confirmation:**
- spread 확장 시 평균 이상 거래량 요구
- 노이즈가 아닌 의미 있는 괴리인지 확인

**Trend Filter:**
- 전체 시장(SPY)이 강한 추세일 때는 진입 회피
- 급락/급등 구간에서는 correlation 붕괴 가능

**Volatility Filter:**
- VIX > 30에서는 진입 스킵(고변동성 환경)
- 변동성 급등 구간에서 pair 관계 안정성 저하

---

## Risk Management

### Position Sizing

**Equal Dollar Allocation:**
```
For $10,000 total allocation to one pair:
- Long Leg: $5,000
- Short Leg: $5,000 × β

If β = 1.2:
- Long Stock A: $5,000
- Short Stock B: $6,000
```

**Volatility-Adjusted Sizing:**

spread 변동성 역수에 비례해 포지션 크기 조정:
```
Position Size = Base Size / (Spread Volatility / Avg Spread Volatility)
```
- High volatility pair → 더 작은 포지션
- Low volatility pair → 더 큰 포지션

### Portfolio-Level Risk

**Diversification:**
- **Minimum**: 5 pairs (개별 종목 리스크 완화)
- **Optimal**: 8-10 pairs (분산과 관리의 균형)
- **Maximum**: 15 pairs (효용 체감, 관리 복잡성 증가)

**Correlation Across Pairs:**
- 중복 종목이 많은 pair 동시 보유 회피(예: AAPL/MSFT + AAPL/GOOGL)
- 단일 섹터 노출 제한(<50% of pairs)
- 포트폴리오 beta 모니터링(0 근처 유지)

**Maximum Risk Allocation:**
- 단일 pair: 총 포트폴리오의 10-15%
- 전체 pair 합산: 총 포트폴리오의 60-80%(나머지 현금/T-bills)

### Transaction Costs

**Components:**
- **Commissions**: 대부분 $0이나 per-share fee 확인
- **Spread**: bid-ask spread 비용(레그당 0.01-0.05%)
- **Slippage**: 시장 충격(레그당 0.02-0.10%)
- **Short Interest**: short leg 대여 비용(연 0-50%)
- **Hard-to-Borrow Fees**: 공매도 난이도 높은 종목 추가 수수료

**Total Round-Trip Cost Estimate:**
```
Conservative: 0.4% (0.1% per leg × 4 legs)
With Short Interest: 0.4% + (0.5% × days held / 365)
```

**Breakeven Z-Score:**

거래비용을 초과하기 위한 최소 z-score:
```
Z_min = Total Transaction Cost / Expected Profit per Std Dev
```

Example:
- Transaction cost: 0.4%
- Expected profit per std dev: 0.8%
- Z_min = 0.4% / 0.8% = 0.5

→ 실제로는 |Z| > 2.0에서 진입(2σ × 0.8% = 1.6% 수익 기대, 비용 0.4% 대비 충분)

### Margin and Leverage

**Regulation T Requirements:**
- Long stock: 50% initial margin
- Short stock: 50% initial margin + 100% collateral
- Pair trade: 실질적으로 100% margin requirement

**Example:**
```
Long $10,000 Stock A:
- Margin required: $5,000

Short $10,000 Stock B:
- Margin required: $5,000
- Collateral required: $10,000
- Total tied up: $15,000

Total capital required: $20,000 for $20,000 exposure
→ No leverage in market-neutral pair trading
```

**Portfolio Margin (Advanced):**
- pair의 상쇄 리스크를 인정
- Reg T 대비 50-70% 수준으로 margin 감소 가능
- 계좌 최소 요건 $125K

---

## Common Pitfalls

### 1. Survivorship Bias

**Problem:**
- 현재 상장 종목만으로 스크리닝
- 상장폐지 종목(파산, 인수) 제외됨
- 과거 성과 과대평가

**Solution:**
- survivorship-bias-free 데이터베이스 사용
- backtest 한계를 명시
- forward testing 비중 확대

### 2. Look-Ahead Bias

**Problem:**
- 과거 분석에 미래 정보가 유입됨
- 예: 전체 기간 평균/표준편차로 z-score 계산

**Incorrect:**
```python
# Using entire dataset mean (look-ahead bias)
mean = spread.mean()
std = spread.std()
zscore = (spread - mean) / std
```

**Correct:**
```python
# Using rolling window (no look-ahead)
zscore = (spread - spread.rolling(90).mean()) / spread.rolling(90).std()
```

### 3. Overfitting

**Problem:**
- 테스트 데이터셋에 파라미터를 과최적화
- 우연한 관계를 실제 신호로 오인

**Solutions:**
- **Out-of-Sample Testing**: 70% 학습, 30% 검증
- **Walk-Forward Analysis**: 최적화 윈도우를 순차 이동
- **Simplicity**: 복잡한 최적화보다 단순 규칙(z=2.0) 선호
- **Economic Rationale**: pair 관계에 펀더멘털 근거 필요

### 4. Ignoring Structural Breaks

**Problem:**
- corporate action(합병, 분할, 구조조정)
- 비즈니스 모델 변화
- 규제 변화

**Examples:**
- tech 기업의 cloud pivot(성장 프로필 변화)
- 은행 합병(리스크 프로필 변화)
- 한 종목에만 영향을 주는 규제 변화

**Detection:**
```python
# Check for sharp correlation drop
recent_corr = returns_A[-60:].corr(returns_B[-60:])
historical_corr = returns_A[:-60].corr(returns_B[:-60])

if recent_corr < historical_corr - 0.20:
    print("WARNING: Correlation breakdown detected")
```

### 5. Insufficient Liquidity

**Problem:**
- 거래량 낮은 small cap 종목
- 넓은 bid-ask spread
- 진입/청산 시 시장 충격

**Solutions:**
- 최소 평균 거래량 요건(1M shares/day)
- mid-price 대비 spread 확인(<0.1% 권장)
- 일평균 거래량 대비 포지션 비중 제한(<5%)

### 6. Correlation ≠ Causation

**Problem:**
- 경제적 연결 없이 correlation만 높은 pair
- correlation이 일시적/우연일 수 있음

**Example:**
- Stock A와 Bitcoin의 6개월 correlation이 0.80
- 관계를 설명할 펀더멘털 근거 없음
- 붕괴 가능성 높음

**Solution:**
- 명확한 경제적 linkage가 있는 pair 우선
- 동일 섹터, 공급망, 경쟁 구도 중심

### 7. Regime Changes

**Problem:**
- 시장 regime이 pair 관계를 변화시킴
- 위기 구간: Correlations → 1 (동반 하락)
- 저변동성: mean reversion 빠름
- 고변동성: mean reversion 느리거나 부재

**VIX-Based Regime Filter:**
```
If VIX < 15: Normal regime → Trade all pairs
If VIX 15-25: Elevated volatility → Trade only high-quality pairs
If VIX > 25: Crisis mode → Exit all pairs, wait for stabilization
```

---

## Advanced Topics

### Time-Varying Hedge Ratios

**Problem with Static Beta:**
- 종목 간 관계는 시간에 따라 변화
- 고정 beta는 쉽게 낡아질 수 있음

**Kalman Filter Approach:**

새 관측치로 beta를 동적으로 업데이트:
```python
from pykalman import KalmanFilter

# Set up Kalman filter
kf = KalmanFilter(
    transition_matrices=[1],
    observation_matrices=[prices_B],
    initial_state_mean=initial_beta,
    initial_state_covariance=1,
    observation_covariance=1,
    transition_covariance=0.01
)

# Estimate time-varying beta
state_means, state_covs = kf.filter(prices_A)
dynamic_beta = state_means.flatten()
```

**Advantages:**
- 변화하는 관계에 적응
- spread 분산 축소 가능

**Disadvantages:**
- 구현 복잡도 증가
- overfitting 리스크

### Multi-Pair Portfolios

**Basket Pair Trading:**

pairwise 대신 basket 기반 구성:
```
Long Basket: Equal-weight portfolio of Stock A, C, E
Short Basket: Equal-weight portfolio of Stock B, D, F
```

**Advantages:**
- 개별 종목 리스크 축소
- 더 안정적인 spread
- 단일 종목 이벤트 영향 완화

**Statistical Arbitrage Portfolios:**
- 전체 유니버스에서 mispriced 종목 스크리닝
- 저평가 상위 decile long
- 고평가 하위 decile short
- 지속적 리밸런싱

### Machine Learning Enhancements

**Cointegration Regime Classification:**

pair의 mean reversion 가능 시점을 ML로 예측:
```python
from sklearn.ensemble import RandomForestClassifier

# Features: VIX, correlation stability, spread volatility, etc.
# Label: Did spread mean-revert within 30 days?

model = RandomForestClassifier()
model.fit(features, labels)

# Predict for current pair
will_revert = model.predict(current_features)
```

**Signal Enhancement:**
- z-score와 ML 확률 결합
- z < -2.0 AND ML_prob > 0.70일 때만 진입

**Caution:**
- overfitting 리스크 존재
- 충분한 out-of-sample 검증 필수

### Intraday Pair Trading

**High-Frequency Approach:**
- minute/tick 데이터 사용
- 더 빠른 mean reversion(half-life가 시간/분 단위)
- 저지연 실행 인프라 필요

**Challenges:**
- 고빈도에서는 transaction costs 영향이 지배적
- co-location, direct market access 필요
- market microstructure noise 증가

**Recommendation:**
- 개인 투자자: daily/weekly pair trading 권장
- 기관 투자자: 인프라 갖춘 경우 intraday 가능

---

## Conclusion

Pair trading은 강한 통계적·경제적 기반을 가진 market-neutral 전략입니다. 성공을 위해서는 다음이 필요합니다:

1. **엄격한 pair selection** (correlation만이 아니라 cointegration)
2. **강건한 통계 검증** (ADF, half-life, structural break)
3. **규율 있는 risk management** (position sizing, stop loss)
4. **현실적 비용 모델링** (transaction costs, short interest)
5. **지속적 모니터링** (regime 변화, correlation 붕괴)

**Key Takeaways:**
- Cointegration > Correlation
- z-score는 객관적 의사결정 프레임워크 제공
- mean reversion은 보장되지 않음(반드시 stop loss 사용)
- 경제적 linkage가 통계 관계를 강화
- 복잡성/과최적화보다 단순성/강건성이 우선

**Further Reading:**
- Engle & Granger (1987): "Co-Integration and Error Correction: Representation, Estimation, and Testing"
- Gatev, Goetzmann, Rouwenhorst (2006): "Pairs Trading: Performance of a Relative-Value Arbitrage Rule"
- Vidyamurthy (2004): "Pairs Trading: Quantitative Methods and Analysis"
- Chan (2013): "Algorithmic Trading: Winning Strategies and Their Rationale" (Chapter 7)

---

**Document Version**: 1.0
**Last Updated**: 2025-11-08
**Author**: Claude Trading Skills - Pair Trade Screener
