# Financial Modeling Prep (FMP) API 가이드

## 개요

Financial Modeling Prep은 주식, forex, crypto 등 폭넓은 금융 데이터 API를 제공합니다. 이 가이드는 RSI 기술 지표를 결합한 배당 성장주 스크리닝에 사용되는 endpoint를 중심으로 설명합니다.

### Two-Stage 스크리닝 접근

이 스크리너는 두 가지 모드를 지원합니다:

**1. Two-Stage (FINVIZ + FMP) - 권장**
- **Stage 1**: FINVIZ Elite API가 RSI 필터로 사전 스크리닝(1 API call → 10-50 후보)
- **Stage 2**: FMP API가 사전 선별 후보에 상세 펀더멘털 분석 수행
- **장점**: FINVIZ의 기술적 필터를 활용해 FMP API 호출을 크게 절감
- **비용**: FINVIZ Elite $40/month + FMP free tier

**2. FMP-Only (기존 방식)**
- **Single Stage**: FMP stock-screener + 상세 분석
- **제약**: FMP free tier(250 requests/day)로 약 40종목 제한
- **비용**: FMP free tier(업그레이드 가능)

**권장안**: 정기 스크리닝(일/주)에서는 Two-Stage 접근이 비용을 낮추면서 커버리지를 최대화합니다.

## API Key 설정

### API Key 발급

1. https://financialmodelingprep.com/developer/docs 방문
2. 무료 계정 가입
3. Dashboard → API Keys 이동
4. API key 복사

### Free Tier 제한

- **일 250 requests**
- **Rate limit**: 초당 약 5 requests
- **신용카드 불필요**
- 일/주 단위 스크리닝에 충분

### Paid Tiers (선택)

- **Starter ($14/month)**: 500 requests/day
- **Professional ($29/month)**: 1,000 requests/day
- **Enterprise ($99/month)**: 10,000 requests/day

## API Key 지정

### 방법 1: Environment Variable (권장)

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

**영구 설정(shell profile 추가):**
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export FMP_API_KEY=your_api_key_here' >> ~/.bashrc
source ~/.bashrc
```

### 방법 2: Command-Line Argument

```bash
python3 scripts/screen_dividend_growth_rsi.py --fmp-api-key your_api_key_here
```

## FINVIZ API 설정 (선택 - Two-Stage용)

### FINVIZ Elite API Key 발급

1. https://elite.finviz.com 방문
2. FINVIZ Elite 구독($40/month 또는 $400/year)
3. Settings → API 이동
4. API key 복사

### FINVIZ API Key 지정

**Environment Variable (권장):**
```bash
export FINVIZ_API_KEY=your_finviz_key_here
```

**Command-Line Argument:**
```bash
python3 screen_dividend_growth_rsi.py --use-finviz --finviz-api-key YOUR_KEY
```

### FINVIZ 사전 스크리닝 필터

`--use-finviz` 사용 시 FINVIZ Elite API에서 아래 필터를 적용합니다:

- **Market Cap**: Mid-cap 이상(≥$2B)
- **Dividend Yield**: 0.5-3% (배당 성장주 포착, 고배당 REITs/utilities 제외)
- **Dividend Growth (3Y)**: 10%+ (FMP가 12%+ 최종 검증)
- **EPS Growth (3Y)**: 5%+ (양의 이익 모멘텀)
- **Sales Growth (3Y)**: 5%+ (양의 매출 모멘텀)
- **RSI (14-period)**: 40 미만(과매도/눌림)
- **Geography**: USA

**출력**: 상세 분석을 위해 FMP로 전달할 종목 심볼 집합(보통 30-50개).

**균형 필터 근거:**
- 10%+ 배당 성장은 고품질 배당 복리주를 보장
- 5%+ EPS/sales 성장은 성숙 배당주가 아닌 성장 기업을 포착
- 0.5-3% 수익률 범위는 성숙 고배당주(>4%)를 배제하고 성장주에 집중
- FINVIZ 후보를 약 90개에서 약 30-50개로 축소
- 효율적 분석으로 FMP free tier 한도(250 requests/day) 내 유지

## 주요 사용 Endpoints

### 1. Stock Screener

**Endpoint:** `/v3/stock-screener`

**목적:** 시가총액/거래소 기준 초기 필터링

**파라미터:**
- `marketCapMoreThan`: 최소 시가총액(예: 2000000000 = $2B)
- `exchange`: 포함 거래소(예: "NASDAQ,NYSE")
- `limit`: 최대 결과 수(기본 1000)

**참고:** 이 screener는 배당수익률 사전 필터를 적용하지 않습니다(value-dividend-screener와 다름). 더 넓은 유니버스를 가져온 후 배당 이력 기반 실제 수익률을 계산해 정확성을 확보합니다.

**요청 예시:**
```
https://financialmodelingprep.com/api/v3/stock-screener?
  marketCapMoreThan=2000000000&
  exchange=NASDAQ,NYSE&
  limit=1000&
  apikey=YOUR_API_KEY
