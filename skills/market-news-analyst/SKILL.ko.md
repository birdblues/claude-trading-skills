---
name: market-news-analyst
description: 최근 10일 내 시장을 움직인 주요 뉴스 이벤트와 미국 주식/원자재 시장 영향도를 분석할 때 사용하는 스킬입니다. 사용자가 FOMC/ECB/BOJ 같은 통화정책 이벤트 반응, 지정학 이슈의 원자재 영향, 메가캡 실적 영향, 최근 핵심 시장 뉴스 종합 분석을 요청할 때 사용합니다. 스킬은 WebSearch/WebFetch로 뉴스를 수집하고 영향도 순위 보고서를 생성합니다. 분석 사고 과정과 출력은 모두 영어로 수행합니다.
---

# Market News Analyst

## 개요

이 스킬은 최근 10일간의 시장 영향 뉴스 이벤트를 종합 분석하며, 미국 주식시장과 원자재 시장에 대한 영향을 중심으로 다룹니다. WebSearch와 WebFetch 도구로 신뢰 가능한 소스에서 뉴스를 자동 수집하고, 영향 규모를 평가하며, 실제 시장 반응을 분석한 뒤, 시장 영향도 기준으로 정렬된 구조화된 영어 보고서를 생성합니다.

## 이 스킬을 사용해야 할 때

다음 상황에서 사용하세요:
- 사용자가 최근 주요 시장 뉴스(지난 10일) 분석을 요청할 때
- 사용자가 특정 이벤트(FOMC 결정, 실적, 지정학 이슈)에 대한 시장 반응을 이해하려고 할 때
- 사용자가 영향도 평가가 포함된 종합 시장 뉴스 요약을 원할 때
- 사용자가 뉴스 이벤트와 원자재 가격 움직임의 상관관계를 물을 때
- 사용자가 중앙은행 정책 발표가 시장에 준 영향을 요청할 때

사용자 요청 예시:
- "Analyze the major market news from the past 10 days"
- "How did the latest FOMC decision impact the market?"
- "What were the most important market-moving events this week?"
- "Analyze recent geopolitical news and commodity price reactions"
- "Review mega-cap tech earnings and their market impact"

## 분석 워크플로우

시장 뉴스를 분석할 때 다음 6단계 구조화 워크플로우를 따르세요.

### Step 1: WebSearch/WebFetch로 뉴스 수집

**목표:** 최근 10일 내 주요 시장 영향 이벤트를 포괄적으로 수집.

**검색 전략:**

서로 다른 뉴스 카테고리를 커버하도록 병렬 WebSearch 쿼리를 실행합니다.

**Monetary Policy:**
- Search: "FOMC meeting past 10 days", "Federal Reserve interest rate", "ECB policy decision", "Bank of Japan"
- Target: 중앙은행 결정, forward guidance 변화, 인플레이션 코멘트

**Inflation/Economic Data:**
- Search: "CPI inflation report [current month]", "jobs report NFP", "GDP data", "PPI producer prices"
- Target: 주요 경제지표 발표 및 서프라이즈

**Mega-Cap Earnings:**
- Search: "Apple earnings [current quarter]", "Microsoft earnings", "NVIDIA earnings", "Amazon earnings", "Tesla earnings", "Meta earnings", "Google earnings"
- Target: 대형주 실적/가이던스/시장 반응

**Geopolitical Events:**
- Search: "Middle East conflict oil prices", "Ukraine war", "US China tensions", "trade war tariffs"
- Target: 시장에 영향을 주는 분쟁, 제재, 무역 갈등

**Commodity Markets:**
- Search: "oil prices news past week", "gold prices", "OPEC meeting", "natural gas prices", "copper prices"
- Target: 공급 차질, 수요 변화, 가격 변동

**Corporate News:**
- Search: "major M&A announcement", "bank earnings", "tech sector news", "bankruptcy", "credit rating downgrade"
- Target: 메가캡 외 대형 기업 이벤트

**권장 뉴스 소스 (우선순위):**
1. 공식 소스: FederalReserve.gov, SEC.gov (EDGAR), Treasury.gov, BLS.gov
2. Tier 1 금융 뉴스: Bloomberg, Reuters, Wall Street Journal, Financial Times
3. 전문 소스: CNBC (실시간), MarketWatch (요약), S&P Global Platts (원자재)

