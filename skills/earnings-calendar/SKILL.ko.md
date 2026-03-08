---
name: earnings-calendar
description: Financial Modeling Prep (FMP) API를 사용해 미국 주식의 예정 실적 발표를 조회하는 스킬입니다. 사용자가 실적 캘린더 데이터, 다음 주 실적 발표 기업, 주간 실적 리뷰를 요청할 때 사용하세요. 이 스킬은 시장 영향이 큰 mid-cap 이상(시가총액 $2B 초과) 기업에 집중하며, 날짜와 발표 시점 기준으로 정리된 markdown 표 형식 보고서를 생성합니다. 유연한 API key 관리와 함께 CLI/Desktop/Web 환경을 지원합니다.
---

# Earnings Calendar

## 개요

이 스킬은 Financial Modeling Prep (FMP) API를 사용해 미국 주식의 예정 실적 발표를 조회합니다. 시장 변동에 영향을 줄 가능성이 큰 시가총액 상위 기업(mid-cap 이상, $2B 초과)에 집중합니다. 생성되는 markdown 보고서는 다음 주 실적 발표 기업을 날짜별/시간대별(장 시작 전, 장 마감 후, 시간 미공개)로 정리해 제공합니다.

**주요 기능**:
- 신뢰 가능한 구조화 실적 데이터를 위해 FMP API 사용
- 시가총액 필터(>$2B)로 시장 영향 종목 중심 구성
- EPS/매출 추정치 포함
- Multi-environment 지원(CLI, Desktop, Web)
- 유연한 API key 관리
- 날짜/시간/시가총액 기준 정리

## 사전 요구사항

### FMP API Key

이 스킬은 Financial Modeling Prep API key가 필요합니다.

**무료 API Key 발급**:
1. 방문: https://site.financialmodelingprep.com/developer/docs
2. 무료 계정 가입
3. API key 즉시 발급
4. Free tier: 250 API calls/day (주간 실적 캘린더에 충분)

**환경별 API Key 설정**:

**Claude Code (CLI)**:
```bash
export FMP_API_KEY="your-api-key-here"
```

**Claude Desktop**:
시스템 환경 변수 설정 또는 MCP server 구성.

**Claude Web**:
스킬 실행 중 API key 입력을 요청합니다(현재 session에서만 저장).

## 핵심 워크플로

### 1단계: 현재 날짜 확인 및 대상 주간 계산

**중요**: 반드시 정확한 현재 날짜 확인부터 시작합니다.

현재 날짜/시간을 조회:
- 시스템 날짜/시간으로 오늘 날짜 확인
- 참고: 환경(<env> tag)에 "today" 정보가 제공됨
- 대상 주간 계산: 현재 날짜 기준 다음 7일

**날짜 범위 계산 예시**:
```
Current Date: [e.g., November 2, 2025]
Target Week Start: [Current Date + 1 day, e.g., November 3, 2025]
Target Week End: [Current Date + 7 days, e.g., November 9, 2025]
```

**이 단계가 중요한 이유**:
- 실적 캘린더는 시간 민감 데이터
- "다음 주"는 실제 현재 날짜 기준으로 계산되어야 함
- API 요청 범위를 정확히 설정 가능

API 호환을 위해 날짜는 **YYYY-MM-DD** 형식으로 사용하세요.

### 2단계: FMP API 가이드 로드

데이터 조회 전, FMP API 가이드를 읽습니다:

```
Read: references/fmp_api_guide.md
```

가이드 포함 내용:
- FMP API endpoint 구조/파라미터
- 인증 요구사항
- 시가총액 필터링 전략(Company Profile API)
- 실적 발표 시간 규칙(BMO, AMC, TAS)
- 응답 형식/필드 설명
- 오류 처리 전략
- 최적화 모범 사례

### 3단계: API Key 탐지 및 설정

실행 환경에 맞게 API key 사용 가능 여부를 확인합니다.

**Multi-Environment API Key Detection**:

#### 3.1 환경 변수 확인 (CLI/Desktop)

```bash
if [ ! -z "$FMP_API_KEY" ]; then
  echo "✓ API key found in environment"
  API_KEY=$FMP_API_KEY
fi
```

환경 변수가 있으면 4단계로 진행합니다.

#### 3.2 사용자에게 API Key 질문 (Desktop/Web)

환경 변수가 없으면 AskUserQuestion 도구를 사용:

