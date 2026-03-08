# Uptrend Analyzer 방법론

## 데이터 소스: Monty's Uptrend Ratio Dashboard

Monty's Uptrend Ratio Dashboard는 11개 GICS 섹터 전반의 미국 주식 약 2,800개를 추적합니다. 각 종목이 아래 기준에 따라 "uptrend" 상태인지 판별합니다. 대시보드는 GitHub에 일일 CSV 데이터를 게시합니다.

**GitHub Repository:** `tradermonty/uptrend-dashboard`
**Live Dashboard:** https://uptrend-dashboard.streamlit.app/

### Uptrend 정의 (Finviz Elite Screener)

아래 조건을 **모두** 만족할 때 종목을 "uptrend"로 분류합니다:

| 조건 | 설명 |
|-----------|-------------|
| Price > $10 | 페니주 제외 |
| Avg Volume > 100K | 충분한 유동성 |
| Market Cap > $50M | 마이크로캡 이상 |
| Price > SMA20 | 단기 상승추세 |
| Price > SMA200 | 장기 상승추세 |
| SMA50 > SMA200 | 골든크로스(강세 구조) |
| 52W High/Low > 30% above Low | 저점 대비 회복 |
| 4-Week Performance: Up | 최근 모멘텀 양호 |

**uptrend ratio** = (모든 조건을 만족한 종목 수) / (기본 필터(가격, 거래량, 시가총액) 충족 종목 수).

### CSV 파일

| 파일 | 설명 | 업데이트 주기 |
|------|-------------|------------------|
| `uptrend_ratio_timeseries.csv` | "all" + 11개 섹터의 일일 ratio | Daily |
| `sector_summary.csv` | 전체 섹터 최신 스냅샷 | Daily |

**데이터 가용성:**
- "all"(전체 시장): 2023-08-11부터
- 섹터 레벨 데이터: 2024-07-21부터

### Timeseries 컬럼

| 컬럼 | 타입 | 설명 |
|--------|------|-------------|
| worksheet | string | "all" 또는 섹터 slug (예: "sec_technology") |
| date | string | YYYY-MM-DD 형식 |
| count | int | uptrend 종목 수 |
| total | int | 추적 종목 수 |
| ratio | float | count/total (0-1 스케일, raw decimal) |
| ma_10 | float | ratio의 10일 단순이동평균 |
| slope | float | ma_10의 1일 차분 (`ma_10.diff()`) |
| trend | string | "up" (slope > 0) 또는 "down" (slope <= 0) |

### Sector Summary 컬럼

| 컬럼 | 타입 | 설명 |
|--------|------|-------------|
| Sector | string | 표시 이름 (예: "Technology") |
| Ratio | float | 현재 uptrend ratio (0-1) |
| 10MA | float | ratio의 10일 MA |
| Trend | string | "Up" 또는 "Down" |
| Slope | float | MA의 1일 차분 |
| Status | string | "Overbought", "Oversold", 또는 "Normal" |

### 지표 계산식 (source code 기준)

모든 지표는 raw count/total 데이터에서 실시간 계산됩니다:

```
ratio    = count / total
ma_10    = ratio.rolling(10).mean()       # 10-day simple MA
slope    = ma_10.diff()                   # 1-day change of MA
trend    = "up" if slope > 0 else "down"
```

**Peak/Trough 탐지:** 대시보드는 `scipy.signal.find_peaks`를 `distance=20, prominence=0.015` 파라미터로 사용해 10MA 시계열의 국소 고점/저점을 식별합니다.

---

## 공식 대시보드 임계값

이 임계값은 원본 저장소의 `src/constants.py`에 정의되어 있습니다:

| 임계값 | 값 | 의미 |
|-----------|-------|---------|
| **상단 (Overbought)** | **37%** | ratio가 이를 초과하면 overbought 조건 |
| **하단 (Oversold)** | **9.7%** | ratio가 이보다 낮으면 oversold / crisis |
| MA 기간 | 10 | 단순이동평균 윈도우 |

### 상태 판정

```
ratio > 0.37  -> "Overbought"
ratio < 0.097 -> "Oversold"
otherwise     -> "Normal"
```

### 실무 해석

