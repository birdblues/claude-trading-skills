# Institutional Flow Tracker

13F filings 데이터를 활용해 기관투자자 보유 비중 변화와 포트폴리오 자금 흐름을 추적하고, "smart money"의 매집(accumulation)/분산(distribution) 패턴을 식별합니다.

## 개요

Institutional Flow Tracker는 SEC 13F filings를 분석해 정교한 투자자(hedge funds, mutual funds, pension funds)가 포지션을 매집하거나 분산하는 종목을 찾아냅니다. 기관 자금의 흐름을 추적하면 다음이 가능합니다:

- **기회 발굴**: 시장의 주류가 되기 전에 기회를 찾기
- **투자 아이디어 검증**: smart money가 같은 방향인지 확인
- **조기 경보 확보**: 우수 투자자들이 포지션을 청산할 때 조기에 감지
- **superinvestor 추적**: Warren Buffett, Seth Klarman, Bill Ackman 같은 투자자 팔로우

**핵심 인사이트:** 기관투자자는 수조 달러를 운용하며 광범위한 리서치를 수행합니다. 이들의 집단적 행동은 주요 가격 움직임보다 1-3분기 먼저 나타나는 경우가 많습니다.

## 기능

✅ **Stock Screening** - 기관 보유 비중 변화가 큰 종목 선별 (>10-15% QoQ)
✅ **Deep Dive Analysis** - 개별 종목의 분기별 추세, 상위 보유자, 포지션 변화 상세 분석
✅ **Institution Tracking** - 특정 hedge fund/mutual fund의 포트폴리오 이동 추적
✅ **Signal Quality Framework** - Tier 기반 가중 시스템 (superinvestors > active funds > index funds)
✅ **Multi-Quarter Trends** - 지속적인 매집/분산 식별 (3+ quarters)
✅ **Concentration Analysis** - 보유 집중도 리스크 평가
✅ **FMP API Integration** - 무료 티어(250 calls/day)만으로도 분기 리뷰 수행 가능

## 사전 요구사항

### 필수: FMP API Key

이 스킬은 Financial Modeling Prep (FMP) API를 사용해 13F filing 데이터에 접근합니다.

**설정:**
```bash
# Set environment variable (recommended)
export FMP_API_KEY="your_key_here"

# Or provide via command-line when running scripts
python3 scripts/track_institutional_flow.py --api-key YOUR_KEY
```

**API Key 발급:**
1. 방문: https://financialmodelingprep.com/developer/docs
2. 무료 계정 가입 (250 requests/day)
3. API key 복사

**API 사용량:**
- 무료 티어: 250 requests/day (분기 기준 30-50개 종목 분석에 충분)
- 종목당 분석: 1-2 API calls 사용
- 분기 리뷰 워크플로우: 총 ~50-100 API calls

## 설치

Python 3와 `requests` 라이브러리 외 추가 설치는 필요 없습니다:

```bash
pip install requests
```

## 사용법

### 1. 기관 보유 변화가 있는 종목 스크리닝

기관 활동이 큰 종목을 찾습니다:

**Quick scan (상위 50개 종목):**
```bash
python3 institutional-flow-tracker/scripts/track_institutional_flow.py \
  --top 50 \
  --min-change-percent 10
```

**Sector 중심 스크리닝:**
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
  --output institutional_results.json
```

**출력:** 상위 accumulators/distributors, 상세 지표, 해석 가이드가 포함된 Markdown 리포트

### 2. 특정 종목 Deep Dive

단일 종목의 기관 보유 현황을 종합 분석합니다:

```bash
python3 institutional-flow-tracker/scripts/analyze_single_stock.py AAPL
```

**확장 히스토리 (12개 분기):**
```bash
python3 institutional-flow-tracker/scripts/analyze_single_stock.py MSFT --quarters 12
```

**출력:** 분기 추세, 신규/증가/감소/청산 포지션, 집중도 분석이 포함된 상세 리포트

### 3. 특정 기관투자자 추적

특정 hedge fund 또는 투자사의 포트폴리오 변화를 추적합니다:

```bash
# Track Warren Buffett's Berkshire Hathaway
python3 institutional-flow-tracker/scripts/track_institution_portfolio.py \
  --cik 0001067983 \
  --name "Berkshire Hathaway"

# Track Cathie Wood's ARK Investment Management
python3 institutional-flow-tracker/scripts/track_institution_portfolio.py \
  --cik 0001579982 \
  --name "ARK Investment Management"
