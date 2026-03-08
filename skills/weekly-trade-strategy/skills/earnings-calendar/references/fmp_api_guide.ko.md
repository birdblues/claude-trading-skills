# FMP Earnings Calendar API 가이드

이 문서는 Financial Modeling Prep (FMP) Earnings Calendar API를 사용해 미국 주식의 예정 실적 발표를 조회하는 방법을 안내합니다.

## FMP API 개요

Financial Modeling Prep (FMP)은 상장기업의 실적 일정 endpoint를 포함한 종합 금융 데이터 API를 제공합니다. 응답은 발표일, EPS 추정치, 매출 추정치, 실제 결과를 포함한 구조화 JSON 데이터입니다.

**공식 문서**: https://site.financialmodelingprep.com/developer/docs/earnings-calendar-api

## API Endpoint

**Earnings Calendar Endpoint**:
```
https://financialmodelingprep.com/api/v3/earning_calendar
```

### 인증

FMP API는 API key 인증이 필요합니다:
```
https://financialmodelingprep.com/api/v3/earning_calendar?apikey=YOUR_API_KEY&from=2025-11-03&to=2025-11-09
```

**API Key 발급 방법**:
- Free tier: https://site.financialmodelingprep.com/developer/docs
- 무료 계정 가입
- 즉시 API key 발급
- Free tier: 250 API calls/day

## 요청 파라미터

### 필수 파라미터

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `apikey` | string | FMP API key | `YOUR_API_KEY` |
| `from` | date | 시작일 (YYYY-MM-DD) | `2025-11-03` |
| `to` | date | 종료일 (YYYY-MM-DD) | `2025-11-09` |

### 제약 조건

- **최대 레코드 수**: 요청당 4000 records
- **최대 날짜 범위**: 90일
- **Rate Limiting**: Free tier = 250 calls/day, Premium = 750-2500 calls/day
- **날짜 형식**: YYYY-MM-DD (ISO 8601)

### 요청 예시

```bash
curl "https://financialmodelingprep.com/api/v3/earning_calendar?apikey=YOUR_KEY&from=2025-11-03&to=2025-11-09"
```

## 응답 형식

### JSON 구조

```json
[
    {
        "symbol": "AAPL",
        "date": "2025-11-04",
        "eps": null,
        "epsEstimated": 1.54,
        "time": "amc",
        "revenue": null,
        "revenueEstimated": 123400000000,
        "fiscalDateEnding": "2025-09-30",
        "updatedFromDate": "2025-11-01"
    },
    {
        "symbol": "MSFT",
        "date": "2025-11-05",
        "eps": null,
        "epsEstimated": 2.75,
        "time": "amc",
        "revenue": null,
        "revenueEstimated": 56200000000,
        "fiscalDateEnding": "2025-09-30",
        "updatedFromDate": "2025-11-02"
    }
]
```

### 필드 설명

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | 주식 ticker symbol |
| `date` | string | 실적 발표일 (YYYY-MM-DD) |
| `eps` | number/null | 실제 EPS (미발표 시 null) |
| `epsEstimated` | number | 애널리스트 EPS 추정치 |
| `time` | string | 발표 시간: "bmo" (장전), "amc" (장후), "tba" (미정) |
| `revenue` | number/null | 실제 매출 (미발표 시 null) |
| `revenueEstimated` | number | 애널리스트 매출 추정치 |
| `fiscalDateEnding` | string | 회계 기간 종료일 |
| `updatedFromDate` | string | 해당 항목 최종 업데이트일 |

## 발표 시간 규칙

### BMO (Before Market Open)
- API 값: `"bmo"` 또는 `"pre-market"`
- 미국 시장 ET 9:30 개장 전 발표
- 일반적으로 ET 6:00-8:00
- **영향**: 개장 전 시장이 정보를 소화할 시간 제공

### AMC (After Market Close)
- API 값: `"amc"` 또는 `"after-market"`
- 미국 시장 ET 4:00 마감 후 발표
- 일반적으로 ET 4:00-5:00
- **영향**: 야간 반응 후 다음 날 시가에서 gap 발생 가능

### TBA (To Be Announced)
- API 값: `"tba"` 또는 `null`
- 구체 시간 미공개
- BMO/AMC 모두 가능
- 기업 IR 공지로 업데이트 추적 필요

## 시가총액 기준 필터링

FMP Earnings Calendar endpoint에는 시가총액이 포함되지 않습니다. 시가총액 필터를 적용하려면:

### 옵션 1: Company Profile API 사용 (권장)

