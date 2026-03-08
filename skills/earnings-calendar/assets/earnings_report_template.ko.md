# 예정 실적 캘린더 - [START_DATE]부터 [END_DATE]까지

**보고서 생성일**: [CURRENT_DATE]
**데이터 소스**: FMP API (Mid-cap 이상, 시가총액 >$2B)
**커버리지 기간**: 향후 7일

---

## Executive Summary

- **실적 발표 기업 수**: [TOTAL_COUNT]
- **Mega/Large Cap (>$10B)**: [LARGE_CAP_COUNT]
- **Mid Cap ($2B-$10B)**: [MID_CAP_COUNT]
- **피크 요일**: [DAY_WITH_MOST_EARNINGS]

---

## [DAY_NAME], [FULL_DATE]

### 장 시작 전 (BMO)

| Ticker | Company | Market Cap | Sector | EPS Est. | Revenue Est. |
|--------|---------|------------|--------|----------|--------------|
| [TICKER] | [COMPANY_NAME] | [MARKET_CAP] | [SECTOR] | [EPS_EST] | [REV_EST] |
| [TICKER] | [COMPANY_NAME] | [MARKET_CAP] | [SECTOR] | [EPS_EST] | [REV_EST] |

### 장 마감 후 (AMC)

| Ticker | Company | Market Cap | Sector | EPS Est. | Revenue Est. |
|--------|---------|------------|--------|----------|--------------|
| [TICKER] | [COMPANY_NAME] | [MARKET_CAP] | [SECTOR] | [EPS_EST] | [REV_EST] |
| [TICKER] | [COMPANY_NAME] | [MARKET_CAP] | [SECTOR] | [EPS_EST] | [REV_EST] |

### 시간 미공개 (TAS)

| Ticker | Company | Market Cap | Sector | EPS Est. | Revenue Est. |
|--------|---------|------------|--------|----------|--------------|
| [TICKER] | [COMPANY_NAME] | [MARKET_CAP] | [SECTOR] | [EPS_EST] | [REV_EST] |

---

## [NEXT_DAY_NAME], [NEXT_FULL_DATE]

[주중 각 요일에 대해 동일 구조 반복]

---

## Key Observations

### 이번 주 시가총액 상위 기업
1. [COMPANY_NAME] ([TICKER]) - [MARKET_CAP] - [DATE] [TIME]
2. [COMPANY_NAME] ([TICKER]) - [MARKET_CAP] - [DATE] [TIME]
3. [COMPANY_NAME] ([TICKER]) - [MARKET_CAP] - [DATE] [TIME]

### 섹터 분포
- **Technology**: [COUNT] companies
- **Healthcare**: [COUNT] companies
- **Financial**: [COUNT] companies
- **Consumer**: [COUNT] companies
- **Other**: [COUNT] companies

### 트레이딩 고려사항
- **거래량 집중일**: [DATES with multiple large-cap earnings]
- **Pre-Market Focus**: [BMO companies that may move markets]
- **After-Hours Focus**: [AMC companies that may move markets]

---

## Timing Reference

- **BMO (Before Market Open)**: 일반적으로 ET 9:30 개장 전인 ET 6:00-8:00에 발표
- **AMC (After Market Close)**: 일반적으로 ET 4:00 마감 후인 ET 4:00-5:00에 발표
- **TAS (Time Not Announced)**: 발표 시간이 아직 공개되지 않음 - 기업 IR 공지 모니터링 필요

---

## Data Notes

- **시가총액 구분**:
  - Mega Cap: >$200B
  - Large Cap: $10B-$200B
  - Mid Cap: $2B-$10B

- **필터 기준**: 다음 주 실적 일정이 있는 시가총액 $2B 이상(mid-cap+) 기업만 포함합니다.

- **데이터 신선도**: 실적 날짜/시간은 변경될 수 있습니다. 최신 정보는 기업 IR 웹사이트에서 재확인하세요.

- **시간 미공개 항목**: "TAS" 표시는 구체 시간 미공개 상태입니다. 실적일 24-48시간 전에 업데이트를 확인하세요.

- **EPS/매출 추정치**: FMP API의 애널리스트 컨센서스 값입니다. 실제 실적은 발표일에 확정됩니다.

---

## Additional Resources

- **FMP API Documentation**: https://site.financialmodelingprep.com/developer/docs
- **Seeking Alpha Calendar**: https://seekingalpha.com/earnings/earnings-calendar
- **Yahoo Finance Calendar**: https://finance.yahoo.com/calendar/earnings

---

*FMP Earnings Calendar API와 mid-cap+ 필터(>$2B market cap)로 생성된 보고서입니다. 데이터는 보고서 생성 시점 기준이며, 실적 일정은 반드시 기업 공식 소스로 최종 확인하세요.*
