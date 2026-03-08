# 시장 분석에서 자주 발생하는 데이터 오류

시장 분석 문서, 블로그 글, 전략 리포트에서 자주 관찰되는
데이터 품질 이슈를 정리한 reference 문서입니다.

## 1. FRED 데이터 지연 패턴

경제 데이터 소스마다 발표 지연이 다릅니다.
지연을 명시하지 않고 오래된 데이터를 사용하면 독자를 오도할 수 있습니다.

| Data Series | Source | Typical Delay | Notes |
|-------------|--------|---------------|-------|
| VIX Close | CBOE via FRED | T+1 business day | VIX settles after market close |
| GDP (Advance) | BEA | ~T+30 days after quarter end | First estimate; revised twice |
| GDP (Final) | BEA | ~T+90 days after quarter end | Third and final estimate |
| CPI | BLS | ~T+14 days after reference month | Released mid-month for prior month |
| PCE | BEA | ~T+30 days after reference month | Fed's preferred inflation gauge |
| NFP (Nonfarm Payrolls) | BLS | First Friday after reference month | Subject to significant revisions |
| ISM Manufacturing | ISM | First business day of the month | For the prior month |
| FOMC Rate Decision | Federal Reserve | Same day (2:00 PM ET) | Minutes released 3 weeks later |
| 10Y Treasury Yield | US Treasury | T+1 | Daily constant maturity rate |
| Consumer Sentiment | U of Michigan | Preliminary: mid-month; Final: end of month | Two releases per month |

### 흔한 오류 패턴

실제 FRED 데이터가 어제 종가임에도
"VIX is at 18.5 as of today"라고 작성하는 경우가 흔합니다.
항상 데이터 기준일을 명시하세요.

## 2. ETF vs Futures 스케일 비율

자주 발생하는 오류는 futures 가격을 ETF 라벨에 붙이거나 그 반대입니다.
대략적인 스케일 비율은 이런 실수를 빠르게 잡아내는 데 유용합니다.

| Asset | ETF Price (approx) | Futures Price (approx) | Ratio (Futures/ETF) |
|-------|--------------------|----------------------|---------------------|
| Gold | GLD ~$260 | GC ~$2,600 | ~10x |
| Silver | SLV ~$28 | SI ~$30 | ~1.1x |
| S&P 500 | SPY ~$580 | ES ~$5,800 (SPX) | ~10x |
| Crude Oil | USO ~$72 | CL ~$78 | ~1.1x |
| Treasuries | TLT ~$92 | ZB ~$118 | ~1.3x |

**핵심 인사이트**: Gold와 S&P 500은 ETF와 futures/index 가격 사이에
약 ~10x 비율이 있습니다. 가격 스케일 오류의 가장 흔한 원인입니다.

## 3. 흔한 날짜 오류

### 3.1 요일 불일치

가장 흔한 날짜 오류는 요일을 잘못 표기하는 것입니다.
특히 다음 경우에 자주 발생합니다:

- 여러 미래 날짜를 참조하는 주간 전략 리포트
- 한자 요일 표기를 사용하는 일본어 리포트
- 연도 경계 교차 참조(1월 문서에 12월 날짜 기재)

**예방 방법**: 항상 `calendar.weekday(year, month, day)`로 요일을 검증하세요.

### 3.2 휴장일 누락

자주 놓치는 미국 시장 휴장일:

| Holiday | Date | Market Status |
|---------|------|---------------|
| New Year's Day | January 1 | Closed |
| MLK Day | Third Monday in January | Closed |
| Presidents' Day | Third Monday in February | Closed |
| Good Friday | Friday before Easter (varies) | Closed |
| Memorial Day | Last Monday in May | Closed |
| Juneteenth | June 19 | Closed |
| Independence Day | July 4 | Closed (early close July 3) |
| Labor Day | First Monday in September | Closed |
| Thanksgiving | Fourth Thursday in November | Closed (early close Wed) |
| Christmas | December 25 | Closed (early close Dec 24) |

**오류 패턴**: "Markets will react on Monday January 1"라고 쓰지만,
New Year's Day에는 시장이 휴장입니다.

### 3.3 연도 추론 오류