```

**응답 형식:**
```json
[
  {
    "symbol": "AAPL",
    "companyName": "Apple Inc.",
    "marketCap": 2800000000000,
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "price": 185.50,
    "exchange": "NASDAQ",
    "isActivelyTrading": true
  }
]
```

### 2. Historical Dividend

**Endpoint:** `/v3/historical-price-full/stock_dividend/{symbol}`

**목적:** 성장률 계산 및 수익률 검증을 위한 배당 이력

**요청 예시:**
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

**스크립트 사용 방식:**
- 연도별 배당 총합 집계(해당 연도 지급 배당 합산)
- 3년 배당 CAGR 계산: `((Div_Year3 / Div_Year0) ^ (1/3) - 1) × 100`
- 최신 연 배당금 추출(수익률 계산용)
- 배당 일관성 검증(연도별 유의미한 삭감 없음)

### 3. Historical Prices (RSI용 신규)

**Endpoint:** `/v3/historical-price-full/{symbol}`

**목적:** RSI 계산용 일별 가격 데이터

**파라미터:**
- `symbol`: 종목 ticker
- `timeseries`: 조회 일수(예: 30)

**요청 예시:**
```
https://financialmodelingprep.com/api/v3/historical-price-full/AAPL?
  timeseries=30&
  apikey=YOUR_API_KEY
```

**응답 형식:**
```json
{
  "symbol": "AAPL",
  "historical": [
    {
      "date": "2024-11-01",
      "open": 184.50,
      "high": 186.20,
      "low": 183.80,
      "close": 185.50,
      "adjClose": 185.50,
      "volume": 45000000,
      "unadjustedVolume": 45000000,
      "change": 1.00,
      "changePercent": 0.54,
      "vwap": 185.10,
      "label": "November 01, 24",
      "changeOverTime": 0.0054
    }
  ]
}
```

**스크립트 사용 방식:**
- 최근 30일 `close` 가격 추출
- 시간순 정렬(과거 → 현재)
- 14-period RSI 계산:
  1. 가격 변화 계산(close[i] - close[i-1])
  2. 상승폭/하락폭 분리
  3. 14기간 평균 상승폭/하락폭 계산
  4. RS = Average Gain / Average Loss
  5. RSI = 100 - (100 / (1 + RS))

**RSI 필터:** RSI > 40 종목은 제외(과매도/눌림 아님)

### 4. Income Statement

**Endpoint:** `/v3/income-statement/{symbol}`

**목적:** 매출, EPS, 순이익 분석

**파라미터:**
- `symbol`: 종목 ticker(예: "AAPL")
- `limit`: 기간 수(예: 5년이면 5)
- `period`: "annual"(기본)

**요청 예시:**
```
https://financialmodelingprep.com/api/v3/income-statement/AAPL?
  limit=5&
  apikey=YOUR_API_KEY
