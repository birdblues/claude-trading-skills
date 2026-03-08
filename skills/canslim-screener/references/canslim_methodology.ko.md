# CANSLIM Methodology - William O'Neil의 성장주 선별 시스템

## 개요

CANSLIM은 Investor's Business Daily(IBD) 창립자 William O'Neil이 개발한 검증된 성장주 선별 방법론입니다. 1953년부터 현재까지의 최고 수익 종목을 광범위하게 분석해, 대형 상승 전에 multi-bagger 종목이 공통적으로 보이는 7가지 특성을 식별합니다.

**역사적 성과**: IBD 연구에 따르면 CANSLIM 7개 특성을 모두 갖춘 종목은 1-3년 구간에서 평균 100-300% 수익을 기록했으며, 일부는 1,000%를 초과했습니다.

**투자 철학**: CANSLIM은 이미 오른 뒤가 아니라 대형 상승 초입의 신흥 성장 리더를 찾는 데 집중합니다. 확인된 시장 uptrend에서, 짧은 조정/눌림 구간에 고품질 성장주를 매수하는 접근을 강조합니다.

---

## CANSLIM 7개 요소

### C - Current Quarterly Earnings (15% Weight)

**O'Neil Rule**: "현재 분기 EPS가 전년 동기 대비 최소 18-20% 이상 증가한 기업을 찾으라."

#### 중요한 이유

실적은 주가를 움직이는 핵심 펀더멘털 동인입니다. 분기 실적이 가속되는 기업은 사업 모멘텀, 경쟁우위, 경영 실행력을 시사합니다. O'Neil 연구에 따르면 주요 상승 직전 분기에 승자 종목 4개 중 3개가 EPS 70% 이상 성장을 보였습니다.

#### 정량 기준

- **Minimum**: 분기 EPS YoY 18% 이상
- **Preferred**: YoY 25% 이상
- **Exceptional**: YoY 50%+ + 가속 추세

#### 점수 공식 (0-100 Points)

```
100 points: EPS growth >= 50% AND revenue growth >= 25% (explosive acceleration)
 80 points: EPS growth 30-49% AND revenue growth >= 15% (strong growth)
 60 points: EPS growth 18-29% AND revenue growth >= 10% (meets minimum)
 40 points: EPS growth 10-17% (below threshold)
  0 points: EPS growth < 10% or negative
```

#### Revenue 성장 검증

**핵심 점검**: EPS 성장은 revenue 성장으로 뒷받침되어야 합니다. EPS가 revenue보다 과도하게 빠르게 증가하면, 실제 사업 확장보다 비용 절감/자사주 매입/회계 조정 영향인지 확인해야 합니다.

**Red Flag**: EPS 성장 > 30%인데 revenue 성장 < 10%면 지속 가능성 의심.

#### 과거 사례

- **AAPL (2009 Q3)**: EPS +45% YoY (iPhone 3GS), 이후 2년 +200%
- **NFLX (2013 Q1)**: EPS +278% YoY (스트리밍 가속), 18개월 +400%
- **TSLA (2020 Q3)**: EPS 흑자 전환(지속 수익성 시작), 12개월 +700%
- **NVDA (2023 Q2)**: EPS +429% YoY (AI chip 수요), YTD +240%

---

### A - Annual Earnings Growth (20% Weight)

**O'Neil Rule**: "최근 3년 각각 연간 EPS가 25% 이상 증가해야 한다."

#### 중요한 이유

C가 단기 모멘텀을 보여준다면 A는 성장의 지속 가능성을 검증합니다. 한 분기 반짝 종목은 대개 상승이 오래가지 못합니다. 다년간 일관성은 진짜 성장 기업을 일시적/순환적 수혜와 구분합니다.

#### 정량 기준

- **Minimum**: 3년 EPS CAGR 25% 이상
- **Preferred**: 연 30-40% CAGR
- **Exceptional**: 40%+ CAGR + down year 없음

#### 3-Year CAGR 계산

