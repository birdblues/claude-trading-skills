# Cointegration Testing Guide

## Table of Contents

1. [What is Cointegration?](#what-is-cointegration)
2. [Cointegration vs Correlation](#cointegration-vs-correlation)
3. [Augmented Dickey-Fuller (ADF) Test](#augmented-dickey-fuller-adf-test)
4. [Practical Implementation](#practical-implementation)
5. [Interpreting Results](#interpreting-results)
6. [Half-Life Estimation](#half-life-estimation)
7. [Testing for Structural Breaks](#testing-for-structural-breaks)
8. [Case Studies](#case-studies)

---

## What is Cointegration?

### Intuitive Explanation

술집에서 집으로 가는 두 취객을 상상해 보세요. 둘 다 비틀거리며 랜덤하게 움직이지만, 한 사람은 목줄로 개를 데리고 있습니다. 사람과 개는 잠시 서로 다른 방향으로 움직일 수 있어도, 목줄 때문에 장기적으로는 함께 움직입니다. 이것이 "cointegrated" 상태입니다.

**In finance:**
- Person A = Stock A price
- Person B (with dog) = Stock B price
- Leash = Economic relationship (sector, supply chain, competition)

두 주가 모두 non-stationary(random walk)일 수 있지만, 경제적 "목줄"이 둘을 다시 끌어당기기 때문에 **difference(또는 spread)**는 stationary가 됩니다.

### Mathematical Definition

두 non-stationary 시계열 **X(t)** 와 **Y(t)** 가 아래 계수 **β** 를 만족할 때 cointegrated입니다:

```
Spread(t) = X(t) - β * Y(t)
```

즉 spread가 stationary(mean-reverting)여야 합니다.

**Key Components:**
- **X(t), Y(t)**: Non-stationary price series (random walks)
- **β**: Cointegration coefficient (hedge ratio)
- **Spread(t)**: Stationary series (mean-reverting)

### Why Cointegration Matters for Pair Trading

**Without Cointegration:**
- 가격이 무기한 벌어질 수 있음
- mean reversion 보장이 없음
- 영구 손실 리스크가 큼

**With Cointegration:**
- 가격에 장기 균형이 존재
- 일시적 괴리가 예측 가능
- mean reversion이 통계적으로 보장됨

**Example:**

**Non-Cointegrated Pair:**
```
Stock A: Oil producer
Stock B: Tech company
Correlation: 0.75 (recent coincidence)

Result: No economic linkage → correlation breaks down → prices diverge forever
```

**Cointegrated Pair:**
```
Stock A: Exxon (XOM)
Stock B: Chevron (CVX)
Correlation: 0.92
Cointegration p-value: 0.008 (strong)

Result: Same sector, similar business → prices stay together → mean reversion reliable
```

---

## Cointegration vs Correlation

### Key Differences

| Aspect | Correlation | Cointegration |
|--------|-------------|---------------|
| **Measures** | 단기 수익률 동행성 | 장기 가격 레벨 관계 |
| **Data** | First differences (returns) | Price levels |
| **Range** | -1 to +1 | p-value (0 to 1) |
| **Stationarity** | 두 시계열 stationary 가정 | non-stationary 시계열 허용 |
| **Mean Reversion** | 의미하지 않음 | 보장함(spread 기준) |
| **Stability** | 불안정할 수 있음 | 상대적으로 더 안정적 |

### Why Correlation Alone is Insufficient

**Problem with Correlation:**

아무 관계 없는 두 random walk도 **우연히** 높은 correlation을 가질 수 있습니다.

**Example:**
```python
import numpy as np

# Generate two independent random walks
np.random.seed(42)
walk_A = np.cumsum(np.random.randn(252))
walk_B = np.cumsum(np.random.randn(252))

# Calculate correlation
correlation = np.corrcoef(walk_A, walk_B)[0, 1]
# Result: Might be 0.60-0.80 purely by chance!
```

**Key Point:**
- High correlation ≠ Mean reversion
- spread stationary 보장을 위해 cointegration 테스트가 필요

### Combining Correlation and Cointegration

**Best Practice:**

두 필터를 함께 사용:
1. **Correlation** (≥ 0.70): 빠른 동행성 1차 스크린
2. **Cointegration** (p < 0.05): mean reversion을 위한 엄격한 검증

**Decision Matrix:**

| Correlation | Cointegration | Trade? |
|-------------|---------------|--------|
| High (≥0.70) | Yes (p<0.05) | ✅ **YES** |
| High (≥0.70) | No (p>0.05) | ❌ **NO** |
| Low (<0.70) | Yes (p<0.05) | 🟡 **MAYBE** (unusual) |
| Low (<0.70) | No (p>0.05) | ❌ **NO** |

---

## Augmented Dickey-Fuller (ADF) Test

### Purpose

ADF test는 시계열에 **unit root(비정상성)** 가 있는지, 또는 stationary인지 판단합니다.

**Hypotheses:**
- **Null (H0)**: 시계열에 unit root가 있음(non-stationary)
- **Alternative (H1)**: 시계열이 stationary

**For pair trading:**
- 개별 가격이 아니라 **spread**를 테스트
- H0 기각 → spread stationary → pair cointegrated

### Test Procedure

**Step 1: Calculate Spread**
```python
spread = price_A - (beta * price_B)
```

**Step 2: Run ADF Test**
```python
from statsmodels.tsa.stattools import adfuller

result = adfuller(spread, maxlag=1, regression='c')
adf_statistic = result[0]
p_value = result[1]
critical_values = result[4]
```

**Parameters:**
- `maxlag=1`: lag 수(일봉 데이터는 보통 1)
- `regression='c'`: 상수항 포함(drift)
- 대안: `'ct'` (상수 + 추세), `'n'` (상수 없음)

**Step 3: Interpret Results**
```python
if p_value < 0.05:
    print("Reject null → Spread is stationary → Cointegrated")
else:
    print("Fail to reject null → Not cointegrated")
```

### ADF Test Equation

ADF test는 다음을 추정합니다:
```
ΔSpread(t) = α + β*Spread(t-1) + Σ(γ_i * ΔSpread(t-i)) + ε(t)
```

Where:
- ΔSpread(t) = Spread(t) - Spread(t-1) (first difference)
- β: 핵심 계수(unit root 여부 테스트)
- α: Drift term
- Σ(γ_i * ΔSpread(t-i)): lagged differences(직렬상관 반영)

**Test Statistic:**
```
ADF = β / SE(β)
```

**Decision Rule:**
- ADF < Critical Value → 귀무가설 기각(stationary)
- p-value < 0.05 → 귀무가설 기각(stationary)

### Critical Values

**Standard Critical Values (constant, no trend):**

| Significance Level | Critical Value |
|--------------------|----------------|
| 1% | -3.43 |
| 5% | -2.86 |
| 10% | -2.57 |

**Example:**
```
ADF Statistic: -3.75
Critical Value (5%): -2.86

Since -3.75 < -2.86 → Reject null → Stationary
```

---

## Practical Implementation

### Complete Python Example

```python
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from scipy import stats

# Step 1: Load price data
prices_A = pd.Series([100, 102, 104, 103, 105, ...])  # Stock A
prices_B = pd.Series([50, 51, 52, 51.5, 52.5, ...])    # Stock B

# Step 2: Calculate beta (hedge ratio)
slope, intercept, r_value, p_value, std_err = stats.linregress(prices_B, prices_A)
beta = slope

print(f"Beta (hedge ratio): {beta:.4f}")
print(f"Correlation: {r_value:.4f}")

# Step 3: Calculate spread
spread = prices_A - (beta * prices_B)

# Step 4: Run ADF test
adf_result = adfuller(spread, maxlag=1, regression='c')

adf_statistic = adf_result[0]
p_value = adf_result[1]
critical_values = adf_result[4]
n_lags = adf_result[2]

# Step 5: Display results
print("\n=== Cointegration Test Results ===")
print(f"ADF Statistic: {adf_statistic:.4f}")
print(f"P-value: {p_value:.4f}")
print(f"Number of Lags: {n_lags}")
print(f"\nCritical Values:")
for key, value in critical_values.items():
    print(f"  {key}: {value:.4f}")

# Step 6: Interpret
if p_value < 0.01:
    print("\n✅ STRONG Cointegration (p < 0.01)")
    strength = "★★★"
elif p_value < 0.05:
    print("\n✅ MODERATE Cointegration (p < 0.05)")
    strength = "★★"
else:
    print("\n❌ NOT Cointegrated (p > 0.05)")
    strength = "☆"

# Step 7: Calculate half-life (if cointegrated)
if p_value < 0.05:
    from statsmodels.tsa.ar_model import AutoReg

    model = AutoReg(spread, lags=1)
    result = model.fit()
    phi = result.params[1]

    half_life = -np.log(2) / np.log(phi)
    print(f"\nHalf-Life: {half_life:.1f} days")

    if half_life < 30:
        print("  → Fast mean reversion (excellent)")
    elif half_life < 60:
        print("  → Moderate mean reversion (good)")
    else:
        print("  → Slow mean reversion (acceptable)")
```

### FMP API Integration

```python
import requests
import pandas as pd

def get_price_history(symbol, api_key, days=730):
    """Fetch historical prices from FMP API"""
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}?apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    # Extract historical prices
    hist = data['historical'][:days]
    hist = hist[::-1]  # Reverse to chronological order

    df = pd.DataFrame(hist)
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')

    return df['adjClose']

# Example usage
api_key = "YOUR_API_KEY"
prices_AAPL = get_price_history("AAPL", api_key)
prices_MSFT = get_price_history("MSFT", api_key)

# Align dates
common_dates = prices_AAPL.index.intersection(prices_MSFT.index)
prices_AAPL = prices_AAPL.loc[common_dates]
prices_MSFT = prices_MSFT.loc[common_dates]

# Test for cointegration
slope, intercept, r_value, p_value, std_err = stats.linregress(prices_MSFT, prices_AAPL)
beta = slope
spread = prices_AAPL - (beta * prices_MSFT)

adf_result = adfuller(spread, maxlag=1)
print(f"AAPL/MSFT Cointegration p-value: {adf_result[1]:.4f}")
```

---

## Interpreting Results

### P-Value Interpretation

**What p-value means:**
- null hypothesis(unit root)가 참일 때 현재 test statistic이 관측될 확률
- p-value가 낮을수록 귀무가설 반박 근거가 강함 = cointegration 강함

**Guidelines:**

| P-Value Range | Interpretation | Confidence | Trade? |
|---------------|----------------|------------|--------|
| p < 0.01 | 매우 강한 cointegration | 99% | ✅ **YES** (★★★) |
| p 0.01-0.03 | 강한 cointegration | 97-99% | ✅ **YES** (★★★) |
| p 0.03-0.05 | 중간 cointegration | 95-97% | ✅ **YES** (★★) |
| p 0.05-0.10 | 약한 증거 | 90-95% | 🟡 **MARGINAL** (★) |
| p > 0.10 | cointegration 없음 | <90% | ❌ **NO** (☆) |

### ADF Statistic Interpretation

**더 음수일수록 cointegration이 강함:**

```
ADF < -4.0: Very strong (★★★★)
ADF -3.5 to -4.0: Strong (★★★)
ADF -3.0 to -3.5: Moderate (★★)
ADF -2.5 to -3.0: Weak (★)
ADF > -2.5: Not cointegrated (☆)
```

**Example Rankings:**

```python
Pair A: ADF = -4.25, p = 0.002 → ★★★★ (Best)
Pair B: ADF = -3.65, p = 0.018 → ★★★ (Excellent)
Pair C: ADF = -2.95, p = 0.042 → ★★ (Good)
Pair D: ADF = -2.45, p = 0.125 → ☆ (Reject)
```

### Common Mistakes

**Mistake 1: Testing Individual Prices**
```python
# WRONG: Testing if stock price is stationary
adf_result = adfuller(prices_A)  # ❌ Will always fail (prices are random walks)
```

**Correct:**
```python
# RIGHT: Test if SPREAD is stationary
spread = prices_A - (beta * prices_B)
adf_result = adfuller(spread)  # ✅ Tests for cointegration
```

**Mistake 2: Ignoring Lag Selection**
```python
# WRONG: Using too many lags (overfitting)
adf_result = adfuller(spread, maxlag=20)  # ❌ Too complex

# RIGHT: Use simple lag structure
adf_result = adfuller(spread, maxlag=1)  # ✅ Appropriate for daily data
```

**Mistake 3: Confusing Correlation with Cointegration**
```python
# WRONG: Assuming high correlation = cointegration
if correlation > 0.80:
    trade_pair()  # ❌ Not sufficient

# RIGHT: Test for cointegration explicitly
if correlation > 0.70 and cointegration_pvalue < 0.05:
    trade_pair()  # ✅ Both conditions required
```

---

## Half-Life Estimation

### What is Half-Life?

half-life는 spread가 평균으로 얼마나 빠르게 되돌아가는지를 측정합니다. 즉, spread가 평균까지 절반 복귀하는 데 걸리는 기대 시간입니다.

**Example:**
```
Current spread: +2.0 (2 std devs above mean)
Half-life: 20 days

Expected spread after 20 days: +1.0 (halfway to mean)
Expected spread after 40 days: +0.5 (halfway from +1.0 to 0)
```

### AR(1) Model Approach

spread를 자기회귀 과정으로 모델링:
```
S(t) = α + φ * S(t-1) + ε(t)
```

Where:
- φ: 자기상관 계수(지속성)
- φ가 1.0에 가까움 → 느린 mean reversion(긴 half-life)
- φ가 0.0에 가까움 → 빠른 mean reversion(짧은 half-life)

**Half-Life Formula:**
```
Half-Life = -ln(2) / ln(φ)
```

### Python Implementation

```python
from statsmodels.tsa.ar_model import AutoReg

# Fit AR(1) model to spread
model = AutoReg(spread, lags=1)
result = model.fit()

# Extract autocorrelation coefficient
phi = result.params[1]

# Calculate half-life
half_life = -np.log(2) / np.log(phi)

print(f"Autocorrelation (φ): {phi:.4f}")
print(f"Half-Life: {half_life:.1f} days")
```

### Interpreting Half-Life

| Half-Life | Speed | Suitability | Holding Period |
|-----------|-------|-------------|----------------|
| < 10 days | Very fast | Day/swing trading | < 2 weeks |
| 10-30 days | Fast | Short-term pairs | 2-6 weeks |
| 30-60 days | Moderate | Standard pairs | 1-3 months |
| 60-90 days | Slow | Long-term pairs | 2-6 months |
| > 90 days | Very slow | 트레이딩 부적합 | Avoid |

**Trading Implications:**

**Fast Half-Life (< 30 days):**
- ✅ 빠른 수익 실현 가능
- ✅ 보유 리스크 낮음
- ✅ 기회 빈도 높음
- ❌ transaction costs 영향이 커짐

**Slow Half-Life (> 60 days):**
- ✅ 관계가 더 안정적인 경우가 있음
- ❌ 자본이 오래 묶임
- ❌ 기회 빈도 낮음
- ❌ 보유 중 regime change 리스크 증가

### Half-Life Stability

**여러 기간에서 half-life 안정성 테스트:**
```python
# Calculate rolling half-life
rolling_half_life = []

for i in range(252, len(spread)):
    window = spread[i-252:i]
    model = AutoReg(window, lags=1)
    result = model.fit()
    phi = result.params[1]
    hl = -np.log(2) / np.log(phi)
    rolling_half_life.append(hl)

# Check stability
std_hl = np.std(rolling_half_life)
mean_hl = np.mean(rolling_half_life)
cv = std_hl / mean_hl  # Coefficient of variation

if cv < 0.30:
    print("Half-life is STABLE (good)")
else:
    print("Half-life is UNSTABLE (warning)")
```

---

## Testing for Structural Breaks

### Why Structural Breaks Matter

**Definition:**
- structural break는 cointegration 관계의 갑작스럽고 영구적인 변화
- 예: 합병, 분할, 비즈니스 모델 전환, 규제 변화

**Impact on Pair Trading:**
- cointegration 붕괴 → spread mean reversion 상실
- break 구간 보유 시 대규모 손실 가능
- 조기 탐지 후 청산이 핵심

### Chow Test

알려진 시점(예: 특정 corporate event 날짜)의 structural break 테스트:

```python
from statsmodels.stats.diagnostic import breaks_cusumolsresid

# Fit OLS regression
from scipy import stats
slope, intercept = stats.linregress(prices_B, prices_A)[:2]
residuals = prices_A - (slope * prices_B + intercept)

# Test for structural breaks
stat, pvalue = breaks_cusumolsresid(residuals)

if pvalue < 0.05:
    print("⚠️ STRUCTURAL BREAK DETECTED")
else:
    print("✅ No structural break")
```

### Rolling Cointegration

**시간에 따른 cointegration 모니터링:**
```python
rolling_pvalues = []

for i in range(252, len(prices_A)):
    window_A = prices_A[i-252:i]
    window_B = prices_B[i-252:i]

    slope, intercept = stats.linregress(window_B, window_A)[:2]
    spread_window = window_A - (slope * window_B)

    adf_result = adfuller(spread_window, maxlag=1)
    pvalue = adf_result[1]
    rolling_pvalues.append(pvalue)

# Plot rolling p-values
import matplotlib.pyplot as plt
plt.plot(rolling_pvalues)
plt.axhline(y=0.05, color='r', linestyle='--', label='Significance threshold')
plt.ylabel('P-Value')
plt.xlabel('Time')
plt.title('Rolling Cointegration P-Value')
plt.legend()
plt.show()
```

**Interpretation:**
- p-value가 0.05 아래 유지 → cointegration 안정적 ✅
- p-value가 0.05 위로 상승 → cointegration 약화 ⚠️
- p-value가 0.10 이상 지속 → 관계 붕괴 ❌

### Early Warning System

**cointegration 약화 기반 청산 규칙:**
```python
# Calculate 90-day rolling cointegration p-value
recent_pvalue = calculate_rolling_cointegration(prices_A[-90:], prices_B[-90:])

if recent_pvalue > 0.10:
    print("🚨 EXIT SIGNAL: Cointegration broken")
    exit_pair()
elif recent_pvalue > 0.05:
    print("⚠️ WARNING: Cointegration weakening")
    reduce_position()
else:
    print("✅ Cointegration healthy")
```

---

## Case Studies

### Case Study 1: XOM/CVX (Strong Cointegration)

**Background:**
- Exxon Mobil (XOM) and Chevron (CVX)
- Both: 대형 oil & gas 기업
- 동일 섹터, 유사한 비즈니스 모델

**Analysis:**
```python
# 2-year data (2023-2025)
correlation: 0.94
beta: 1.08
adf_statistic: -4.25
p_value: 0.0008
half_life: 28 days
```

**Interpretation:**
- ✅ 매우 강한 cointegration (p < 0.01)
- ✅ 높은 correlation (0.94)
- ✅ 빠른 mean reversion (28 days)
- ✅ 경제적 연결성(동일 섹터)

**Rating:** ★★★★ (Excellent pair)

**Trade Signal (Example):**
```
Current Z-Score: +2.3 (XOM expensive relative to CVX)
→ SHORT XOM, LONG CVX
Entry: Z > +2.0
Exit: Z < 0.0
Stop: Z > +3.0
```

### Case Study 2: JPM/BAC (Moderate Cointegration)

**Background:**
- JPMorgan Chase (JPM) and Bank of America (BAC)
- Both: 대형 은행
- 사업 포커스 차이 존재(JPM은 IB 비중, BAC는 리테일 비중)

**Analysis:**
```python
correlation: 0.85
beta: 1.35
adf_statistic: -3.12
p_value: 0.031
half_life: 42 days
```

**Interpretation:**
- ✅ 중간 cointegration (p = 0.031)
- ✅ 양호한 correlation (0.85)
- ✅ 수용 가능한 mean reversion (42 days)
- ⚠️ 사업 믹스가 달라 연결성 완전 일치 아님

**Rating:** ★★★ (Good pair)

### Case Study 3: AAPL/TSLA (No Cointegration)

**Background:**
- Apple (AAPL) and Tesla (TSLA)
- Both: 고성장 tech 성격
- 사업 구조 상이(consumer electronics vs EV)

**Analysis:**
```python
correlation: 0.72
beta: 0.88
adf_statistic: -2.15
p_value: 0.182
half_life: N/A (not stationary)
```

**Interpretation:**
- ❌ cointegration 없음 (p = 0.182)
- ✅ 중간 correlation (0.72)
- ❌ mean reversion 근거 없음
- ❌ 경제적 연결성 약함

**Rating:** ☆ (Reject pair)

**Why correlation failed:**
- 2023-2024의 성장주 랠리로 동행
- correlation이 펀더멘털이 아닌 macro factor(금리)에 의해 형성
- 시장 환경 변화 시 괴리 가능성 큼

### Case Study 4: Structural Break Example (GE)

**Background:**
- General Electric (GE)는 2018-2021 대규모 구조조정 진행
- healthcare(GEHC), energy 부문 분할

**Analysis:**
```python
# Pre-spinoff (2018-2020): GE/UTX pair
correlation: 0.81
p_value: 0.025 (cointegrated)

# Post-spinoff (2021-2023): GE/UTX pair
correlation: 0.52
p_value: 0.235 (NOT cointegrated)
```

**Lesson:**
- corporate action은 cointegration 관계를 깨뜨릴 수 있음
- structural break 모니터링이 필수
- cointegration 악화 시 pair 청산

---

## Summary Checklist

거래 전에 아래를 확인하세요:

### Statistical Checklist
- [ ] Correlation ≥ 0.70 (preferably ≥ 0.80)
- [ ] Cointegration p-value < 0.05 (preferably < 0.03)
- [ ] ADF statistic < -3.0
- [ ] Half-life 20-60 days
- [ ] 최근 6개월 structural break 없음

### Economic Checklist
- [ ] 동일 섹터 또는 공급망 관계
- [ ] 유사한 비즈니스 모델
- [ ] 대기 중인 M&A/구조조정 없음
- [ ] 유사한 시가총액과 유동성
- [ ] 공매도 가능 종목(숏 레그)

### Risk Checklist
- [ ] transaction costs < expected profit
- [ ] 충분한 유동성(>1M avg volume)
- [ ] 적절한 position sizing(최대 10-15%)
- [ ] stop loss 정의됨(Z > ±3.0)
- [ ] 최대 보유 기간 설정(90 days)

---

**Document Version**: 1.0
**Last Updated**: 2025-11-08
**References**:
- Engle & Granger (1987): "Co-Integration and Error Correction"
- Hamilton (1994): "Time Series Analysis" (Chapter 19)
- Tsay (2010): "Analysis of Financial Time Series" (Chapter 8)