**1단계**: earnings calendar 데이터 조회
```
GET /api/v3/earning_calendar?apikey=KEY&from=2025-11-03&to=2025-11-09
```

**2단계**: 각 symbol에 대해 profile endpoint로 시가총액 조회
```
GET /api/v3/profile/{symbol}?apikey=KEY
```

응답 예시:
```json
{
    "symbol": "AAPL",
    "companyName": "Apple Inc.",
    "mktCap": 3000000000000,
    "sector": "Technology",
    "industry": "Consumer Electronics"
}
```

**3단계**: `mktCap > 2000000000` ($2B+) 조건으로 필터

### 옵션 2: Batch Profile API 사용 (더 효율적)

여러 symbol을 한 번에 조회:
```
GET /api/v3/profile/AAPL,MSFT,GOOGL,AMZN?apikey=KEY
```

API 호출 수를 크게 줄일 수 있습니다.

## Python 구현 전략

### 기본 요청

```python
import requests
from datetime import datetime, timedelta

def fetch_earnings_calendar(api_key, start_date, end_date):
    """
    Fetch earnings calendar from FMP API

    Args:
        api_key: FMP API key
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)

    Returns:
        List of earnings announcements
    """
    url = "https://financialmodelingprep.com/api/v3/earning_calendar"
    params = {
        "apikey": api_key,
        "from": start_date,
        "to": end_date
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()

# Usage
api_key = "YOUR_API_KEY"
earnings = fetch_earnings_calendar(api_key, "2025-11-03", "2025-11-09")
```

### 시가총액 필터 포함

```python
def fetch_company_profiles(api_key, symbols):
    """
    Fetch company profiles for multiple symbols (batch)

    Args:
        api_key: FMP API key
        symbols: List of ticker symbols

    Returns:
        Dictionary mapping symbol to profile data
    """
    # Batch symbols (max 100 per request)
    batch_size = 100
    profiles = {}

    for i in range(0, len(symbols), batch_size):
        batch = symbols[i:i+batch_size]
        symbols_str = ",".join(batch)

        url = f"https://financialmodelingprep.com/api/v3/profile/{symbols_str}"
        params = {"apikey": api_key}

        response = requests.get(url, params=params)
        response.raise_for_status()

        for profile in response.json():
            profiles[profile["symbol"]] = profile

    return profiles

def filter_by_market_cap(earnings, profiles, min_market_cap=2000000000):
    """
    Filter earnings by minimum market cap ($2B default)

    Args:
        earnings: List of earnings announcements
        profiles: Dictionary of company profiles
        min_market_cap: Minimum market cap in dollars

    Returns:
        Filtered list of earnings for mid-cap+ companies
    """
    filtered = []

    for earning in earnings:
        symbol = earning["symbol"]
        profile = profiles.get(symbol)

        if profile and profile.get("mktCap", 0) >= min_market_cap:
            # Merge earnings data with profile data
            earning["marketCap"] = profile["mktCap"]
            earning["companyName"] = profile.get("companyName", symbol)
            earning["sector"] = profile.get("sector", "N/A")
            earning["industry"] = profile.get("industry", "N/A")
            filtered.append(earning)

    return filtered

# Complete workflow
api_key = "YOUR_API_KEY"

# Step 1: Get earnings calendar
earnings = fetch_earnings_calendar(api_key, "2025-11-03", "2025-11-09")

# Step 2: Get company profiles
symbols = [e["symbol"] for e in earnings]
profiles = fetch_company_profiles(api_key, symbols)

# Step 3: Filter by market cap (>$2B)
filtered_earnings = filter_by_market_cap(earnings, profiles)
```

## API Key 관리 - Multi-Environment 지원

### Environment 1: Claude Code (CLI)

환경 변수 설정:
```bash
export FMP_API_KEY="your-api-key-here"
```

Python에서 접근:
```python
import os
api_key = os.environ.get('FMP_API_KEY')
```

### Environment 2: Claude Desktop

MCP server 설정 또는 시스템 환경 변수 사용.

### Environment 3: Claude Web

API key를 영구 저장할 수 없으므로 실행 중 사용자에게 요청해야 합니다.

**워크플로:**
1. 환경 변수 확인
2. 없으면 사용자에게 요청: "Please provide your FMP API key"
3. 현재 대화 session 변수에 저장
4. 해당 session의 모든 API 호출에 재사용

**보안 참고:**
- key는 대화 컨텍스트에만 저장
- session 종료 시 폐기
- free tier 또는 제한 권한 key 권장

## 오류 처리

### 자주 발생하는 오류

