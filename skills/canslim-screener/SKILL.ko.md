---
name: canslim-screener
description: William O'Neil의 CANSLIM 성장주 방법론으로 미국 주식을 스크리닝합니다. 사용자가 CANSLIM 스크리닝, 성장주 분석, 모멘텀 종목 식별을 요청하거나, O'Neil 투자 시스템에 따라 강한 실적과 가격 모멘텀을 가진 종목을 찾고자 할 때 사용합니다.
---

# CANSLIM Stock Screener - Phase 3 (Full CANSLIM)

## 개요

이 스킬은 William O'Neil의 검증된 CANSLIM 방법론을 사용해 미국 주식을 스크리닝합니다. CANSLIM은 강한 펀더멘털과 가격 모멘텀을 가진 성장주를 찾기 위한 체계적 접근이며, 7개 핵심 요소를 분석합니다: **C**urrent Earnings, **A**nnual Growth, **N**ewness/New Highs, **S**upply/Demand, **L**eadership/RS Rank, **I**nstitutional Sponsorship, **M**arket Direction.

**Phase 3**는 7개 요소 전체(C, A, N, S, L, I, M)를 구현하여 **전체 방법론 100%**를 반영합니다.

**2단계 접근:**
1. **Stage 1 (FMP API + Finviz)**: 7개 CANSLIM 요소로 종목 유니버스 분석
2. **Stage 2 (Reporting)**: composite score로 순위화하고 실행 가능한 보고서 생성

**핵심 기능:**
- 가중치 기반 composite scoring (0-100 scale)
- 기관 보유 데이터용 **Finviz fallback** (FMP 데이터 불완전 시 자동)
- API 사용 최적화를 위한 progressive filtering
- JSON + Markdown 출력
- 해석 밴드: Exceptional+ (90+), Exceptional (80-89), Strong (70-79), Above Average (60-69)
- bear market 보호(M component gating)

