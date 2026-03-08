---
name: us-market-bubble-detector
description: 개정된 Minsky/Kindleberger framework v2.1을 사용해 정량 데이터 기반으로 시장 버블 리스크를 평가합니다. 주관적 인상보다 객관적 지표(Put/Call, VIX, margin debt, breadth, IPO 데이터)를 우선합니다. 확증 편향 방지를 포함한 엄격한 정성 조정 기준을 적용합니다. 필수 데이터 수집과 기계적 스코어링으로 실전 투자 의사결정을 지원합니다. 사용자가 버블 리스크, 밸류에이션 우려, 수익 실현 타이밍을 물을 때 사용하세요.
---

# US Market Bubble Detection Skill (개정 v2.1)

## v2.1 핵심 개정 사항

**v2.0 대비 치명적 변경:**
1. ✅ **필수 정량 데이터 수집** - 인상이나 추측이 아니라 측정값 사용
2. ✅ **명확한 임계값 설정** - 각 지표별 구체적인 수치 기준
3. ✅ **2단계 평가 프로세스** - 정량 평가 → 정성 조정 (엄격한 순서)
4. ✅ **더 엄격한 정성 기준** - 최대 +3점 (기존 +5에서 축소), 측정 가능한 증거 필요
5. ✅ **확증 편향 방지** - 과대 점수화를 피하기 위한 명시적 체크리스트
6. ✅ **세분화된 리스크 단계** - 정교한 리스크 관리를 위해 "Elevated Risk" 단계(8-9점) 추가

---

## 이 스킬을 사용할 때

다음 상황에서 이 스킬을 사용합니다:

**English:**
- User asks "Is the market in a bubble?" or "Are we in a bubble?"
- User seeks advice on profit-taking, new entry timing, or short-selling decisions
- User reports social phenomena (non-investors entering, media frenzy, IPO flood)
- User mentions narratives like "this time is different" or "revolutionary technology" becoming mainstream
- User consults about risk management for existing positions

**Korean:**
- 사용자가 "지금 시장이 버블인가?"라고 질문
- 투자 수익 실현·신규 진입·공매도 타이밍 판단을 요청
- 사회 현상(비투자자의 진입, 미디어 과열, IPO 범람)을 관찰하고 우려를 표명
- "이번에는 다르다" "혁명적 기술" 등의 내러티브가 주류화되는 상황을 보고
- 보유 포지션의 리스크 관리 방법을 상담

---

## 평가 프로세스 (엄격한 순서)

### Phase 1: 필수 정량 데이터 수집

**CRITICAL: 평가를 시작하기 전에 반드시 다음 데이터를 수집하세요**

#### 1.1 시장 구조 데이터 (최우선)
```
□ Put/Call Ratio (CBOE Equity P/C)
  - Source: CBOE DataShop or web_search "CBOE put call ratio"
  - Collect: 5-day moving average

□ VIX (Fear Index)
  - Source: Yahoo Finance ^VIX or web_search "VIX current"
  - Collect: Current value + percentile over past 3 months

□ Volatility Indicators
  - 21-day realized volatility
  - Historical position of VIX (determine if in bottom 10th percentile)
```

#### 1.2 레버리지 및 포지셔닝 데이터
```
□ FINRA Margin Debt Balance
  - Source: web_search "FINRA margin debt latest"
  - Collect: Latest month + Year-over-Year % change

□ Breadth (Market Participation)
  - % of S&P 500 stocks above 50-day MA
  - Source: web_search "S&P 500 breadth 50 day moving average"
```

#### 1.3 IPO 및 신규 발행 데이터
```
□ IPO Count & First-Day Performance
  - Source: Renaissance Capital IPO or web_search "IPO market 2025"
  - Collect: Quarterly count + median first-day return
```

**⚠️ CRITICAL: Phase 1 데이터 수집 없이 평가를 진행하지 마세요**

---

### Phase 2: 정량 평가 (Quantitative Scoring)

수집한 데이터를 아래 기준으로 기계적으로 점수화합니다:

#### Indicator 1: Put/Call Ratio (시장 심리)
```
Scoring Criteria:
- 2 points: P/C < 0.70 (excessive optimism, call-heavy)
- 1 point: P/C 0.70-0.85 (slightly optimistic)
- 0 points: P/C > 0.85 (healthy caution)

Rationale: P/C < 0.7 is historically characteristic of bubble periods
```

