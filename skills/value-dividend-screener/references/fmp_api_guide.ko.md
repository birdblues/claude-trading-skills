# Financial Modeling Prep (FMP) API 가이드

## 개요

Financial Modeling Prep는 주식, 외환, 암호화폐 등 다양한 자산을 위한 종합 financial data API를 제공합니다. 이 가이드는 배당주 스크리닝에 사용되는 endpoint에 초점을 맞춥니다.

## API Key 설정

### API Key 발급

1. https://financialmodelingprep.com/developer/docs 방문
2. 무료 계정 가입
3. Dashboard → API Keys로 이동
4. API key 복사

### Free Tier 제한

- **하루 250 requests**
- **Rate limit**: 초당 약 5 requests
- **신용카드 불필요**
- 일간/주간 스크리닝 실행에 충분

### 유료 Tier (선택사항)

- **Starter ($14/month)**: 500 requests/day
- **Professional ($29/month)**: 1,000 requests/day
- **Enterprise ($99/month)**: 10,000 requests/day

## API Key 설정 방법

### Method 1: Environment Variable (권장)

**Linux/macOS:**
```bash
export FMP_API_KEY=your_api_key_here
```

**Windows (Command Prompt):**
```cmd
set FMP_API_KEY=your_api_key_here
```

**Windows (PowerShell):**
```powershell
$env:FMP_API_KEY="your_api_key_here"
```

**Persistent (shell profile에 추가):**
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export FMP_API_KEY=your_api_key_here' >> ~/.bashrc
source ~/.bashrc
```

### Method 2: Command-Line Argument

```bash
python3 scripts/screen_dividend_stocks.py --api-key your_api_key_here
```

## 사용되는 주요 Endpoints

### 1. Stock Screener

**Endpoint:** `/v3/stock-screener`

**용도:** dividend yield, P/E, P/B, market cap 기준 1차 필터링

**파라미터:**
- `dividendYieldMoreThan`: 최소 dividend yield (예: 3.5)
- `priceEarningRatioLowerThan`: 최대 P/E ratio (예: 20)
- `priceToBookRatioLowerThan`: 최대 P/B ratio (예: 2)
- `marketCapMoreThan`: 최소 market cap (예: 2000000000 = $2B)
- `exchange`: 포함할 거래소 (예: "NASDAQ,NYSE")
- `limit`: 최대 결과 수 (기본값: 1000)

**예시 요청:**
```
https://financialmodelingprep.com/api/v3/stock-screener?
  dividendYieldMoreThan=3.5&
  priceEarningRatioLowerThan=20&
  priceToBookRatioLowerThan=2&
  marketCapMoreThan=2000000000&
  exchange=NASDAQ,NYSE&
  limit=1000&
  apikey=YOUR_API_KEY
```

**응답 형식:**
```json
[
  {
    "symbol": "T",
    "companyName": "AT&T Inc.",
    "marketCap": 150000000000,
    "sector": "Communication Services",
    "industry": "Telecom Services",
    "beta": 0.65,
    "price": 20.50,
    "lastAnnualDividend": 1.11,
    "volume": 35000000,
    "exchange": "NYSE",
    "exchangeShortName": "NYSE",
    "country": "US",
    "isEtf": false,
    "isActivelyTrading": true,
    "dividendYield": 0.0541,
    "pe": 7.5,
    "priceToBook": 1.2
  }
]
```

### 2. Income Statement

**Endpoint:** `/v3/income-statement/{symbol}`

**용도:** revenue, EPS, net income 분석

**파라미터:**
- `symbol`: 주식 ticker (예: "AAPL")
- `limit`: 기간 개수 (예: 5년이면 5)
- `period`: "annual" 또는 "quarter"

**예시 요청:**
```
https://financialmodelingprep.com/api/v3/income-statement/AAPL?
  limit=5&
  apikey=YOUR_API_KEY
```

**사용하는 핵심 필드:**
- `revenue`: 총매출
- `eps`: 주당순이익
- `netIncome`: 순이익
- `date`: 회계기간 종료일

### 3. Balance Sheet Statement

**Endpoint:** `/v3/balance-sheet-statement/{symbol}`

**용도:** 부채, 자본, 유동성 분석

**파라미터:**
- `symbol`: 주식 ticker
- `limit`: 기간 개수

**사용하는 핵심 필드:**
- `totalDebt`: 총부채(단기 + 장기)
- `totalStockholdersEquity`: 주주자본
- `totalCurrentAssets`: 유동자산
- `totalCurrentLiabilities`: 유동부채

### 4. Cash Flow Statement

**Endpoint:** `/v3/cash-flow-statement/{symbol}`

**용도:** free cash flow, 지급배당 분석

**파라미터:**
- `symbol`: 주식 ticker
- `limit`: 기간 개수

**사용하는 핵심 필드:**
- `operatingCashFlow`: 영업활동현금흐름
- `capitalExpenditure`: 설비투자(Capex, 음수값)
- `dividendsPaid`: 지급배당(음수값)
- `freeCashFlow`: OCF - Capex

### 5. Key Metrics

**Endpoint:** `/v3/key-metrics/{symbol}`

**용도:** ROE, ROA 및 기타 품질 지표

**파라미터:**
- `symbol`: 주식 ticker
- `limit`: 기간 개수

**사용하는 핵심 필드:**
- `roe`: 자기자본이익률(소수, 예: 0.15 = 15%)
- `roa`: 총자산이익률
- `roic`: 투하자본수익률
- `debtToEquity`: 부채비율(debt-to-equity)
- `currentRatio`: 유동비율

### 6. Historical Dividend

**Endpoint:** `/v3/historical-price-full/stock_dividend/{symbol}`

**용도:** 성장률 계산을 위한 배당 이력

**예시 요청:**
```
https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/AAPL?
  apikey=YOUR_API_KEY
