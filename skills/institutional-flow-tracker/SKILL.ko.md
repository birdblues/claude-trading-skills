---
name: institutional-flow-tracker
description: 13F 공시 데이터를 사용해 기관투자자 보유 변화와 포트폴리오 자금 흐름을 추적하는 스킬입니다. 헤지펀드, 뮤추얼펀드 및 기타 기관 보유자를 분석하여 스마트 머니의 의미 있는 매집/분산이 나타나는 종목을 식별합니다. 정교한 투자자들이 자본을 배치하는 방향을 따라 주요 움직임 전에 종목을 발굴하도록 돕습니다.
---

# Institutional Flow Tracker

## 개요

이 스킬은 13F SEC filings를 통해 기관투자자 활동을 추적하여 주식으로 유입/유출되는 "smart money" 흐름을 식별합니다. 기관 보유의 분기별 변화를 분석하면, 정교한 투자자들이 큰 가격 변동 전에 매집하는 종목을 찾거나 기관이 포지션을 줄일 때의 잠재적 리스크를 파악할 수 있습니다.

**핵심 인사이트:** 기관투자자(hedge funds, pension funds, mutual funds)는 수조 달러를 운용하며 광범위한 리서치를 수행합니다. 이들의 집합적 매수/매도 패턴은 종종 1-3분기 앞서 의미 있는 가격 변동을 선행합니다.

## 사전 준비

- **FMP API Key:** `FMP_API_KEY` 환경 변수를 설정하거나 스크립트에 `--api-key` 전달
- **Python 3.8+:** 분석 스크립트 실행에 필요
- **Dependencies:** `pip install requests` (스크립트가 누락 의존성을 안전하게 처리)

## 이 스킬을 사용해야 할 때

다음 상황에서 사용하세요:
- 투자 아이디어 검증(스마트 머니가 내 thesis에 동의하는지 확인)
- 신규 기회 발굴(기관이 매집 중인 종목 탐색)
- 리스크 평가(기관이 이탈 중인 종목 식별)
- 포트폴리오 모니터링(보유 종목의 기관 수급 지지 추적)
- 특정 투자자 추적(Warren Buffett, Cathie Wood 등)
- 섹터 로테이션 분석(기관이 자본을 어디로 이동시키는지 파악)

**다음 경우에는 사용하지 마세요:**
- 실시간 장중 신호가 필요할 때(13F 데이터는 45일 보고 지연 존재)
- 마이크로캡 분석(<$100M market cap, 기관 관심 제한적)
- 단기 트레이딩 신호(<3개월) 탐색 시

## 데이터 소스 및 요구사항

### 필수: FMP API Key

이 스킬은 Financial Modeling Prep (FMP) API를 사용해 13F filing 데이터에 접근합니다.

**설정:**
```bash
# Set environment variable (preferred)
export FMP_API_KEY=your_key_here

# Or provide when running scripts
python3 scripts/track_institutional_flow.py --api-key YOUR_KEY
```

**API Tier 요구사항:**
- **Free Tier:** 250 requests/day (분기 기준 20-30개 종목 분석에 충분)
- **Paid Tiers:** 대규모 스크리닝용 상위 한도

**13F Filing 일정:**
- 분기 종료 후 45일 이내 분기별 제출
- Q1 (Jan-Mar): 5월 중순까지 제출
- Q2 (Apr-Jun): 8월 중순까지 제출
- Q3 (Jul-Sep): 11월 중순까지 제출
- Q4 (Oct-Dec): 2월 중순까지 제출

## 분석 워크플로우

### Step 1: 의미 있는 기관 변화 종목 식별

주요 기관 활동이 있는 종목을 찾기 위해 메인 스크리닝 스크립트를 실행합니다.

**퀵 스캔(기관 변화 기준 상위 50개 종목):**
```bash
python3 institutional-flow-tracker/scripts/track_institutional_flow.py \
  --top 50 \
  --min-change-percent 10
```

**섹터 집중 스캔:**
```bash
python3 institutional-flow-tracker/scripts/track_institutional_flow.py \
  --sector Technology \
  --min-institutions 20
```

**커스텀 스크리닝:**
```bash
python3 institutional-flow-tracker/scripts/track_institutional_flow.py \
  --min-market-cap 2000000000 \
  --min-change-percent 15 \
  --top 100 \
  --output institutional_flow_results.json
```