**질문 구성**:
```
Question: "This skill requires an FMP API key to retrieve earnings data. Do you have an FMP API key?"
Header: "API Key"
Options:
  1. "Yes, I'll provide it now" → Proceed to 3.3
  2. "No, get free key" → Show instructions (3.2.1)
  3. "Skip API, use manual entry" → Jump to Step 8 (fallback mode)
```

**3.2.1 사용자가 "No, get free key" 선택 시**:

아래 안내를 제공합니다:
```
To get a free FMP API key:

1. Visit: https://site.financialmodelingprep.com/developer/docs
2. Click "Get Free API Key" or "Sign Up"
3. Create account (email + password)
4. Receive API key immediately
5. Free tier includes 250 API calls/day (sufficient for daily use)

Once you have your API key, please select "Yes, I'll provide it now" to continue.
```

#### 3.3 API Key 입력 요청

사용자가 key를 가지고 있으면 입력 요청:

**프롬프트**:
```
Please paste your FMP API key below:

(Your API key will only be stored for this conversation session and will be forgotten when the session ends. For regular use, consider setting the FMP_API_KEY environment variable.)
```

**session 변수 저장**:
```
API_KEY = [user_input]
```

**사용자 확인 메시지**:
```
✓ API key received and stored for this session.

Security Note:
- API key is stored only in current conversation context
- Not saved to disk or persistent storage
- Will be forgotten when session ends
- Do not share this conversation if it contains your API key

Proceeding with earnings data retrieval...
```

### 4단계: FMP API로 실적 데이터 조회

Python 스크립트로 FMP API 실적 데이터를 가져옵니다.

**스크립트 위치**:
```
scripts/fetch_earnings_fmp.py
```

**실행 방법**:

**옵션 A: 환경 변수 사용(CLI)**
```bash
python scripts/fetch_earnings_fmp.py 2025-11-03 2025-11-09
```

**옵션 B: Session API Key 사용(Desktop/Web)**
```bash
python scripts/fetch_earnings_fmp.py 2025-11-03 2025-11-09 "${API_KEY}"
```

**스크립트 내부 워크플로**(자동):
1. API key/날짜 파라미터 검증
2. FMP Earnings Calendar API 호출
3. 회사 profile 조회(시총/섹터/산업)
4. 시총 >$2B 기업 필터링
5. 시간대 정규화(BMO/AMC/TAS)
6. 날짜 → 시간대 → 시총(내림차순) 정렬
7. JSON을 stdout으로 출력

**예상 출력 형식**(JSON):
```json
[
  {
    "symbol": "AAPL",
    "companyName": "Apple Inc.",
    "date": "2025-11-04",
    "timing": "AMC",
    "marketCap": 3000000000000,
    "marketCapFormatted": "$3.0T",
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "epsEstimated": 1.54,
    "revenueEstimated": 123400000000,
    "fiscalDateEnding": "2025-09-30",
    "exchange": "NASDAQ"
  },
  ...
]
```

**파일 저장 권장 방식**:
```bash
python scripts/fetch_earnings_fmp.py 2025-11-03 2025-11-09 "${API_KEY}" > earnings_data.json
```

또는 변수 캡처:
```bash
earnings_data=$(python scripts/fetch_earnings_fmp.py 2025-11-03 2025-11-09 "${API_KEY}")
```

**오류 처리**:

스크립트 오류 시:
- **401 Unauthorized**: API key 무효 → key 재확인/재입력
- **429 Rate Limit**: 일일 한도 초과 → 대기 또는 요금제 업그레이드
- **Empty Result**: 범위 내 실적 없음 → 기간 확대 또는 보고서에 명시
- **Connection Error**: 네트워크 이슈 → 재시도 또는 캐시 데이터 사용

### 5단계: 데이터 처리 및 정리

JSON 실적 데이터를 수신한 후 정리합니다.

#### 5.1 JSON 파싱

스크립트 출력 JSON 로드:
```python
import json
earnings_data = json.loads(earnings_json_string)
```

파일 저장 시:
```python
with open('earnings_data.json', 'r') as f:
    earnings_data = json.load(f)
```

#### 5.2 데이터 구조 검증

필수 필드 확인:
- ✓ symbol
- ✓ companyName
- ✓ date
- ✓ timing (BMO/AMC/TAS)
- ✓ marketCap
- ✓ sector

#### 5.3 날짜 기준 그룹화

