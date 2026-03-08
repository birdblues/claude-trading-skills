# FMP API Endpoints - CANSLIM Screener Phase 3 (Full CANSLIM)

## 개요

이 문서는 CANSLIM 스크리너 Phase 3 구현(7개 요소 전체: C, A, N, S, L, I, M)에 필요한 Financial Modeling Prep(FMP) API endpoint를 명시합니다.

**Base URL**: `https://financialmodelingprep.com/api/v3`

**Authentication**: 모든 요청에 `apikey` 파라미터 필요

**Rate Limiting**:
- Free tier: 250 requests/day
- 권장 지연: 요청 사이 0.3초 (분당 최대 200 requests)

---

## C Component - Current Quarterly Earnings

### Endpoint: Income Statement (Quarterly)

**URL**: `/income-statement/{symbol}?period=quarter&limit=8`

**Method**: GET

**Parameters**:
- `symbol`: 종목 티커 (예: "AAPL")
- `period`: "quarter" (분기 데이터)
- `limit`: 8 (최근 8개 분기 = 2년)
- `apikey`: FMP API key

**Example Request**:
```bash
curl "https://financialmodelingprep.com/api/v3/income-statement/AAPL?period=quarter&limit=8&apikey=YOUR_KEY"
```

**사용 필드**:
```json
[
  {
    "date": "2023-09-30",  # Quarter end date
    "symbol": "AAPL",
    "reportedCurrency": "USD",
    "fillingDate": "2023-11-02",
    "eps": 1.46,           # Diluted EPS ← KEY
    "epsdiلuted": 1.46,     # Alternative field
    "revenue": 89498000000, # Total revenue ← KEY
    "grossProfit": 41104000000,
    "operatingIncome": 26982000000,
    "netIncome": 22956000000
  },
  # ... 7 more quarters
]
```

**사용 방법**:
- 최근 분기 `eps`와 4분기 전 `eps`를 비교해 YoY 계산
- `revenue`도 동일 방식으로 YoY 계산
- YoY 성장률 산출

**API Calls**: 종목당 1회

---

## A Component - Annual EPS Growth

### Endpoint: Income Statement (Annual)

**URL**: `/income-statement/{symbol}?period=annual&limit=5`

**Method**: GET

**Parameters**:
- `symbol`: 종목 티커
- `period`: "annual" (연간 데이터)
- `limit`: 5 (4년 CAGR 계산을 위해 최근 5년)
- `apikey`: FMP API key

**Example Request**:
```bash
curl "https://financialmodelingprep.com/api/v3/income-statement/AAPL?period=annual&limit=5&apikey=YOUR_KEY"
```

**사용 필드**:
```json
[
  {
    "date": "2023-09-30",   # Fiscal year end
    "symbol": "AAPL",
    "eps": 6.13,            # Annual diluted EPS ← KEY
    "revenue": 383285000000, # Annual revenue ← KEY
    "netIncome": 96995000000
  },
  # ... 4 more years
]
```

**사용 방법**:
- 최근 4개 연도로 3-year CAGR 계산
- CAGR = ((EPS_current / EPS_3years_ago) ^ (1/3)) - 1
- 안정성 점검(no down years)
- revenue CAGR로 교차 검증

**API Calls**: 종목당 1회

---

## N Component - Newness / New Highs

### Endpoint 1: Historical Prices (Daily)

**URL**: `/historical-price-full/{symbol}?timeseries=365`

**Method**: GET

**Parameters**:
- `symbol`: 종목 티커
- `timeseries`: 365 (최근 365일)
- `apikey`: FMP API key

**Example Request**:
```bash
curl "https://financialmodelingprep.com/api/v3/historical-price-full/AAPL?timeseries=365&apikey=YOUR_KEY"
```

**사용 필드**:
```json
{
  "symbol": "AAPL",
  "historical": [
    {
      "date": "2024-01-10",
      "open": 185.16,
      "high": 186.40,     # Daily high ← KEY
      "low": 184.00,      # Daily low ← KEY
      "close": 185.92,    # Close price ← KEY
      "volume": 50123456  # Daily volume ← KEY
    },
    # ... 364 more days
  ]
}
```

**사용 방법**:
- 52-week high 계산: `max(historical[0:252].high)`
- 52-week low 계산: `min(historical[0:252].low)`
- 현재가: `historical[0].close`
- 고점 대비 거리: `(current / 52wk_high - 1) * 100`
- breakout 감지: 최근 high가 52wk_high에 도달/근접 + 거래량 증가