**401 Unauthorized:**
```json
{
    "Error Message": "Invalid API KEY. Please retry or visit our documentation to create one FREE https://site.financialmodelingprep.com/developer/docs"
}
```
해결: API key 정확성 확인

**429 Rate Limit Exceeded:**
```json
{
    "Error Message": "Limit Reach. Please upgrade your plan or visit our documentation for more details at https://site.financialmodelingprep.com/developer/docs"
}
```
해결: API 호출 수 축소 또는 플랜 업그레이드

**400 Bad Request:**
- 날짜 형식 오류
- 90일 초과 범위
- 필수 파라미터 누락

### 오류 처리 코드

```python
def fetch_earnings_with_error_handling(api_key, start_date, end_date):
    """Fetch earnings with proper error handling"""
    try:
        url = "https://financialmodelingprep.com/api/v3/earning_calendar"
        params = {
            "apikey": api_key,
            "from": start_date,
            "to": end_date
        }

        response = requests.get(url, params=params, timeout=30)

        # Check for API errors
        if response.status_code == 401:
            print("ERROR: Invalid API key")
            print("Get free API key: https://site.financialmodelingprep.com/developer/docs")
            return None

        if response.status_code == 429:
            print("ERROR: Rate limit exceeded")
            print("Free tier: 250 calls/day. Consider upgrading.")
            return None

        response.raise_for_status()
        data = response.json()

        # Check if response is error message
        if isinstance(data, dict) and "Error Message" in data:
            print(f"API Error: {data['Error Message']}")
            return None

        return data

    except requests.exceptions.Timeout:
        print("ERROR: Request timeout. Please try again.")
        return None

    except requests.exceptions.ConnectionError:
        print("ERROR: Connection error. Check your internet connection.")
        return None

    except Exception as e:
        print(f"ERROR: Unexpected error: {str(e)}")
        return None
```

## 데이터 품질 고려사항

### 정확성
- FMP 데이터는 실적 일정 기준으로 전반적으로 신뢰도 높음
- EPS/매출 추정치는 애널리스트 컨센서스로 정기 업데이트
- 기업이 마지막 순간 날짜를 변경할 수 있으므로 중요 일정은 재확인 필요

### 완전성
- 미국 상장기업 대부분 커버
- 일부 소형주는 데이터가 제한적일 수 있음
- IPO 전 기업은 거래 시작 전까지 노출되지 않음

### 시의성
- API는 하루 중 지속 업데이트
- 실적 일정은 보통 2-4주 전에 확정
- 일부 기업은 실적 1-2일 전에 늦게 일정 공지

### 데이터 신선도
- `updatedFromDate`로 최종 업데이트 시점 확인
- 실적일이 다가오면 추정치가 바뀔 수 있음
- Time field (`bmo`/`amc`/`tba`)도 일정 임박 시 업데이트 가능

## 모범 사례

### 1. 날짜 범위를 정확히 계산
항상 현재 날짜부터 계산:
```python
from datetime import datetime, timedelta

today = datetime.now()
start_date = (today + timedelta(days=1)).strftime("%Y-%m-%d")
end_date = (today + timedelta(days=7)).strftime("%Y-%m-%d")
```

### 2. API 호출 배치 처리
배치 endpoint로 호출 수 최소화:
- earnings calendar: 한 주 데이터 1회 호출
- company profiles: 요청당 최대 100 symbol 배치

### 3. 결과 캐시
동일일 반복 분석 시:
```python
import json
from pathlib import Path

def cache_earnings_data(data, cache_file="earnings_cache.json"):
    """Save earnings data to cache file"""
    cache_path = Path(cache_file)
    cache_path.write_text(json.dumps(data, indent=2))

def load_cached_data(cache_file="earnings_cache.json", max_age_hours=6):
    """Load cached data if recent enough"""
    cache_path = Path(cache_file)
    if not cache_path.exists():
        return None

    # Check cache age
    cache_age = datetime.now() - datetime.fromtimestamp(cache_path.stat().st_mtime)
    if cache_age.total_seconds() > max_age_hours * 3600:
        return None

    return json.loads(cache_path.read_text())
```

### 4. 누락 데이터 안전 처리
```python
def safe_get(data, key, default="N/A"):
    """Safely get value from dict with default"""
    value = data.get(key)
    return value if value is not None else default
```

### 5. 시가총액 기준 정렬/우선순위
```python
def sort_by_market_cap(earnings):
    """Sort earnings by market cap descending"""
    return sorted(
        earnings,
        key=lambda x: x.get("marketCap", 0),
        reverse=True
    )
```