**검색 실행:**
- 광범위 주제는 WebSearch 사용
- 공식 사이트/주요 매체의 특정 URL은 WebFetch 사용
- 최근 10일 창(window) 내 뉴스인지 발행일 확인
- 기록 항목: 이벤트 날짜, 소스, 헤드라인, 핵심 세부사항, 시장 맥락(프리마켓/정규장/애프터마켓)

**필터링 기준:**
- Tier 1 market-moving events 중심(참고: references/market_event_patterns.md)
- 명확한 시장 영향(가격 급변, 거래량 급증)이 있는 뉴스 우선
- 제외: 소형주 개별 뉴스, 사소한 제품 업데이트, 루틴 공시

수집 과정 전반은 영어로 사고하세요. 각 중요 뉴스 항목에 아래를 문서화하세요:
- 날짜/시간
- 이벤트 유형(통화정책, 실적, 지정학 등)
- 소스 신뢰도 티어
- 초기 시장 반응(관측 가능 시)

### Step 2: 지식 베이스 Reference 로드

**목표:** 영향도 평가에 필요한 도메인 지식 확보.

수집된 뉴스 유형에 따라 관련 reference 파일을 로드합니다.

**항상 로드:**
- `references/market_event_patterns.md` - 주요 이벤트 유형별 종합 패턴
- `references/trusted_news_sources.md` - 소스 신뢰도 평가

**조건부 로드 (수집 뉴스 기반):**

**통화정책 뉴스**가 있으면:
- Focus: market_event_patterns.md → Central Bank Monetary Policy Events 섹션
- 핵심 프레임워크: 금리 인상/인하 반응, QE/QT 영향, hawkish/dovish 톤

**지정학 이벤트**가 있으면:
- 로드: `references/geopolitical_commodity_correlations.md`
- Focus: Energy Commodities, Precious Metals, 해당 지역 프레임워크

**메가캡 실적**이 있으면:
- 로드: `references/corporate_news_impact.md`
- Focus: 기업별 섹션, 섹터 전염(contagion) 패턴

**원자재 뉴스**가 있으면:
- 로드: `references/geopolitical_commodity_correlations.md`
- Focus: 해당 원자재 섹션(Oil, Gold, Copper 등)

**지식 통합:**
수집 뉴스를 과거 패턴과 비교해 다음을 수행:
- 예상 시장 반응 예측
- 이상치 식별(역사적 패턴과 다른 반응)
- 반응 크기가 전형적이었는지 과도했는지 평가
- 예상한 전염 효과가 실제로 발생했는지 판정

### Step 3: 영향 규모 평가(Impact Magnitude Assessment)

**목표:** 각 뉴스 이벤트를 시장 영향 중요도 순으로 랭킹.

**영향 평가 프레임워크:**

각 뉴스 항목을 아래 3개 차원으로 평가합니다.

**1. 자산 가격 영향 (Primary Factor):**

실제 또는 추정 가격 변동을 측정합니다.

**주식시장:**
- 지수 레벨: S&P 500, Nasdaq 100, Dow Jones
  - Severe: 일중 ±2%+
  - Major: ±1-2%
  - Moderate: ±0.5-1%
  - Minor: ±0.2-0.5%
  - Negligible: <0.2%

- 섹터 레벨: 섹터 ETF
  - Severe: ±5%+
  - Major: ±3-5%
  - Moderate: ±1-3%
  - Minor: <1%

- 개별 종목: 메가캡
  - Severe: ±10%+ (지수 비중으로 지수까지 움직이는 경우)
  - Major: ±5-10%
  - Moderate: ±2-5%

**원자재 시장:**
- Oil (WTI/Brent):
  - Severe: ±5%+
  - Major: ±3-5%
  - Moderate: ±1-3%

- Gold:
  - Severe: ±3%+
  - Major: ±1.5-3%
  - Moderate: ±0.5-1.5%

- Base Metals (Copper 등):
  - Severe: ±4%+
  - Major: ±2-4%
  - Moderate: ±1-2%

**채권시장:**
- 10-Year Treasury Yield:
  - Severe: 일중 ±20bps+
  - Major: ±10-20bps
  - Moderate: ±5-10bps

**외환시장:**
- USD Index (DXY):
  - Severe: ±1.5%+
  - Major: ±0.75-1.5%
  - Moderate: ±0.3-0.75%