**API Calls**: 종목당 1회

### Endpoint 2: Quote (Real-Time Price)

**URL**: `/quote/{symbol}`

**Method**: GET

**Parameters**:
- `symbol`: 종목 티커(콤마 구분 batch 가능)
- `apikey`: FMP API key

**Example Request**:
```bash
curl "https://financialmodelingprep.com/api/v3/quote/AAPL?apikey=YOUR_KEY"
```

**사용 필드**:
```json
[
  {
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "price": 185.92,               # Current price ← KEY
    "changesPercentage": 1.23,
    "change": 2.25,
    "dayLow": 184.00,
    "dayHigh": 186.40,
    "yearHigh": 198.23,            # 52-week high ← KEY
    "yearLow": 164.08,             # 52-week low ← KEY
    "marketCap": 2913000000000,
    "volume": 50123456,
    "avgVolume": 48000000,         # Average volume ← KEY
    "exchange": "NASDAQ",
    "sector": "Technology"
  }
]
```

**사용 방법**:
- 52-week high/low를 빠르게 얻는 대안
- historical prices보다 빠름(세밀도는 낮음)
- 빠른 초기 스크리닝에 적합, 상세 분석은 historical prices 권장

**API Calls**: 종목당 1회(또는 batch)

### Endpoint 3: Stock News (선택 - New Product 감지)

**URL**: `/stock_news?tickers={symbol}&limit=50`

**Method**: GET

**Parameters**:
- `tickers`: 종목 티커(다중 가능)
- `limit`: 50 (최근 기사)
- `apikey`: FMP API key

**Example Request**:
```bash
curl "https://financialmodelingprep.com/api/v3/stock_news?tickers=AAPL&limit=50&apikey=YOUR_KEY"
```

**사용 필드**:
```json
[
  {
    "symbol": "AAPL",
    "publishedDate": "2024-01-10T14:30:00.000Z",
    "title": "Apple Launches Revolutionary AI Chip",  # ← KEY (keyword search)
    "image": "https://...",
    "site": "Reuters",
    "text": "Apple Inc announced today...",
    "url": "https://..."
  },
  # ... 49 more articles
]
```

**사용 방법**:
- `title` keyword 검색:
  - High impact: "FDA approval", "patent granted", "breakthrough"
  - Moderate: "new product", "product launch", "acquisition"
- catalyst 감지 시 N component 보너스 부여
- **선택 사항**: API 절약을 위해 생략 가능(N은 주로 price action 기반)

**API Calls**: 종목당 1회(선택)

---

## M Component - Market Direction

### Endpoint 1: Quote (Major Indices)

**URL**: `/quote/^GSPC,^IXIC,^DJI`

**Method**: GET

**Parameters**:
- Symbol: `^GSPC` (S&P 500), `^IXIC` (Nasdaq), `^DJI` (Dow Jones)
- 다중 지수 batch 호출 가능
- `apikey`: FMP API key

**Example Request**:
```bash
curl "https://financialmodelingprep.com/api/v3/quote/%5EGSPC,%5EIXIC,%5EDJI?apikey=YOUR_KEY"
```

**사용 필드**:
```json
[
  {
    "symbol": "^GSPC",
    "name": "S&P 500",
    "price": 4783.45,         # Current level ← KEY
    "changesPercentage": 0.85,
    "change": 40.25,
    "dayLow": 4750.20,
    "dayHigh": 4790.10,
    "yearHigh": 4818.62,
    "yearLow": 4103.78,
    "marketCap": null,
    "volume": null,
    "avgVolume": null
  },
  # IXIC, DJI...
]
```

**사용 방법**:
- 현재 S&P 500 가격 확인
- 50-day EMA와 비교해 추세 판단

**API Calls**: 1회(지수 batch)

### Endpoint 2: Historical Prices (S&P 500 EMA 계산)

**URL**: `/historical-price-full/^GSPC?timeseries=60`

**Method**: GET

**Parameters**:
- Symbol: `^GSPC`
- `timeseries`: 60 (50-day EMA 계산용)
- `apikey`: FMP API key

**Example Request**:
```bash
curl "https://financialmodelingprep.com/api/v3/historical-price-full/%5EGSPC?timeseries=60&apikey=YOUR_KEY"
```

**사용 필드**:
```json
{
  "symbol": "^GSPC",
  "historical": [
    {
      "date": "2024-01-10",
      "close": 4783.45  # ← KEY (for EMA calculation)
    },
    # ... 59 more days
  ]
}
```