```python
# Compound Annual Growth Rate formula
EPS_CAGR = ((EPS_current / EPS_3_years_ago) ^ (1/3)) - 1

# Example: MSFT 2017-2020
# EPS: $3.25 (2017) → $5.76 (2020)
# CAGR = (5.76 / 3.25) ^ (1/3) - 1 = 21.0%
```

#### 점수 공식 (0-100 Points)

```
90 points: EPS CAGR >= 40% AND stable (no down years) AND revenue CAGR >= 20%
70 points: EPS CAGR 30-39% AND stable
50 points: EPS CAGR 25-29% (meets CANSLIM minimum)
30 points: EPS CAGR 15-24% (below threshold)
 0 points: EPS CAGR < 15% or erratic (down years present)

Bonus: +10 points if all 3 years show year-over-year growth (stability bonus)
Penalty: -20% of score if revenue CAGR < 50% of EPS CAGR (buyback-driven growth)
```

#### 성장 안정성 평가

**Stable Growth (권장)**: 3년 내 매년 EPS 증가
- 예: $1.00 → $1.30 → $1.69 → $2.20 (일관 성장)

**Erratic Growth (패널티)**: 1년 이상 EPS 감소 구간 존재
- 예: $1.00 → $1.50 → $1.20 → $1.80 (변동성 큼)

**O'Neil Insight**: "80% 1년 + 10% 2년보다, 25% 3년 연속이 낫다."

#### Revenue 성장 검증

**건강한 성장**: EPS CAGR과 Revenue CAGR이 모두 강함(격차 10%p 이내)
- 예: EPS 30% + Revenue 25% = 지속 가능

**경고 신호**: EPS CAGR이 Revenue CAGR을 크게 상회(격차 > 15%p)
- 마진 확대/자사주 매입/비용 절감 영향 가능성(지속성 낮음)
- 예: EPS 35% + Revenue 10% = 품질 점검 필요

#### 과거 사례

- **V (2015-2018)**: EPS CAGR 29%, Revenue CAGR 18% → 주가 +180%
- **MA (2014-2017)**: EPS CAGR 33%, Revenue CAGR 14% → 주가 +200%
- **MSFT (2017-2020)**: EPS CAGR 21%, Revenue CAGR 13% → 주가 +280%
- **NVDA (2020-2023)**: EPS CAGR 76%, Revenue CAGR 52% → 주가 +450%

---

### N - New Products, Management, or Highs (15% Weight)

**O'Neil Rule**: "신고가를 만드는 종목은 overhead supply(저항)가 없고 수요가 강하다는 의미다. 새 제품/서비스/경영진은 대형 상승의 촉매가 된다."

#### 중요한 이유

52-week high 근처의 가격 행동은 기관 accumulation과 수요를 시사합니다. 신제품은 실적 catalyst를 만들고, 새 경영진은 전략 전환을 가져옵니다. N은 기술적 모멘텀(신고가)과 펀더멘털 catalyst(새로움)를 결합합니다.

**핵심 인사이트**: CANSLIM 승자 95%는 대형 상승 전에 신고가를 돌파했습니다. 고점과 먼 종목은 저항이 많고 수급 후원이 약합니다.

#### 정량 기준

**가격 위치:**
- **Ideal**: 52-week high 대비 5% 이내
- **Acceptable**: 15% 이내
- **Caution**: 15-25% 하단
- **Avoid**: 25% 초과 하단(모멘텀 부족)

**Breakout Pattern** (보너스):
- 평균 대비 40-50%+ 높은 거래량으로 52-week high 돌파
- 기관 매수 신호

#### 점수 공식 (0-100 Points)

```python
# Distance from 52-week high
distance_pct = ((current_price / week_52_high) - 1) * 100

# Base score from price position
100 points: distance <= 5% from high AND breakout detected AND new product/catalyst
 80 points: distance <= 10% from high AND breakout detected
 60 points: distance <= 15% from high OR breakout detected
 40 points: distance <= 25% from high
 20 points: distance > 25% from high (insufficient momentum)

# Bonus for new product/catalyst signals (from news)
+10-20 points: Keywords detected - "FDA approval", "new product", "patent granted", "breakthrough"
```

#### New Product/Catalyst 감지 (보조)