#### Indicator 2: 변동성 억제 + 신고가
```
Scoring Criteria:
- 2 points: VIX < 12 AND major index within 5% of 52-week high
- 1 point: VIX 12-15 AND near highs
- 0 points: VIX > 15 OR more than 10% from highs

Rationale: Extreme low volatility + highs indicates excessive complacency
```

#### Indicator 3: 레버리지 (Margin Debt Balance)
```
Scoring Criteria:
- 2 points: YoY +20% or more AND all-time high
- 1 point: YoY +10-20%
- 0 points: YoY +10% or less OR negative

Rationale: Rapid leverage increase is a bubble precursor
```

#### Indicator 4: IPO 시장 과열
```
Scoring Criteria:
- 2 points: Quarterly IPO count > 2x 5-year average AND median first-day return +20%+
- 1 point: Quarterly IPO count > 1.5x 5-year average
- 0 points: Normal levels

Rationale: Poor-quality IPO flood is characteristic of late-stage bubbles
```

#### Indicator 5: Breadth 이상 (좁은 리더십)
```
Scoring Criteria:
- 2 points: New high AND < 45% of stocks above 50DMA (narrow leadership)
- 1 point: 45-60% above 50DMA (somewhat narrow)
- 0 points: > 60% above 50DMA (healthy breadth)

Rationale: Rally driven by few stocks is fragile
```

#### Indicator 6: 가격 가속도
```
Scoring Criteria:
- 2 points: Past 3-month return exceeds 95th percentile of past 10 years
- 1 point: Past 3-month return in 85-95th percentile of past 10 years
- 0 points: Below 85th percentile

Rationale: Rapid price acceleration is unsustainable
```

---

### Phase 3: 정성 조정 (REVISED v2.1)

**한도: 최대 +3점 (v2.0의 +5에서 축소)**

**⚠️ CONFIRMATION BIAS PREVENTION CHECKLIST:**
```
Before adding ANY qualitative points:
□ Do I have concrete, measurable data? (not impressions)
□ Would an independent observer reach the same conclusion?
□ Am I avoiding double-counting with Phase 2 scores?
□ Have I documented specific evidence with sources?
```

#### Adjustment A: 사회적 침투 (0-1점, 엄격 기준)
```
+1 point: ALL THREE criteria must be met:
  ✓ Direct user report of non-investor recommendations
  ✓ Specific examples with names/dates/conversations
  ✓ Multiple independent sources (minimum 3)

+0 points: Any criteria missing

⚠️ INVALID EXAMPLES:
- "AI narrative is prevalent" (unmeasurable)
- "I saw articles about retail investors" (not direct report)
- "Everyone is talking about stocks" (vague, unverified)

✅ VALID EXAMPLE:
"My barber asked about NVDA (Nov 1), dentist mentioned AI stocks (Nov 2),
Uber driver discussed crypto (Nov 3)"
```

#### Adjustment B: 미디어/검색 트렌드 (0-1점, 측정 필수)
```
+1 point: BOTH criteria must be met:
  ✓ Google Trends showing 5x+ YoY increase (measured)
  ✓ Mainstream coverage confirmed (Time covers, TV specials with dates)

+0 points: Search trends <5x OR no mainstream coverage

⚠️ CRITICAL: "Elevated narrative" without data = +0 points

HOW TO VERIFY:
1. Search "[topic] Google Trends 2025" and document numbers
2. Search "[topic] Time magazine cover" for specific dates
3. Search "[topic] CNBC special" for episode confirmation

✅ VALID EXAMPLE:
"Google Trends: 'AI stocks' at 780 (baseline 150 = 5.2x).
Time cover 'AI Revolution' (Oct 15, 2025).
CNBC 'AI Investment Special' (3 episodes Oct 2025)."

⚠️ INVALID EXAMPLE:
"AI/technology narrative seems elevated" (unmeasurable)
```

#### Adjustment C: 밸류에이션 괴리 (0-1점, 이중 계산 방지)
```
+1 point: ALL criteria must be met:
  ✓ P/E >25 (if NOT already counted in Phase 2 quantitative)
  ✓ Fundamentals explicitly ignored in mainstream discourse
  ✓ "This time is different" documented in major media

+0 points: P/E <25 OR fundamentals support valuations

⚠️ SELF-CHECK QUESTIONS (if ANY is YES, score = 0):
- Is P/E already in Phase 2 quantitative scoring?
- Do companies have real earnings supporting valuations?
- Is the narrative backed by fundamental improvements?

✅ VALID EXAMPLE for +1:
"S&P P/E = 35x (vs historical 18x).
CNBC article: 'Earnings don't matter in AI era' (Oct 2025).
Bloomberg: 'Traditional metrics obsolete' (Nov 2025)."

⚠️ INVALID EXAMPLE:
"P/E 30.8 but companies have real earnings and AI has fundamental backing"
(fundamentals support = +0 points)
```