실적 발표를 날짜별로 그룹화:
- Sunday, [Full Date] (해당 시)
- Monday, [Full Date]
- Tuesday, [Full Date]
- Wednesday, [Full Date]
- Thursday, [Full Date]
- Friday, [Full Date]
- Saturday, [Full Date] (해당 시)

#### 5.4 시간대 기준 하위 그룹

날짜별로 3개 하위 섹션 생성:
1. **Before Market Open (BMO)**
2. **After Market Close (AMC)**
3. **Time Not Announced (TAS)**

스크립트가 이미 timing 정렬을 수행하므로 순서를 유지합니다.

#### 5.5 시간대 그룹 내 정렬

기업은 스크립트 출력 기준 시총 내림차순 정렬됨:
- Mega-cap (>$200B) 우선
- Large-cap ($10B-$200B) 다음
- Mid-cap ($2B-$10B) 다음

가장 시장 영향이 큰 기업을 먼저 보이게 하기 위한 우선순위입니다.

#### 5.6 요약 통계 계산

다음을 계산:
- **Total Companies**: 전체 기업 수
- **Mega/Large Cap Count**: marketCap >= $10B 개수
- **Mid Cap Count**: marketCap이 $2B-$10B인 개수
- **Peak Day**: 발표 기업 수가 가장 많은 요일
- **Sector Distribution**: 섹터별 건수(Technology, Healthcare, Financial 등)
- **Highest Market Cap Companies**: 시총 상위 5개

### 6단계: Markdown 보고서 생성

JSON 데이터를 기반으로 보고서 생성 스크립트를 사용합니다.

**스크립트 위치**:
```
scripts/generate_report.py
```

**실행**:

**옵션 A: stdout 출력**
```bash
python scripts/generate_report.py earnings_data.json
```

**옵션 B: 파일 저장**
```bash
python scripts/generate_report.py earnings_data.json earnings_calendar_2025-11-02.md
```

**스크립트 수행 내용**:
1. JSON 파일에서 실적 데이터 로드
2. 날짜/시간대(BMO/AMC/TAS) 그룹화
3. 그룹 내 시총 정렬
4. 요약 통계 계산
5. 포맷된 markdown 보고서 생성
6. stdout 출력 또는 파일 저장

스크립트가 자동 처리하는 항목:
- markdown table 형식
- 날짜 그룹/요일명
- 시총 정렬
- EPS/매출 포맷
- 요약 통계 계산

**보고서 구조**:

```markdown
# Upcoming Earnings Calendar - Week of [START_DATE] to [END_DATE]

**Report Generated**: [Current Date]
**Data Source**: FMP API (Mid-cap and above, >$2B market cap)
**Coverage Period**: Next 7 days
**Total Companies**: [COUNT]

---

## Executive Summary

- **Total Companies Reporting**: [TOTAL_COUNT]
- **Mega/Large Cap (>$10B)**: [LARGE_CAP_COUNT]
- **Mid Cap ($2B-$10B)**: [MID_CAP_COUNT]
- **Peak Day**: [DAY_WITH_MOST_EARNINGS]

---

## [Day Name], [Full Date]

### Before Market Open (BMO)

| Ticker | Company | Market Cap | Sector | EPS Est. | Revenue Est. |
|--------|---------|------------|--------|----------|--------------|
| [TICKER] | [COMPANY] | [MCAP] | [SECTOR] | [EPS] | [REV] |

### After Market Close (AMC)

| Ticker | Company | Market Cap | Sector | EPS Est. | Revenue Est. |
|--------|---------|------------|--------|----------|--------------|
| [TICKER] | [COMPANY] | [MCAP] | [SECTOR] | [EPS] | [REV] |

### Time Not Announced (TAS)

| Ticker | Company | Market Cap | Sector | EPS Est. | Revenue Est. |
|--------|---------|------------|--------|----------|--------------|
| [TICKER] | [COMPANY] | [MCAP] | [SECTOR] | [EPS] | [REV] |

---

[Repeat for each day of week]

---

## Key Observations

### Highest Market Cap Companies This Week
1. [COMPANY] ([TICKER]) - [MCAP] - [DATE] [TIME]
2. [COMPANY] ([TICKER]) - [MCAP] - [DATE] [TIME]
3. [COMPANY] ([TICKER]) - [MCAP] - [DATE] [TIME]

### Sector Distribution
- **Technology**: [COUNT] companies
- **Healthcare**: [COUNT] companies
- **Financial**: [COUNT] companies
- **Consumer**: [COUNT] companies
- **Other**: [COUNT] companies

### Trading Considerations
- **Days with Heavy Volume**: [DATES with multiple large-cap earnings]
- **Pre-Market Focus**: [BMO companies that may move markets]
- **After-Hours Focus**: [AMC companies that may move markets]

---

## Timing Reference

- **BMO (Before Market Open)**: Announcements typically around 6:00-8:00 AM ET before market opens at 9:30 AM ET
- **AMC (After Market Close)**: Announcements typically around 4:00-5:00 PM ET after market closes at 4:00 PM ET
- **TAS (Time Not Announced)**: Specific time not yet disclosed - monitor company investor relations

---

## Data Notes

- **Market Cap Categories**:
  - Mega Cap: >$200B
  - Large Cap: $10B-$200B
  - Mid Cap: $2B-$10B

- **Filter Criteria**: This report includes companies with market cap $2B and above (mid-cap+) with earnings scheduled for the next week.

- **Data Source**: Financial Modeling Prep (FMP) API

- **Data Freshness**: Earnings dates and times can change. Verify critical dates through company investor relations websites for the most current information.

- **EPS and Revenue Estimates**: Analyst consensus estimates from FMP API. Actual results will be reported on earnings date.

---

## Additional Resources

- **FMP API Documentation**: https://site.financialmodelingprep.com/developer/docs
- **Seeking Alpha Calendar**: https://seekingalpha.com/earnings/earnings-calendar
- **Yahoo Finance Calendar**: https://finance.yahoo.com/calendar/earnings

---

*Report generated using FMP Earnings Calendar API with mid-cap+ filter (>$2B market cap). Data current as of report generation time. Always verify earnings dates through official company sources.*
```