**사용 방법**:
- 종가 배열로 50-day EMA 계산
- EMA 공식: `EMA_today = (Price_today * k) + (EMA_yesterday * (1 - k))`, `k = 2/(50+1)`
- 단순화를 위해 SMA 사용도 가능

**API Calls**: 1회(모든 종목 공용)

### Endpoint 3: VIX (Fear Gauge)

**URL**: `/quote/^VIX`

**Method**: GET

**Parameters**:
- Symbol: `^VIX`
- `apikey`: FMP API key

**Example Request**:
```bash
curl "https://financialmodelingprep.com/api/v3/quote/%5EVIX?apikey=YOUR_KEY"
```

**사용 필드**:
```json
[
  {
    "symbol": "^VIX",
    "name": "CBOE Volatility Index",
    "price": 13.24,  # Current VIX level ← KEY
    "changesPercentage": -2.15,
    "change": -0.29
  }
]
```

**사용 방법**:
- VIX < 15: Low fear (bullish)
- VIX 15-20: Normal
- VIX 20-30: Elevated
- VIX > 30: Panic (bear market signal)

**API Calls**: 1회(모든 종목 공용)

---

## L Component - Leadership / Relative Strength (Phase 3)

### Endpoint: Historical Prices (52-Week)

**URL**: `/v3/historical-price-full/{symbol}?timeseries=365`

**목적**: RS Rank 추정을 위해 52주 종목 성과를 S&P 500 benchmark와 비교

**Request**:
```bash
curl "https://financialmodelingprep.com/api/v3/historical-price-full/NVDA?timeseries=365&apikey=YOUR_KEY"
```

**Response Structure**:
```json
{
  "symbol": "NVDA",
  "historical": [
    {
      "date": "2025-01-10",
      "close": 148.50,
      "open": 146.20,
      "high": 149.80,
      "low": 145.90,
      "volume": 250000000
    }
    // ... 364 more days
  ]
}
```

**사용 방법**:
```python
# Stock 52-week performance
current_price = historical[0]['close']
price_52w_ago = historical[-1]['close']  # ~252 trading days
stock_perf = ((current_price / price_52w_ago) - 1) * 100

# Compare vs S&P 500 (^GSPC) for RS calculation
relative_perf = stock_perf - sp500_perf
```

**S&P 500 Benchmark Data**: S&P 500 52주 데이터는 `^GSPC`로 1회 호출 후 공유되며, M component EMA와 L component RS 계산 모두에 사용됩니다. quote와 historical 모두 `^GSPC`를 사용해 가격 스케일 일관성을 유지합니다.

**API Calls**: 종목당 1회 + S&P 500 공유 1회

---

## S Component - Supply and Demand

### Endpoint: Historical Prices (N Component 데이터 재사용)

**URL**: `/v3/historical-price-full/{symbol}?timeseries=90`

**목적**: 거래량 기반 accumulation/distribution 분석

**Data Reuse**: S component는 N component에서 이미 수집한 historical_prices를 재사용합니다. **추가 API 호출 없음**.

**Algorithm**:
```python
# Classify last 60 days into up-days and down-days
for day in last_60_days:
    if close > previous_close:
        up_days.append(volume)
    elif close < previous_close:
        down_days.append(volume)

# Calculate accumulation/distribution ratio
avg_up_volume = sum(up_days) / len(up_days)
avg_down_volume = sum(down_days) / len(down_days)
ratio = avg_up_volume / avg_down_volume
```

**Scoring**:
- Ratio ≥ 2.0: 100 points (Strong Accumulation)
- Ratio 1.5-2.0: 80 points (Accumulation)
- Ratio 1.0-1.5: 60 points (Neutral/Weak Accumulation)
- Ratio 0.7-1.0: 40 points (Neutral/Weak Distribution)
- Ratio 0.5-0.7: 20 points (Distribution)
- Ratio < 0.5: 0 points (Strong Distribution)

**API Calls**: 0회(기존 데이터 재사용)

---

## I Component - Institutional Sponsorship (Phase 2)

### Endpoint: Institutional Holders

**URL**: `/v3/institutional-holder/{symbol}`

**목적**: 기관 holder 수와 ownership % 분석

**Authentication**: FMP API key 필요(free tier 사용 가능)

**Request**:
```bash
curl "https://financialmodelingprep.com/api/v3/institutional-holder/AAPL?apikey=YOUR_KEY"
```