| Ratio | 해석 | 시장 환경 |
|-------|---------------|-------------------|
| 50%+ | 강한 breadth | 광범위한 bull market, 다수 종목 참여 |
| 37-50% | Overbought / Healthy | 상단 임계값 위, 강하지만 과열 가능 |
| 25-37% | Normal / Recovering | 임계값 사이, 전형적 거래 범위 |
| 9.7-25% | Weak | 정상 이하, breadth 악화 |
| < 9.7% | Oversold / Crisis | 하단 임계값 아래, 극단적 매도 |

---

## 5-구성요소 점수 체계

### 구성요소 1: Market Breadth (Overall) - 가중치: 30%

**근거:** 전체 uptrend ratio는 시장 건전성의 가장 중요한 단일 지표입니다. ratio가 높으면 참여가 넓고, 낮으면 시장이 좁고 취약합니다.

**점수 구간(대시보드 임계값 정렬):**

| Ratio | 점수 범위 | 신호 |
|-------|-------------|--------|
| >= 50% | 90-100 | Strong Bull |
| 37-50% | 70-89 | Bullish (overbought 임계값 상회) |
| 25-37% | 40-69 | Neutral/Recovering |
| 9.7-25% | 10-39 | Weak (임계값 사이) |
| < 9.7% | 0-9 | Crisis (oversold 임계값 하회) |

**추세 조정:** trend="up" 이고 slope>0이면 +5, trend="down" 이고 slope<0이면 -5.

### 구성요소 2: Sector Participation - 가중치: 25%

**근거:** 건전한 시장은 대부분 섹터가 함께 참여합니다. 2-3개 섹터만 주도하면 시장은 취약하고 섹터 로테이션 충격에 취약합니다.

**하위 점수:**
- **Uptrend Count (60%):** uptrend 섹터 수를 0-100으로 매핑
- **Spread (40%):** max-min ratio spread. 좁을수록 참여 균일(긍정), 넓을수록 선택적 시장(리스크).

**Overbought/Oversold 분류는 대시보드 임계값 사용:** >37% = Overbought, <9.7% = Oversold.

### 구성요소 3: Sector Rotation - 가중치: 15%

**근거:** 건전한 bull market에서는 경기민감(Cyclical) 섹터가 방어(Defensive) 섹터를 주도합니다. 방어 섹터가 주도하면 risk-off 행동 신호입니다.

**섹터 분류:**

| 그룹 | 섹터 |
|-------|---------|
| Cyclical | Technology, Consumer Cyclical, Communication Services, Financial, Industrials |
| Defensive | Utilities, Consumer Defensive, Healthcare, Real Estate |
| Commodity | Energy, Basic Materials |

**점수화:** cyclical_avg - defensive_avg 차이에 기반.
- Cyclical lead > +15pp = Strong risk-on (90-100)
- +/-5pp 이내 균형 = Neutral (45-69)
- Defensive lead > +15pp = Strong risk-off (0-19)

**Commodity 조정:** Commodity 섹터가 Cyclical/Defensive를 모두 상회하면 late-cycle 가능성을 시사합니다. -5~-10 패널티를 적용합니다.

**그룹 내 분산(Divergence) 탐지:** Cyclical/Defensive 그룹 내부에서 큰 분산을 탐지합니다. 아래 중 하나라도 충족하면 divergence flag를 트리거합니다:
- 그룹 내부 표준편차 > 8 percentage points
- 그룹 내부 max-min spread > 20 percentage points
- 그룹 다수 추세와 반대 방향인 섹터가 1개 이상

Divergence가 감지되면 구성요소 3 점수에 -5 패널티를 적용합니다. 이는 그룹 평균이 내부 불일치를 가리는 문제(예: 다른 Cyclical은 상승인데 Financial만 하락)를 방지합니다.

> **참고 (이중 레이어 패널티):** Divergence는 두 단계에서 패널티를 유발합니다.
> (1) 구성요소 3 점수에 -5(로테이션 점수 현실화),
> (2) 복합 점수에 -3(아래 Warning System 참조, 익스포저 가이던스 강화 트리거).
> 복합 점수 순영향 ≈ 5 × 0.15 (가중치) + 3 = **3.75 points**.

### 구성요소 4: Momentum - 가중치: 20%

