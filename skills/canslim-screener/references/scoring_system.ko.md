# CANSLIM Scoring System - Phase 3 (Full CANSLIM)

## 개요

이 문서는 CANSLIM 스크리너의 composite scoring 체계를 정의합니다. Phase 3는 **7개 요소 전체**(C, A, N, S, L, I, M)를 구현하며, O'Neil 원본 가중치 기준으로 CANSLIM 전체 방법론 100%를 반영합니다.

---

## 요소 가중치

### Phase 3 가중치 (Full CANSLIM - 7 Components)

| Component | Weight | Rationale |
|-----------|--------|-----------|
| **C** - Current Earnings | **15%** | 가장 예측력이 높은 단일 요인 (O'Neil #1) |
| **A** - Annual Growth | **20%** | 실적 성장의 지속 가능성 검증 |
| **N** - Newness | **15%** | 모멘텀 확인의 핵심 |
| **S** - Supply/Demand | **15%** | 거래량 accumulation/distribution 분석 |
| **L** - Leadership/RS Rank | **20%** | A와 동률의 최대 비중 - 섹터 리더 식별 |
| **I** - Institutional Sponsorship | **10%** | smart money 확인 |
| **M** - Market Direction | **5%** | gating filter - 모든 종목에 영향 |
| **Total** | **100%** | O'Neil 원본 가중치 |

### Legacy Phase 가중치 (참고용)

**Phase 1 MVP** (4 components - C, A, N, M): 정규화 가중치 C 27%, A 36%, N 27%, M 10%  
**Phase 2** (6 components - C, A, N, S, I, M): 정규화 가중치 C 19%, A 25%, N 19%, S 19%, I 13%, M 6%

---

## 요소별 점수 산식 (0-100 Scale)

각 요소는 O'Neil의 정량 임계값에 따라 0-100점으로 산출합니다.

### C - Current Quarterly Earnings (0-100 Points)

**필수 입력 데이터:**
- 최신 분기 EPS (most recent quarter)
- 전년 동기 EPS (same quarter, prior year)
- 최신 분기 revenue
- 전년 동기 revenue

**계산:**
```python
eps_growth_pct = ((latest_qtr_eps - year_ago_qtr_eps) / abs(year_ago_qtr_eps)) * 100
revenue_growth_pct = ((latest_qtr_revenue - year_ago_qtr_revenue) / year_ago_qtr_revenue) * 100
```

**점수 로직:**
```python
if eps_growth_pct >= 50 and revenue_growth_pct >= 25:
    c_score = 100  # Explosive growth
elif eps_growth_pct >= 30 and revenue_growth_pct >= 15:
    c_score = 80   # Strong growth
elif eps_growth_pct >= 18 and revenue_growth_pct >= 10:
    c_score = 60   # Meets CANSLIM minimum
elif eps_growth_pct >= 10:
    c_score = 40   # Below threshold
else:
    c_score = 0    # Weak or negative growth
```

**해석:**
- **100점**: Exceptional - 최상위 실적 가속
- **80점**: Strong - CANSLIM 기준을 크게 상회
- **60점**: Acceptable - 최소 18% 기준 충족
- **40점**: Weak - CANSLIM 기준 미달
- **0점**: Fails - 성장 부족

**품질 점검:**
- revenue growth가 EPS growth의 50% 미만이면 실적 품질 점검 필요(자사주 매입 영향 가능성)
- revenue가 음수인데 EPS가 양수면 red flag

---

### A - Annual EPS Growth (0-100 Points)

**필수 입력 데이터:**
- 현재 연도 포함 직전 3년까지 연간 EPS (총 4년)
- 동일 4년의 연간 revenue (검증용)

**계산:**
```python
# 3-year CAGR (Compound Annual Growth Rate)
eps_cagr_3yr = (((current_year_eps / eps_3_years_ago) ** (1/3)) - 1) * 100
revenue_cagr_3yr = (((current_year_revenue / revenue_3_years_ago) ** (1/3)) - 1) * 100

# Growth stability check
eps_values = [year1_eps, year2_eps, year3_eps, year4_eps]  # chronological order
stable = all(eps_values[i] >= eps_values[i-1] for i in range(1, 4))  # No down years
```

**점수 로직:**
```python
# Base score from EPS CAGR
if eps_cagr_3yr >= 40:
    base_score = 90
elif eps_cagr_3yr >= 30:
    base_score = 70
elif eps_cagr_3yr >= 25:
    base_score = 50  # Meets CANSLIM minimum
elif eps_cagr_3yr >= 15:
    base_score = 30
else:
    base_score = 0

# Revenue growth validation penalty
if revenue_cagr_3yr < (eps_cagr_3yr * 0.5):
    base_score = int(base_score * 0.8)  # 20% penalty for weak revenue growth

# Stability bonus
if stable:  # No down years
    base_score += 10

a_score = min(base_score, 100)  # Cap at 100
```

**해석:**
- **90-100점**: Exceptional - 고성장 + 안정성
- **70-89점**: Strong - 25% 기준을 충분히 상회
- **50-69점**: Acceptable - CANSLIM 최소 기준 충족
- **30-49점**: Weak - 기준 미달
- **0-29점**: Fails - 성장 부족 또는 변동성 과다

**품질 점검:**
- 안정성 보너스(+10): down year가 없는 일관 성장 보상
- revenue 검증: buyback-driven EPS 급증을 방지

---

### N - Newness / New Highs (0-100 Points)

**필수 입력 데이터:**
- 현재 주가
- 52-week high
- 52-week low
- 최근 일별 volume(30일)
- 평균 volume(30일 평균)
- 최근 뉴스 헤드라인(선택, new product 감지)

**계산:**
```python
# Distance from 52-week high
distance_from_high_pct = ((current_price / week_52_high) - 1) * 100

# Breakout detection (new high on volume)
breakout_detected = (
    current_price >= week_52_high * 0.995 and  # Within 0.5% of high
    recent_volume > avg_volume * 1.4           # Volume 40%+ above average
)

# New product signal detection (keyword search in news)
new_product_signals = search_news_keywords([
    "FDA approval", "patent granted", "breakthrough", "game-changer",
    "new product", "product launch", "expansion", "acquisition"
])
```

**점수 로직:**
```python
# Base score from price position
if distance_from_high_pct >= -5 and breakout_detected and new_product_signals:
    base_score = 100  # Perfect setup
elif distance_from_high_pct >= -10 and breakout_detected:
    base_score = 80   # Strong momentum
elif distance_from_high_pct >= -15 or breakout_detected:
    base_score = 60   # Acceptable
elif distance_from_high_pct >= -25:
    base_score = 40   # Weak momentum
else:
    base_score = 20   # Too far from highs

# Bonus for new product/catalyst signals (optional data)
if new_product_signals:
    if "FDA approval" in signals or "breakthrough" in signals:
        base_score += 20  # High-impact catalyst
    elif "new product" in signals or "acquisition" in signals:
        base_score += 10  # Moderate catalyst

n_score = min(base_score, 100)  # Cap at 100
```

**해석:**
- **90-100점**: Exceptional - 신고가 + catalyst
- **70-89점**: Strong - 신고가 근접 + 거래량 확인
- **50-69점**: Acceptable - 고점 대비 15% 이내
- **30-49점**: Weak - 모멘텀 부족
- **0-29점**: Fails - 고점과 거리 멀고 sponsorship 부족

**참고**: N 점수의 주 신호는 price position(80%), new product 감지는 보조(20% bonus)입니다.

---

### M - Market Direction (0-100 Points)

**필수 입력 데이터:**
- S&P 500 현재 가격
- S&P 500 50-day Exponential Moving Average (EMA)
- VIX 현재 레벨
- Follow-through day 감지(선택 고급 기능)

**계산:**
```python
# Distance from 50-day EMA
distance_from_ema_pct = ((sp500_price / sp500_ema_50) - 1) * 100

# Trend determination
if distance_from_ema_pct >= 2.0:
    trend = "strong_uptrend"
elif distance_from_ema_pct >= 0:
    trend = "uptrend"
elif distance_from_ema_pct >= -2.0:
    trend = "choppy"
elif distance_from_ema_pct >= -5.0:
    trend = "downtrend"
else:
    trend = "bear_market"
```

**점수 로직:**
```python
# Base score from trend
if trend == "strong_uptrend" and vix < 15:
    base_score = 100  # Ideal conditions
elif trend == "strong_uptrend" or (trend == "uptrend" and vix < 20):
    base_score = 80   # Favorable
elif trend == "uptrend":
    base_score = 60   # Acceptable
elif trend == "choppy":
    base_score = 40   # Neutral/caution
elif trend == "downtrend":
    base_score = 20   # Weak market
else:  # bear_market or vix > 30
    base_score = 0    # Avoid stocks entirely

# VIX adjustment (fear gauge)
if vix < 15:
    base_score += 10  # Low fear, bullish
elif vix > 30:
    base_score = 0    # Panic, override trend

# Follow-through day bonus (optional advanced feature)
if follow_through_day_detected:
    base_score += 10  # Confirmed institutional buying

m_score = min(max(base_score, 0), 100)  # Cap between 0-100
```

**해석:**
- **90-100점**: Strong bull market - 공격적 매수 가능
- **70-89점**: Bull market - 표준 사이징
- **50-69점**: Early uptrend - 소규모 초기 진입
- **30-49점**: Choppy/neutral - 노출 축소 및 선별
- **10-29점**: Downtrend - 방어적 포지션
- **0점**: Bear market - 현금 80-100%, 매수 금지

**핵심 규칙**: M score = 0이면 다른 요소 점수와 무관하게 **어떤 종목도 매수하지 않습니다**.

---

### L - Leadership / Relative Strength (0-100 Points)

**필수 입력 데이터:**
- 종목 52주 historical prices
- S&P 500 52주 historical prices (benchmark)

**계산:**
```python
# 52-week stock performance
stock_perf = ((current_price / price_52w_ago) - 1) * 100

# 52-week S&P 500 performance
sp500_perf = ((sp500_current / sp500_52w_ago) - 1) * 100

# Relative performance
relative_perf = stock_perf - sp500_perf

# RS Rank estimate (1-99 scale)
rs_rank = calculate_rs_rank(relative_perf)
```

**점수 로직:**
```python
if rs_rank >= 90:
    base_score = 100  # Top decile leader
elif rs_rank >= 80:
    base_score = 80   # Strong leader
elif rs_rank >= 70:
    base_score = 60   # Above average
elif rs_rank >= 60:
    base_score = 40   # Average
else:
    base_score = 20   # Laggard
```

**해석:**
- **90-100점**: 최상위 RS leader - 시장 대비 큰 초과성과
- **70-89점**: 강한 relative strength - 시장 초과성과
- **50-69점**: 평균 RS
- **30-49점**: 평균 이하 - 시장 underperform
- **0-29점**: laggard - 크게 underperform, CANSLIM 기준 회피

**O'Neil 규칙**: "RS rating 80 이상 종목을 매수하고, 70 미만 laggard는 피하라."

---

## Composite Score 계산

### 공식 (Phase 3 - Full CANSLIM)

```python
composite_score = (
    c_score * 0.15 +  # Current Earnings: 15% weight
    a_score * 0.20 +  # Annual Growth: 20% weight
    n_score * 0.15 +  # Newness: 15% weight
    s_score * 0.15 +  # Supply/Demand: 15% weight
    l_score * 0.20 +  # Leadership/RS Rank: 20% weight
    i_score * 0.10 +  # Institutional: 10% weight
    m_score * 0.05    # Market Direction: 5% weight
)

# Result: 0-100 composite score
```

### 해석 밴드 (Phase 3)

| Score Range | Rating | Percentile | Meaning | Action |
|-------------|--------|------------|---------|--------|
| **90-100** | **Exceptional+** | Top 1-2% | 드문 multi-bagger 셋업 + 강한 기관 수급 | 즉시 매수, 공격적 사이징 (15-20%) |
| **80-89** | **Exceptional** | Top 5-10% | 뛰어난 펀더멘털 + accumulation | Strong buy, 표준 사이징 (10-15%) |
| **70-79** | **Strong** | Top 15-20% | 고품질 CANSLIM 종목 | 눌림목 매수, 표준 사이징 (10-15%) |
| **60-69** | **Above Average** | Top 30% | 준수하나 일부 약점 | Watchlist, 소규모 사이징 (5-10%) |
| **50-59** | **Average** | Top 50% | 최소 기준 충족, 확신 부족 | Watchlist, 개선 대기 |
| **40-49** | **Below Average** | Bottom 50% | 핵심 요소 하나 이상 약함 | 모니터링만, 매수 금지 |
| **<40** | **Weak** | Bottom 30% | CANSLIM 기준 미충족 | 회피 |

### Weakest Component 식별

각 종목에서 **최저 개별 점수 요소**를 식별해 추가 리스크 분석에 사용:

```python
components = {
    'C': c_score,
    'A': a_score,
    'N': n_score,
    'S': s_score,
    'L': l_score,
    'I': i_score,
    'M': m_score
}

weakest_component = min(components, key=components.get)
weakest_score = components[weakest_component]
```

**활용 예시:**
- Weakest = C → 실적 둔화 리스크
- Weakest = A → 지속 성장 이력 부족
- Weakest = N → 모멘텀 부족, 고점과 거리 멂
- Weakest = S → 분산(Distribution) 패턴, 기관 매도 가능성
- Weakest = L → 시장 후행, 섹터 리더 아님
- Weakest = I → 기관 보유 과소/과밀, 추가 조사 필요
- Weakest = M → 시장 타이밍 불리, 대기 고려

### 공식 (Phase 2 - 6 Components)

```python
composite_score = (
    c_score * 0.19 +  # Current Earnings: 19% weight
    a_score * 0.25 +  # Annual Growth: 25% weight
    n_score * 0.19 +  # Newness: 19% weight
    s_score * 0.19 +  # Supply/Demand: 19% weight (NEW)
    i_score * 0.13 +  # Institutional: 13% weight (NEW)
    m_score * 0.06    # Market Direction: 6% weight
)

# Result: 0-100 composite score (Phase 2)
```

### 해석 밴드 (Phase 2)

| Score Range | Rating | Percentile | Meaning | Action |
|-------------|--------|------------|---------|--------|
| **90-100** | **Exceptional+** | Top 1-2% | 드문 multi-bagger 셋업 + 강한 기관 수급 | 즉시 매수, 공격적 사이징 (15-20%) |
| **80-89** | **Exceptional** | Top 5-10% | 뛰어난 펀더멘털 + accumulation | Strong buy, 표준 사이징 (10-15%) |
| **70-79** | **Strong** | Top 15-20% | 고품질 CANSLIM 종목 | 눌림목 매수, 표준 사이징 (10-15%) |
| **60-69** | **Above Average** | Top 30% | 준수하나 일부 약점 | Watchlist, 소규모 사이징 (5-10%) |
| **<60** | **Below Standard** | Bottom 70% | 기준 미달 요소 존재 | 모니터링만, 매수 금지 |

**주요 개선점**: Phase 2 점수는 기관 검증(S, I)을 포함해 Phase 1보다 예측력이 높습니다.

### 최소 기준 (Phase 2)

매수 가능한 CANSLIM 후보가 되려면 6개 요소 모두 baseline 충족 필요:

```python
thresholds = {
    "C": 60,  # 18%+ quarterly EPS growth
    "A": 50,  # 25%+ annual CAGR
    "N": 40,  # Within 15% of 52-week high
    "S": 40,  # Accumulation pattern (ratio ≥ 1.0)
    "I": 40,  # 30+ holders OR 20%+ ownership
    "M": 40   # Market in uptrend
}

# Stock passes if ALL components >= thresholds
passes_threshold = all(score >= thresholds[comp] for comp, score in scores.items())
```

**미충족 해석:**
- C 미달 → 실적 둔화, 회피
- A 미달 → 지속 성장 부족
- N 미달 → 고점과 거리 멀어 강세 부족
- S 미달 → distribution 패턴, 기관 매도 가능성
- I 미달 → 기관 수급 약함
- M 미달 → 시장 약세, 회복 대기

### Weakest Component 식별 (Phase 2)

```python
components = {
    'C': c_score,
    'A': a_score,
    'N': n_score,
    'S': s_score,  # NEW
    'I': i_score,  # NEW
    'M': m_score
}

weakest_component = min(components, key=components.get)
weakest_score = components[weakest_component]
```

**추가 해석:**
- Weakest = S → distribution 패턴, 기관 매도 우위 가능성
- Weakest = I → underowned 또는 overcrowded 가능성

---

## 계산 예시

### Example 1: NVDA (2023 Q2) - Exceptional Setup

**Component Scores:**
- **C Score**: 100 points (EPS +429% YoY, Revenue +101% YoY)
- **A Score**: 95 points (3yr CAGR 89%, stable, revenue strong)
- **N Score**: 98 points (신고가, AI catalyst, breakout volume)
- **M Score**: 100 points (S&P 500 strong uptrend, VIX <15)

**Composite Calculation:**
```python
composite = (100 * 0.27) + (95 * 0.36) + (98 * 0.27) + (100 * 0.10)
          = 27.0 + 34.2 + 26.46 + 10.0
          = 97.66 points
```

**Rating**: Exceptional (97.66/100)  
**해석**: 교과서적 CANSLIM 셋업 - 전 요소 정렬, 드문 multi-bagger 후보  
**Weakest Component**: A (95) - 최약 요소조차도 매우 강함  
**Action**: Strong buy, 공격적 사이징(포트폴리오 15-20%)

---

### Example 2: META (2023 Q3) - Strong Setup

**Component Scores:**
- **C Score**: 85 points (EPS +164% YoY, Revenue +23% YoY)
- **A Score**: 78 points (3yr CAGR 28%, 2022 저점 이후 회복)
- **N Score**: 88 points (52-week high 대비 5%, breakout pattern)
- **M Score**: 80 points (S&P 500 above EMA, VIX 18)

**Composite Calculation:**
```python
composite = (85 * 0.27) + (78 * 0.36) + (88 * 0.27) + (80 * 0.10)
          = 22.95 + 28.08 + 23.76 + 8.0
          = 82.79 points
```

**Rating**: Exceptional (82.79/100)  
**해석**: 강한 CANSLIM 후보, 과거 성장 이력에서 약한 부분 존재  
**Weakest Component**: A (78) - 과거 둔화 구간 회복 단계  
**Action**: Buy, 표준 사이징(10-15%)

---

### Example 3: 가상의 "Average" 종목

**Component Scores:**
- **C Score**: 60 points (EPS +20% YoY - 최소 기준 충족)
- **A Score**: 55 points (3yr CAGR 26%, down year 1회)
- **N Score**: 65 points (고점 대비 12%, catalyst 없음)
- **M Score**: 60 points (S&P 500이 EMA 소폭 상회, early uptrend)

**Composite Calculation:**
```python
composite = (60 * 0.27) + (55 * 0.36) + (65 * 0.27) + (60 * 0.10)
          = 16.2 + 19.8 + 17.55 + 6.0
          = 59.55 points
```

**Rating**: Average (59.55/100)  
**해석**: 최소 기준은 충족하나 확신 부족  
**Weakest Component**: A (55) - 성장 이력 일관성 부족  
**Action**: Watchlist only, A 또는 N 개선 대기

---

### Example 4: Bear Market 시나리오 (M Score = 0)

**Component Scores:**
- **C Score**: 100 points (Excellent earnings)
- **A Score**: 90 points (Excellent growth)
- **N Score**: 95 points (신고가)
- **M Score**: 0 points (S&P 500 bear market, VIX > 30)

**Composite Calculation:**
```python
composite = (100 * 0.27) + (90 * 0.36) + (95 * 0.27) + (0 * 0.10)
          = 27.0 + 32.4 + 25.65 + 0
          = 85.05 points
```

**Rating**: 펀더멘털 기준 Exceptional (85.05)이지만 bear market  
**해석**: 점수가 높아도 **DO NOT BUY** - 시장 방향이 종목 품질보다 우선  
**Weakest Component**: M (0) - 시장 환경 악화  
**Action**: 현금 확대, M > 40(시장 회복 신호)까지 대기

**핵심 교훈**: O'Neil 원칙 확인 - "종목에 대해 맞아도 시장에 대해 틀리면 돈을 잃을 수 있다."

---

## Scoring Evolution 히스토리

Phase 3(현재)는 7개 요소 전체에 O'Neil 원본 가중치를 적용합니다. 이전 단계는 미구현 요소를 보정하기 위해 정규화 가중치를 사용했습니다:

- **Phase 1 MVP** (4 components): C 27%, A 36%, N 27%, M 10%
- **Phase 2** (6 components): C 19%, A 25%, N 19%, S 19%, I 13%, M 6%
- **Phase 3** (7 components): C 15%, A 20%, N 15%, S 15%, L 20%, I 10%, M 5% (O'Neil 원본)

---

## 사용 노트

### 스크리너 구현 시

1. 종목별 **7개 요소 점수(C, A, N, S, L, I, M)** 계산
2. Phase 3 가중치로 composite formula 적용
3. 종목별 weakest component 식별
4. composite score 기준으로 정렬(내림차순)
5. **시장 필터 우선 적용**: M score < 40이면 노출 축소 경고

### 사용자 보고서 작성 시

**반드시 포함:**
- composite score (0-100)
- rating (Exceptional / Strong / Above Average / Average / Below Average / Weak)
- 요소별 점수(C, A, N, S, L, I, M)
- weakest component 식별
- 해석 가이드
- 권장 액션(buy / watchlist / avoid)

**형식 예시:**
```
NVDA - NVIDIA Corporation
Composite Score: 95.2 / 100 (Exceptional+)

Component Breakdown:
C (Current Earnings): 100 / 100 - Explosive growth (EPS +429% YoY)
A (Annual Growth): 95 / 100 - Exceptional 3yr CAGR (89%)
N (Newness): 98 / 100 - At new highs with AI catalyst
S (Supply/Demand): 85 / 100 - Strong accumulation pattern
L (Leadership): 92 / 100 - RS Rank 95, sector leader
I (Institutional): 90 / 100 - 6199 holders, 68% ownership
M (Market Direction): 100 / 100 - Strong bull market

Weakest Component: S (85) - Strong accumulation
Recommendation: Strong buy - Rare multi-bagger setup
```

---

## 검증 및 테스트

### 테스트 케이스

알려진 CANSLIM 승자 종목으로 점수 체계를 검증합니다.

**예상 결과 (Phase 1 MVP):**
- NVDA (2023 Q2): 95-100점 (Exceptional)
- META (2023 Q3): 80-90점 (Exceptional/Strong)
- AAPL (2009 Q3): 85-95점 (Exceptional)
- TSLA (2020 Q3): 80-90점 (Exceptional)

**비-CANSLIM 종목 예상 결과:**
- 실적 하락 종목: C < 40 → Composite < 50
- 고점과 먼 종목: N < 40 → Composite < 60
- bear market: M = 0 → 다른 점수와 무관하게 경고 생성

### 점수 시스템 무결성 점검

1. **Range Validation**: 모든 요소 점수는 0-100 범위
2. **Weight Validation**: 가중치 합 = 100% (0.27 + 0.36 + 0.27 + 0.10 = 1.00)
3. **Monotonicity**: 입력 개선 시 점수 상승(선형 또는 step-function)
4. **Boundary Conditions**: 극단 케이스(0 EPS, 음수 성장 등) 테스트
5. **Historical Validation**: 2019-2024 known winners 백테스트

---

이 scoring system은 O'Neil의 완전한 CANSLIM 방법론을 정량적이고 객관적으로 구현하기 위한 프레임워크입니다. Phase 3는 7개 요소를 원본 가중치로 모두 반영하여 성장주 스크리닝의 완결성을 제공합니다.