**서식 모범 사례**:
- 가독성을 위해 markdown table 사용
- 필요 시 mega-cap 기업명 강조
- 사람이 읽기 쉬운 시총 표기($3.0T, $150B, $5.2B) 사용 - 스크립트에서 포맷 제공
- 날짜 → 시간대 순으로 논리적 그룹화
- 상단 요약 섹션 제공
- 가능하면 EPS/매출 추정치 포함

### 7단계: 품질 검증(QA)

보고서 최종화 전 아래를 점검하세요.

**데이터 품질 점검**:
1. ✓ 모든 날짜가 대상 주간(다음 7일) 범위에 포함되는지
2. ✓ 모든 기업에 시총 값이 있는지
3. ✓ 각 기업의 timing(BMO/AMC/TAS)이 명시되는지
4. ✓ 각 섹션에서 시총 내림차순 정렬이 맞는지
5. ✓ 요약 통계가 정확한지
6. ✓ 보고서 생성일이 명확히 표기됐는지
7. ✓ 가능한 EPS/매출 추정치가 포함됐는지

**완전성 점검**:
1. ✓ 대상 주간 모든 요일 포함(실적이 없더라도)
2. ✓ 알려진 주요 기업 누락 여부(필요 시 외부 소스 교차 확인)
3. ✓ 가능한 섹터 정보 포함
4. ✓ Timing reference 섹션 포함
5. ✓ 데이터 출처(FMP API) 명시

**형식 점검**:
1. ✓ markdown table 포맷 정상
2. ✓ 날짜 표기 일관성
3. ✓ 시총 단위 일관성(B, T)
4. ✓ 템플릿 구조 준수
5. ✓ placeholder 텍스트([PLACEHOLDER]) 제거
6. ✓ EPS/매출 값 포맷 정상

### 8단계: 저장 및 전달

보고서 파일명을 아래 규칙으로 저장:

**파일명 규칙**:
```
earnings_calendar_[YYYY-MM-DD].md
```

예: `earnings_calendar_2025-11-02.md`

파일명의 날짜는 실적 주간이 아니라 **보고서 생성일**입니다.

**전달 방식**:
- markdown 파일을 작업 디렉터리에 저장
- 사용자에게 생성 완료 알림
- 핵심 요약을 함께 전달(예: "다음 주 45개 기업 발표, 월요일 Apple/Microsoft 포함")

**요약 예시**:
```
✓ Earnings calendar report generated: earnings_calendar_2025-11-02.md

Summary for week of November 3-9, 2025:
- 45 companies reporting earnings
- 28 large/mega-cap, 17 mid-cap
- Peak day: Thursday (15 companies)
- Notable: Apple (Mon AMC), Microsoft (Tue AMC), Tesla (Wed AMC)

Top 5 by market cap:
1. Apple - $3.0T (Mon AMC)
2. Microsoft - $2.8T (Tue AMC)
3. Alphabet - $1.8T (Thu AMC)
4. Amazon - $1.6T (Fri AMC)
5. Tesla - $800B (Wed AMC)
```