**2. 영향 범위(Breadth) (Multiplier):**

몇 개 시장/섹터가 영향을 받았는지 평가합니다.

- **Systemic (3x multiplier):** 복수 자산군 + 글로벌 시장
  - 예: FOMC 서프라이즈, 은행 위기, 대형 전쟁 발발

- **Cross-Asset (2x multiplier):** 주식+원자재 또는 주식+채권
  - 예: 인플레이션 서프라이즈, 지정학 공급 쇼크

- **Sector-Wide (1.5x multiplier):** 특정 섹터 또는 연관 섹터 전체
  - 예: 테크 실적 클러스터, 에너지 정책 발표

- **Stock-Specific (1x multiplier):** 단일 기업(단, 지수 영향 메가캡 제외)
  - 예: 개별 실적, M&A

**3. 선행 의미(Forward-Looking Significance) (Modifier):**

미래 함의를 반영합니다.

- **Regime Change (+50%):** 시장 구조의 근본적 변화
  - 예: Fed가 인상에서 인하로 피벗, 지정학 질서 재편

- **Trend Confirmation (+25%):** 기존 추세 강화
  - 예: 연속적인 고인플레이션, 지속 실적 서프라이즈

- **Isolated Event (0%):** 단발성 이벤트
  - 예: 범위 내 단일 데이터, 기업 고유 이슈

- **Contrary Signal (-25%):** 기존 내러티브와 반대
  - 예: 호재 무시, 악재 랠리

**Impact Score 계산식:**

```
Impact Score = (Price Impact Score × Breadth Multiplier) + Forward-Looking Modifier

Price Impact Score:
- Severe: 10 points
- Major: 7 points
- Moderate: 4 points
- Minor: 2 points
- Negligible: 1 point
```

**계산 예시:**

**FOMC 75bps 금리 인상(hawkish tone):**
- Price Impact: S&P 500 -2.5% (Severe = 10 points)
- Breadth: Systemic (주식, 채권, USD, 원자재 동시 반응) = 3x
- Forward: Trend confirmation (긴축 지속) = +25%
- **Score: (10 × 3) × 1.25 = 37.5**

**NVIDIA Earnings Beat:**
- Price Impact: NVDA +15%, Nasdaq +1.5% (Severe = 10 points)
- Breadth: Sector-wide (반도체/테크 전반) = 1.5x
- Forward: Trend confirmation (AI 수요) = +25%
- **Score: (10 × 1.5) × 1.25 = 18.75**

**지정학 긴장 고조(중동):**
- Price Impact: Oil +8%, S&P -1.2% (Severe = 10 points)
- Breadth: Cross-asset (oil, equities, gold) = 2x
- Forward: Isolated event (확전 없음) = 0%
- **Score: (10 × 2) × 1.0 = 20**

**개별 실적(비 메가캡):**
- Price Impact: Stock +12%, index 영향 없음 (Major = 7 points)
- Breadth: Stock-specific = 1x
- Forward: Isolated = 0%
- **Score: (7 × 1) × 1.0 = 7**

**랭킹:**
모든 뉴스 항목 점수 산출 후, 영향 점수 내림차순으로 정렬합니다. 이 순서가 보고서 정렬 기준입니다.

### Step 4: 시장 반응 분석

**목표:** 각 이벤트에 대한 실제 시장 반응을 분석.

각 중요 뉴스 항목(Impact Score >5)에 대해 상세 반응 분석 수행:

**즉시 반응(Intraday):**
- 방향: Positive / Negative / Mixed
- 크기: 가격 영향 카테고리와 정렬
- 시점: 프리마켓, 정규장, 애프터마켓
- 변동성: VIX 변화, bid-ask spread

**멀티 자산 반응:**

**Equities:**
- 지수 성과(S&P 500, Nasdaq, Dow, Russell 2000)
- 섹터 로테이션(상대 강/약 섹터)
- 개별 종목(메가캡, 관련 기업)
- Growth vs Value, Large vs Small Cap 차별화

**Fixed Income:**
- Treasury yields(2Y, 10Y, 30Y)
- 수익률 곡선 형태(steepening, flattening, inversion)
- Credit spreads(IG, HY)
- TIPS breakevens(인플레 기대)

**Commodities:**
- Energy: Oil(WTI, Brent), Natural Gas
- Precious Metals: Gold, Silver
- Base Metals: Copper, Aluminum(필요 시)
- Agricultural: Wheat, Corn, Soybeans(필요 시)