**Response Structure**:
```json
[
  {
    "holder": "Vanguard Group Inc",
    "shares": 1295611697,
    "dateReported": "2024-09-30",
    "change": 12500000,
    "changePercent": 0.0097
  },
  {
    "holder": "Blackrock Inc.",
    "shares": 1042156037,
    "dateReported": "2024-09-30",
    "change": -5234567,
    "changePercent": -0.0050
  },
  {
    "holder": "Berkshire Hathaway Inc",
    "shares": 915560382,
    "dateReported": "2024-09-30",
    "change": 0,
    "changePercent": 0.0000
  }
  // ... hundreds more holders ...
]
```

**Key Fields**:
- `holder`: 기관명
- `shares`: 보유 주식 수
- `dateReported`: 13F 신고일
- `change`: 전분기 대비 변화량
- `changePercent`: 변화율

**Typical Response Size**: 종목당 100-7,000 holders (AAPL 약 7,111)

**Free Tier Availability**: ✅ 사용 가능 (2026-01-12 AAPL 테스트 기준)

**사용 방법**:
```python
# Calculate total institutional ownership
total_shares_held = sum(holder['shares'] for holder in institutional_holders)
ownership_pct = (total_shares_held / shares_outstanding) * 100

# Count unique holders
num_holders = len(institutional_holders)

# Detect superinvestors
SUPERINVESTORS = [
    "BERKSHIRE HATHAWAY",
    "BAUPOST GROUP",
    "PERSHING SQUARE",
    # ...
]
superinvestor_present = any(
    superinvestor in holder['holder'].upper()
    for holder in institutional_holders
    for superinvestor in SUPERINVESTORS
)
```