## API 호출 최적화

### 호출 수 최소화

일반적인 주간 실적 캘린더 기준:
1. **Earnings Calendar API**: 1 call(주간 전체)
2. **Company Profiles API**: N/100 calls (N = symbol 수)

**예시**:
- 실적 발표 기업 200개
- Profile API calls: 200/100 = 2
- **총합**: 3 calls (250/day free limit 대비 충분)

### Rate Limit 관리

```python
import time

def rate_limited_request(url, params, delay=0.1):
    """Make request with rate limiting"""
    time.sleep(delay)
    return requests.get(url, params=params)
```

Free tier(250 calls/day) 기준:
- 시간당 안전선: 약 10 calls/hour
- 많은 요청 시 호출 간 0.5-1초 지연 권장

## 대체 Endpoints

### 실시간 시가총액 데이터

**Market Capitalization Endpoint**:
```
GET /api/v3/market-capitalization/{symbol}?apikey=KEY
```

현재 시가총액만 반환(빠르지만 symbol별 개별 호출 필요).

### 과거 실적 결과

**Historical Earnings Endpoint**:
```
GET /api/v3/historical/earning_calendar/{symbol}?apikey=KEY
```

과거 실적의 actual vs estimate 비교 데이터를 반환.

## 비교: FMP vs 기타 소스

| Feature | FMP API | Finviz | Yahoo Finance |
|---------|---------|--------|---------------|
| **Access Method** | REST API | Web Scraping | Web Scraping |
| **Authentication** | API Key | None | None |
| **Data Format** | JSON | HTML | HTML |
| **Rate Limit** | 250/day (free) | IP-based | IP-based |
| **Reliability** | High | Medium | Medium |
| **Market Cap Filter** | Via Profile API | Built-in | Manual |
| **EPS Estimates** | ✓ | ✗ | ✓ |
| **Revenue Estimates** | ✓ | ✗ | ✓ |
| **Timing Info** | ✓ | ✓ | ✓ |
| **Historical Data** | ✓ | ✗ | Limited |
| **Free Tier** | ✓ | ✓ | ✓ |

**권장:** 프로그래밍 방식 접근에서는 FMP API가 가장 구조적이고 신뢰도 높은 선택입니다.

## 문제 해결

### 문제: API가 빈 배열 반환

**해결 방법:**
- 날짜 범위가 유효한지 확인(미래 날짜)
- 날짜 형식 YYYY-MM-DD 확인
- API key 활성 상태 확인
- 날짜 범위 확대(+7일 대신 +14일)

### 문제: 주요 기업 일부 누락

**해결 방법:**
- 기업이 아직 실적 일정을 공지하지 않았을 수 있음
- 일부 기업은 실적 1-2일 전 늦게 공지
- 기업 IR 웹사이트와 교차 검증
- 해당 기업의 실적 일정 보류 여부 확인

### 문제: 시가총액 데이터 누락

**해결 방법:**
- 해당 기업 profile 데이터가 없을 수 있음
- 대체 market cap endpoint 사용
- 수동 시가총액 보완
- 유동성 낮은 일부 종목은 profile이 비어 있을 수 있음

### 문제: 예상보다 빠른 rate limit 도달

**해결 방법:**
- 동일 API key를 쓰는 다른 스크립트/도구 확인
- 반복 호출을 줄이기 위해 cache 적용
- 요청 간 지연 추가
- 필요 시 유료 tier 업그레이드

## 출력 데이터 구조 예시

FMP 데이터를 조회/가공한 후:

```python
{
    "symbol": "AAPL",
    "companyName": "Apple Inc.",
    "date": "2025-11-04",
    "time": "amc",
    "marketCap": 3000000000000,
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "epsEstimated": 1.54,
    "revenueEstimated": 123400000000
}
```

이 확장 데이터는 최종 실적 캘린더 보고서를 위해 날짜/시간/시가총액 기준으로 정리할 수 있습니다.

## 리소스

- **FMP Documentation**: https://site.financialmodelingprep.com/developer/docs
- **API Key Signup**: https://site.financialmodelingprep.com/developer/docs
- **Earnings Calendar API**: https://site.financialmodelingprep.com/developer/docs/earnings-calendar-api
- **Company Profile API**: https://site.financialmodelingprep.com/developer/docs/companies-key-metrics-api
- **Rate Limits**: https://site.financialmodelingprep.com/developer/docs/pricing

---

*이 가이드는 earnings-calendar 스킬과 FMP API 연동에 맞춰 최적화되었습니다.*