**출력 항목:**
- 주식 ticker 및 회사명
- 현재 기관 보유율 %(유통주식 대비)
- 분기 대비 보유 주식 수 변화
- 보유 기관 수
- 기관 수 변화(신규 매수자 vs 매도자)
- 상위 기관 보유자

### Step 2: 특정 종목 심층 분석

특정 종목의 기관 보유를 상세 분석하려면:

```bash
python3 institutional-flow-tracker/scripts/analyze_single_stock.py AAPL
```

**생성 내용:**
- 기관 보유 추세 히스토리(8개 분기)
- 포지션 변화가 포함된 전체 기관 보유자 목록
- 집중도 분석(상위 10개 보유자의 기관 보유 총합 대비 비중)
- 신규 포지션 vs 증액 vs 감액
- 신뢰도 등급이 포함된 데이터 품질 평가

**평가할 핵심 지표:**
- **Ownership %:** 기관 보유율이 높을수록(>70%) 안정성은 높지만 업사이드는 제한될 수 있음
- **Ownership Trend:** 보유율 상승 = bullish, 하락 = bearish
- **Concentration:** 집중도 높음(top 10 > 50%) = 매도 시 리스크
- **Quality of Holders:** 장기 우량 투자자(Berkshire, Fidelity) 존재 여부 vs 모멘텀 펀드

### Step 3: 특정 기관투자자 추적

> **참고:** `track_institution_portfolio.py`는 **아직 구현되지 않았습니다**. FMP API는
> 기관 보유자 데이터를 기관 기준이 아닌 종목 기준으로 구성하므로, 이 API만으로는
> 전체 포트폴리오 재구성이 사실상 어렵습니다.

**대안 — `analyze_single_stock.py`로 특정 기관의 보유 여부 확인:**
```bash
# Analyze a stock and look for a specific institution in the output
python3 institutional-flow-tracker/scripts/analyze_single_stock.py AAPL
# Then search the report for "Berkshire" or "ARK" in the Top 20 holders table
```

**기관 단위 전체 포트폴리오 추적이 필요하면 아래 외부 리소스를 사용하세요:**
1. **WhaleWisdom:** https://whalewisdom.com (free tier 제공, 13F portfolio viewer)
2. **SEC EDGAR:** https://www.sec.gov/cgi-bin/browse-edgar (공식 13F filings)
3. **DataRoma:** https://www.dataroma.com (superinvestor portfolio tracker)

### Step 4: 해석과 실행

해석 가이드를 위해 references를 읽으세요:
- `references/13f_filings_guide.md` - 13F 데이터 이해 및 한계
- `references/institutional_investor_types.md` - 기관투자자 유형과 전략
- `references/interpretation_framework.md` - 기관 자금흐름 신호 해석 방법

**Signal Strength Framework:**

**강한 Bullish (매수 고려):**
- 기관 보유율이 QoQ 기준 >15% 증가
- 기관 수가 >10% 증가
- 우량 장기 투자자가 포지션 추가
- 현재 보유율이 낮음(<40%) + 상승 여지 존재
- 여러 분기에 걸친 매집 진행

**보통 Bullish:**
- 기관 보유율이 QoQ 5-15% 증가
- 신규 매수와 매도가 혼재하나 순증
- 현재 보유율 40-70%

**중립:**
- 보유율 변화 미미(<5%)
- 매수자와 매도자 수가 유사
- 기관 기반이 안정적

**보통 Bearish:**
- 기관 보유율이 QoQ 5-15% 감소
- 매도자가 매수자보다 많음
- 높은 보유율(>80%)로 신규 매수 여력 제한

**강한 Bearish (매도/회피 고려):**
- 기관 보유율이 QoQ >15% 감소
- 기관 수가 >10% 감소
- 우량 투자자가 포지션 이탈
- 여러 분기에 걸친 분산(distribution)
- 집중도 리스크(상위 보유자 대량 매도)

### Step 5: 포트폴리오 적용

**신규 포지션의 경우:**
1. 아이디어 종목에 기관 분석 실행
2. 확인 신호 탐색(기관도 동시 매집하는지)
3. 강한 bearish 신호면 재검토 또는 비중 축소
4. 강한 bullish 신호면 thesis 확신 강화

**기존 보유 종목의 경우:**
1. 13F 마감 일정 이후 분기별 리뷰
2. 분산(distribution) 모니터링(조기 경보 시스템)
3. 기관 이탈 시 thesis 재평가
4. 광범위한 기관 매도 시 비중 축소 고려

