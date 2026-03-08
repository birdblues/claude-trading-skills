# VCP 스크리너에서 사용하는 FMP API 엔드포인트

## 엔드포인트

### 1. S&P 500 구성 종목
- **URL:** `GET /api/v3/sp500_constituent`
- **Calls:** 1 (cached)
- **Returns:** `[{symbol, name, sector, subSector}, ...]`
- **Used in:** Phase 1 - 유니버스 정의

### 2. 배치 시세
- **URL:** `GET /api/v3/quote/{symbols}` (comma-separated, max 5)
- **Calls:** ~101 (503 stocks / 5 per batch)
- **Returns:** `[{symbol, price, yearHigh, yearLow, avgVolume, marketCap, ...}]`
- **Used in:** Phase 1 - Pre-filter

### 3. 과거 가격
- **URL:** `GET /api/v3/historical-price-full/{symbol}?timeseries=260`
- **Calls:** 1 (SPY) + up to 100 (candidates)
- **Returns:** `{symbol, historical: [{date, open, high, low, close, adjClose, volume}, ...]}`
- **Used in:** Phase 2 - Trend Template, Phase 3 - VCP detection

## API 예산 요약

| Phase | Operation | API Calls |
|-------|-----------|-----------|
| 1 | S&P 500 constituents | 1 |
| 1 | Batch quotes (503 / 5) | ~101 |
| 2 | SPY 260-day history | 1 |
| 2 | Candidate histories (max 100) | 100 |
| **Total (default)** | | **~203** |
| **Total (--full-sp500)** | | **~350** |

## Rate Limits

- **Free tier:** 250 API calls/day - 기본 스크리닝은 이 한도 내에서 수행 가능
- **Starter tier ($29.99/mo):** 750 calls/day
- **Rate limiting:** 요청 간 0.3초 지연, 429 응답 시 자동 재시도
- **Caching:** 메모리 세션 캐시로 중복 요청 방지

## 참고

- 모든 과거 데이터는 `timeseries=260` 파라미터 사용(260 거래일 = 약 1년)
- Phase 3(VCP 탐지, 스코어링, 리포팅)는 API 추가 호출이 **없음**
- `--full-sp500` 플래그는 pre-filter 통과 종목 전체(약 250개)의 히스토리를 조회