**근거:** breadth의 수준만큼 방향과 변화율이 중요합니다. breadth 개선(양의 slope, 가속)은 환경 개선을, breadth 악화는 주의를 시사합니다.

**하위 점수:**
- **Slope Score (50%):** 스무딩 slope(EMA-3)를 0-100으로 매핑(일반 범위: -0.02 ~ +0.02). raw 1일 slope(`ma_10.diff()`)를 3기간 Exponential Moving Average로 스무딩해 일간 노이즈를 줄입니다.
- **Acceleration (30%):** 최근 10포인트 스무딩 slope 평균 vs 직전 10포인트 평균(10v10 윈도우). 데이터가 20포인트 미만이면 5v5로 대체.
- **Sector Slope Breadth (20%):** 양(+)의 slope를 가진 섹터 수

**모멘텀 스무딩:** Monty 대시보드의 raw slope 신호는 10일 이동평균의 1일 차분이므로 본질적으로 노이즈가 있습니다. EMA(3) 스무딩은 방향성은 유지하면서 단일 일자 변동을 줄입니다. 투명성을 위해 raw/smoothed slope를 모두 보고합니다.

### 구성요소 5: Historical Context - 가중치: 10%

**근거:** 현재 ratio가 과거 분포에서 어느 위치인지 알면 맥락 파악에 도움이 됩니다. 현재 값이 낮아 보여도 역사적으로는 평균일 수 있고, 그 반대도 가능합니다.

**점수화:** 전체 과거 분포(2023년 8월~현재)에서 현재 ratio의 percentile rank.

**참고:** "all" 데이터는 2023-08-11부터(~650+ 데이터 포인트), 섹터 데이터는 2024-07-21부터(각 ~370+ 데이터 포인트).

**신뢰도 평가:** 과거 데이터셋이 제한적(~650 포인트)이므로, 시스템은 percentile 분석 신뢰도를 평가/보고합니다:

| 요소 | 기준 | 점수 |
|--------|----------|-------|
| **샘플 크기** | >=1000: full (3), 500-999: moderate (2), 200-499: limited (1), <200: minimal (0) | 0-3 |
| **Regime Coverage** | bear 데이터(min<10%)와 bull 데이터(max>40%) 모두 있음: Both (2), 하나만: Partial (1), 둘 다 없음: Narrow (0) | 0-2 |
| **Recency Bias** | 최근 90일 범위가 전체 범위의 >=30%: balanced (1), 그 외: biased (0) | 0-1 |

총점 5-6 = High, 3-4 = Moderate, 1-2 = Low, 0 = Very Low confidence.

신뢰도가 Low 또는 Very Low이면 signal 텍스트에 `[confidence: Low]` 경고를 포함합니다.

---

## 점수 구간과 익스포저 가이던스

### 5-레벨 Zone (하위호환)

| 점수 | Zone | Exposure | 설명 |
|-------|------|----------|-------------|
| 80-100 | Strong Bull | Full (100%) | 광범위한 참여, 강한 모멘텀. 공격적 포지셔닝에 적합. |
| 60-79 | Bull | Normal (80-100%) | 건강한 breadth. 표준 포지션 관리. |
| 40-59 | Neutral | Reduced (60-80%) | 신호 혼재. 선택적 참여. |
| 20-39 | Cautious | Defensive (30-60%) | 약한 breadth. 자본 보존 우선. |
| 0-19 | Bear | Preservation (0-30%) | 심각한 악화. 최대 방어. |

### 7-레벨 Zone 상세

`zone_detail` 필드는 Bull/Cautious 구간을 분할해 더 세밀한 구분을 제공합니다:

| 점수 | Zone (5-level) | Zone Detail (7-level) | Exposure Range |
|-------|----------------|----------------------|----------------|
| 80-100 | Strong Bull | Strong Bull | 100% |
| 70-79 | Bull | Bull-Upper | 90-100% |
| 60-69 | Bull | Bull-Lower | 80-90% |
| 40-59 | Neutral | Neutral | 60-80% |
| 30-39 | Cautious | Cautious-Upper | 45-60% |
| 20-29 | Cautious | Cautious-Lower | 30-45% |
| 0-19 | Bear | Bear | 0-30% |

