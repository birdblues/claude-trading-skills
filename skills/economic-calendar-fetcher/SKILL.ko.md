---
name: economic-calendar-fetcher
description: FMP API를 사용해 예정된 경제 이벤트와 데이터 발표를 조회합니다. 지정한 날짜 범위(기본: 향후 7일)에 대해 중앙은행 결정, 고용 보고서, 인플레이션 데이터, GDP 발표 등 시장에 영향을 주는 경제 지표 일정을 가져옵니다. 영향도 평가가 포함된 시간순 markdown 보고서를 출력합니다.
---

# Economic Calendar Fetcher

## 개요

Financial Modeling Prep (FMP) Economic Calendar API에서 예정된 경제 이벤트와 데이터 발표를 조회합니다. 이 스킬은 중앙은행 통화정책 결정, 고용 보고서, 인플레이션 데이터(CPI/PPI), GDP 발표, 소매판매, 제조업 데이터 등 금융시장에 영향을 주는 주요 경제 지표 일정을 수집합니다.

스킬은 Python 스크립트로 FMP API를 조회하고, 각 이벤트의 영향도 평가를 포함한 시간순 markdown 보고서를 생성합니다.

**주요 기능:**
- 지정한 날짜 범위의 경제 이벤트 조회(최대 90일)
- 유연한 API key 입력 지원(환경 변수 또는 사용자 입력)
- 영향도, 국가, 이벤트 유형별 필터링
- 영향 분석이 포함된 구조화 markdown 보고서 생성
- 빠른 시장 점검을 위한 기본값(향후 7일)

**데이터 소스:**
- FMP Economic Calendar API: `https://financialmodelingprep.com/stable/economic-calendar`
- 주요 경제권 포함: US, EU, UK, Japan, China, Canada, Australia
- 이벤트 유형: 중앙은행 결정, 고용, 인플레이션, GDP, 무역, 주택, 설문

## 이 스킬을 사용할 때

사용자가 다음을 요청할 때 사용하세요:

1. **Economic Calendar 조회:**
   - "이번 주에 어떤 경제 이벤트가 있나요?"
   - "다음 2주 economic calendar를 보여줘"
   - "다음 FOMC 회의는 언제야?"
   - "다음 달 주요 경제지표 발표 일정 알려줘"

2. **시장 이벤트 계획:**
   - "이번 주 시장에서 뭘 봐야 하나요?"
   - "고영향 경제 발표 예정 있어?"
   - "다음 jobs report / CPI release / GDP report가 언제야?"

3. **특정 날짜 범위 요청:**
   - "1월 1일부터 1월 31일까지 경제 이벤트 가져와"
   - "Q1 2025 economic calendar 뭐 있어?"

4. **국가별 조회:**
   - "다음 주 US 경제지표 발표 보여줘"
   - "ECB 관련 일정 뭐가 잡혀 있어?"
   - "Japan 인플레이션 데이터 발표 언제야?"

**다음 용도로는 사용하지 마세요:**
- 과거 경제 이벤트 분석(과거 분석은 market-news-analyst 사용)
- 기업 실적 캘린더(이 스킬은 earnings 제외)
- 실시간 시세/호가 데이터
- 기술적 분석 또는 차트 해석

## 사전 요구사항

- **FMP API Key** (필수): https://financialmodelingprep.com 에서 무료 key 발급(250 requests/day). `FMP_API_KEY` 환경 변수 또는 스크립트 `--api-key`로 설정.
- **Python 3.10+**: `skills/economic-calendar-fetcher/scripts/get_economic_calendar.py` 실행에 필요.
- **서드파티 패키지 없음**: 스크립트는 Python 표준 라이브러리만 사용.

## 워크플로

다음 단계로 economic calendar를 조회/분석합니다:

### 1단계: FMP API Key 확보

**API key 사용 가능 여부 확인:**

1. 먼저 FMP_API_KEY 환경 변수가 설정되어 있는지 확인
2. 없으면 채팅에서 사용자에게 API key 제공 요청
3. 사용자에게 key가 없으면 아래 안내 제공:
   - https://financialmodelingprep.com 방문
   - 무료 계정 가입(250 requests/day)
   - API dashboard에서 key 발급

**사용자 상호작용 예시:**
```
User: "Show me economic events for next week"
Assistant: "I'll fetch the economic calendar. Do you have an FMP API key? I can use the FMP_API_KEY environment variable, or you can provide your API key now."
```

### 2단계: 날짜 범위 결정

**사용자 요청에 맞는 날짜 범위 설정:**

**기본값(날짜 지정 없음):** 오늘 + 7일
**사용자 지정 기간:** 정확한 날짜 사용(형식 검증: YYYY-MM-DD)
**최대 범위:** 90일(FMP API 제한)

**예시:**
- "다음 주" → 오늘부터 +7일
- "다다음 2주" → 오늘부터 +14일
- "January 2025" → 2025-01-01 ~ 2025-01-31
- "Q1 2025" → 2025-01-01 ~ 2025-03-31

**날짜 범위 검증:**
- 시작일 ≤ 종료일
- 범위 ≤ 90일
- 과거 날짜 조회 시 경고