```

**주요 사용 필드:**
- `revenue`: 총매출
- `eps`: 주당순이익
- `netIncome`: 순이익(payout ratio 계산용)
- `date`: 회계 기간 종료일

**스크립트 사용 방식:**
- 3년 매출 CAGR 계산(통과 조건: 양수)
- 3년 EPS CAGR 계산(통과 조건: 양수)
- 순이익 추출(payout ratio 계산용)

### 5. Balance Sheet Statement

**Endpoint:** `/v3/balance-sheet-statement/{symbol}`

**목적:** 부채, 자본, 유동성 분석

**파라미터:**
- `symbol`: 종목 ticker
- `limit`: 기간 수(보통 5)

**주요 사용 필드:**
- `totalDebt`: 총부채(단기+장기)
- `totalStockholdersEquity`: 자기자본
- `totalCurrentAssets`: 유동자산
- `totalCurrentLiabilities`: 유동부채

**스크립트 사용 방식:**
- Debt-to-Equity: totalDebt / totalStockholdersEquity (2.0 미만 필요)
- Current Ratio: totalCurrentAssets / totalCurrentLiabilities (1.0 초과 필요)
- 재무건전성 체크(두 비율 모두 통과 필요)

### 6. Cash Flow Statement

**Endpoint:** `/v3/cash-flow-statement/{symbol}`

**목적:** 배당 지속 가능성 평가를 위한 Free Cash Flow 분석

**파라미터:**
- `symbol`: 종목 ticker
- `limit`: 기간 수

**주요 사용 필드:**
- `freeCashFlow`: Free cash flow (OCF - Capex)
- `dividendsPaid`: 실제 배당 지급액(음수 값)

**스크립트 사용 방식:**
- FCF Payout Ratio: dividendsPaid / freeCashFlow
- 현금 창출로 배당이 커버되는지 검증(100% 미만이 지속 가능)

### 7. Key Metrics

**Endpoint:** `/v3/key-metrics/{symbol}`

**목적:** ROE, 이익률, 밸류에이션 비율

**파라미터:**
- `symbol`: 종목 ticker
- `limit`: 기간 수(최신값이면 보통 1)

**주요 사용 필드:**
- `roe`: Return on Equity (소수, 예: 0.15 = 15%)
- `netProfitMargin`: 순이익률(소수)
- `peRatio`: Price-to-Earnings 비율
- `pbRatio`: Price-to-Book 비율
- `numberOfShares`: 발행주식수(payout ratio 계산용)

**스크립트 사용 방식:**
- ROE: 종합 점수의 품질 지표(높을수록 우수)
- Profit Margin: 수익성 지표
- P/E, P/B: 참고용(배제 조건 없음)
- Number of Shares: 총배당 지급액 계산에 사용

## Rate Limiting 전략

### 내장 보호 기능

스크리닝 스크립트에는 다음 rate limiting 보호가 포함됩니다:
- 요청 간 **0.3초 지연**(~초당 3회)
- 429(한도 초과) 발생 시 **자동 재시도**(60초 backoff)
- 요청당 **timeout 30초**
- **graceful degradation**: 한도 도달 시 분석 중단 후 부분 결과 반환

### 요청 예산 관리

Free tier(250 requests/day) 기준:

**종목당 필요한 requests:**
- Stock Screener: 1 request(100-1000종목 반환)
- Dividend History: 심볼당 1
- Historical Prices (RSI): 심볼당 1
- Income Statement: 심볼당 1
- Balance Sheet: 심볼당 1
- Cash Flow: 심볼당 1
- Key Metrics: 심볼당 1

**합계: 심볼당 6 requests + screener 1 request**

**예산 배분:**
- 초기 screener: 1 request
- 상세 분석: 6 × N 종목 = 6N requests
- **실행당 최대 종목 수**: (250 - 1) / 6 = 약 41개

**FMP-Only 모드 최적화**: `--max-candidates`로 분석 대상을 제한:
```bash
python3 screen_dividend_growth_rsi.py --max-candidates 40
```

**Two-Stage 모드 (권장):**

FINVIZ 사전 스크리닝(`--use-finviz`) 사용 시:

**요청 구성:**
- FINVIZ 사전 스크린: FINVIZ API 1회 → 10-50 심볼
- FMP quote 조회: 심볼당 1 request(현재가)
- FMP 상세 분석: 심볼당 6 requests(dividend, prices, income, balance, cashflow, metrics)

**FMP 총 requests:**
- 10개 심볼: 10 + (6 × 10) = 70
- 30개 심볼: 30 + (6 × 30) = 210
- 50개 심볼: 50 + (6 × 50) = 350 (free tier 초과)

**장점:** FINVIZ RSI 필터는 보통 10-30종목을 반환(1000개 아님)하므로 FMP free tier 내 분석이 현실적입니다.

**비용 비교:**
- **FMP Starter Plan** ($14/month, 500 requests): 약 80종목/일
- **FINVIZ Elite + FMP Free** ($40/month, 250 FMP requests): RSI 사전 필터 기준 약 30종목/일
- **결론**: 물량은 적어도 FINVIZ 접근은 RSI 사전 필터로 후보 품질이 높음

### Best Practices

1. **정기 스크리닝은 FINVIZ two-stage 사용**: 후보 품질을 높이고 FMP free tier 한도 내 유지
2. **일회성 분석은 FMP-only 사용**: FINVIZ 구독이 없거나 테스트 목적에 적합
3. **비혼잡 시간대 실행**: rate limit 충돌 가능성 감소
4. **실행 간격 확보**: 시간당 다회 실행보다 일/주 단위 실행
5. **결과 캐시**: JSON 출력 저장 후 로컬 분석
6. **필요 시 업그레이드**: 하루 30종목 이상이면 FMP Starter($14/month) 고려

## 오류 처리

### 자주 발생하는 오류

**1. Invalid API Key**
```json
{
  "Error Message": "Invalid API KEY. Please retry or visit our documentation."
}
```
**해결:** API key 확인 및 FMP dashboard 활성 상태 검증

**2. Rate Limit Exceeded (429)**
```json
{
  "Error Message": "You have exceeded the rate limit. Please wait."
}
```
**해결:** 스크립트는 60초 후 1회 자동 재시도. 지속되면 24시간 후 limit reset 대기.

**3. Symbol Not Found**
```json
{
  "Error Message": "Invalid ticker symbol"
}
```
**해결:** 스크립트가 해당 심볼을 건너뛰고 계속 진행(상장폐지/오류 ticker에서 일반적)

**4. RSI용 가격 데이터 부족**
- 빈 배열 또는 가격 데이터 < 20일
**해결:** 스크립트가 해당 심볼 건너뜀(신규 상장, 저유동성, 데이터 공백에서 흔함)

**5. 배당 데이터 부족**
- 배당 이력 없음 또는 4년 미만
**해결:** 스크립트가 해당 심볼 건너뜀(3년 CAGR 계산을 위해 4년+ 필요)

### 디버깅

**요청 수 확인:**
```bash
# Count API calls in script output
python3 scripts/screen_dividend_growth_rsi.py 2>&1 | grep "Analyzing" | wc -l
```

**Rate limit 상태 모니터링:**
스크립트는 limit 근접 시 경고 출력:
```
⚠️  API rate limit reached after analyzing 41 stocks.
Returning results collected so far: 3 qualified stocks
```

**Verbose debugging (필요 시):**
스크립트 상단에 추가:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 데이터 품질 고려사항

### 데이터 신선도

- **연간 재무제표**: 회계연도 종료 후 업데이트(지연 가능)
- **실시간 가격**: 시장 시간 중 업데이트
- **배당 이력**: 공시/지급 후 업데이트
- **RSI 계산**: 최근 30일 가격 데이터 기반

### 데이터 공백

일부 종목은 다음 문제가 있을 수 있습니다:
- **가격 이력 불충분**: 30일 미만(신규 상장, 거래 정지)
- **배당 데이터 누락**: 모든 배당주가 API에 완전 보고되지 않음
- **지표 불일치**: 회계 기준 차이, 재작성(restatement)
- **조정 가격 영향**: 주식분할/배당이 과거 가격에 반영

**스크립트 동작:** 데이터 부족 종목은 건너뜁니다(배당 4년+, 가격 30일+ 필요).

### 데이터 정확성

FMP의 데이터 소스:
- SEC EDGAR filings (미국 기업)
- 거래소 data feeds (실시간 가격)
- 기업 IR 자료

**참고:** 중요한 투자 판단은 반드시 아래와 교차 검증하세요:
- sec.gov의 10-K, 10-Q
- 기업 IR 웹사이트
- 복수 데이터 소스

### RSI 계산 정확도

**입력:**
- 종가 30일(14-period RSI + 여유 버퍼)
- 표준 14-period RSI 공식

**잠재 이슈:**
- **데이터 공백**: 주말/휴일/거래정지(스크립트는 가용 데이터 사용)
- **분할 조정**: FMP 조정 가격 제공(정상 동작)
- **장중 변동성**: RSI는 종가만 사용(고가/저가 미반영)

**검증:** TradingView, Yahoo Finance 등과 계산 RSI를 비교해 정확도 점검.

## 스크리닝 워크플로

### 요청 시퀀스

```
1. Stock Screener (1 request)
   ↓ Returns 100-1000 candidates