## Fallback Mode (8단계 대체): 수동 데이터 입력

API 접근 불가 또는 사용자가 API 건너뛰기를 선택한 경우:

**수동 입력 안내**:

```
Since FMP API is not available, you can manually gather earnings data:

1. Visit Finviz: https://finviz.com/screener.ashx?v=111&f=cap_midover%2Cearningsdate_nextweek
2. Or Yahoo Finance: https://finance.yahoo.com/calendar/earnings
3. Note down companies reporting next week

Please provide the following information for each company:
- Ticker symbol
- Company name
- Earnings date
- Timing (BMO/AMC/TAS)
- Market cap (approximate)
- Sector

I will format this into the standard earnings calendar report.
```

**수동 입력 처리**:
1. 사용자가 제공한 실적 데이터 파싱
2. 날짜/시간/시총 기준 정리
3. 동일 템플릿으로 보고서 생성
4. 보고서에 "Data Source: Manual Entry" 명시

## 사용 사례 및 예시

### 사용 사례 1: 주간 리뷰(기본)

**사용자 요청**: "다음 주 실적 캘린더 가져와"

**워크플로**:
1. 현재 날짜 확인(예: November 2, 2025)
2. 대상 주간 계산(November 3-9, 2025)
3. FMP API 가이드 로드
4. API key 탐지/요청
5. 실적 데이터 조회:
   ```bash
   python scripts/fetch_earnings_fmp.py 2025-11-03 2025-11-09 > earnings_data.json
   ```
6. markdown 보고서 생성:
   ```bash
   python scripts/generate_report.py earnings_data.json earnings_calendar_2025-11-02.md
   ```
7. 사용자에게 요약 포함 안내

**원라인 실행 예시**:
```bash
python scripts/fetch_earnings_fmp.py 2025-11-03 2025-11-09 > earnings_data.json && \
python scripts/generate_report.py earnings_data.json earnings_calendar_2025-11-02.md
```

### 사용 사례 2: 특정 요일 중심

**사용자 요청**: "월요일 실적 발표 뭐 있어?"

**워크플로**:
1. 현재 날짜 확인 후 다음 Monday 계산(예: November 4, 2025)
2. 사용 사례 1과 동일하게 주간 데이터 조회
3. 전체 보고서 생성하되 Monday 섹션 강조
4. Monday 발표 기업을 구두 요약으로 추가 제공

### 사용 사례 3: Mega-Cap 중심

**사용자 요청**: "다음 주 시총 $100B 이상 실적만 보여줘"

**워크플로**:
1. 전체 실적 데이터 조회(기본 필터 >$2B)
2. 일반 처리 수행
3. 보고서 상단에 "Mega-Cap Focus" 섹션 추가
4. 표에는 >$100B 기업만 표시
5. 필요 시 부록에 전체 데이터 제공

### 사용 사례 4: 섹터 중심

**사용자 요청**: "다음 주 tech 기업 실적 일정 알려줘"

**워크플로**:
1. 전체 실적 데이터 조회
2. 일반 처리 수행
3. sector = "Technology" 필터 적용
4. 기술 섹터 중심 보고서 생성
5. 템플릿 구조는 유지하되 콘텐츠만 필터링

## 문제 해결

### 문제: API key가 동작하지 않음

**해결 방법**:
- API key가 정확한지 확인(복사/붙여넣기 오류 확인)
- FMP dashboard에서 key 활성 상태 확인
- 앞뒤 공백 제거
- FMP dashboard에서 key 재발급 시도

### 문제: 스크립트가 빈 결과 반환

**해결 방법**:
- 날짜 범위가 미래인지 확인(과거 날짜 제외)
- 날짜 형식 YYYY-MM-DD 확인
- 범위 확대 시도(7일 → 14일)
- 해당 주간 실적 일정 공시 여부 확인

### 문제: 주요 기업 누락

**해결 방법**:
- 해당 기업이 아직 실적일 미공시일 수 있음
- 일부 기업은 발표 1-2일 전에 늦게 공시
- 기업 IR 웹사이트와 교차 검증
- 시총이 $2B 아래로 하락했는지 확인

### 문제: Rate limit(429) 발생