**Scoring** (O'Neil 기준):
- 50-100 holders + 30-60% ownership: 100점 (sweet spot)
- Superinvestor 존재 + 양호 holder 수: 90점
- 30-50 holders + 20-40% ownership: 80점
- 허용 구간: 60점
- 비최적(<20% 또는 >80% ownership): 40점
- 극단(<10% 또는 >90% ownership): 20점

**API Calls**: 종목당 1회

**Data Freshness**: 분기 업데이트(13F는 분기말 후 45일)

**품질 참고:**
- 대형주: 5,000-10,000 holders
- 중형주: 500-2,000
- 소형주: 50-500
- 초소형주: < 50 (기관 관심 부족 가능성)

---

## API 호출 요약 (종목당)

### Phase 3 (Full CANSLIM: C, A, N, S, L, I, M)

**Per-Stock Calls:**
1. Profile (기업 정보): 1 call
2. Quote (현재 가격): 1 call
3. Income Statement (Quarterly): 1 call
4. Income Statement (Annual): 1 call
5. Historical Prices (90 days): 1 call (N/S 재사용)
6. Historical Prices (365 days): 1 call (L RS 계산용)
7. Institutional Holders: 1 call

**Per-Stock Total**: 7 calls

**Market Data Calls** (세션당 1회):
1. S&P 500 Quote (`^GSPC`): 1 call
2. S&P 500 Historical (`^GSPC`, 365 days): 1 call (M EMA + L RS benchmark 공용)
3. VIX Quote (`^VIX`): 1 call

**Market Data Total**: 3 calls

**중요**: M component EMA 계산의 스케일 일관성을 위해 quote/historical 모두 `^GSPC`를 사용합니다. historical에 SPY(~500), quote에 ^GSPC(~5000)를 혼용하면 약 10배 스케일 불일치가 발생합니다.

**40종목 기준 총 호출:**
- Per-stock: 40 × 7 = 280 calls
- Market data: 3 calls
- **Grand Total: 약 283 calls (free tier 250 초과)** ⚠️

**효율 포인트:**
- S component: 추가 호출 0회(N의 90일 historical 재사용)
- L component: 종목당 +1 call(365일 historical)
- S&P 500 historical: M/L 공용

**Free Tier 우회:** `--max-candidates 35` 사용(35 × 7 + 3 = 248). 40종목은 FMP Starter($29.99/mo, 750/day) 권장.

**`mktCap` 필드 참고**: FMP profile은 `marketCap`이 아닌 `mktCap`을 반환할 수 있으며, 스크리너는 두 필드를 모두 처리합니다.

---

## Rate Limiting 전략

### 구현 예시

```python
import time

def rate_limited_get(url, params):
    """Enforce 0.3s delay between requests (200 requests/minute max)"""
    response = requests.get(url, params=params)
    time.sleep(0.3)  # 300ms delay
    return response
```

### 429 에러 처리

```python
def handle_rate_limit(response):
    """Retry once with 60-second wait if rate limit hit"""
    if response.status_code == 429:
        print("WARNING: Rate limit exceeded. Waiting 60 seconds...")
        time.sleep(60)
        return True  # Signal to retry
    return False  # No retry needed
```

### Free Tier 관리

**일일 쿼터**: 250 requests/day

**쿼터 내 운영 전략:**
1. **Batch call 활용**: quote endpoint에서 콤마 구분 다중 symbol
2. **Market data 캐싱**: S&P 500/VIX 1회 호출 후 재사용
3. **선택 endpoint 생략**: 뉴스 endpoint는 생략 가능(40 calls 절약)
4. **유니버스 제한**: free tier는 35종목, 40종목은 Starter tier
5. **Progressive filtering**: 저비용 필터(시총/섹터) 먼저 적용

---

## 에러 처리

### 공통 에러

**401 Unauthorized**:
- 원인: API key 누락/오류
- 해결: `apikey` 파라미터와 환경변수 확인

**404 Not Found**:
- 원인: 잘못된 symbol 또는 endpoint
- 해결: 티커/URL 검증

**429 Too Many Requests**:
- 원인: 분/일 rate limit 초과
- 해결: 60초 대기(분 제한) 또는 24시간(일 제한)

**500 Internal Server Error**:
- 원인: FMP 서버 이슈
- 해결: 5초 후 재시도, 지속 시 종목 건너뛰기

**Empty Response `[]`**:
- 원인: 데이터 없음(신규 IPO, 상폐 등)
- 해결: 종목 건너뛰고 warning 기록

### Retry 로직

```python
MAX_RETRIES = 1
retry_count = 0

while retry_count <= MAX_RETRIES:
    response = make_request()
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        time.sleep(60)
        retry_count += 1
    else:
        print(f"ERROR: {response.status_code}")
        return None

print("ERROR: Max retries exceeded")
return None
```

---

## 데이터 품질 고려사항

### Freshness

- **Quarterly/Annual Data**: 실적 발표 후 1-2일 내 갱신
- **Price Data**: 준실시간(Free tier는 약 15분 지연)
- **News Data**: 수시 갱신

### Completeness

- **Large-cap**: 과거 데이터 완전성 높음(10년+)
- **Mid-cap**: 대체로 충분(보통 5년+)
- **Small-cap/Recent IPO**: 공백 가능성(<2년)

### Validation

항상 점검:
- 핵심 필드(EPS, revenue)의 `null`/`0`
- 성장률 계산 시 EPS 음수 처리(분모 절댓값)
- 누락 분기(상폐/특수 상황)

---

## 예시 API 호출 시퀀스

NVDA 분석 예시:

```bash
# 1. Quarterly income statement (C component)
curl "https://financialmodelingprep.com/api/v3/income-statement/NVDA?period=quarter&limit=8&apikey=YOUR_KEY"

# 2. Annual income statement (A component)
curl "https://financialmodelingprep.com/api/v3/income-statement/NVDA?period=annual&limit=5&apikey=YOUR_KEY"

# 3. Historical prices (N component)
curl "https://financialmodelingprep.com/api/v3/quote/NVDA?apikey=YOUR_KEY"

# 4. S&P 500 for market direction (M component - once per session)
curl "https://financialmodelingprep.com/api/v3/quote/%5EGSPC&apikey=YOUR_KEY"
curl "https://financialmodelingprep.com/api/v3/historical-price-full/%5EGSPC?timeseries=60&apikey=YOUR_KEY"
curl "https://financialmodelingprep.com/api/v3/quote/%5EVIX&apikey=YOUR_KEY"
```

**총합**: 종목당 7 calls + market 공용 3 calls

---

## 비용 분석

### Free Tier (250 requests/day)

- **40 stocks × 7 calls = 280 calls**
- **Market data: 3 calls**
- **Total: 약 283 calls (250 초과)** ⚠️
- **우회안**: `--max-candidates 35` (35 × 7 + 3 = 248)

### Paid Tiers

- **Starter ($29.99/month)**: 750 calls/day → 1회당 약 106종목
- **Professional ($79.99/month)**: 2000 calls/day → 1회당 약 285종목

**Phase 3 권장**: Free tier는 `--max-candidates 35`까지. 기본 40종목은 Starter tier 권장.

---

이 API 레퍼런스는 Phase 3(Full CANSLIM) 구현에 필요한 전체 문서를 제공합니다. Free tier 사용자는 일일 250 calls 제한 내 운영을 위해 `--max-candidates 35` 사용을 권장합니다.