**Currencies:**
- USD Index(DXY)
- EUR/USD, USD/JPY, GBP/USD
- EM 통화
- Safe havens(JPY, CHF)

**Derivatives:**
- VIX
- 옵션 활동(put/call ratio, unusual volume)
- 선물 포지셔닝

**패턴 비교:**

관측 반응을 knowledge base의 예상 반응과 비교:

- **Consistent:** 역사적 패턴과 일치
  - 예: Fed hike → Tech down, USD up (예상과 일치)

- **Amplified:** 전형 패턴보다 과대 반응
  - 예: CPI가 컨센서스 +0.3% 초과 → 통상 대비 2배 매도
  - 점검: 포지셔닝, 심리, 누적 요인

- **Dampened:** 전형 패턴보다 약한 반응
  - 예: 지정학 이벤트에도 Oil 반응 미미
  - 점검: 선반영 여부, 상쇄 요인

- **Inverse:** 역사 패턴과 반대
  - 예: 호재 무시, 악재 랠리
  - 점검: "Good news is bad news", Fed pivot 기대

**이상치 식별:**

패턴과 유의미하게 다른 반응을 플래그:
- 보통 시장을 흔드는 뉴스를 시장이 무시
- 통상 경미한 뉴스에 과잉 반응
- 예상한 전염이 확산되지 않음
- Safe haven 상관관계 붕괴

**심리 지표:**

- Risk-On vs Risk-Off: 어떤 레짐이 지배했는가
- 포지셔닝: crowded trade unwinding 징후
- 모멘텀: 이후 세션에서 추세 지속/반전 여부

### Step 5: 상관관계 vs 인과관계 평가

**목표:** 직접 영향과 우연한 동시성 구분.

**복수 이벤트 분석:**

10일 내 여러 중요 이벤트가 발생했다면 상호작용을 평가:

**Reinforcing Events:**
- 동일 방향 영향
- 예: Hawkish FOMC + 높은 CPI → 둘 다 주식 bearish, 낙폭 증폭
- 결합 영향은 비선형(합보다 클 수 있음)

**Offsetting Events:**
- 반대 방향 영향
- 예: 강한 실적(+) + 지정학 긴장(-) → 순반응 약화
- 어느 요인이 우세했는지 식별

**Sequential Events:**
- 앞선 이벤트가 다음 이벤트 반응을 준비
- 예: 첫 금리 인상은 반응 미미, 두 번째 인상은 급락(누적 긴축 우려)
- 경로 의존성 중요

**Coincidental Timing:**
- 무관 이벤트가 동시 발생
- 개별 영향 분리 어려움
- 기여도 판단의 불확실성 명시

**Geopolitical-Commodity Correlations:**

지정학 이벤트는 geopolitical_commodity_correlations.md를 사용해 원자재 반응을 별도 분석:

**Energy:**
- 분쟁/제재를 공급 차질 리스크로 매핑
- 실제 공급 영향 vs 공포 프리미엄 비교
- 지속성: 일시 급등 vs 장기 고착

**Precious Metals:**
- Safe-haven flow vs 실질금리 요인
- 리스크오프 시 Gold 반응
- 중앙은행 매수 함의

**Industrial Metals:**
- 경기둔화 우려에 따른 수요 파괴
- 공급망 차질
- Copper/Aluminum의 China 요인

**Agriculture:**
- 러-우 전쟁의 흑해 곡물 수출
- 기상 요인 오버레이
- 식량안보 정책 반응

**전달 메커니즘(Transmission Mechanisms):**

뉴스 영향이 시장에 전달되는 경로를 추적:

**직접 채널:**
- 뉴스 → 즉시 가격 반응
- 예: OPEC 감산 → 즉시 Oil 상승

**간접 채널:**
- 뉴스 → 경제 영향 → 자산 가격
- 예: 금리 인상 → 모기지 금리 상승 → 주택 둔화 → 주택주 하락

**심리 채널:**
- 뉴스 → 위험선호 변화 → 광범위한 리밸런싱
- 예: 은행 위기 → 안전자산 선호 → Treasury 강세, 주식 약세

**피드백 루프:**
- 초기 반응이 2차 효과 유발
- 예: 주가 급락 → 마진콜 → 강제 청산 → 하락 가속