**Phase 3 요소 가중치 (O'Neil 원본):**
- C (Current Earnings): 15%
- A (Annual Growth): 20%
- N (Newness): 15%
- S (Supply/Demand): 15%
- L (Leadership/RS Rank): 20%
- I (Institutional): 10%
- M (Market Direction): 5%

**향후 단계:**
- Phase 4: FINVIZ Elite 통합 → 실행 속도 10배 향상

---

## 이 스킬을 사용할 때

**명시적 트리거:**
- "CANSLIM 종목 찾아줘"
- "O'Neil 방식으로 성장주 스크리닝해줘"
- "실적과 모멘텀이 강한 종목은?"
- "52-week high 근처에서 실적이 가속되는 종목 찾아줘"
- "[섹터/유니버스]로 CANSLIM 스크리너 돌려줘"

**암묵적 트리거:**
- 사용자가 multi-bagger 후보를 찾고 싶어함
- 검증된 펀더멘털을 갖춘 성장주를 찾고 있음
- 과거 승자 패턴 기반의 체계적 종목 선별을 원함
- O'Neil 기준을 충족하는 랭킹 리스트가 필요함

**사용하지 말아야 할 경우:**
- 가치투자 중심 요청 (대신 value-dividend-screener 사용)
- 배당/인컴 중심 요청 (대신 dividend-growth-pullback-screener 사용)
- bear market 상황 (M component가 경고 - 현금 비중 확대 고려)

---

## 사전 요구사항

**API 요구사항:**
- **FMP API key** (free tier: 250 calls/day, 35종목 충분; 40+ 종목은 Starter tier $29.99/mo 권장)
  - 가입: https://site.financialmodelingprep.com/developer/docs
  - 환경변수 설정: `export FMP_API_KEY=your_key_here`

**Python 의존성:**
- Python 3.7+
- `requests` (FMP API 호출)
- `beautifulsoup4` (Finviz 웹 스크래핑)
- `lxml` (HTML 파싱)

**설치:**
```bash
pip install requests beautifulsoup4 lxml
```

---

## 출력

**출력 디렉터리:** 기본 `reports/` 또는 `--output-dir`로 지정

**생성 파일:**
- `canslim_screener_YYYY-MM-DD_HHMMSS.json` - 프로그램 활용용 구조화 데이터
- `canslim_screener_YYYY-MM-DD_HHMMSS.md` - 사람이 읽기 좋은 보고서

**보고서 내용:**
- Market Condition Summary (trend, M score, warnings)
- Top N CANSLIM Candidates (composite score 순)
- 종목별 요소 세부(C, A, N, S, L, I, M score + 상세)
- Rating 해석(Exceptional+/Exceptional/Strong/Above Average)
- 품질 경고 및 데이터 소스 노트
- 요약 통계(등급 분포)

**등급 밴드:**
- **Exceptional+ (90-100):** 전 요소가 거의 완벽, 공격적 매수
- **Exceptional (80-89):** 우수한 펀더멘털 + 모멘텀, 강한 매수
- **Strong (70-79):** 전반적으로 견고, 표준 매수
- **Above Average (60-69):** 기준 충족 + 일부 약점, 눌림목 매수

---

## 워크플로

### Step 1: API 접근 및 요구사항 확인

사용자 환경에 FMP API key가 설정되어 있는지 확인:

```bash
# Check environment variable
echo $FMP_API_KEY

# If not set, prompt user to provide it
```

**요구사항:**
- **FMP API key** (free tier: 250 calls/day, 40종목 기준 한계 근접)
- **Python 3.7+** 및 필수 라이브러리:
  - `requests` (FMP API calls)
  - `beautifulsoup4` (Finviz web scraping)
  - `lxml` (HTML parsing)

**설치:**
```bash
pip install requests beautifulsoup4 lxml
```

API key가 없으면 다음을 안내:
1. https://site.financialmodelingprep.com/developer/docs 에 가입
2. free API key 발급(250 calls/day)
3. 환경변수 설정: `export FMP_API_KEY=your_key_here`

### Step 2: 종목 유니버스 결정

**Option A: 기본 유니버스 (권장)**
스크립트에 사전 정의된 S&P 500 시총 상위 40종목 사용:

```bash
python3 skills/canslim-screener/scripts/screen_canslim.py
```

**Option B: 커스텀 유니버스**
사용자가 심볼 목록/섹터를 직접 지정:

```bash
python3 skills/canslim-screener/scripts/screen_canslim.py \
  --universe AAPL MSFT GOOGL AMZN NVDA META TSLA
```

**Option C: 섹터 특화 유니버스**
사용자가 Technology, Healthcare 등 섹터 중심 리스트 제공

**API 예산 고려사항 (Phase 3):**
- 40 stocks × 7 FMP calls/stock = 280 calls
  - FMP: 종목당 7 calls (profile, quote, income×2, historical_90d, historical_365d, institutional)
  - Finviz: 종목당 약 1.8 calls (기관 보유 fallback, 2초 rate limit, FMP 예산 미포함)
- Market data(^GSPC quote, ^VIX quote, ^GSPC 52-week history): 3 FMP calls
- 총합: screening 1회당 약 283 FMP calls (free tier 250 초과)
- **권장**: free tier는 `--max-candidates 35` 사용(35 × 7 + 3 = 248), 40종목은 FMP Starter tier($29.99/mo, 750 calls/day) 권장

### Step 3: CANSLIM 스크리닝 스크립트 실행

적절한 파라미터로 메인 스크립트를 실행:

```bash
cd /Users/takueisaotome/PycharmProjects/claude-trading-skills/skills/canslim-screener/scripts

# Basic run (40 stocks, top 20 in report)
python3 screen_canslim.py --api-key $FMP_API_KEY

# Custom parameters
python3 screen_canslim.py \
  --api-key $FMP_API_KEY \
  --max-candidates 40 \
  --top 20 \
  --output-dir ../../../
```

**스크립트 워크플로 (Phase 3 - Full CANSLIM):**
1. **Market Direction (M)**: S&P 500 vs 50-day EMA 분석(정확한 EMA를 위해 실제 과거 데이터 사용)
   - bear market 감지(M=0) 시 현금 비중 확대 경고
2. **S&P 500 과거 데이터**: M component EMA와 L component RS 계산용 52주 데이터 수집
3. **종목 분석**: 각 종목별 계산
   - **C Component**: 분기 EPS/revenue YoY 성장
   - **A Component**: 3년 EPS CAGR 및 안정성
   - **N Component**: 52-week high 대비 거리, breakout 감지
   - **S Component**: 거래량 기반 accumulation/distribution (상승일 vs 하락일 volume)
   - **L Component**: S&P 500 대비 52주 Relative Strength
   - **I Component**: 기관 holder 수 + ownership % (Finviz fallback 포함)
4. **Composite Scoring**: 7개 요소 가중 평균
5. **Ranking**: composite score 내림차순 정렬
6. **Reporting**: JSON + Markdown 출력 생성

**예상 실행 시간 (Phase 3):**
- 40종목: **약 2분** (L component용 종목별 52주 데이터 추가 호출)
- Finviz fallback은 종목당 약 2초 추가(rate limiting)
- L component는 종목별 365일 historical data 필요

**Finviz Fallback 동작:**
- FMP `sharesOutstanding` 누락 시 자동 발동
- Finviz.com에서 기관 ownership % 스크래핑(free, API key 불필요)
- I component 정확도 35/100(부분 데이터) → 60-100/100(완전 데이터)로 향상
- 사용자 로그 예시: `✅ Using Finviz institutional ownership for NVDA: 68.3%`

### Step 4: 스크리닝 결과 읽기 및 파싱

스크립트는 두 개의 출력 파일을 생성합니다:
- `canslim_screener_YYYY-MM-DD_HHMMSS.json` - 구조화 데이터
- `canslim_screener_YYYY-MM-DD_HHMMSS.md` - 사람이 읽는 보고서

Markdown 보고서를 읽어 상위 후보를 확인:

```bash
# Find the latest report
ls -lt canslim_screener_*.md | head -1

# Read the report
cat canslim_screener_YYYY-MM-DD_HHMMSS.md
```

**보고서 구조 (Phase 3 - Full CANSLIM):**
- Market Condition Summary (trend, M score, warnings)
- Top N CANSLIM Candidates (N = --top)
- 종목별:
  - Composite Score 및 Rating (Exceptional+/Exceptional/Strong 등)
  - Component Breakdown (C, A, N, S, L, I, M score + 상세)
  - Interpretation (등급 설명, 가이드, weakest component)
  - Warnings (품질 이슈, 시장 상황, 데이터 소스 노트)
- Summary Statistics (등급 분포)
- Methodology note (Phase 3: 7개 요소, 100% coverage)

**보고서의 요소 상세 예시:**
- **S Component**: "Up/Down Volume Ratio: 1.06 ✓ Accumulation"
- **L Component**: "52wk: +45.2% (+22.1% vs S&P) RS: 88"
- **I Component**: "6199 holders, 68.3% ownership ⭐ Superinvestor"

### Step 5: 상위 후보 분석 및 권고

상위 랭크 종목을 리뷰하고 레퍼런스 문서와 교차 검증:

**참고 문서:**
1. `references/interpretation_guide.md` - 등급 밴드/포트폴리오 사이징 해석
2. `references/canslim_methodology.md` - 요소 의미 심화(S, I 포함)
3. `references/scoring_system.md` - 점수 산식 이해(Phase 3 가중치)

**분석 프레임워크:**

**Exceptional+ (90-100점)**:
- 전 요소가 거의 완벽(C≥85, A≥85, N≥85, S≥80, L≥85, I≥80, M≥80)
- 가이드: 즉시 매수, 공격적 사이징(포트폴리오 15-20%)
- 예시: "NVDA 97.2점 - 폭발적 분기 실적(100), 강한 3년 성장(95), 신고가(98), 거래량 축적(85), RS 리더(92), 강한 기관 수급(90), uptrend 시장(100)"

**Exceptional (80-89점)**:
- 뛰어난 펀더멘털 + 강한 모멘텀
- 가이드: Strong buy, 표준 사이징(10-15%)

**Strong (70-79점)**:
- 전 요소가 견고, 일부 약점
- 가이드: Buy, 표준 사이징(8-12%)
- Phase 3 예시: "77.5점 - 강한 실적(85), 견조 성장(80), 신고가 근접(70), accumulation(60), RS leader(75), 양호한 기관(60), uptrend(90)"

**Above Average (60-69점)**:
- 기준 충족, 1개 요소 약함
- 가이드: 눌림목 매수, 보수적 사이징(5-8%)

**Bear Market Override:**
- M component = 0(베어마켓)면 다른 점수가 좋아도 **매수 금지**
- 가이드: 현금 80-100% 확대, 시장 회복 대기
- CANSLIM은 베어마켓에서 효율이 낮음(주식 4개 중 3개가 시장 추세를 따름)

### Step 6: 사용자용 보고서 생성

사용자에게 간결하고 실행 가능한 요약을 작성합니다.

**보고서 형식:**

```markdown
# CANSLIM Stock Screening Results (Phase 3 - Full CANSLIM)
**Date:** YYYY-MM-DD
**Market Condition:** [Trend] - M Score: [X]/100
**Stocks Analyzed:** [N]
**Components:** C, A, N, S, L, I, M (7 of 7, 100% coverage)

## Market Summary
[2-3 sentences on current market environment based on M component]
[If bear market: WARNING - Consider raising cash allocation]

## Top 5 CANSLIM Candidates

### 1. [SYMBOL] - [Company Name] ⭐⭐⭐
**Score:** [X.X]/100 ([Rating])
**Price:** $[XXX.XX] | **Sector:** [Sector]

**Component Breakdown:**
- C (Earnings): [X]/100 - [EPS growth]% QoQ, [Revenue growth]% revenue
- A (Growth): [X]/100 - [CAGR]% 3yr EPS CAGR
- N (Newness): [X]/100 - [Distance]% from 52wk high
- S (Supply/Demand): [X]/100 - Up/Down Volume Ratio: [X.XX]
- L (Leadership): [X]/100 - 52wk: [+X.X]% ([+X.X]% vs S&P) RS: [XX]
- I (Institutional): [X]/100 - [N] holders, [X.X]% ownership [⭐ Superinvestor if present]
- M (Market): [X]/100 - [Trend]

**Interpretation:** [Rating description and guidance]
**Weakest Component:** [X] ([score])
**Data Source Note:** [If Finviz used: "Institutional data from Finviz"]

[Repeat for top 5 stocks]

## Investment Recommendations

**Immediate Buy List (90+ score):**
- [List stocks with exceptional+ ratings]
- Position sizing: 15-20% each

**Strong Buy List (80-89 score):**
- [List stocks with exceptional ratings]
- Position sizing: 10-15% each

**Watchlist (70-79 score):**
- [List stocks with strong ratings]
- Buy on pullback

## Risk Factors
- [Identify any quality warnings from components]
- [Market condition warnings]
- [Sector concentration risks if applicable]
- [Data source reliability notes if Finviz heavily used]

## Next Steps
1. Conduct detailed fundamental analysis on top 3 candidates
2. Check earnings calendars for upcoming reports
3. Review technical charts for entry timing
4. [If bear market: Wait for market recovery before deploying capital]

---
**Note:** This is Phase 3 (Full CANSLIM: C, A, N, S, L, I, M - 100% coverage).
```

---

## 리소스

### Scripts 디렉터리 (`scripts/`)

**메인 스크립트:**
- `screen_canslim.py` - 메인 오케스트레이터
  - 스크리닝 워크플로 진입점
  - 인자 파싱, API 조정, 랭킹, 리포팅 처리
  - 사용법: `python3 screen_canslim.py --api-key KEY [options]`

- `fmp_client.py` - FMP API 클라이언트 래퍼
  - rate limiting (호출 간 0.3초)
  - 429 에러 시 60초 후 재시도
  - session 기반 캐싱
  - 메서드: `get_income_statement()`, `get_quote()`, `get_historical_prices()`, `get_institutional_holders()`

- `finviz_stock_client.py` - Finviz 웹 스크래핑 클라이언트 ← **NEW**
  - BeautifulSoup 기반 HTML 파싱
  - Finviz.com에서 기관 ownership % 수집
  - rate limiting (호출 간 2.0초)
  - API key 불필요(free scraping)
  - 메서드: `get_institutional_ownership()`, `get_stock_data()`

**계산기 (`scripts/calculators/`):**
- `earnings_calculator.py` - C component (Current Earnings)
  - 분기 EPS/revenue YoY 성장
  - 점수: 50%+ = 100pts, 30-49% = 80pts, 18-29% = 60pts

- `growth_calculator.py` - A component (Annual Growth)
  - 3년 EPS CAGR 계산
  - 안정성 점검(음수 성장 연도 없음)
  - 점수: 40%+ = 90pts, 30-39% = 70pts, 25-29% = 50pts

- `new_highs_calculator.py` - N component (Newness)
  - 52-week high 대비 거리
  - 거래량 확인 breakout 감지
  - 점수: 고점 5% 이내 + breakout = 100pts, 10% 이내 + breakout = 80pts

- `supply_demand_calculator.py` - S component (Supply/Demand) ← **NEW**
  - 거래량 기반 accumulation/distribution 분석
  - 상승일 vs 하락일 volume 비율(60일 lookback)
  - 점수: ratio ≥2.0 = 100pts, 1.5-2.0 = 80pts, 1.0-1.5 = 60pts

- `leadership_calculator.py` - L component (Leadership/Relative Strength)
  - S&P 500 대비 52주 성과
  - RS Rank 추정(1-99 scale, O'Neil 방식)
  - 점수: RS 90+ & 시장 초과성과 = 100pts, RS 80-89 = 80pts

- `institutional_calculator.py` - I component (Institutional)
  - 기관 holder 수(FMP)
  - ownership %(FMP 또는 Finviz fallback)
  - Superinvestor 탐지(Berkshire Hathaway, Baupost 등)
  - 점수: 50-100 holders + 30-60% ownership = 100pts

- `market_calculator.py` - M component (Market Direction)
  - S&P 500 vs 50-day EMA
  - VIX 조정 점수
  - 점수: Strong uptrend = 100pts, Uptrend = 80pts, Bear market = 0pts

**지원 모듈:**
- `scorer.py` - composite score 계산
  - Phase 3 가중 평균: C×15% + A×20% + N×15% + S×15% + L×20% + I×10% + M×5%
  - 등급 해석(Exceptional+/Exceptional/Strong 등)
  - 최소 기준 검증(7개 요소 모두 baseline 충족 필요)

- `report_generator.py` - 출력 생성
  - JSON export (programmatic use)
  - Markdown export (human-readable)
  - Phase 3 요소 분해 표(7개 요소 전체)
  - 요약 통계 계산

### References 디렉터리 (`references/`)

**지식 베이스:**
- `references/canslim_methodology.md` (27KB) - CANSLIM 전체 설명
  - O'Neil 원본 임계값 기반 7개 요소
  - S component(Volume accumulation/distribution) 상세
  - L component(Leadership/Relative Strength) 상세
  - I component(Institutional sponsorship) 상세
  - 역사적 예시(AAPL 2009, NFLX 2013, TSLA 2019, NVDA 2023)

- `references/scoring_system.md` (21KB) - 기술 점수 규격(Phase 3)
  - Phase 3 가중치/산식(7개 요소 전체)
  - 해석 밴드(90-100, 80-89 등)
  - 7개 요소 최소 기준
  - composite score 계산 예시

- `references/fmp_api_endpoints.md` (18KB) - API 통합 가이드(Phase 3)
  - 7개 요소 필수 endpoint
  - L component: 52-week historical prices endpoint
  - institutional holder endpoint 문서
  - Finviz fallback 전략 설명
  - rate limiting 전략
  - 비용 분석(Phase 3: 40종목 약 283 FMP calls, free tier 250 초과)

- `references/interpretation_guide.md` (18KB) - 사용자 가이드
  - 포트폴리오 구성 규칙
  - 등급별 포지션 사이징
  - 진입/청산 전략
  - bear market 보호 규칙

**레퍼런스 사용법:**
- 먼저 `references/canslim_methodology.md`를 읽어 O'Neil 시스템 이해(S, I 포함)
- 결과 해석 시 `references/interpretation_guide.md` 참고
- 점수가 예상과 다르면 `references/scoring_system.md` 참조
- API 문제/Finviz fallback 이슈는 `references/fmp_api_endpoints.md` 확인

---

## 문제 해결 (Troubleshooting)

### Issue 1: FMP API Rate Limit 초과

**증상:**
```
ERROR: 429 Too Many Requests - Rate limit exceeded
Retrying in 60 seconds...
```

**원인:**
- 짧은 시간 내 여러 번 스크리닝 실행
- free tier 250 calls/day 초과
- 동일 API key를 다른 앱이 사용

**해결:**
1. **Wait and Retry**: 스크립트가 60초 후 자동 재시도
2. **유니버스 축소**: `--max-candidates 30`으로 API 사용량 감소
3. **일일 사용량 확인**: free tier는 UTC 자정에 리셋
4. **플랜 업그레이드**: FMP Starter($29.99/month, 750 calls/day)

### Issue 2: 필수 라이브러리 누락

**증상:**
```
ERROR: required libraries not found. Install with: pip install beautifulsoup4 requests lxml
```

**해결:**
```bash
# Install all required libraries
pip install requests beautifulsoup4 lxml

# Or install individually
pip install beautifulsoup4
pip install requests
pip install lxml
```

### Issue 3: Finviz Fallback로 실행 지연

**증상:**
```
Execution time: 2 minutes 30 seconds for 40 stocks (slower than expected)
```

**원인:**
- Finviz rate limiting (요청당 2.0초)
- FMP 데이터 공백으로 모든 종목에서 fallback 발생

**해결:**
1. **지연 수용**: 40종목 기준 1-2분은 정상 범위
2. **fallback 사용량 모니터링**: 로그의 "Using Finviz institutional ownership" 메시지 확인
3. **Rate Limit 조정** (고급): `finviz_stock_client.py`에서 `rate_limit_seconds=2.0` → `1.5`로 변경(IP ban 위험)

**참고:** Finviz fallback은 종목당 약 2초를 추가하지만 I component 정확도를 크게 향상(35 → 60-100점)합니다.

### Issue 4: Finviz 웹 스크래핑 실패

**증상:**
```
WARNING: Finviz request failed with status 403 for NVDA
⚠️ Using Finviz institutional ownership data - FMP shares outstanding unavailable. Finviz fallback also unavailable. Score reduced by 50%.
```

**원인:**
- Finviz의 스크래핑 차단(User-Agent 감지)
- 요청 과다로 rate limit 초과
- 네트워크 이슈 또는 Finviz 다운타임

**해결:**
1. **Wait and Retry**: 몇 분 후 rate limit 리셋
2. **인터넷 연결 확인**: finviz.com 접속 가능 여부 확인
3. **Fallback 허용**: 스크립트는 FMP holder count만으로 계속 진행(I score 상한 70/100)
4. **수동 검증**: IP 차단 여부를 Finviz 웹사이트에서 확인

**Graceful Degradation:**
- Finviz 문제로 스크립트가 중단되지 않음
- FMP holder count only 모드로 자동 전환
- 보고서에 품질 경고 표시

### Issue 5: 최소 기준 충족 종목 없음

**증상:**
```
✓ Successfully analyzed 40 stocks
Top 5 Stocks:
  1. AAPL  -  58.3 (Average)
  2. MSFT  -  55.1 (Average)
  ...
```

**원인:**
- bear market 환경(M component 저점)
- 선택 유니버스의 성장주 부족
- 성장주에서 다른 스타일로 시장 로테이션

**해결:**
1. **M Component 확인**: M=0이면 CANSLIM 규칙대로 현금 확대
2. **유니버스 확장**: 다른 섹터/시총 범위 시도
3. **기대치 조정**: 약세장에서는 55-65점도 실무적으로 의미 있을 수 있음
4. **더 나은 구간 대기**: CANSLIM은 bull market에서 성과가 좋음

### Issue 6: 데이터 품질 경고

**증상:**
```
⚠️ Revenue declining despite EPS growth (possible buyback distortion)
⚠️ Using Finviz institutional ownership data (68.3%) - FMP shares outstanding unavailable.
```

**해석:**
- 오류가 아니라 계산기의 **품질 플래그**
- Revenue 경고: EPS 성장이 유기적 성장보다 자사주 매입 영향일 수 있음
- Finviz 경고: 데이터 소스가 FMP에서 Finviz로 전환됨(여전히 유효)

**조치:**
1. 전체 보고서의 component 상세 검토
2. 펀더멘털 분석으로 교차 확인
3. 리스크 수준에 맞춰 포지션 사이징 조정
4. Finviz 데이터 소스 경고는 일반적으로 추가 조치 불필요

---

## 중요 참고

### Phase 3 구현 상태

이 버전은 CANSLIM 7개 요소 전부를 구현한 **Phase 3**입니다:
- ✅ **C** (Current Earnings) - 구현 완료
- ✅ **A** (Annual Growth) - 구현 완료
- ✅ **N** (Newness) - 구현 완료
- ✅ **S** (Supply/Demand) - 구현 완료
- ✅ **L** (Leadership/RS Rank) - 구현 완료
- ✅ **I** (Institutional) - 구현 완료
- ✅ **M** (Market Direction) - 구현 완료

**의미:**
- composite score가 **전체 CANSLIM 100%**를 반영
- O'Neil 원본 가중치 사용(C 15%, A 20%, N 15%, S 15%, L 20%, I 10%, M 5%)
- L component(20%)는 A와 함께 가장 큰 개별 비중으로 RS 리더십을 강조
- M component는 과거 데이터 기반 실제 50-day EMA 사용(추정 fallback 아님)

### Finviz 통합 이점

**자동 Fallback 시스템:**
- FMP API가 `sharesOutstanding`을 제공하지 않으면 Finviz 자동 활성화
- Finviz.com에서 기관 ownership % 스크래핑(free, API key 불필요)
- I component 정확도 35/100(부분) → 60-100/100(완전) 향상

**데이터 소스 우선순위:**
1. **FMP API** (기본): 기관 holder 수 + shares outstanding 기반 계산
2. **Finviz** (fallback): 웹페이지 직접 기관 ownership %
3. **Partial Data** (최후 수단): holder count only, 50% 페널티 적용

**테스트 신뢰성:**
- Finviz로 39/39 종목 ownership % 수집 성공(성공률 100%)
- 평균 실행 시간: 종목당 2.54초
- 테스트 중 오류/IP 차단 없음

### 향후 개선

**Phase 4 (계획):**
- FINVIZ Elite 사전 스크리닝 통합
- 실행 시간: 2분 → 10-15초
- FMP API 사용량 90% 감소
- 더 큰 유니버스(100+ 종목) 가능

### 데이터 소스 출처

- **FMP API**: 손익계산서, 시세, 과거 가격, key metrics, 기관 holder
- **Finviz**: 기관 ownership %(fallback), 시장 데이터
- **Methodology**: William O'Neil의 "How to Make Money in Stocks" (4th edition)
- **Scoring System**: IBD MarketSmith proprietary system을 기반으로 조정

### 면책 조항

**이 스크리너는 교육 및 정보 제공 목적 전용입니다.**
- 투자 자문이 아님
- 과거 성과가 미래 성과를 보장하지 않음
- CANSLIM은 bull market에서 성능이 가장 좋음(M component 확인)
- 투자 전 스스로 리서치하고 금융 전문가와 상의 필요
- O'Neil의 과거 승자 예시(AAPL 2009: +1,200%, NFLX 2013: +800%)가 있지만, 많은 종목은 기대 성과를 내지 못함

---

**Version:** Phase 3
**Last Updated:** 2026-02-20
**API Requirements:** FMP API (free tier: 최대 35종목; 40종목은 Starter tier 권장) + Finviz용 BeautifulSoup/requests/lxml
**Execution Time:** 40종목 약 2분
**Output Formats:** JSON + Markdown
**Components Implemented:** C, A, N, S, L, I, M (7 of 7, 100% coverage)
