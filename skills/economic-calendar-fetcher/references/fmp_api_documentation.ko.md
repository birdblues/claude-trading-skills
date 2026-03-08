# FMP Economic Calendar API 문서

## 개요

Financial Modeling Prep (FMP) Economic Calendar API는 예정/과거 경제 데이터 발표, 중앙은행 결정, 기타 시장 영향 이벤트에 접근할 수 있게 해줍니다. 이 API를 통해 트레이더와 투자자는 금융시장에 영향을 줄 수 있는 예정 이벤트를 파악할 수 있습니다.

## API Endpoint (Stable)

```
https://financialmodelingprep.com/stable/economic-calendar
```

> **참고:** 레거시 endpoint (`/api/v3/economic_calendar`)는
> 2025년 8월 31일 이후 non-legacy 구독에서 종료되었습니다.
> 위 stable endpoint를 사용하세요.

## 인증

API 접근에는 유효한 FMP API key가 필요하며, 모든 요청의 query parameter에 포함해야 합니다.

**파라미터:** `apikey`
**형식:** String
**필수 여부:** Yes

### API Key 발급

1. https://financialmodelingprep.com 방문
2. 계정 가입(무료/유료 tier 제공)
3. API dashboard에서 API key 확인
4. free tier는 일일 제한 요청 수 제공(~250-300 requests)
5. paid tiers는 더 높은 rate limit 및 추가 기능 제공

## 요청 파라미터

### 필수 파라미터

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `from` | date | 캘린더 기간 시작일 | `2025-01-01` |
| `to` | date | 캘린더 기간 종료일 | `2025-01-31` |
| `apikey` | string | FMP API key | `YOUR_API_KEY` |

### 날짜 형식

- **형식:** `YYYY-MM-DD` (ISO 8601 date format)
- **예시:** `2025-07-20`
- **최대 범위:** `from`과 `to` 사이 최대 90일
- **Timezone:** 모든 날짜는 UTC 기준

### 날짜 범위 제한

- 최소 범위: 1일
- 최대 범위: 90일
- 과거 날짜: API는 actual 값을 포함한 historical events 반환
- 미래 날짜: API는 estimate가 포함된 예정 이벤트 반환(actual은 null)

## 응답 형식

API는 경제 이벤트 객체의 JSON 배열을 반환합니다.

### 응답 구조

```json
[
    {
        "date": "2024-03-01 03:35:00",
        "country": "JP",
        "event": "3-Month Bill Auction",
        "currency": "JPY",
        "previous": -0.112,
        "estimate": null,
        "actual": -0.096,
        "change": 0.016,
        "impact": "Low",
        "changePercentage": 14.286
    }
]
```

### 응답 필드

| Field | Type | Description | Nullable |
|-------|------|-------------|----------|
| `date` | string | UTC 기준 이벤트 일시 (형식: `YYYY-MM-DD HH:MM:SS`) | No |
| `country` | string | ISO 2자리 국가 코드 (예: `US`, `JP`, `GB`, `EU`) | No |
| `event` | string | 경제 이벤트 이름/설명 | No |
| `currency` | string | ISO 3자리 통화 코드 (예: `USD`, `EUR`, `JPY`) | No |
| `previous` | number | 이전 발표 값 | Yes |
| `estimate` | number | 시장 컨센서스 추정치/전망치 | Yes |
| `actual` | number | 실제 발표 값(미래 이벤트는 null) | Yes |
| `change` | number | 이전 값 대비 절대 변화량 | Yes |
| `impact` | string | 시장 영향도: `"High"`, `"Medium"`, `"Low"` | No |
| `changePercentage` | number | 이전 값 대비 변화율(%) | Yes |

### 필드 상세

**`date`:**
- 형식: UTC timezone 기준 `YYYY-MM-DD HH:MM:SS`
- 경제 데이터 예정 발표 시각을 의미
- 미래 이벤트에서는 예상 발표 시각
- 발표 지연 시 시각이 조정될 수 있음

**`country`:**
- ISO 3166-1 alpha-2 국가 코드
- 특수 코드:
  - `EU`: European Union (ECB 관련 이벤트)
  - `G7`: G7 정상회의/공동 이벤트
  - 국제기구는 특수 코드를 사용할 수 있음