**고임팩트 촉매:**
- FDA 승인(제약)
- 신규 플랫폼/서비스 출시(테크)
- 특허 취득
- 전략적 인수
- 성공 기업 출신 신규 경영진

**데이터 소스**: 최근 뉴스 제목 keyword 검색(FMP news API)
- "FDA approval" → +20
- "new product", "product launch" → +10
- "acquisition", "expansion" → +10

**참고**: N 점수의 주축은 price action(80%), new product 감지는 보조(20% 보너스)입니다.

#### 과거 사례

**신고가 + 신제품:**
- **AAPL (2007)**: iPhone 출시 + 신고가 → 5년 +600%
- **TSLA (2020)**: Model 3 대량생산 + 신고가 → 12개월 +700%
- **NVDA (2023)**: H100 AI chip 수요 + 신고가 → YTD +240%

**횡보 후 신고가 돌파:**
- **MSFT (2018)**: Azure 성장 + 3년 박스 돌파 → 3년 +350%
- **META (2023)**: AI 효율성 개선 + 2022 하락장 베이스 돌파 → 12개월 +200%

**주의 - 고점과 먼 종목:**
- 고점 대비 30-50% 하단 종목은 차기 상승 주도 가능성이 낮음
- 예외: bear market 깊은 조정 후 reset 가능, 다음 bull market의 신고가 재돌파 확인 필요

---

### M - Market Direction (5% Weight)

**O'Neil Rule**: "종목은 맞고 시장은 틀릴 수 있으며, 그래도 돈을 잃는다. 주식 4개 중 3개는 시장 추세를 따른다."

#### 중요한 이유

CANSLIM은 bear market에서 잘 작동하지 않습니다. 최고의 성장주도 지속 하락장에서 20-50% 하락할 수 있습니다. O'Neil 연구:
- **Bull markets**: 종목 75%가 시장 방향 동조
- **Bear markets**: 종목 선별만으로 수익 내기 매우 어려움
- **시장 타이밍**: 조정기 현금 보유가 다음 bull phase 준비에 유리

**핵심 인사이트**: "가장 중요한 결정은 무엇을 살지보다, 지금 투자 상태여야 하는지 여부다."

#### 정량 기준

**Primary Signal**: S&P 500 vs 50-day EMA
- **Uptrend**: S&P 500이 50-day EMA 위에서 3일+ 마감
- **Choppy/Neutral**: 50-day EMA 주변(±2%) 진동
- **Downtrend**: 50-day EMA 아래 3일+ 마감

**Secondary Signal**: VIX
- **Low Fear**: VIX < 15
- **Normal**: VIX 15-20
- **Elevated**: VIX 20-30
- **Panic**: VIX > 30 (매도/현금 신호)

#### 점수 공식 (0-100 Points)

```python
# Calculate distance from 50-day EMA
distance_from_ema = (sp500_price / sp500_ema_50) - 1

# Market trend scoring
100 points: sp500 > EMA by 2%+ AND VIX < 15 AND follow-through day detected
 80 points: sp500 > EMA by 1-2% AND VIX < 20
 60 points: sp500 > EMA by 0-1% (early uptrend)
 40 points: sp500 within ±2% of EMA (choppy, neutral)
 20 points: sp500 < EMA by 1-3% (early downtrend)
  0 points: sp500 < EMA by 3%+ OR VIX > 30 (bear market - DO NOT BUY)
```

#### Follow-Through Day (FTD) - O'Neil식 bull market 확인

**정의**: 조정 이후 반등 시도 Day 4-10에, 주요 지수(S&P 500/Nasdaq)가 전일 대비 거래량 증가를 동반해 1.25%+ 상승하는 날.

**의미**:
- 기관 매수가 재개됐음을 시사
- 시장 바닥 형성 과정 완료 신호
- 리더 성장주 매수의 Green Light

**FTD 부재 시**: 반등 시도가 실패할 가능성이 높아 조기 진입 손실 가능성 증가

#### 시장 방향 해석

**100점 (Strong Uptrend)**:
- S&P 500이 50-day EMA를 충분히 상회
- VIX 낮음
- FTD 확인
- **Action**: 리더 성장주(CANSLIM 후보) 공격적 매수