**스크리닝 워크플로우 통합:**
1. Value Dividend Screener 또는 기타 스크리너로 후보 발굴
2. 상위 후보에 Institutional Flow Tracker 실행
3. 기관 매집 종목 우선순위 부여
4. 기관 분산 종목 회피

## 출력 형식

모든 분석은 구조화된 markdown report로 생성되며 저장 위치는 repository root입니다.

**파일명 규칙:** `institutional_flow_analysis_<TICKER/THEME>_<DATE>.md`

**리포트 섹션:**
1. Executive Summary (핵심 결과)
2. Institutional Ownership Trend (현재 vs 과거)
3. Top Holders and Changes
4. New Buyers vs Sellers
5. Concentration Analysis
6. Interpretation and Recommendations
7. Data Sources and Timestamp

## 데이터 신뢰도 등급

모든 분석은 데이터 품질 기반의 **reliability grade**를 포함합니다.

- **Grade A:** Coverage ratio < 3x, match ratio >= 50%, genuine holder ratio >= 70%. 투자 의사결정에 안전.
- **Grade B:** Genuine holder ratio >= 30%. 참고용 - 주의 필요.
- **Grade C:** Genuine holder ratio < 30%. UNRELIABLE - 스크리닝 결과에서 제외.

스크리닝 스크립트(`track_institutional_flow.py`)는 Grade C 종목을 자동 제외합니다.
단일 종목 분석(`analyze_single_stock.py`)은 적절한 경고와 함께 등급을 표시합니다.

**중요한 이유:** FMP는 분기마다 서로 다른 보유자 수를 반환합니다. 어떤 종목은
Q4에 5,415명이지만 Q3에는 201명만 표시될 수 있습니다. 필터링이 없으면 집계 지표가
오해를 부르는 퍼센트 변화(예: +400%)를 만들 수 있습니다. 데이터 품질 모듈은 "genuine" holders
(양 분기에 모두 존재)만 필터링해 신뢰 가능한 지표를 만듭니다.

## 한계와 주의사항

**데이터 지연:**
- 13F filings는 45일 보고 지연이 있음
- filing 시점 이후 포지션이 바뀌었을 수 있음
- 선행 신호가 아니라 확인 지표로 사용

**커버리지:**
- >$100M 운용 기관만 filing 의무
- 개인 투자자 및 소형 펀드 제외
- 해외 기관은 13F를 제출하지 않을 수 있음

**보고 규칙:**
- 롱 equity 포지션만 보고(숏, options, bonds 미포함)
- 분기말 시점 스냅샷 보유
- 일부 포지션은 기밀 처리(보고 지연) 가능

**해석:**
- 상관관계 ≠ 인과관계(기관 매수에도 주가 하락 가능)
- 시장 환경 및 펀더멘털을 함께 고려
- 기술적 분석 및 다른 스킬과 병행

## 고급 활용 사례

**Insider + Institutional 조합:**
- insiders와 institutions가 동시에 매수하는 종목 탐색
- 정렬(alignment)될 때 특히 강력한 신호

**Sector Rotation 탐지:**
- 섹터별 기관 순유입/유출 집계 추적
- 가격에 반영되기 전 초기 로테이션 식별

**Contrarian 플레이:**
- 기관이 매도하는 우량 종목 발굴(잠재 가치 구간)
- 강한 펀더멘털 확신이 필요

**Smart Money 검증:**
- 큰 포지션 진입 전 스마트 머니 동의 여부 확인
- 확신을 높이거나 간과한 리스크를 탐색

## References

`references/` 폴더에 상세 가이드가 있습니다:

- **13f_filings_guide.md** - 13F SEC filings의 구성, 보고 요건, 데이터 품질 고려사항 종합 가이드
- **institutional_investor_types.md** - 기관투자자 유형(hedge funds, mutual funds, pension funds 등), 일반 전략, 움직임 해석법
- **interpretation_framework.md** - 기관 보유 변화 해석, 신호 품질 평가, 타 분석과의 통합 프레임워크

## 스크립트 파라미터

### track_institutional_flow.py

의미 있는 기관 변화 종목을 찾는 메인 스크리닝 스크립트입니다.

**필수:**
- `--api-key`: FMP API key (또는 FMP_API_KEY 환경 변수 설정)