**`event`:**
- 경제 지표/이벤트의 설명형 이름
- 예시:
  - `"Non-Farm Payrolls"`
  - `"Consumer Price Index (CPI)"`
  - `"Federal Funds Rate Decision"`
  - `"GDP Growth Rate QoQ"`
  - `"Unemployment Rate"`

**`currency`:**
- ISO 4217 통화 코드
- 이벤트가 영향을 주는 통화를 의미
- 국가와 통화가 다를 수 있음(예: EU 이벤트는 다국가에 걸쳐 EUR 영향)

**`previous`:**
- 해당 지표의 직전 발표 값
- 현재 발표와 비교하는 기준값
- 최초 발표 후 수정(revision)될 수 있음
- 이전 데이터가 없으면 `null` (신규 지표)

**`estimate`:**
- 애널리스트 설문 기반 시장 컨센서스 전망치
- 보통 Bloomberg, Reuters 등 컨센서스 서비스 기반
- 컨센서스가 없거나 관심도가 낮은 지표는 `null`
- `actual`과 `estimate` 비교가 "surprise" 판단 핵심

**`actual`:**
- 데이터 발표 시 공개되는 공식 수치
- 미래 이벤트에서는 `null`(미발표)
- 발표 순간 시장을 움직이는 핵심 필드
- 이후 발표에서 수정될 수 있음(예비치 → 확정치)

**`change`:**
- 계산식: `actual - previous` (과거 이벤트 기준)
- `null` if either `actual` or `previous` is null
- 부호 의미: 양수 = 증가, 음수 = 감소
- 퍼센트가 아닌 절대값

**`impact`:**
- 시장 영향 잠재력에 대한 정성 평가
- 3단계:
  - `"High"`: 주요 이벤트(NFP, FOMC, CPI)
  - `"Medium"`: 중요하지만 변동성은 상대적으로 낮음(Retail Sales, PMI)
  - `"Low"`: 소규모 지표, 정례 데이터 발표
- FMP가 과거 변동성 영향 기준으로 산정

**`changePercentage`:**
- 계산식: `((actual - previous) / previous) * 100`
- `null` if either value is null or if `previous` is zero
- 변화량의 퍼센트 표현
- 서로 다른 지표 간 상대적 변화 규모 비교에 유용

## 요청 예시

### 향후 7일 이벤트 조회

```bash
curl "https://financialmodelingprep.com/stable/economic-calendar?from=2025-01-01&to=2025-01-07&apikey=YOUR_API_KEY"
```

### High-Impact 이벤트만 조회(후처리)

참고: API에는 `impact` 필터 파라미터가 없으므로, 조회 후 필터링해야 합니다.

```python
import requests

response = requests.get(
    "https://financialmodelingprep.com/stable/economic-calendar",
    params={
        "from": "2025-01-01",
        "to": "2025-01-31",
        "apikey": "YOUR_API_KEY"
    }
)

events = response.json()
high_impact_events = [e for e in events if e["impact"] == "High"]
```

### 특정 국가 이벤트 조회(후처리)

```python
us_events = [e for e in events if e["country"] == "US"]
eu_events = [e for e in events if e["country"] == "EU"]
```

## Rate Limits

rate limit은 FMP 구독 tier에 따라 달라집니다:

| Tier | Requests/Day | Requests/Second |
|------|--------------|-----------------|
| Free | 250 | 5 |
| Starter | 500 | 10 |
| Professional | 1,000+ | 20+ |

rate limit을 초과하면 API는 HTTP 429 (Too Many Requests)를 반환합니다.

## 오류 처리

### HTTP 상태 코드

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | Success | 요청 성공, 데이터 반환 |
| 400 | Bad Request | 잘못된 파라미터(날짜 형식 오류, 필수 파라미터 누락 등) |
| 401 | Unauthorized | API key 누락 또는 무효 |
| 403 | Forbidden | API key는 유효하지만 권한 없음(구독 만료 등) |
| 429 | Too Many Requests | rate limit 초과 |
| 500 | Internal Server Error | FMP 서버 오류(지연 후 재시도) |

### 오류 응답 형식