### Step 6: 보고서 생성

**목표:** 시장 영향도 순으로 정렬된 구조화된 영어 Markdown 보고서 생성.

**보고서 구조:**

```markdown
# Market News Analysis Report - [Date Range]

## Executive Summary

[3-4 sentences covering:]
- Period analyzed (specific dates)
- Number of significant events identified
- Dominant market theme/regime (risk-on/risk-off, sector rotation)
- Top 1-2 highest-impact events

## Market Impact Rankings

[Table format, sorted by Impact Score descending]

| Rank | Event | Date | Impact Score | Asset Classes Affected | Market Reaction |
|------|-------|------|--------------|------------------------|-----------------|
| 1 | [Event] | [Date] | [Score] | [Equities, Commodities, etc.] | [Brief reaction] |
| 2 | ... | ... | ... | ... | ... |

---

## Detailed Event Analysis

[For each event in rank order, provide comprehensive analysis]

### [Rank]. [Event Name] (Impact Score: [X])

**Event Date:** [Date, Time]
**Event Type:** [Monetary Policy / Earnings / Geopolitical / Economic Data / Corporate]
**News Source:** [Source, with credibility tier]

#### Event Summary
[3-4 sentences describing what happened]
- Key details (e.g., rate decision, earnings beat/miss magnitude, conflict developments)
- Context (was this expected, surprise factor)
- Forward guidance or implications stated

#### Market Reaction

**Immediate (Day-of):**
- **Equities:** S&P 500 [+/-X%], Nasdaq [+/-X%], Sector rotation [details]
- **Bonds:** 10Y yield [change], credit spreads [movement]
- **Commodities:** Oil [+/-X%], Gold [+/-X%], Copper [+/-X%] (if relevant)
- **Currencies:** USD [+/-X%], [other relevant pairs]
- **Volatility:** VIX [level/change]

**Follow-Through (Subsequent Sessions):**
- [Direction: sustained, reversed, or consolidated]
- [Additional price action details if significant]

**Pattern Comparison:**
- **Expected Reaction:** [Based on historical patterns from knowledge base]
- **Actual vs Expected:** [Consistent / Amplified / Dampened / Inverse]
- **Explanation of Deviation:** [If applicable, why reaction differed]

#### Impact Assessment Detail

**Asset Price Impact:** [Severe/Major/Moderate/Minor] - [Justification]
**Breadth:** [Systemic/Cross-Asset/Sector/Stock-Specific] - [Affected markets]
**Forward Significance:** [Regime Change/Trend Confirmation/Isolated/Contrary] - [Rationale]

**Calculated Score:** ([Price Score] × [Breadth Multiplier]) × [Forward Modifier] = [Total]

#### Sector-Specific Impacts

[If relevant, detail which sectors/industries were most affected]
- [Sector 1]: [Impact and reason]
- [Sector 2]: [Impact and reason]
- [Example: Technology -3% (rate sensitivity), Energy +5% (oil price spillover)]

#### Geopolitical-Commodity Correlation Analysis

[Include this section only for geopolitical events]
- [Specific commodity affected]: [Price movement]
- [Supply/demand mechanism]: [Explanation]
- [Historical precedent]: [Comparison to similar past events]
- [Expected duration]: [Temporary shock vs sustained impact]

[Repeat detailed analysis for each ranked event]

---

## Thematic Synthesis

### Dominant Market Narrative
[Identify overarching theme across the 10-day period]
- [E.g., "Persistent inflation concerns dominated despite mixed economic data"]
- [E.g., "Tech sector strength drove markets higher despite geopolitical headwinds"]

### Interconnected Events
[Analyze how events related or compounded]
- [Event A] + [Event B] → [Combined impact analysis]
- [Sequential causation if applicable]

### Market Regime Assessment
**Risk Appetite:** [Risk-On / Risk-Off / Mixed]
**Evidence:**
- [Supporting indicators: sector performance, safe haven flows, credit spreads, VIX]

**Sector Rotation Trends:**
- [Growth vs Value]
- [Cyclicals vs Defensives]
- [Outperformers and underperformers]

### Anomalies and Surprises
[Highlight unexpected market reactions]
1. [Event]: Market reacted [unexpectedly] because [explanation]
2. [Continue for significant anomalies]

---

## Commodity Market Deep Dive

[Dedicated section for commodity movements]

### Energy
- **Crude Oil (WTI/Brent):** [Price level, % change over period, key drivers]
- **Natural Gas:** [If significant movement]
- **Key Events:** [Specific news impacting energy: OPEC, geopolitics, inventory data]

### Precious Metals
- **Gold:** [Price level, % change, safe-haven flows vs real rate dynamics]
- **Silver:** [If significant divergence from gold]
- **Drivers:** [Geopolitical risk premium, inflation hedging, USD strength]

### Base Metals
- **Copper:** [As economic barometer - demand signals]
- **Aluminum, Nickel:** [If relevant supply/demand news]
- **China Factor:** [Impact of Chinese economic data/policy]

### Agricultural (If Relevant)
- **Grains:** [Wheat, Corn, Soybeans - weather, Ukraine conflict impacts]

[For each commodity, reference geopolitical events from main analysis and draw correlations]

---

## Forward-Looking Implications

### Market Positioning Insights
[What the news suggests for current market positioning]
- [Trend continuation or reversal signals]
- [Overvaluation or undervaluation indications]
- [Sentiment extremes (complacency or panic)]

### Upcoming Catalysts
[Events on horizon that may be set up by recent news]
- [Next FOMC meeting expectations post-recent decision]
- [Upcoming earnings seasons based on guidance]
- [Geopolitical developments to monitor]

### Risk Scenarios
[Based on recent news, identify key risks]
1. **[Risk Name]:** [Description, probability, potential impact]
2. **[Risk Name]:** [Description, probability, potential impact]
3. [Continue for 3-5 key risks]

---

## Data Sources and Methodology

### News Sources Consulted
[List primary sources used, organized by tier]
- **Official Sources:** [e.g., FederalReserve.gov, SEC.gov]
- **Tier 1 Financial News:** [e.g., Bloomberg, Reuters, WSJ]
- **Specialized:** [e.g., S&P Global Platts for commodities]

### Analysis Period
- **Start Date:** [Specific date]
- **End Date:** [Specific date]
- **Total Days:** 10

### Market Data
- Equity indices: [Data sources]
- Commodity prices: [Data sources]
- Economic data: [Government sources]

### Knowledge Base References
- `market_event_patterns.md` - Historical reaction patterns
- `geopolitical_commodity_correlations.md` - Geopolitical-commodity frameworks
- `corporate_news_impact.md` - Mega-cap impact analysis
- `trusted_news_sources.md` - Source credibility assessment

---

*Analysis Date: [Date report generated]*
*Language: English*
*Analysis Thinking: English*

```