**60점 (Early Uptrend)**:
- S&P 500이 EMA를 막 상향 돌파
- 추세 확립 초기
- **Action**: 소규모 포지션으로 시작(25-50% allocation)

**40점 (Choppy/Neutral)**:
- EMA 주변 등락
- 방향 불명확
- **Action**: 노출 25-50%로 축소, 확인 대기

**0점 (Downtrend/Bear Market)**:
- EMA 아래 하락 추세
- VIX 상승/급등
- **Action**: 주식 전량 정리, 현금 80-100%, FTD 대기

#### 과거 사례

**Bull market phases (M 80-100):**
- 2009-2011: 금융위기 후 회복(AAPL, PCLN)
- 2013-2015: QE rally(NFLX, FB)
- 2016-2018: 감세 랠리(NVDA, AMD, FANG)
- 2020-2021: 팬데믹 회복(TSLA, NVDA)
- 2023-2024: AI boom(NVDA, META, MAG7)

**Bear market phases (M 0-20):**
- 2008: 금융위기(최우량도 40-60% 하락)
- 2011: 부채한도 위기(20% 조정)
- 2015-2016: 중국 절하(성장주 20-30% 하락)
- 2018: 긴축기(Nasdaq -23%)
- 2022: 인플레/긴축(Nasdaq -33%, 성장주 -50~80%)

**핵심 요약**: bear market(M < 20)에서는 펀더멘털이 좋아도 하락할 수 있습니다. 시장 방향이 종목 선별보다 우선합니다.

---

### S - Supply and Demand (15% Weight)

**O'Neil Rule**: "거래량은 주가 상승의 연료다. 연료가 없으면 차는 가지 않는다. 상승일 volume이 늘고 하락일 volume이 줄어드는 종목을 찾아라."

#### 중요한 이유

거래량 패턴은 기관 accumulation(매수)과 distribution(매도)을 드러냅니다. 개인은 소량 거래하지만 기관은 대량을 움직입니다. 기관 accumulation 시 상승일 거래량이 급증하고, distribution 시 하락일 거래량이 급증합니다. 즉, 거래량은 가격보다 선행할 때가 많습니다.

**핵심 원칙**: UP-DAY VOLUME > DOWN-DAY VOLUME = Accumulation (bullish)

#### 정량 기준

**Accumulation/Distribution 분석** (60일):
- 각 거래일을 up-day(close > prev close), down-day(close < prev close)로 분류
- up-day 평균 volume vs down-day 평균 volume 계산
- **Accumulation Ratio** = Avg Up-Day Volume / Avg Down-Day Volume

**Thresholds:**
- **Strong Accumulation**: Ratio ≥ 2.0
- **Accumulation**: Ratio 1.5-2.0
- **Neutral**: Ratio 1.0-1.5
- **Distribution**: Ratio 0.5-0.7
- **Strong Distribution**: Ratio < 0.5

#### 점수 공식 (0-100 Points)

```python
# Calculate accumulation/distribution ratio
up_days_volume = [volume for day in last_60_days if close > prev_close]
down_days_volume = [volume for day in last_60_days if close < prev_close]

avg_up_volume = sum(up_days_volume) / len(up_days_volume)
avg_down_volume = sum(down_days_volume) / len(down_days_volume)

ratio = avg_up_volume / avg_down_volume

# Scoring
100 points: ratio >= 2.0 (Strong Accumulation)
 80 points: ratio 1.5-2.0 (Accumulation)
 60 points: ratio 1.0-1.5 (Neutral/Weak Accumulation)
 40 points: ratio 0.7-1.0 (Neutral/Weak Distribution)
 20 points: ratio 0.5-0.7 (Distribution)
  0 points: ratio < 0.5 (Strong Distribution)
```

#### 과거 사례

- **NVDA (2023)**: Up/Down ratio 2.3, 이후 +500%
- **META (2023)**: ratio 1.8, 2022 저점 회복 구간
- **TSLA (2019-2020)**: ratio 2.1, Model 3 램프업
- **AAPL (2019)**: ratio 1.7, iPhone 11 cycle 전