```

**CIK (Central Index Key) 찾기:**
- SEC EDGAR 검색: https://www.sec.gov/cgi-bin/browse-edgar
- 또는 FMP API institutional search 사용

**출력:** 현재 포트폴리오 보유 종목, 신규 포지션, 청산 포지션, 최대 변화 항목

## Signal Interpretation Framework

### Strong Buy Signal (95th percentile)

**기준:**
- Institutional ownership이 QoQ 기준 >15% 증가
- 3개 분기 이상 연속 매집
- 여러 Tier 1/2 투자자가 매수 (clustering score >60)
- 장기 성향의 quality investors가 포지션을 추가

**액션:** 높은 확신으로 BUY (포트폴리오 2-5% 비중)

### Moderate Buy Signal (75th percentile)

**기준:**
- Institutional ownership이 QoQ 기준 7-15% 증가
- 2개 분기 연속 매집
- quality buyers가 혼합되어 유입

**액션:** 중간 확신으로 BUY (1-3% 비중)

### Neutral Signal

**기준:**
- Institutional ownership 변화가 QoQ 기준 <5%
- 뚜렷한 추세 없음
- 매수/매도 활동 혼재

**액션:** HOLD 또는 다른 요인 기반으로 판단

### Moderate/Strong Sell Signal

**기준:**
- Institutional ownership이 QoQ 기준 7-15% 감소(moderate) 또는 >15%(strong)
- 2-3개 분기 이상 연속 분산(distribution)
- quality investors가 이탈

**액션:** 포지션 TRIM/SELL, 신규 진입 회피

## Institutional Investor Quality Tiers

**Tier 1 - Superinvestors (Weight: 3.0-3.5x):**
- Warren Buffett (Berkshire Hathaway)
- Seth Klarman (Baupost Group)
- Bill Ackman (Pershing Square)
- David Tepper (Appaloosa Management)
- 인내심 있는 자본, 장기 지향, 집중 포트폴리오

**Tier 2 - Quality Active Managers (Weight: 2.0-2.5x):**
- Fidelity Management & Research
- T. Rowe Price Associates
- Dodge & Cox
- Wellington Management
- 리서치 중심, 견고한 트랙 레코드

**Tier 3 - Average Institutional (Weight: 1.0-1.5x):**
- 지역 기반 mutual funds
- 대부분의 pension funds
- benchmark 인지형, committee 주도

**Tier 4 - Passive/Mechanical (Weight: 0.0-0.5x):**
- Index funds (Vanguard, BlackRock, State Street)
- Momentum/quant funds
- 펀더멘털 뷰 없이 index/price action 추종

## 워크플로우 예시

### 분기 포트폴리오 리뷰

**목표:** 보유 종목에 대한 기관 수급 지지 여부 모니터링

1. 13F filing 마감 이후 각 보유 종목에 대해 기관 분석 실행
2. 기관 지지가 약화되는 포지션 플래그 처리
3. Strong Sell 신호가 나온 포지션의 투자 thesis 재평가
4. quality investors가 분산 중이면 비중 축소/청산 고려

**13F Filing 마감 일정:**
- Q1 (Jan-Mar): Mid-May
- Q2 (Apr-Jun): Mid-August
- Q3 (Jul-Sep): Mid-November
- Q4 (Oct-Dec): Mid-February

### 신규 포지션 검증

**목표:** 기관 데이터로 종목 아이디어 검증

1. 후보 종목에 대한 fundamental analysis 수행
2. institutional flow 신호 확인 (accumulation or distribution?)
3. Strong Buy 신호면 확신 강화 후 포지션 진입
4. Strong Sell 신호면 재검토 또는 회피
5. Neutral이면 fundamentals와 technicals를 기반으로 결정

### Smart Money 복제

**목표:** superinvestor 포트폴리오 움직임 추적

1. Berkshire Hathaway, Baupost 등 Tier 1 투자자를 분기별로 추적
2. 신규 포지션 또는 유의미한 증액 포지션 식별
3. 해당 종목을 리서치해 투자 thesis 이해
4. 확신도 높은 아이디어부터 포지션 진입

### 섹터 로테이션 감지

**목표:** 초기 섹터 로테이션 추세 식별

1. 섹터별 aggregate institutional flow 계산
2. 순 institutional inflow/outflow 기준으로 섹터 랭킹
3. 경기 사이클 기반 예상 패턴과 비교
4. 기관 매집이 나타나는 섹터 비중 확대
5. 분산이 나타나는 섹터는 비중 축소/회피

## 다른 Skills와의 연계

**Value Dividend Screener + Institutional Flow:**
```
1. Run Value Dividend Screener to find candidates
2. For each candidate, check institutional flow
3. Prioritize stocks with Strong Buy institutional signal
```

**US Stock Analysis + Institutional Flow:**
```
1. Run comprehensive fundamental analysis
2. Validate with institutional ownership trends
3. If institutions selling despite strong fundamentals: investigate discrepancy
```

**Portfolio Manager + Institutional Flow:**
```
1. Fetch current portfolio via Alpaca
2. Run institutional analysis on each holding quarterly
3. Flag positions with deteriorating institutional support
4. Rebalance away from Strong Sell signals
```

**Technical Analyst + Institutional Flow:**
```
1. Identify technical setup (e.g., breakout, basing pattern)
2. Check if institutional buying confirms
3. Higher conviction if both technical + institutional signals align
```

## 데이터 한계

**보고 지연 (Reporting Lag):**
- 13F filings는 분기 종료 후 45일 내 제출
- 포지션은 분기말 시점 스냅샷
- 제출 이후 현재 포지션은 이미 바뀌었을 수 있음

**커버리지:**
- 13F는 운용자산 >$100M 기관만 제출
- 개인투자자 및 소형 펀드는 제외
- 롱 equity 포지션만 포함 (shorts, options, bonds 제외)

**Best Practices:**
- 선행 신호가 아니라 확인 지표로 사용
- multi-quarter 추세(3+ quarters) 확인
- 기관 퀄리티에 가중치 부여 (Tier 1 > Tier 4)
- fundamental/technical 분석과 결합
- 일간이 아닌 분기 단위로 업데이트

## 참고 자료

`references/` 폴더에는 종합 가이드가 포함되어 있습니다:

- **13f_filings_guide.md** - 13F SEC filings 이해, 보고 요건, 데이터 품질 고려사항, 흔한 함정
- **institutional_investor_types.md** - 투자자 유형(hedge funds, mutual funds 등), 전략, quality tiers, weighting framework
- **interpretation_framework.md** - 신호 해석의 체계적 접근, decision trees, multi-factor integration

## Script Parameters Reference

### track_institutional_flow.py

**필수:**
- `--api-key` 또는 FMP_API_KEY environment variable

**선택:**
- `--top N` - 상위 N개 종목 반환 (default: 50)
- `--min-change-percent X` - 최소 보유 비중 변화율 % (default: 10)
- `--min-market-cap X` - 최소 시가총액(달러) (default: 1B)
- `--sector NAME` - 섹터 필터
- `--min-institutions N` - 최소 기관 보유자 수 (default: 10)
- `--sort-by FIELD` - ownership_change/institution_count_change/dollar_value_change 기준 정렬
- `--output FILE` - 출력 JSON 파일

### analyze_single_stock.py

**필수:**
- 주식 ticker symbol (positional argument)
- `--api-key` 또는 FMP_API_KEY environment variable

**선택:**
- `--quarters N` - 분석할 분기 수 (default: 8)
- `--output FILE` - 출력 markdown report 경로

### track_institution_portfolio.py

**필수:**
- `--cik CIK` - 기관의 Central Index Key
- `--name NAME` - 리포트용 기관명
- `--api-key` 또는 FMP_API_KEY environment variable

**선택:**
- `--top N` - 상위 N개 보유 종목 표시 (default: 50)
- `--output FILE` - 출력 markdown report 경로

## 추적할 만한 주요 기관투자자

### Tier 1 Superinvestors

| Investor | CIK | Strategy | Track Because |
|----------|-----|----------|---------------|
| Berkshire Hathaway (Warren Buffett) | 0001067983 | Value/Quality | Long-term compounders, patient capital |
| Baupost Group (Seth Klarman) | 0001061768 | Deep Value | Distressed opportunities, contrarian |
| Pershing Square (Bill Ackman) | 0001336528 | Activist/Value | Catalytic events, concentrated bets |
| Appaloosa Management (David Tepper) | 0001079114 | Value | Contrarian, high conviction |
| Third Point (Dan Loeb) | 0001040273 | Event-Driven | Catalyst-driven, activism |

### Tier 2 Quality Active Managers

| Fund Family | CIK | Strategy | Track Because |
|-------------|-----|----------|---------------|
| Fidelity Management | 0000315066 | Growth & Value | Large analyst team, quality research |
| T. Rowe Price | 0001113169 | Growth | Bottom-up research, growth focus |
| Dodge & Cox | 0000922614 | Deep Value | Contrarian, value-oriented |
| ARK Investment (Cathie Wood) | 0001579982 | Disruptive Innovation | High-conviction tech/innovation bets |

## 지원 및 리소스

- FMP API Documentation: https://financialmodelingprep.com/developer/docs
- SEC 13F Filings Database: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&type=13F
- WhaleWisdom (free tier): https://whalewisdom.com

## 라이선스

교육 및 리서치 목적. 자세한 내용은 repository license를 확인하세요.