**파일명 규칙:**
`market_news_analysis_[START_DATE]_to_[END_DATE].md`

예시: `market_news_analysis_2024-10-25_to_2024-11-03.md`

**보고서 품질 기준:**
- 추측보다 사실 기반의 객관적 분석(가능성 기반 시나리오만 허용)
- 가격 변동은 반드시 구체적 %로 정량화
- 핵심 주장에는 출처 인용
- 상관관계와 인과관계 엄격 구분
- 특정 뉴스에 대한 귀속이 불확실하면 명시
- 정확한 금융 용어 사용
- 전 구간 영어 일관성 유지

## 핵심 분석 원칙

시장 뉴스 분석 시:

1. **Impact Over Noise:** 사소한 이벤트를 걸러내고 실제 시장 영향 뉴스에 집중
2. **Multi-Asset Perspective:** 주식/채권/원자재/외환을 함께 봐서 전체 임팩트 파악
3. **Pattern Recognition:** 과거 패턴과 비교하되 이번 국면의 고유성도 기록
4. **Causation Discipline:** 시장 움직임 귀속을 엄밀히 수행(우연한 동시성 배제)
5. **Forward-Looking:** 과거 설명보다 향후 시사점 중심
6. **Objectivity:** 시장 반응(what happened)과 개인 뷰(what should happen) 분리
7. **Quantification:** "significant" 대신 %, bps로 표현
8. **Source Credibility:** 루머보다 공식/ Tier 1 소스 우선
9. **Breadth Analysis:** 개별 주식 움직임은 메가캡/시스템 신호일 때만 중요
10. **English Consistency:** 사고, 분석, 출력 전부 영어 유지

## 피해야 할 흔한 함정

**Over-Attribution:**
- 모든 시장 움직임이 뉴스 때문은 아님(테크니컬, 자금 흐름, 월말 리밸런싱 존재)
- 귀속이 불명확하면 불확실성을 명시