**Red Flag**: ratio < 0.7이면 distribution 신호로, 회피 또는 청산 고려.

---

### I - Institutional Sponsorship (10% Weight)

**O'Neil Rule**: "큰손을 우리 편에 두어야 한다. 기관 보유가 증가하는 종목을 찾되 과도하면 안 된다. 이상적인 구간은 기관 holder 50-100개, ownership 30-60%다."

#### 중요한 이유

기관 투자자(뮤추얼펀드, 연기금, 헤지펀드)는 리서치 역량, 긴 투자 기간, 대규모 자본을 보유합니다. 이들의 sponsorship은 다음을 제공합니다:
1. **Liquidity**: 과도한 slippage 없이 거래 가능
2. **Price Support**: 조정 시 대형 보유자의 방어 매수 가능
3. **Discovery**: 추가 기관/개인 자금 유입 촉진
4. **Validation**: smart money가 투자 가설을 확인

**핵심 인사이트**: 기관 보유가 너무 낮으면(<20%) 소외 종목일 수 있고, 너무 높으면(>80%) 이미 매수 여력이 소진됐을 수 있습니다.

#### 정량 기준

**Holder Count**:
- **Sweet Spot**: 50-100 기관
- **Good**: 30-50 (관심 증가 단계)
- **Acceptable**: 100-150 (다소 혼잡)
- **Avoid**: <30(과소 보유) 또는 >150(과밀)

**Ownership Percentage**:
- **Ideal**: 30-60%
- **Acceptable**: 20-30% 또는 60-80%
- **Caution**: <20%(소외) 또는 >80%(포화)

**Quality Signal (보너스)**: Superinvestor 보유
- Berkshire Hathaway, Baupost Group, Pershing Square, Greenlight Capital, Third Point, Appaloosa Management 등

#### 점수 공식 (0-100 Points)

```python
# Calculate institutional ownership %
total_shares_held = sum(holder.shares for holder in institutional_holders)
ownership_pct = (total_shares_held / shares_outstanding) * 100

# Scoring logic
if 50 <= num_holders <= 100 and 30 <= ownership_pct <= 60:
    score = 100  # O'Neil's sweet spot

elif superinvestor_present and 30 <= num_holders <= 150:
    score = 90  # Superinvestor quality signal

elif (30 <= num_holders < 50 and 20 <= ownership_pct <= 40) or \
     (100 < num_holders <= 150 and 40 <= ownership_pct <= 70):
    score = 80  # Good ranges

elif (20 <= num_holders < 30 and 20 <= ownership_pct <= 50) or \
     (50 <= num_holders <= 150 and 20 <= ownership_pct <= 70):
    score = 60  # Acceptable

elif ownership_pct < 20 or ownership_pct > 80:
    score = 40  # Suboptimal ownership

elif ownership_pct < 10 or ownership_pct > 90:
    score = 20  # Extreme ownership (avoid)

else:
    score = 50  # Default

# Superinvestor bonus
if superinvestor_present and score < 100:
    score = min(score + 10, 100)
```

#### 해석

**100점 (Ideal)**:
- 50-100 holders, ownership 30-60%
- **Action**: 이상적 기관 수급, 높은 신뢰로 진행 가능

**90점 (Quality Signal)**:
- Superinvestor 보유 + 양호한 holder 수
- **Action**: 질 높은 투자자 보유가 안전마진 제공

**60점 (Acceptable)**:
- 기관 관심은 있으나 최적 아님
- **Action**: 신중 접근, 변화 모니터링

**40점 (Suboptimal)**:
- 과소(<20%) 또는 과밀(>80%)
- **Action**: 왜 기관이 회피/포화인지 점검

**20점 (Avoid)**:
- 극단 ownership(<10% 또는 >90%)
- **Action**: 회피 - 소외 또는 추가 매수 여력 부족

#### 과거 사례

- **NVDA (2023 Q2)**: 74 holders, 44% ownership → YTD +240%
- **META (2023 Q1)**: 68 holders, 51% ownership → +194%
- **TSLA (2020)**: 35 → 89 holders 증가 구간에서 +700%
- **AAPL (2019)**: Berkshire Hathaway 보유(quality signal)