**선택:**
- `--top N`: 기관 변화 기준 상위 N개 종목 반환 (기본값: 50)
- `--min-change-percent X`: 기관 보유 최소 변화율 % (기본값: 10)
- `--min-market-cap X`: 최소 시가총액 달러 기준 (기본값: 1B)
- `--sector NAME`: 특정 섹터 필터
- `--min-institutions N`: 최소 기관 보유자 수 (기본값: 10)
- `--limit N`: 스크리너에서 가져올 종목 수 (기본값: 100). 낮출수록 API 호출 절약.
- `--output FILE`: 출력 JSON 파일 경로
- `--output-dir DIR`: 리포트 출력 디렉터리 (기본값: reports/)
- `--sort-by FIELD`: 'ownership_change' 또는 'institution_count_change' 정렬

### analyze_single_stock.py

특정 종목의 기관 보유 심층 분석 스크립트입니다.

**필수:**
- Ticker symbol (위치 인자)
- `--api-key`: FMP API key (또는 FMP_API_KEY 환경 변수 설정)

**선택:**
- `--quarters N`: 분석 분기 수 (기본값: 8, 즉 2년)
- `--output FILE`: 출력 markdown report 경로
- `--output-dir DIR`: 리포트 출력 디렉터리 (기본값: reports/)
- `--compare-to TICKER`: 다른 종목과 기관 보유 비교 (향후 기능)

### track_institution_portfolio.py

**상태: NOT YET IMPLEMENTED**

이 스크립트는 placeholder입니다. 대체 리소스(WhaleWisdom, SEC EDGAR, DataRoma)를 출력하고 error code 1로 종료합니다. FMP API는 기관 보유자 데이터를 종목 기준으로 구성하므로, 전체 포트폴리오 재구성은 현실적으로 어렵습니다.

기관별 포트폴리오 추적은 아래를 사용하세요:
1. WhaleWisdom: https://whalewisdom.com (free tier 제공)
2. SEC EDGAR: https://www.sec.gov/cgi-bin/browse-edgar
3. DataRoma: https://www.dataroma.com

### Data Quality Module (data_quality.py)

`track_institutional_flow.py`와 `analyze_single_stock.py`가 공유하는 유틸리티 모듈:

- **classify_holder():** 보유자를 genuine/new_full/exited/unknown으로 분류
- **calculate_filtered_metrics():** genuine holders만 사용해 지표 계산
- **reliability_grade():** 데이터 품질 기반 A/B/C 등급 부여
- **is_tradable_stock():** ETFs, funds, inactive stocks 필터링
- **deduplicate_share_classes():** BRK-A/B, GOOG/GOOGL 중복 제거

## 다른 스킬과의 통합

**Value Dividend Screener + Institutional Flow:**
```
1. Run Value Dividend Screener to find candidates
2. For each candidate, check institutional flow
3. Prioritize stocks with rising institutional ownership
```

**US Stock Analysis + Institutional Flow:**
```
1. Run comprehensive fundamental analysis
2. Validate with institutional ownership trends
3. If institutions are selling, investigate why
```

**Portfolio Manager + Institutional Flow:**
```
1. Fetch current portfolio via Alpaca
2. Run institutional analysis on each holding
3. Flag positions with deteriorating institutional support
4. Consider rebalancing away from distribution
```

**Technical Analyst + Institutional Flow:**
```
1. Identify technical setup (e.g., breakout)
2. Check if institutional buying confirms
3. Higher conviction if both align
```

## Best Practices

1. **분기별 리뷰:** 13F filing 마감일 캘린더 리마인더 설정
2. **다분기 추세:** 일회성 변화보다 지속 추세(3+분기) 중시
3. **Quality Over Quantity:** Berkshire의 매수 > 100개 소형 펀드 매수
4. **맥락 중요:** 하락 종목의 보유율 상승은 falling knife를 잡는 value 투자일 수 있음
5. **신호 결합:** 기관 흐름을 단독으로 사용하지 않기
6. **데이터 업데이트:** 신규 13F filing마다 분기별 재분석

## Support & Resources

- FMP API Documentation: https://financialmodelingprep.com/developer/docs
- SEC 13F Filings Database: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&type=13F
- Institutional Investor Database: https://whalewisdom.com (free tier available)

---

**참고:** 이 스킬은 장기 투자자(3-12개월 horizon)를 위해 설계되었습니다. 단기 트레이딩에는 기술적 분석 및 기타 모멘텀 지표와 함께 사용하세요.