### 3단계: API 조회 스크립트 실행

**적절한 파라미터로 get_economic_calendar.py를 실행합니다:**

**기본 사용법(기본 7일):**
```bash
python3 skills/economic-calendar-fetcher/scripts/get_economic_calendar.py --api-key YOUR_KEY
```

**특정 날짜 범위 사용:**
```bash
python3 skills/economic-calendar-fetcher/scripts/get_economic_calendar.py \
  --from 2025-01-01 \
  --to 2025-01-31 \
  --api-key YOUR_KEY \
  --format json
```

**환경 변수 사용(no --api-key needed):**
```bash
export FMP_API_KEY=your_key_here
python3 skills/economic-calendar-fetcher/scripts/get_economic_calendar.py \
  --from 2025-01-01 \
  --to 2025-01-07
```

**스크립트 파라미터:**
- `--from`: 시작일 (YYYY-MM-DD) - 기본값: 오늘
- `--to`: 종료일 (YYYY-MM-DD) - 기본값: 오늘 + 7일
- `--api-key`: FMP API key (optional if FMP_API_KEY env var set)
- `--format`: 출력 형식(json 또는 text) - 기본값: json
- `--output`: 출력 파일 경로(선택, 기본: stdout)

**오류 처리:**
- 잘못된 API key → 사용자에게 key 검증 요청
- rate limit 초과(429) → 대기 또는 FMP tier 업그레이드 안내
- 네트워크 오류 → exponential backoff 재시도
- 잘못된 날짜 형식 → 올바른 형식 예시 제공

### 4단계: 이벤트 파싱 및 필터링

**스크립트의 JSON 응답 처리:**

1. **이벤트 데이터 파싱:** API 응답에서 전체 이벤트 추출
2. **요청된 필터 적용(있을 경우):**
   - 영향도: "High", "Medium", "Low"
   - 국가: "US", "EU", "JP", "CN" 등
   - 이벤트 유형: FOMC, CPI, Employment, GDP 등
   - 통화: USD, EUR, JPY 등

**필터 예시:**
- "고영향 이벤트만" → impact == "High"
- "US 이벤트만" → country == "US"
- "중앙은행 결정" → 이벤트명에서 "Rate", "Policy", "FOMC", "ECB", "BOJ" 검색

**이벤트 데이터 구조:**
```json
{
  "date": "2025-01-15 14:30:00",
  "country": "US",
  "event": "Consumer Price Index (CPI) YoY",
  "currency": "USD",
  "previous": 2.6,
  "estimate": 2.7,
  "actual": null,
  "change": null,
  "impact": "High",
  "changePercentage": null
}
```

### 5단계: 시장 영향도 평가

**각 이벤트의 시장 중요도 평가:**

**영향도 분류(FMP 기준):**
- **High Impact:** 주요 시장 변동 이벤트
  - FOMC 금리결정, ECB/BOJ 정책회의
  - Non-Farm Payrolls (NFP), CPI, GDP
  - 일반적으로 장중 0.5-2%+ 변동성 발생

- **Medium Impact:** 중요하지만 변동성은 상대적으로 낮음
  - Retail Sales, Industrial Production
  - PMI 서베이, Consumer Confidence
  - Housing data, Durable Goods Orders

- **Low Impact:** 경미한 지표
  - 주간 실업수당 청구(극단값 제외)
  - 지역 제조업 서베이
  - 소규모 입찰 결과

**추가 컨텍스트 요소:**

1. **현재 시장 민감도:**
   - 고인플레이션 환경 → CPI/PPI 중요도 상승
   - 경기침체 우려 → 고용 데이터 중요도 상승
   - 금리 인하 기대 → 중앙은행 회의 중요

2. **서프라이즈 가능성:**
   - estimate와 previous 값 비교
   - 예상 변화 폭이 크면 주목도 상승
   - 컨센서스 불확실성이 크면 영향 잠재력 증가

3. **이벤트 군집:**
   - 같은 날 연관 이벤트 다수 발생 시 영향 증폭
   - 예: CPI + Retail Sales + Fed speech = Very High impact day

4. **선행 중요도:**
   - 해당 이벤트가 향후 중앙은행 결정에 영향이 있는지
   - 예비치인지 최종치인지
   - 향후 수정 가능성 여부

### 6단계: 출력 보고서 생성

**아래 섹션 구조로 markdown 보고서 생성:**

**보고서 헤더:**
```markdown
# Economic Calendar
**Period:** [Start Date] to [End Date]
**Report Generated:** [Timestamp]
**Total Events:** [Count]
**High Impact Events:** [Count]
```

**이벤트 목록(시간순):**

각 이벤트별로 다음을 제공합니다:

```markdown
## [Date] - [Day of Week]

### [Event Name] ([Impact Level])
- **Country:** [Country Code] ([Currency])
- **Time:** [HH:MM UTC]
- **Previous:** [Value]
- **Estimate:** [Consensus Forecast]
- **Impact Assessment:** [Your analysis]

**Market Implications:**
[2-3 sentences on why this matters, what markets watch for, typical reaction patterns]

---
```