```

**응답 형식:**
```json
{
  "symbol": "AAPL",
  "historical": [
    {
      "date": "2024-11-08",
      "label": "November 08, 24",
      "adjDividend": 0.25,
      "dividend": 0.25,
      "recordDate": "2024-11-11",
      "paymentDate": "2024-11-14",
      "declarationDate": "2024-10-31"
    }
  ]
}
```

## Rate Limiting 전략

### 내장 보호 기능

스크리닝 스크립트는 다음과 같은 rate limiting을 포함합니다:
- requests 간 **0.3초 지연**(초당 약 3 requests)
- 429(rate limit 초과) 발생 시 60초 backoff 후 **자동 재시도**
- request당 **timeout**: 30초

### Request Budget 관리

free tier(250 requests/day) 기준:

**분석 종목 1개당 요청 수:**
- Stock Screener: 1 request (100-1000개 종목 반환)
- Income Statement: symbol당 1 request
- Balance Sheet: symbol당 1 request
- Cash Flow: symbol당 1 request
- Key Metrics: symbol당 1 request
- Dividend History: symbol당 1 request

**합계: symbol당 5 requests + screener 1 request**

**예산 배분:**
- 초기 screener: 1 request
- 상세 분석: 5 × N stocks = 5N requests
- **1회 실행 최대 종목 수**: (250 - 1) / 5 = 약 49 stocks

**스크립트 기본값**: 첫 100개 후보를 분석하지만, 보통 모든 기준을 통과하는 종목은 약 20-30개입니다.

### Best Practices

1. **비혼잡 시간대 실행**: rate limit 발생 가능성 감소
2. **실행 간격 확보**: 시간당 여러 번 대신 일간/주간 실행
3. **결과 캐시**: JSON 출력을 저장하고 로컬에서 분석
4. **필요 시 업그레이드**: 대규모 유니버스를 자주 스크리닝하면 유료 tier 고려

## Error Handling

### 공통 오류

**1. Invalid API Key**
```json
{
  "Error Message": "Invalid API KEY. Please retry or visit our documentation."
}
```
**해결**: API key 확인, FMP dashboard에서 활성 상태 검증

**2. Rate Limit Exceeded (429)**
```json
{
  "Error Message": "You have exceeded the rate limit. Please wait."
}
```
**해결**: 스크립트가 60초 후 자동 재시도

**3. Symbol Not Found**
```json
{
  "Error Message": "Invalid ticker symbol"
}
```
**해결**: 스크립트가 해당 symbol을 건너뛰고 계속 진행(상장폐지/유효하지 않은 ticker에서 정상적으로 발생 가능)

**4. Insufficient Data**
- 재무제표에서 빈 배열 반환
**해결**: 스크립트가 해당 symbol을 건너뜀(신규 상장 또는 데이터 불완전 종목에서 흔함)

### 디버깅

**요청 수 확인:**
```bash
# Count API calls in script output
python3 scripts/screen_dividend_stocks.py 2>&1 | grep "Analyzing" | wc -l
```

**Verbose mode (필요 시 스크립트에 추가):**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 데이터 품질 고려사항

### 데이터 최신성

- **연간 재무제표**: 회계연도 종료 후 업데이트(지연 가능)
- **분기 데이터**: 분기 종료 후 약 1-2개월 내 제공
- **실시간 가격**: 장중 업데이트
- **배당 이력**: 선언/지급 이후 업데이트

### 데이터 결측

일부 종목은 다음 문제가 있을 수 있습니다:
- **불완전한 이력**: 데이터 4년 미만(신규 상장 기업)
- **누락 배당 데이터**: 모든 배당주가 API를 통해 보고되지는 않음
- **지표 불일치**: 회계기준 차이, 정정 공시 등

**스크립트 동작**: 데이터가 불충분한 종목은 건너뜀(4년 이상 데이터 필요)

### 데이터 정확성

FMP 데이터 소스:
- SEC EDGAR filings(미국 기업)
- 기업 IR 자료
- 거래소 데이터 피드

**참고**: 중요한 투자 의사결정은 반드시 기업 공시(10-K, 10-Q)로 재검증하세요.

## API 문서

**공식 문서**: https://financialmodelingprep.com/developer/docs

**주요 섹션:**
- Stock Fundamentals API
- Stock Screener API
- Historical Dividend API
- Ratios API

**지원**: support@financialmodelingprep.com

## 대체 데이터 소스

FMP 제한이 제약이 된다면:

1. **Alpha Vantage**: Free tier, 500 requests/day
2. **Yahoo Finance (yfinance)**: 무료, 무제한(단, 신뢰도는 낮을 수 있음)
3. **Quandl/Nasdaq Data Link**: Free tier 제공
4. **IEX Cloud**: Free tier, 월 50k messages

**참고**: 대체 소스는 데이터 형식이 달라 스크립트 수정이 필요할 수 있습니다.