날짜에 연도가 없을 때:
- 2026년 1월 리포트의 "December 25"는 보통 2025년 12월을 의미
- 2026년 1월 리포트의 "March 15"는 보통 2026년 3월을 의미
- 6개월 창 heuristic:
  기준일에서 6개월 이상 떨어진 날짜면 인접 연도를 고려

## 4. 배분 합계 오류 패턴

### 4.1 반올림 오차

개별 배분값을 반올림하면 합계가 100%와 다를 수 있습니다:

```
Stocks:  33.3%
Bonds:   33.3%
Cash:    33.3%
Total:   99.9%  (should be 100%)
```

**수정**: 한 값을 조정해 반올림 차이를 흡수합니다
(예: Cash: 33.4%).

### 4.2 구간 표기 함정

구간 기반 배분(예: "40-45%")은 최소/최대 합계를 모두 점검해야 합니다:

```
Stocks:  50-55%    min=50  max=55
Bonds:   25-30%    min=25  max=30
Gold:    15-20%    min=15  max=20
Cash:     5-10%    min=5   max=10
                   ------- -------
                   min=95  max=115
```

100%가 [95%, 115%]에 포함되므로 이는 유효합니다.

**무효 예시**:
```
A: 60-65%    min=60  max=65
B: 30-35%    min=30  max=35
C: 15-20%    min=15  max=20
             ------- -------
             min=105 max=120
```

최소값(105%)이 이미 100%를 초과하므로 무효입니다.

### 4.3 Cash 또는 "Other" 누락

배분 항목 합계가 100% 미만인데 "Cash"나 "Other"를
명시하지 않는 실수가 자주 발생합니다.

### 4.4 비-배분 퍼센트

모든 퍼센트가 배분은 아닙니다. 체커는 다음을 무시해야 합니다:
- 확률 문장: "There is a 60% chance..."
- 지표 값: "RSI at 35%", "YoY growth of 3.2%"
- 트리거 조건: "If drawdown exceeds 10%..."
- 과거 수익률: "S&P 500 returned 12% last year"

## 5. 단위 혼동 패턴

### 5.1 Basis Points vs Percentage

| Expression | Meaning | Common In |
|-----------|---------|-----------|
| 25 bp | 0.25 percentage points | Bond yields, rate changes |
| 0.25% | 0.25 percent | Same concept, different notation |
| 25% | 25 percent | Equity returns, allocations |

**오류 패턴**: "The Fed raised rates by 25%"라고 쓰는 경우
(올바른 표기는 "25 bp" 또는 "0.25%").

### 5.2 Dollar vs Cent

| Expression | Meaning |
|-----------|---------|
| $1.50 | One dollar and fifty cents |
| 150 cents | Same value |
| $0.015 | 1.5 cents (common in EPS) |

### 5.3 단위 누락

"Gold moved 50 today" 같은 문장은 모호합니다:
- $50 (절대 가격 변화)?
- 50 bp (basis points)?
- 0.50% (퍼센트 변화)?

항상 단위를 명시하세요:
"Gold moved $50 today" 또는 "Gold moved 2.1% today."

### 5.4 단위당 값 vs 총액

futures 계약은 여러 단위를 나타냅니다:
- Gold (GC): 계약당 100 트로이온스
- Crude Oil (CL): 계약당 1,000 배럴
- E-mini S&P (ES): 계약당 $50 x index

"gold가 $50 움직였다"는 의미:
- 온스당: $50
- 계약당: $5,000 (100 oz x $50)

어떤 기준인지 항상 명확히 하세요.

## 6. 타임존 혼동

| Abbreviation | UTC Offset (Winter) | UTC Offset (Summer) |
|-------------|--------------------|--------------------|
| ET (Eastern) | UTC-5 | UTC-4 |
| CT (Central) | UTC-6 | UTC-5 |
| PT (Pacific) | UTC-8 | UTC-7 |
| JST (Japan) | UTC+9 | UTC+9 (no DST) |
| GMT/UTC | UTC+0 | UTC+0 |

**ET -> JST 변환**:
- Winter (11월 첫째 일요일 ~ 3월 둘째 일요일): JST = ET + 14시간
- Summer (3월 둘째 일요일 ~ 11월 첫째 일요일): JST = ET + 13시간

**흔한 오류**: 특히 3월/11월 전환 시점에 DST 반영을 놓치는 경우가 많습니다.