**Phase 3 Total: Maximum +3 points**

---

### Phase 4: 최종 판정 (REVISED v2.1)

```
Final Score = Phase 2 Total (0-12 points) + Phase 3 Adjustment (0 to +3 points)
Range: 0 to 15 points

Judgment Criteria (with Risk Budget):
- 0-4 points: Normal (Risk Budget: 100%)
- 5-7 points: Caution (Risk Budget: 70-80%)
- 8-9 points: Elevated Risk (Risk Budget: 50-70%) ⚠️ NEW in v2.1
- 10-12 points: Euphoria (Risk Budget: 40-50%)
- 13-15 points: Critical (Risk Budget: 20-30%)
```

**v2.1의 핵심 변경:**
- 더 세분화된 포지셔닝을 위해 "Elevated Risk" 단계(8-9점) 추가
- 9점은 더 이상 극단적 방어 구간이 아님 (기존 리스크 예산 40%)
- 8-9점에서 리스크 예산 50-70% 허용
- Caution에서 Euphoria로의 전환이 더 점진적

---

## 데이터 소스 (필수)

### US Market
- **Put/Call**: https://www.cboe.com/tradable_products/vix/
- **VIX**: Yahoo Finance (^VIX) or https://www.cboe.com/
- **Margin Debt**: https://www.finra.org/investors/learn-to-invest/advanced-investing/margin-statistics
- **Breadth**: https://www.barchart.com/stocks/indices/sp/sp500?viewName=advanced
- **IPO**: https://www.renaissancecapital.com/IPO-Center/Stats

### Japanese Market
- **Nikkei Futures P/C**: https://www.barchart.com/futures/quotes/NO*0/options
- **JNIVE**: https://www.investing.com/indices/nikkei-volatility-historical-data
- **Margin Debt**: JSF (Japan Securities Finance) Monthly Report
- **Breadth**: https://en.macromicro.me/series/31841/japan-topix-index-200ma-breadth
- **IPO**: https://www.pwc.co.uk/services/audit/insights/global-ipo-watch.html

---

## 구현 체크리스트

사용 시 아래를 확인하세요:

```
□ Have you collected all Phase 1 data?
□ Did you apply each indicator's threshold mechanically?
□ Did you keep qualitative evaluation within +5 point limit?
□ Are you NOT assigning points based on news article impressions?
□ Does your final score align with other quantitative frameworks?
```

---

## 중요한 원칙 (개정)

### 1. Data > Impressions
정량 데이터 없이 "뉴스 보도가 많다" 또는 "전문가가 조심스럽다"는 표현은 무시하세요.

### 2. 엄격한 순서: Quantitative → Qualitative
반드시 이 순서로 평가하세요: Phase 1 (Data Collection) → Phase 2 (Quantitative) → Phase 3 (Qualitative Adjustment).

### 3. 주관 지표 상한
정성 조정 총합은 +5점 한도입니다. 정량 평가를 뒤집을 수 없습니다.

### 4. "Taxi Driver"는 상징적 신호
비투자자의 직접 추천이 없으면 대중 침투를 쉽게 인정하지 마세요.

---

## 흔한 실패와 해결책 (개정)

### Failure 1: 뉴스 기사 기반 평가
❌ "Takaichi Trade 관련 보도가 많다" → 미디어 포화 2점
✅ Google Trends 수치 검증 → 측정값 기반 평가

### Failure 2: 전문가 코멘트 과잉 반응
❌ "과열 경고" → Euphoria 구간
✅ Put/Call, VIX, margin debt 측정값으로 판정

### Failure 3: 가격 상승에 대한 감정 반응
❌ 하루 4.5% 상승 → 가격 가속도 2점
✅ 10년 분포 내 위치 검증 → 객관 평가

### Failure 4: 밸류에이션 단독 판단
❌ P/E 17 → Valuation disconnect 2점
✅ P/E + 내러티브 의존 + 기타 정량 지표를 종합 판단

---

## 버블 단계별 권장 액션 (REVISED v2.1)

### Normal (0-4 points)
**Risk Budget: 100%**
- 정상 투자 전략 지속
- ATR 2.0× trailing stop 설정
- 계단식 수익 실현 규칙 적용 (+20%에서 25% 실현)