**이벤트 항목 예시:**

```markdown
## 2025-01-15 - Wednesday

### Consumer Price Index (CPI) YoY (High Impact)
- **Country:** US (USD)
- **Time:** 14:30 UTC (8:30 AM ET)
- **Previous:** 2.6%
- **Estimate:** 2.7%
- **Impact Assessment:** Very High - Core inflation metric for Fed policy decisions

**Market Implications:**
CPI reading above estimate (>2.7%) likely strengthens hawkish Fed expectations, potentially pressuring equities and supporting USD. Reading at or below 2.7% could reinforce disinflation narrative and support risk assets. Options market pricing 1.2% S&P 500 move on release day.

---
```

**요약 섹션:**

보고서 마지막에 분석 요약을 추가합니다:

```markdown
## Key Takeaways

**Highest Impact Days:**
- [Date]: [Events] - [Combined impact rationale]
- [Date]: [Events] - [Combined impact rationale]

**Central Bank Activity:**
- [Summary of any scheduled Fed/ECB/BOJ meetings or speeches]

**Major Data Releases:**
- Employment: [NFP, Unemployment Rate dates]
- Inflation: [CPI, PPI dates]
- Growth: [GDP, Retail Sales dates]

**Market Positioning Considerations:**
[2-3 bullets on how traders might position around these events]

**Risk Events:**
[Highlight any particularly high-uncertainty or surprise-potential events]
```

**필터 적용 메모:**

사용자가 특정 필터를 요청한 경우 상단에 명시:
```markdown
**Filters Applied:**
- Impact Level: High only
- Country: US
- Events shown: [X] of [Y] total events in date range
```

**출력 형식:**
- 기본: 디스크에 저장되는 Markdown 파일
- 파일명 형식: `economic_calendar_[START]_to_[END].md`
- 사용자 채팅에는 요약도 함께 제공

## 출력 형식 명세

**파일명 규칙:**
```
economic_calendar_2025-01-01_to_2025-01-31.md
economic_calendar_2025-01-15_to_2025-01-21.md  (weekly)
economic_calendar_high_impact_2025-01.md  (with filters)
```

**Markdown 구조 요구사항:**

1. **시간순 정렬:** 이벤트를 날짜/시간 기준 오름차순 정렬
2. **영향도 표시:** (High Impact), (Medium Impact), (Low Impact) 레이블 사용
3. **시간대 명확성:** 항상 UTC를 명시하고 US 이벤트는 ET/PT 변환도 제공
4. **데이터 완전성:** 가능한 모든 필드 포함(previous, estimate, 과거 이벤트의 actual)
5. **null 처리:** null은 "N/A" 또는 "No estimate"로 표시
6. **영향 분석:** high/medium 영향 이벤트에는 market implications 분석 필수

**표 형식 옵션(고밀도 목록):**

```markdown
| Date/Time (UTC) | Event | Country | Impact | Previous | Estimate | Assessment |
|-----------------|-------|---------|--------|----------|----------|------------|
| 01-15 14:30 | CPI YoY | US | High | 2.6% | 2.7% | Core inflation metric |
```

**언어:** 모든 보고서는 English로 작성

## 리소스

**Python 스크립트:**
- `skills/economic-calendar-fetcher/scripts/get_economic_calendar.py`: CLI 인터페이스가 있는 메인 API 조회 스크립트

**참조 문서:**
- `references/fmp_api_documentation.md`: FMP Economic Calendar API 전체 레퍼런스
  - 인증 및 API key 관리
  - 요청 파라미터/날짜 형식
  - 응답 필드 정의
  - rate limit 및 오류 처리
  - 캐싱/효율화 모범 사례

**API 상세:**
- Endpoint: `https://financialmodelingprep.com/stable/economic-calendar`
- 인증: API key 필요(free tier: 250 requests/day)
- 최대 날짜 범위: 요청당 90일
- 응답 형식: 이벤트 객체 JSON 배열
- rate limits: 5 requests/second (free tier)

**이벤트 커버리지:**
- 주요 경제권: US, EU, UK, Japan, China, Canada, Australia, Switzerland
- 이벤트 범주: 통화정책, 고용, 인플레이션, GDP, 무역, 주택, 설문
- 업데이트 주기: 실시간(일정 추가/수정 즉시 반영)
- 과거 데이터: actual 값 포함 형태로 조회 가능

**사용 팁:**
1. API 호출 최소화를 위해 결과 캐시 사용(일정은 확정 후 변경이 적음)
2. 7-30일 범위 조회가 요청 효율에 유리
3. 6개월 이상 미래 조회는 지양(희소 데이터, 추정 일정)
4. 다음 주 데이터는 일 1회 캐시 갱신(시간 변경 반영)
5. 실시간 모니터링은 1-7일의 짧은 범위 사용

**오류 처리:**
- API key 오류: 무료 key 발급 안내를 명확히 제공
- rate limit: exponential backoff 재시도
- 네트워크 실패: 가능하면 캐시 데이터로 graceful degradation
- 잘못된 날짜: 검증 후 이해하기 쉬운 오류 메시지 제공