**Recency Bias:**
- 최신 뉴스가 항상 가장 중요한 건 아님
- 시간순이 아니라 실질 영향 기준으로 랭크

**Hindsight Bias:**
- "사후적으로 당연"과 "당시 서프라이즈"를 구분
- 컨센서스 기대치 대비 결과를 명확히 기록

**Single-Factor Analysis:**
- 시장은 다중 요인에 동시 반응
- 상호작용 효과를 인정하고 기록

**Ignoring Magnitude:**
- CPI가 컨센서스 +0.1%와 +0.5%는 완전히 다른 이벤트
- 서프라이즈 크기를 정량화

## 리소스

### references/

**market_event_patterns.md** - 종합 지식 베이스:
- 중앙은행 통화정책 이벤트(FOMC, ECB, BOJ, PBOC)
- 인플레이션 지표(CPI, PPI, PCE)
- 고용 지표(NFP, 실업률, 임금)
- GDP 보고서
- 지정학 이벤트(분쟁, 무역전쟁, 제재)
- 기업 실적(메가캡 테크, 은행, 에너지)
- 신용 이벤트 및 신용등급 변경
- 원자재 특화 이벤트(OPEC, 기상, 공급차질)
- 경기침체 지표
- 역사적 케이스 스터디(2008 위기, COVID-19, 2022 인플레이션)
- 패턴 인식 프레임워크 및 심리 분석

**geopolitical_commodity_correlations.md** - 상세 상관관계:
- 에너지 원자재(crude oil, natural gas, coal)와 지정학 분쟁
- 귀금속(gold, silver, platinum, palladium) 안전자산 동학
- 비철금속(copper, aluminum, nickel, zinc)과 경제/정치 리스크
- 농산물(wheat, corn, soybeans)과 기상/정책 영향
- 희토류/핵심 광물(중국 지배력, 공급안보)
- 지역 지정학 프레임워크(중동, 러시아-유럽, 아시아-태평양, 중남미)
- 상관관계 요약 테이블
- 기간별(time horizon) 고려사항

**corporate_news_impact.md** - 메가캡 분석 프레임워크:
- "Magnificent 7"(NVIDIA, Apple, Microsoft, Amazon, Meta, Google, Tesla)
- 금융 메가캡(JPMorgan, Bank of America 등)
- 헬스케어 메가캡(UnitedHealth, Pfizer, J&J, Merck)
- 에너지 메가캡(Exxon Mobil, Chevron)
- 필수소비재 메가캡(P&G, Coca-Cola, PepsiCo)
- 산업재 메가캡(Boeing, Caterpillar)
- 실적 영향 프레임워크, 제품 출시, M&A, 규제 이슈
- 섹터 전염(contagion) 패턴
- 영향 규모 프레임워크

**trusted_news_sources.md** - 소스 신뢰도 가이드:
- Tier 1 1차 소스(중앙은행, 정부기관, SEC)
- Tier 2 주요 금융 뉴스(Bloomberg, Reuters, WSJ, FT, CNBC)
- Tier 3 전문 소스(에너지, 테크, 신흥국, 중국, 크립토)
- Tier 4 분석/리서치(독립 리서치, 중앙은행 publications, think tanks)
- 검색/집계 도구
- 소스 품질 평가 기준
- 속도 vs 정확도 트레이드오프
- 10일 분석용 권장 검색 전략
- 소스 신뢰도 프레임워크
- 피해야 할 red flag 소스

## 중요 노트

- 모든 분석 사고 과정은 영어로 수행
- 모든 출력 Markdown 파일은 영어로 작성
- 뉴스 수집은 WebSearch/WebFetch 자동화 사용
- references에 정의된 신뢰 소스 중심으로 수집
- 이벤트는 영향 점수(가격 영향 × 범위 × 선행 의미)로 랭크
- 분석 기간: 현재일 기준 최근 10일
- 핵심 대상: 미국 주식시장 + 원자재 시장
- FOMC 및 중앙은행 정책 결정은 최우선 분석 대상
- 상관관계와 인과관계를 엄격히 구분
- 모든 시장 반응은 구체적 퍼센트로 정량화
- 수집 뉴스 유형에 맞는 reference 파일 로드
- 시장 영향도 순(높은 영향부터)으로 종합 보고서 생성
