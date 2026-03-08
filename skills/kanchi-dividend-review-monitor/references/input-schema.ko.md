# Input Schema

`build_review_queue.py`에는 이 정규화 JSON 스키마를 사용합니다.

## 필수 최상위 필드

- `as_of`: ISO 날짜 문자열.
- `holdings`: 티커 레코드 배열.

## Holding 객체

```json
{
  "ticker": "ABC",
  "instrument_type": "stock",
  "dividend": {
    "latest_regular": 0.50,
    "prior_regular": 0.52,
    "is_missing": false
  },
  "cashflow": {
    "fcf": 1200.0,
    "ffo": null,
    "nii": null,
    "dividends_paid": 900.0,
    "coverage_ratio_history": [0.72, 0.85]
  },
  "balance_sheet": {
    "net_debt_history": [3000.0, 3400.0, 3800.0],
    "interest_coverage_history": [4.6, 3.8, 2.9]
  },
  "capital_returns": {
    "buybacks": 250.0,
    "dividends_paid": 900.0,
    "fcf": 1200.0
  },
  "filings": {
    "recent_text": "8-K filed. No restatement language.",
    "latest_8k_text": "Item 4.02 non-reliance ...",
    "headlines": ["Company files 8-K", "Audit committee review announced"]
  },
  "operations": {
    "revenue_cagr_5y": -1.2,
    "margin_trend": "down",
    "guidance_trend": "down",
    "dividend_growth_stalled": true
  }
}
```

## 최소 실행 입력

상위 데이터가 부분적이어도 최소한 다음은 포함하세요:
- `ticker`
- `instrument_type`
- `dividend.latest_regular`
- `dividend.prior_regular`

규칙 엔진은 계속 실행되며, 사용 불가능한 트리거는 건너뜁니다.