For each candidate (up to max-candidates limit):

2. Dividend History (1 request)
   ↓ Calculate dividend yield and CAGR
   ↓ If yield < 1.5% or CAGR < 12% → Skip

3. Historical Prices (1 request)
   ↓ Calculate RSI
   ↓ If RSI > 40 → Skip

4. Income Statement (1 request)
   ↓ Calculate revenue/EPS growth
   ↓ If negative growth → Skip

5. Balance Sheet (1 request)
   ↓ Check financial health
   ↓ If unhealthy ratios → Skip

6. Cash Flow (1 request)
   ↓ Calculate FCF payout ratio

7. Key Metrics (1 request)
   ↓ Extract ROE, margins, valuation

8. Composite Scoring
   ↓ Rank qualified stocks

9. Output JSON + Markdown Report
```

**최적화:** 조기 탈락이 API 호출을 줄입니다. 배당/RSI(2-3단계)에서 탈락하면 이후 4개 API 호출은 생략됩니다.

## API 문서

**공식 문서**: https://financialmodelingprep.com/developer/docs

**핵심 섹션:**
- Stock Fundamentals API
- Stock Screener API
- Historical Dividend API
- Historical Price API
- Ratios API

**지원**: support@financialmodelingprep.com

## 대체 데이터 소스

FMP 제한이 엄격할 경우:

1. **Alpha Vantage**: free tier, 500 requests/day, RSI endpoint 제공
2. **Yahoo Finance (yfinance)**: 무료, 사실상 무제한, Python 라이브러리
3. **Quandl/Nasdaq Data Link**: free tier로 펀더멘털 데이터 일부 제공
4. **IEX Cloud**: free tier, 50k messages/month

**구현 참고:**
- 대체 소스는 데이터 형식이 달라 스크립트 수정 필요
- Yahoo Finance(yfinance)는 RSI 계산 도구 활용 가능
- Alpha Vantage는 technical indicators 전용 endpoint 제공

**yfinance 예시 (무료 대안):**
```python
import yfinance as yf