**Short-Selling: Not Allowed**
- 종합 조건 미충족 (0/7)

### Caution (5-7 points)
**Risk Budget: 70-80%**
- 부분 수익 실현 시작 (20-30% 축소)
- ATR 1.8×로 타이트닝
- 신규 포지션 사이징 50% 축소

**Short-Selling: Not Recommended**
- 더 명확한 반전 신호를 기다림

### Elevated Risk (8-9 points) ⚠️ NEW in v2.1
**Risk Budget: 50-70%**
- 수익 실현 확대 (30-50% 축소)
- ATR 1.6×로 타이트닝
- 신규 포지션: 엄선된 high quality만
- 향후 기회를 위한 현금 비중 점진적 확대

**Short-Selling: Consider Cautiously**
- 종합 조건 2/7 이상 확인 후에만
- 탐색적 소규모 포지션 (평소 사이즈의 10-15%)
- 엄격한 손절 (ATR 2.0×)

**Rationale for NEW phase:**
이 구간은 극단적 방어 없이 경계 수준이 높아진 상태를 의미합니다.
시장은 경고 신호를 보이지만 즉각적 붕괴를 뜻하지는 않습니다.
퀄리티 포지션 익스포저는 유지하되 유연성을 확보하세요.

### Euphoria (10-12 points)
**Risk Budget: 40-50%**
- 계단식 수익 실현 가속 (50-60% 축소)
- ATR 1.5×로 타이트닝
- 큰 조정 외 신규 롱 포지션 금지

**Short-Selling: Active Consideration**
- 종합 조건 3/7 이상 확인 후
- 소규모 포지션 (평소 사이즈의 20-25%)
- 정의된 리스크만 사용 (옵션, 타이트한 스탑)

### Critical (13-15 points)
**Risk Budget: 20-30%**
- 대규모 수익 실현 또는 전체 헤지 실행
- ATR 1.2× 또는 고정 손절
- 현금 보존 모드 - 큰 변동성 이벤트 대비

**Short-Selling: Recommended**
- 종합 조건 5/7 이상 확인 후
- 소규모로 분할 진입, 확인 시 피라미딩
- 타이트한 손절 (ATR 1.5× or higher)
- 정의된 리스크를 위해 put options 고려

---

## 공매도용 종합 조건 (7개)

아래 중 최소 3개 확인 후에만 공매도를 고려:

```
1. Weekly chart shows lower highs
2. Volume peaks out
3. Leverage indicators drop sharply (margin debt decline)
4. Media/search trends peak out
5. Weak stocks start to break down first
6. VIX surges (spike above 20)
7. Fed/policy shift signals
```

---

## 출력 형식

### 평가 보고서 구조 (v2.1)

```markdown
# [Market Name] Bubble Evaluation Report (Revised v2.1)

## Overall Assessment
- Final Score: X/15 points (v2.1: max reduced from 16)
- Phase: [Normal/Caution/Elevated Risk/Euphoria/Critical]
- Risk Level: [Low/Medium/Medium-High/High/Extremely High]
- Evaluation Date: YYYY-MM-DD

## Quantitative Evaluation (Phase 2)

| Indicator | Measured Value | Score | Rationale |
|-----------|----------------|-------|-----------|
| Put/Call | [value] | [0-2] | [reason] |
| VIX + Highs | [value] | [0-2] | [reason] |
| Margin YoY | [value] | [0-2] | [reason] |
| IPO Heat | [value] | [0-2] | [reason] |
| Breadth | [value] | [0-2] | [reason] |
| Price Accel | [value] | [0-2] | [reason] |

**Phase 2 Total: X/12 points**

## Qualitative Adjustment (Phase 3) - STRICT CRITERIA

**⚠️ Confirmation Bias Check:**
- [ ] All qualitative points have measurable evidence
- [ ] No double-counting with Phase 2
- [ ] Independent observer would agree

### A. Social Penetration (0-1 points)
- Evidence: [REQUIRED: Direct user reports with dates/names]
- Score: [+0 or +1]
- Justification: [Must meet ALL three criteria]

### B. Media/Search Trends (0-1 points)
- Google Trends Data: [REQUIRED: Measured numbers, YoY multiplier]
- Mainstream Coverage: [REQUIRED: Specific Time covers, TV specials with dates]
- Score: [+0 or +1]
- Justification: [Must have 5x+ search AND mainstream confirmation]

### C. Valuation Disconnect (0-1 points)
- P/E Ratio: [Current value]
- Fundamental Backing: [Yes/No - if Yes, score = 0]
- Narrative Analysis: [REQUIRED: Specific media quotes ignoring fundamentals]
- Score: [+0 or +1]
- Justification: [Must show fundamentals actively ignored]

**Phase 3 Total: +X/3 points (max reduced from +5 in v2.0)**

## Recommended Actions

**Risk Budget: X%** (Phase: [Normal/Caution/Elevated Risk/Euphoria/Critical])
- [Specific action 1]
- [Specific action 2]
- [Specific action 3]

**Short-Selling: [Not Allowed/Consider Cautiously/Active/Recommended]**
- Composite conditions: X/7 met
- Minimum required: [0/2/3/5] for current phase

## Key Changes in v2.1
- Stricter qualitative criteria (max +3, down from +5)
- Added "Elevated Risk" phase for 8-9 points
- Confirmation bias prevention checklist
- All qualitative points require measurable evidence
```