**이유:** 기존 Bull 구간(60-79)이 너무 넓었습니다. 66점과 78점이 모두 "Bull"로 표시되지만 익스포저 수준은 달라야 합니다. Bull-Lower는 Bull-Upper 대비 더 보수적 신호입니다.

### Zone 경계 근접 지표

복합 점수가 zone 경계(20, 40, 60, 80)에서 10포인트 이내이면 `zone_proximity` 필드가 `at_boundary=True`와 거리/방향 정보를 표시합니다. 작은 점수 변화로 zone 분류가 바뀔 수 있음을 경고합니다.

---

## Warning 시스템

### 구성요소 레벨 Warning

Warning은 복합 점수가 시장 건전성을 과대평가할 수 있는 상황을 탐지합니다:

| Warning | 트리거 | Composite Penalty | 근거 |
|---------|---------|-------------------|-----------|
| **Late Cycle** | Commodity 평균 > Cyclical/Defensive 그룹 평균 모두 | -5 | Commodity 주도는 광범위한 시장 약세에 선행하는 경우가 많음 |
| **High Spread** | max-min 섹터 ratio spread > 40pp | -3 | 넓은 spread는 평균에 가려진 리더십 집중을 시사 |
| **Divergence** | 그룹 내 std > 8pp, spread > 20pp, 또는 trend dissenters | -3 | 그룹 평균이 내부 불일치를 숨김(구성요소 3 점수에도 -5) |

### Multi-Warning Discount

동시에 2개 이상 warning이 활성화되면, warning 조건 간 상관관계를 고려해 총 penalty를 1포인트 줄입니다.

**예시:** Late Cycle (-5) + High Spread (-3) = -8 + discount (+1) = **총 -7 penalty**

### Warning의 가이던스 영향

Bull 또는 Strong Bull zone에서 warning이 활성화되면:
- 익스포저 가이던스를 더 보수적으로 조정(예: "Normal Exposure (80-100%)" 대신 "Normal Exposure, Lower End (80-90%)")
- 가이던스 텍스트에 점수와 warning 간 긴장을 명시
- 권장 액션 목록 앞에 warning 대응 액션을 우선 배치

투명성을 위해 penalty 적용 전 raw score는 `composite_score_raw`로 보존합니다.

---

## 가중치 근거

| 구성요소 | 가중치 | 근거 |
|-----------|--------|-----------|
| Market Breadth | 30% | 시장 건전성을 가장 직접적으로 측정 |
| Sector Participation | 25% | 섹터 참여 breadth는 지속성에 핵심 |
| Momentum | 20% | 수준만큼 방향이 중요 |
| Sector Rotation | 15% | 로테이션 신호는 중요한 risk-on/off 맥락 제공 |
| Historical Context | 10% | 맥락은 제공하지만 실시간 신호보다 실행성은 낮음 |

---

## 한계

1. **데이터 히스토리:** "all" 데이터는 2023년 8월, 섹터 데이터는 2024년 7월부터 시작. 장기 percentile 분석에 제약이 있습니다. confidence indicator가 이 한계를 정량화합니다.
2. **단일 소스:** Monty 대시보드(Finviz Elite 데이터)에 전적으로 의존하며, 다른 breadth 지표와 교차검증이 없습니다.
3. **거래량 데이터 부재:** Uptrend ratio는 가격 기반이며 거래량 확인이 없습니다.
4. **후행성:** 10일 이동평균과 slope는 본질적 지연을 가집니다. EMA(3) 스무딩은 추가 지연이 미미하지만 노이즈를 줄입니다.
5. **미국 한정:** 미국 주식만 포함, 해외 시장 breadth는 미포함.
6. **섹터 분류:** 고정 GICS 섹터를 사용하며 모든 로테이션 동학을 포착하지 못할 수 있습니다.
7. **Finviz 의존성:** 상위 데이터는 Finviz Elite 가용성과 스크리너 정확도에 의존합니다.

---

## 보완 분석

이 스킬은 아래와 함께 사용할 때 가장 효과적입니다:
- **Market Top Detector:** 분산일(distribution day) 및 리더십 악화 신호 확인
- **Technical Analyst:** 지수 차트 레벨 확인
- **Sector Analyst:** 섹터 로테이션 정밀 분석
- **Market News Analyst:** 펀더멘털 촉매 맥락 보강