**경고**: >150 holders + >80% ownership 종목은 약세 구간에서 매도 압력이 커져 underperform할 수 있습니다.

---

## Phase 2 구현 노트

Phase 2는 **C, A, N, S, I, M**을 포함해 CANSLIM 전체 가중치의 80%를 다룹니다. Phase 1 대비 핵심 2요소가 추가됩니다:

1. **S (Supply/Demand)**: 거래량 기반 accumulation/distribution - 기관 매수/매도 추적
2. **I (Institutional Sponsorship)**: holder 수/ownership % - smart money backing 검증

**Phase 1 대비 개선점:**
- 필터 정확도 향상: S로 distribution 종목 제거
- 품질 검증 강화: I로 투자 가설 확인
- 랭킹 개선: 펀더멘털 + 기관 수급 동시 강한 종목 상위 배치
- API 효율: 40종목 기준 약 203 calls(Free tier의 81%)

### Component Weights (Phase 2 - Renormalized)

| Component | Original Weight | Phase 2 Weight | Rationale |
|-----------|-----------------|----------------|-----------|
| C - Current Earnings | 15% | **19%** | 분기 실적 모멘텀 |
| A - Annual Growth | 20% | **25%** | 지속 성장 검증 |
| N - Newness | 15% | **19%** | 모멘텀 확인 |
| S - Supply/Demand | 15% | **19%** | 기관 accumulation 신호 |
| I - Institutional | 10% | **13%** | smart money 검증 |
| M - Market Direction | 5% | **6%** | gating filter |
| **Subtotal (Phase 2)** | **80%** | **100%** | L 제외 후 100%로 정규화 |

**Future Phases:**
- **Phase 3**: L(Leadership/RS Rank) 추가 → 100% complete
- **Phase 4**: FINVIZ Elite 통합 → 속도 10배 향상

### Phase 2 점수 해석

Phase 2는 7개 중 6개(80% weight)를 구현해 Phase 1보다 실무 예측력이 크게 높습니다:

- **90-100**: Exceptional+ (기관 수급 포함 rare multi-bagger)
- **80-89**: Exceptional (우수 펀더멘털 + accumulation)
- **70-79**: Strong (고품질 CANSLIM)
- **60-69**: Above Average (Watchlist, 개선 모니터링)
- **<60**: CANSLIM 기준 미달

**Minimum Thresholds (Phase 2):**
6개 요소 baseline 충족 필요:
- C ≥ 60 (분기 EPS +18%+)
- A ≥ 50 (연 EPS CAGR +25%+)
- N ≥ 40 (52-week high 대비 15% 이내)
- S ≥ 40 (accumulation pattern, ratio ≥ 1.0)
- I ≥ 40 (30+ holders OR 20%+ ownership)
- M ≥ 40 (시장 uptrend)

**Phase 1 대비 핵심 차이**: S/I가 반영되어 false positive를 줄입니다. C/A가 좋아도 S < 40(distribution)이면 낮은 점수를 받습니다.

---

## 투자 철학 및 Best Practices

### CANSLIM이 잘 작동하는 환경

1. **Confirmed Bull Market**: S&P 500이 50-day/200-day MA 위
2. **성장주 우호 환경**: 저금리, 경기 확장, 혁신 사이클
3. **성장 섹터 로테이션**: Technology/Healthcare/Consumer Discretionary 리딩
4. **양호한 Market Breadth**: 다수 종목이 uptrend(200-day MA 위 >50%)

### CANSLIM을 피해야 할 환경

1. **Bear Market**: 주요 지수 200-day MA 아래, VIX > 30
2. **Value 우위 시장**: 고인플레/금리상승 국면
3. **방어 섹터 로테이션**: Utilities/Consumer Staples/REITs 리딩
4. **악화된 Breadth**: 하락 추세 종목 다수

### 포지션 관리 규칙

**Entry:**
- 80+ (Phase 1) 또는 140+ (Full CANSLIM) 종목 매수
- 10-week MA 눌림목 진입 선호
- 종목당 10-20%, 총 5-10개 포지션