---

## 참고 문서

### `references/implementation_guide.md` (English) - **첫 사용 시 권장**
- 필수 데이터 수집을 포함한 단계별 평가 프로세스
- NG 예시 vs OK 예시
- Self-check 품질 기준 (4개 레벨)
- 검토 중 red flag
- 객관 평가를 위한 best practice

### `references/bubble_framework.md` (Japanese)
- 상세 이론 프레임워크
- Minsky/Kindleberger 모델 설명
- 행동심리 요소

### `references/historical_cases.md` (Japanese)
- 과거 버블 사례 분석
- Dotcom, Crypto, Pandemic 버블
- 공통 패턴 추출

### `references/quick_reference.md` (Japanese)
### `references/quick_reference_en.md` (English)
- 일일 체크리스트
- 비상 3문항 평가
- 빠른 점수 가이드
- 핵심 데이터 소스

### 참고 문서를 로드할 때
- **처음 사용하거나 상세 가이드가 필요할 때:** `implementation_guide.md` 로드
- **이론적 배경이 필요할 때:** `bubble_framework.md` 로드
- **역사적 맥락이 필요할 때:** `historical_cases.md` 로드
- **일상 운영:** `quick_reference.md` (Japanese) 또는 `quick_reference_en.md` (English) 로드

---

## 요약: v2.1 개정의 본질

**v2.0 문제 (2025년 11월 확인):**
- 정성 조정이 너무 느슨함 (최대 +5)
- "AI narrative elevated" → +1점 (데이터 없음)
- "P/E 30.8" → +1점 (정량과 이중 계산)
- **결과: 11/16점 - 증거 없는 과도한 약세 판단**

**v2.1 해법:**
- 정성 조정 엄격화 (최대 +3)
- "AI narrative elevated" → 0점 (미측정)
- "P/E 30.8 but AI has fundamental backing" → 0점 (펀더멘털 지지)
- **결과: 9/15점 - 균형 잡힌 데이터 기반 평가**

**핵심 개선 사항:**
1. **확증 편향 방지**: 정성 점수 추가 전 명시적 체크리스트
2. **측정 가능한 증거 필수**: 구체 데이터(Google Trends, 미디어 커버리지) 없이는 점수 없음
3. **이중 계산 방지**: 밸류에이션 항목은 Phase 2 정량과 중복 금지
4. **세분화된 리스크 단계**: 정교한 포지셔닝을 위한 "Elevated Risk"(8-9점) 추가
5. **균형 잡힌 리스크 예산**: 9점 = 50-70% (기존 40% 극단 방어 아님)

**Core Principle:**
> "In God we trust; all others must bring data." - W. Edwards Deming

**2025년 교훈:**
데이터 기반 프레임워크도 주관적 정성 조정으로 훼손될 수 있습니다.
v2.1은 ALL 정성 점수에 대해 MEASURABLE evidence를 요구합니다.
독립 관찰자가 각 조정을 검증할 수 있어야 합니다.

---

**Version History:**
- **v2.0** (Oct 27, 2025): Mandatory quantitative data collection
- **v2.1** (Nov 3, 2025): Stricter qualitative criteria, confirmation bias prevention, granular risk phases

**Reason for v2.1 Revision:**
측정되지 않은 "narrative" 평가와 이중 계산으로 인한 과대 점수화를 방지합니다.
모든 버블 리스크 평가가 독립적으로 검증 가능하고 확증 편향에서 자유롭도록 보장합니다.