```json
{
    "Error Message": "Invalid API KEY. Please retry or visit our documentation to create one FREE https://financialmodelingprep.com/developer/docs"
}
```

### 자주 발생하는 오류

**Invalid API Key:**
```json
{"Error Message": "Invalid API KEY..."}
```
**해결:** API key 정확성 및 활성 구독 상태 확인

**Date Range Too Large:**
```json
{"Error Message": "Maximum date range is 90 days"}
```
**해결:** 날짜 범위를 90일 이하로 축소

**Rate Limit Exceeded:**
- HTTP 429 응답
**해결:** 다음 요청 전 대기 또는 구독 tier 업그레이드

## 모범 사례

### 1. Rate Limits 준수

재시도 시 exponential backoff를 구현하세요:
```python
import time

def fetch_with_retry(url, params, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url, params=params)
        if response.status_code == 429:
            wait_time = 2 ** attempt  # Exponential backoff
            time.sleep(wait_time)
            continue
        return response
    raise Exception("Max retries exceeded")
```

### 2. 결과 캐시

economic calendar 데이터는 발표 후 자주 바뀌지 않습니다:
- 과거 이벤트는 무기한 캐시(actual 값 고정)
- 미래 이벤트는 1-24시간 캐시(estimate 변경 드묾)
- 이벤트 발표 시각이 지나면 캐시 갱신

### 3. 효율적인 날짜 범위

- API 호출 최소화를 위해 7-30일 범위를 조회
- 3-6개월 이상 먼 미래는 조회 지양(희소 데이터)
- 실시간 모니터링은 1-7일의 짧은 범위 사용

### 4. Null 값 처리

특히 미래 이벤트는 많은 필드가 `null`일 수 있습니다:
```python
event_value = event.get("actual") or event.get("estimate") or event.get("previous")
if event_value is None:
    print("No value available for this event")
```

### 5. Time Zone 인지

API 시각은 모두 UTC 기준입니다:
```python
from datetime import datetime, timezone

utc_time = datetime.strptime(event["date"], "%Y-%m-%d %H:%M:%S")
utc_time = utc_time.replace(tzinfo=timezone.utc)

# Convert to local timezone
local_time = utc_time.astimezone()
```

## 데이터 정확성 및 시의성

### 발표 시각 정확도

- 대부분 ±1분 이내로 정확
- 기술 이슈/휴일로 지연 가능
- 서머타임 전환 시 시각 변동 가능

### 데이터 수정

economic data는 자주 수정됩니다:
- **Preliminary:** 최초 발표(시장 영향 가장 큼)
- **Revised:** 1-2개월 후 수정
- **Final:** 2-3개월 후 확정

API의 `previous`는 최초 예비치가 아니라 최신 수정값을 반영합니다.

### 커버리지

FMP Economic Calendar는 다음을 포함합니다:
- **주요 경제권:** US, EU, UK, Japan, China, Canada, Australia
- **이벤트 유형:**
  - 고용 지표(NFP, unemployment rate)
  - 인플레이션(CPI, PPI, PCE)
  - 성장 지표(GDP, retail sales, industrial production)
  - 중앙은행 결정(FOMC, ECB, BOJ, BOE)
  - 설문(PMI, consumer confidence, sentiment indices)
  - 무역 지표(trade balance, exports/imports)
  - 주택 지표(starts, permits, sales)

## 타 소스 비교

| Feature | FMP API | Forex Factory | Investing.com |
|---------|---------|---------------|---------------|
| API Access | Yes | No (scraping only) | No (scraping only) |
| Historical Data | Yes | Limited | Yes (web only) |
| Free Tier | Yes (250/day) | N/A | N/A |
| Data Format | JSON | HTML | HTML |
| Reliability | High | Medium (changes) | Medium (changes) |

FMP는 금융 캘린더 웹사이트 스크래핑(ToS 위반 가능, 취약) 대비 신뢰 가능한 공식 API 소스입니다.

## 지원 및 문서

- **공식 문서:** https://financialmodelingprep.com/developer/docs/economic-calendar-api
- **API 상태:** https://status.financialmodelingprep.com
- **지원 이메일:** support@financialmodelingprep.com
- **커뮤니티:** FMP 사용자 Discord/forum 활발