**Stops:**
- 초기 stop loss: 진입가 -7~8% (엄격 규칙)
- +15% 수익 시 stop을 breakeven으로 상향
- 상승 진행 시 peak 대비 -10~15% trailing stop

**Profit Taking:**
- +20~25%: 포지션 20-25% 매도
- +50%: 추가 20-25% 매도
- 최종 50%는 Stage 2 uptrend 유지 시 보유

**Sell Signals:**
1. stop loss 도달(-7~8%) 즉시 매도
2. 시장 조정 진입(M 0-20)
3. 펀더멘털 악화(C/A < 40)
4. climax top(급등 + 과대 거래량 후 반전)
5. distribution(하락일 대량 거래)

---

## 흔한 실수와 방지법

### Mistake 1: M Component 무시

**오류**: "펀더멘털 좋으니 bear market에서도 사도 된다"

**현실**: 종목 75%는 시장 방향을 따릅니다. 완벽한 CANSLIM 종목도 하락장에서는 20-50% 하락할 수 있습니다.

**해결:**
- 개별 종목 전에 M을 먼저 확인
- M < 40이면 현금 80-100% 유지
- "종목이 맞아도 시장이 틀리면 손실"

### Mistake 2: 고점과 먼 종목 추격

**오류**: "고점 대비 30-50% 하락했으니 싸다"

**현실**: 고점과 먼 종목은 기관 sponsorship 부족 + overhead resistance 부담

**해결:**
- N component 중심: 52-week high 대비 15% 이내 선호
- 적절한 base breakout(최소 7-8주) 확인 후 진입
- "이전 상승장의 리더가 다음 상승장의 리더가 아닐 수 있다"

### Mistake 3: C 과대평가, A 무시

**오류**: 분기 급성장(C)만 보고 다년 성장(A) 불안정 종목 매수

**현실**: 반짝 실적은 되돌림 가능성 큼. 장기 승자는 다년 일관 성장.

**해결:**
- C >= 60, A >= 50 동시 충족 요구
- A를 C의 검증 수단으로 사용
- "장기 복리는 변동성보다 일관성이 유리"

### Mistake 4: 손절 지연

**오류**: "손실 포지션도 버티면 돌아온다"

**현실**: 작은 손실이 큰 손실로 확대됩니다. O'Neil 연구에서 손실의 대부분은 조기 손절 실패에서 발생.

**해결:**
- 진입 시점에 stop 설정(-7~8%)
- 예외 없이 stop 도달 즉시 실행
- "첫 손실이 가장 작은 손실"

---

## 결론

CANSLIM은 대형 상승 전에 신흥 성장 리더를 식별하기 위한 검증된 정량 방법론입니다. 펀더멘털(C, A)과 기술 확인(N, M)을 결합해, 기관 수급과 모멘텀이 동반된 종목을 선별합니다.

**Phase 1 MVP (C, A, N, M)**는 다음 조건 종목을 즉시 필터링해 실무 가치를 제공합니다:
- 분기 실적 가속(C)
- 다년 일관 성장(A)
- 신고가 근접 모멘텀(N)
- 시장 uptrend 확인(M)

**향후 단계**에서는 공급/수요(S), 기관 sponsorship(I), 상대강도 리더십(L)을 추가해 O'Neil 시스템 완전 구현으로 확장됩니다.

**기억할 점**: CANSLIM은 확인된 bull market에서 가장 효과적입니다. bear market에서는 현금 비중을 높이고, 기관 매수 재개를 확인하는 다음 follow-through day를 기다리는 것이 우선입니다.

---

## 참고 문헌

- **"How to Make Money in Stocks"** by William J. O'Neil (4th Edition, 2009)
- **"The Successful Investor"** by William J. O'Neil (2004)
- **IBD (Investor's Business Daily)** - 일일 CANSLIM 스크린 및 시장 분석
- **MarketSmith** - IBD의 기관급 분석 플랫폼(공식 RS Ranks 제공)
- **Historical Studies**: 1953-2008 승자 600+ 종목에 대한 IBD 검증 연구