# Get stock data
ticker = yf.Ticker("AAPL")

# Dividend history
dividends = ticker.dividends

# Historical prices
prices = ticker.history(period="1mo")

# Calculate RSI manually or use TA-Lib
```

**트레이드오프:**
- FMP: 구조화/포괄적/요청 제한 있음
- yfinance: 무료/무제한/안정성 낮음(Yahoo API 변경 빈번)
- Alpha Vantage: 기술 지표 강점, 펀더멘털은 제한적

## 문제 해결

### "No Results Found"

**가능한 원인:**
1. 모든 종목이 RSI 체크에서 탈락(시장 과매도 아님)
2. 높은 배당 성장(12%+) 자체가 희소
3. 통과 종목 찾기 전에 API limit 도달

**해결 방법:**
- RSI 완화: `--rsi-max 45`
- 배당 성장 기준 완화: `--min-div-growth 10.0`
- rate limit 절약 위해 후보 축소: `--max-candidates 30`
- 시장 조정 구간에서 확인(과매도 기회 증가)

### "Rate Limit Reached Quickly"

**원인:**
- 오늘 이미 다른 용도로 API 사용
- 통과 종목 찾기 전 많은 종목을 분석
- API limit reset 시점 미도래(UTC 자정 리셋)

**해결 방법:**
- 24시간 후 limit reset 대기
- `--max-candidates 30`으로 요청 절약
- paid tier 업그레이드(500 requests/day는 $14/month)
- FMP dashboard에서 현재 사용량 확인

### "RSI Calculation Errors"

**원인:**
- 종목의 거래 이력이 20일 미만
- 데이터 공백(거래정지, 신규 상장)
- API가 불완전한 가격 데이터 반환

**해결:**
스크립트는 해당 종목을 경고와 함께 자동으로 건너뜁니다:
```
⚠️  Insufficient price data for RSI calculation
```

별도 조치가 필요 없는 정상 동작입니다.

---

**Last Updated**: November 2025
**Script Version**: 1.0
**FMP API Version**: v3