**해결 방법**:
- Free tier: 250 calls/day
- 주간 보고서 1회는 보통 ~3-5 calls 사용
- 같은 key를 사용하는 다른 도구/스크립트 확인
- 24시간 후 limit reset 대기
- 잦은 사용 시 유료 tier 고려

### 문제: 스크립트 실행 오류

**해결 방법**:
- Python 3 설치 확인: `python3 --version`
- requests 라이브러리 설치: `pip install requests`
- 실행 권한 확인: `chmod +x fetch_earnings_fmp.py`
- 명시적으로 python3 사용: `python3 fetch_earnings_fmp.py ...`

## Best Practices

### Do's
✓ 데이터 조회 전 반드시 현재 날짜를 먼저 확인
✓ 신뢰성을 위해 FMP API를 기본 소스로 사용
✓ CLI에서는 API key를 환경 변수로 저장
✓ 시총 정렬로 시장 영향 종목 우선 제시
✓ 날짜 → 시간대 순 그룹화로 가독성 확보
✓ 빠른 파악을 위한 요약 통계 포함
✓ 보고서 하단에 데이터 소스 명시
✓ 깔끔한 markdown table 사용
✓ 시간대 설명(Timing reference) 섹션 포함
✓ 데이터 신선도 및 변경 가능성 명시
✓ 가능하면 EPS/매출 추정치 포함

### Don'ts
✗ 현재 날짜 계산 없이 "다음 주"를 가정하지 않기
✗ timing 정보(BMO/AMC/TAS) 누락하지 않기
✗ 보고서 내 날짜 형식 혼용 금지
✗ 별도 요청 없으면 micro/small-cap 포함 금지
✗ 섹션 내 시총 정렬 누락 금지
✗ 대화/보고서에 API key 노출 금지
✗ 현재 주/과거 날짜 실적 포함 금지
✗ QA 없이 보고서 생성 금지
✗ API key를 버전 관리에 커밋 금지

## 보안 참고

### API Key 보안

**중요 지침**:
1. ✓ 테스트에는 free tier key 사용
2. ✓ key 정기 교체
3. ✓ API key가 포함된 대화 공유 금지
4. ✓ CLI에서는 환경 변수 사용
5. ✓ 채팅으로 받은 key는 session 한정(종료 시 폐기)
6. ✗ API key를 Git repository에 커밋 금지
7. ✗ 민감 데이터 접근 권한이 있는 production key 사용 금지

**권장 방식**:
Claude Code (CLI)에서는 환경 변수를 사용:
```bash
# Add to ~/.zshrc or ~/.bashrc
export FMP_API_KEY="your-key-here"
```

Claude Web 사용 시:
- 채팅 입력 key는 임시값
- 대화 컨텍스트에만 저장
- 디스크에 저장되지 않음
- session 종료 시 자동 폐기

## 리소스

**FMP API**:
- Main Documentation: https://site.financialmodelingprep.com/developer/docs
- Get API Key: https://site.financialmodelingprep.com/developer/docs
- Earnings Calendar API: https://site.financialmodelingprep.com/developer/docs/earnings-calendar-api
- Company Profile API: https://site.financialmodelingprep.com/developer/docs/companies-key-metrics-api
- Pricing/Rate Limits: https://site.financialmodelingprep.com/developer/docs/pricing

**보조 소스** (검증용):
- Seeking Alpha: https://seekingalpha.com/earnings/earnings-calendar
- Yahoo Finance: https://finance.yahoo.com/calendar/earnings
- MarketWatch: https://www.marketwatch.com/tools/earnings-calendar

**스킬 리소스**:
- FMP API Guide: `references/fmp_api_guide.md`
- Python Script: `scripts/fetch_earnings_fmp.py`
- Report Template: `assets/earnings_report_template.md`

---

## 요약

이 스킬은 미국 주식의 주간 실적 캘린더를 API 기반으로 안정적으로 생성합니다. FMP API를 사용해 구조화된 정확한 데이터를 제공하며 EPS/매출 추정치 같은 추가 인사이트도 포함합니다. Multi-environment 지원(CLI/Desktop/Web)으로 활용성이 높고, API 미사용 상황에서도 fallback mode로 기능을 유지할 수 있습니다.

**핵심 흐름**: 날짜 계산 → API Key 설정 → API 데이터 조회 → 처리 → 보고서 생성 → QA → 전달

**출력**: 날짜/시간/시총 기준으로 정리된 깔끔한 markdown 실적 보고서(요약 통계 및 트레이딩 고려사항 포함)
