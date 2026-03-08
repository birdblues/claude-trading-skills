---
name: value-dividend-screener
description: 가치 특성(P/E 20 미만, P/B 2 미만), 매력적인 배당수익률(3% 이상), 그리고 일관된 성장(배당/매출/EPS 3년 상승 추세)을 결합해 미국 주식의 고품질 배당 기회를 스크리닝합니다. FINVIZ Elite API로 효율적인 1차 필터링 후 FMP API로 상세 분석하는 2단계 스크리닝을 지원합니다. 배당주 스크리닝, 인컴 포트폴리오 아이디어, 견고한 펀더멘털의 가치주를 요청할 때 사용하세요.
---

# Value Dividend Screener

## Overview

이 스킬은 **two-stage screening approach**를 사용해 가치 특성, 매력적 인컴, 일관된 성장을 동시에 갖춘 고품질 배당주를 식별합니다:

1. **FINVIZ Elite API (Optional but Recommended)**: 기본 조건으로 사전 스크리닝(빠르고 비용 효율적)
2. **Financial Modeling Prep (FMP) API**: 후보 종목의 상세 펀더멘털 분석

미국 주식을 밸류에이션 비율, 배당 지표, 재무 건전성, 수익성 등 정량 기준으로 스크리닝합니다. composite quality score 기반 순위와 함께 상세 펀더멘털 분석 리포트를 생성합니다.

**Efficiency Advantage**: FINVIZ 사전 스크리닝을 사용하면 FMP API 호출을 최대 90% 줄일 수 있어 free-tier 사용자에게 유리합니다.

## When to Use

사용자가 다음을 요청할 때 이 스킬을 호출합니다:
- "고품질 배당주를 찾아줘"
- "가치 배당 기회를 스크리닝해줘"
- "배당 성장성이 좋은 종목을 보여줘"
- "합리적 밸류에 거래되는 인컴 주식을 찾아줘"
- "지속 가능한 고배당 종목을 스크리닝해줘"
- 배당수익률, 밸류에이션, 펀더멘털 분석을 결합한 모든 요청

## Workflow

### Step 1: Verify API Key Availability

**For Two-Stage Screening (Recommended):**

두 API key 모두 있는지 확인:

```python
import os
fmp_api_key = os.environ.get('FMP_API_KEY')
finviz_api_key = os.environ.get('FINVIZ_API_KEY')
```

없으면 사용자에게 API key 제공 또는 환경 변수 설정을 요청:
```bash
export FMP_API_KEY=your_fmp_key_here
export FINVIZ_API_KEY=your_finviz_key_here
```

**For FMP-Only Screening:**

FMP API key 존재 여부 확인:

```python
import os
api_key = os.environ.get('FMP_API_KEY')
```

없으면 사용자에게 API key 제공 또는 환경 변수 설정을 요청:
```bash
export FMP_API_KEY=your_key_here
```

**FINVIZ Elite API Key:**
- FINVIZ Elite 구독 필요(~$40/month 또는 ~$330/year)
- 사전 스크리닝 결과 CSV export 접근 제공
- FMP 사용량 절감을 위해 강력 권장

필요하면 `references/fmp_api_guide.md`의 안내를 제공합니다.

### Step 2: Execute Screening Script

적절한 파라미터로 스크리닝 스크립트를 실행합니다:

#### **Two-Stage Screening (RECOMMENDED)**

FINVIZ 사전 스크리닝 후 FMP 상세 분석 수행:

**Default execution (Top 20 stocks):**
```bash
python3 scripts/screen_dividend_stocks.py --use-finviz
```

**With explicit API keys:**
```bash
python3 scripts/screen_dividend_stocks.py --use-finviz \
  --fmp-api-key $FMP_API_KEY \
  --finviz-api-key $FINVIZ_API_KEY
```

**Custom top N:**
```bash
python3 scripts/screen_dividend_stocks.py --use-finviz --top 50
```

**Custom output location:**
```bash
python3 scripts/screen_dividend_stocks.py --use-finviz --output /path/to/results.json
```

**Script behavior (Two-Stage):**
1. FINVIZ Elite pre-screening:
   - Market cap: Mid-cap 이상
   - Dividend yield: 3%+
   - Dividend growth (3Y): 5%+
   - EPS growth (3Y): Positive
   - P/B: Under 2
   - P/E: Under 20
   - Sales growth (3Y): Positive
   - Geography: USA
2. FINVIZ 결과(보통 20-50개)에 대한 FMP 상세 분석:
   - Dividend growth rate 계산(3-year CAGR)
   - Revenue/EPS 추세 분석
   - Dividend sustainability 평가(payout ratio, FCF coverage)
   - 재무 건전성 지표(debt-to-equity, current ratio)
   - 품질 점수화(ROE, profit margin)
3. Composite score 계산 및 랭킹
4. 상위 N개 종목을 JSON 파일로 출력

**Expected runtime (Two-Stage):** FINVIZ 후보 30-50개 기준 2-3분(FMP-only 대비 훨씬 빠름)

#### **FMP-Only Screening (Original Method)**

FMP Stock Screener API만 사용(API 사용량 높음):

**Default execution:**
```bash
python3 scripts/screen_dividend_stocks.py
```

**With explicit API key:**
```bash
python3 scripts/screen_dividend_stocks.py --fmp-api-key $FMP_API_KEY
```

**Script behavior (FMP-Only):**
1. FMP Stock Screener API로 1차 스크리닝(dividend yield >=3.0%, P/E <=20, P/B <=2)
2. 후보(보통 100-300종목) 상세 분석:
   - two-stage와 동일한 상세 분석 수행
3. Composite score 계산 및 랭킹
4. 상위 N개 종목 JSON 출력

**Expected runtime (FMP-Only):** 100-300개 후보 기준 5-15분(rate limiting 적용)

**API Usage Comparison:**
- Two-Stage: ~50-100 FMP API calls (FINVIZ가 ~30개로 사전 필터)
- FMP-Only: ~500-1500 FMP API calls (스크리너 결과 전체 분석)

### Step 3: Parse and Analyze Results

생성된 JSON 파일을 읽습니다:

```python
import json

with open('dividend_screener_results.json', 'r') as f:
    data = json.load(f)

metadata = data['metadata']
stocks = data['stocks']
```

**Key data points per stock:**
- 기본 정보: `symbol`, `company_name`, `sector`, `market_cap`, `price`
- 밸류에이션: `dividend_yield`, `pe_ratio`, `pb_ratio`
- 성장 지표: `dividend_cagr_3y`, `revenue_cagr_3y`, `eps_cagr_3y`
- 지속가능성: `payout_ratio`, `fcf_payout_ratio`, `dividend_sustainable`
- 재무 건전성: `debt_to_equity`, `current_ratio`, `financially_healthy`
- 품질: `roe`, `profit_margin`, `quality_score`
- 종합 랭킹: `composite_score`

### Step 4: Generate Markdown Report

사용자용 구조화 markdown 리포트를 다음 섹션으로 작성합니다:

#### Report Structure

```markdown
# Value Dividend Stock Screening Report

**Generated:** [Timestamp]
**Screening Criteria:**
- Dividend Yield: >= 3.5%
- P/E Ratio: <= 20
- P/B Ratio: <= 2
- Dividend Growth (3Y CAGR): >= 5%
- Revenue Trend: Positive over 3 years
- EPS Trend: Positive over 3 years

**Total Results:** [N] stocks

---

## Top 20 Stocks Ranked by Composite Score

| Rank | Symbol | Company | Yield | P/E | Div Growth | Score |
|------|--------|---------|-------|-----|------------|-------|
| 1 | [TICKER] | [Name] | [%] | [X.X] | [%] | [XX.X] |
| ... |

---

## Detailed Analysis

### 1. [SYMBOL] - [Company Name] (Score: XX.X)

**Sector:** [Sector Name]
**Market Cap:** $[X.XX]B
**Current Price:** $[XX.XX]

**Valuation Metrics:**
- Dividend Yield: [X.X]%
- P/E Ratio: [XX.X]
- P/B Ratio: [X.X]

**Growth Profile (3-Year):**
- Dividend CAGR: [X.X]% [✓ Consistent / ⚠ One cut]
- Revenue CAGR: [X.X]%
- EPS CAGR: [X.X]%

**Dividend Sustainability:**
- Payout Ratio: [XX]%
- FCF Payout Ratio: [XX]%
- Status: [✓ Sustainable / ⚠ Monitor / ❌ Risk]

**Financial Health:**
- Debt-to-Equity: [X.XX]
- Current Ratio: [X.XX]
- Status: [✓ Healthy / ⚠ Caution]

**Quality Metrics:**
- ROE: [XX]%
- Net Profit Margin: [XX]%
- Quality Score: [XX]/100

**Investment Considerations:**
- [Key strength 1]
- [Key strength 2]
- [Risk factor or consideration]

---

[Repeat for other top stocks]

---

## Portfolio Construction Guidance

**Diversification Recommendations:**
- Sector breakdown of top 20 results
- Suggested allocation strategy
- Concentration risk warnings

**Monitoring Recommendations:**
- Key metrics to track quarterly
- Warning signs for each position
- Rebalancing triggers

**Risk Considerations:**
- Market cap concentration
- Sector biases in results
- Economic sensitivity warnings
```

### Step 5: Provide Context and Methodology

결과 설명 시 스크리닝 방법론을 함께 제공합니다:

**Key concepts to explain:**
- 왜 이 임계값을 쓰는지(3.5% yield, P/E 20, P/B 2)
- 정적 고배당보다 배당 성장성이 중요한 이유
- composite score가 value, growth, quality를 어떻게 균형화하는지
- dividend sustainability와 dividend trap의 구분
- 재무 건전성 지표의 중요성

`references/screening_methodology.md`를 로드해 아래를 상세히 설명합니다:
- Phase 1: Initial quantitative filters
- Phase 2: Growth quality filters
- Phase 3: Sustainability and quality analysis
- Composite scoring system
- Investment philosophy and limitations

### Step 6: Answer Follow-up Questions

사용자 후속 질문에 대비:

**"Why did [stock] not make the list?"**
- 어떤 기준에서 탈락했는지 확인(yield, valuation, growth, sustainability)
- 제외된 구체 필터를 설명

**"Can I screen for specific sectors?"**
- 스크립트에서 필터링 가능(라인 383-388 수정)
- sector 파라미터를 추가해 재실행 제안

**"What if I want higher/lower yield threshold?"**
- 스크립트 파라미터 조정 가능
- yield와 growth 간 트레이드오프 설명
- 새 조건으로 재스크리닝 권장

**"How often should I re-run this screen?"**
- 분기별 실행 권장(실적 사이클 정합)
- 장기 보유자는 반기별도 충분
- 시장 환경에 따라 더 잦은 실행이 필요할 수 있음

**"How many stocks should I buy?"**
- 배당 포트폴리오 분산 가이드: 최소 10-15종목
- 섹터 균형 고려
- 위험 성향 기반 포지션 사이징 적용

## Resources

### scripts/screen_dividend_stocks.py

다음을 수행하는 종합 스크리닝 스크립트:
- FMP API 연동 데이터 수집
- 다단계 필터링 로직 구현
- 3년 성장률(CAGR) 계산
- payout ratio/FCF coverage 기반 배당 지속가능성 평가
- 재무 건전성 평가(D/E, current ratio)
- 품질 점수 계산(ROE, profit margins)
- composite score 순위화
- 구조화 JSON 결과 출력

**Dependencies:** `requests` 라이브러리 (`pip install requests`)

**Rate limiting:** FMP 한도(무료 250 requests/day)를 고려한 내장 지연

**Error handling:** 결측 데이터, rate limit 재시도, API 에러에 대한 graceful degradation

### references/screening_methodology.md

스크리닝 접근법 종합 문서:

**Phase 1: Initial Quantitative Filters**
- dividend yield >= 3.5%의 근거 및 계산
- P/E ratio <= 20 임계값 근거
- P/B ratio <= 2 밸류에이션 논리

**Phase 2: Growth Quality Filters**
- Dividend growth (3-year CAGR >= 5%)
- Revenue 양(+) 추세 분석
- EPS 양(+) 추세 분석

**Phase 3: Quality & Sustainability Analysis**
- dividend sustainability 지표(payout ratio, FCF coverage)
- 재무 건전성 지표(D/E, current ratio)
- 품질 점수 방법론(ROE, profit margins)

**Composite Scoring System (0-100 points)**
- 점수 구성 요소 및 가중치
- 해석 가이드라인

**Investment Philosophy**
- 이 접근법이 유효한 이유
- 회피 대상(dividend trap, value trap)
- 이상적 후보 프로필

**Usage Notes & Limitations**
- 포트폴리오 구성 best practice
- 매도 기준 시점
- 임계값의 역사적 배경

### references/fmp_api_guide.md

Financial Modeling Prep API 완전 가이드:

**API Key Setup**
- 무료 API key 발급
- 환경 변수 설정
- free tier 한도(250 requests/day)

**Key Endpoints Used**
- Stock Screener API
- Income Statement API
- Balance Sheet API
- Cash Flow Statement API
- Key Metrics API
- Historical Dividend API

**Rate Limiting Strategy**
- 스크립트 내장 보호 로직
- request budget 관리
- free tier 운영 best practice

**Error Handling**
- 일반 에러 및 해결책
- 디버깅 기법

**Data Quality Considerations**
- 데이터 최신성 및 결측
- 데이터 정확성 관련 주의사항
- SEC filing으로 교차검증이 필요한 경우

## Advanced Usage

### Customizing Screening Criteria

`scripts/screen_dividend_stocks.py`에서 임계값 수정:

**Line 383-388** - 초기 스크리닝 파라미터:
```python
candidates = client.screen_stocks(
    dividend_yield_min=3.5,  # Adjust yield threshold
    pe_max=20,               # Adjust P/E threshold
    pb_max=2,                # Adjust P/B threshold
    market_cap_min=2_000_000_000  # Minimum $2B market cap
)
```

**Line 423** - Dividend CAGR 임계값:
```python
if not div_cagr or div_cagr < 5.0:  # Adjust growth threshold
```

### Sector-Specific Screening

초기 스크리닝 후 sector 필터 추가:

```python
# Filter for specific sectors
target_sectors = ['Consumer Defensive', 'Utilities', 'Healthcare']
candidates = [s for s in candidates if s.get('sector') in target_sectors]
```

### Excluding REITs and Financials

REITs와 금융주는 배당 특성이 다릅니다(높은 payout, 다른 지표 체계):

```python
# Exclude REITs and Financials
exclude_sectors = ['Real Estate', 'Financial Services']
candidates = [s for s in candidates if s.get('sector') not in exclude_sectors]
```

### Exporting to CSV

JSON 결과를 CSV로 변환해 Excel 분석에 사용:

```python
import json
import csv

with open('dividend_screener_results.json', 'r') as f:
    data = json.load(f)

stocks = data['stocks']

with open('screening_results.csv', 'w', newline='') as csvfile:
    if stocks:
        fieldnames = stocks[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(stocks)
```

## Troubleshooting

### "ERROR: requests library not found"
**Solution:** requests 라이브러리 설치
```bash
pip install requests
```

### "ERROR: FMP API key required"
**Solution:** 환경 변수 설정 또는 command-line로 전달
```bash
export FMP_API_KEY=your_key_here
# OR
python3 scripts/screen_dividend_stocks.py --fmp-api-key your_key_here
```

### "ERROR: FINVIZ API key required when using --use-finviz"
**Solution:** 환경 변수 설정 또는 command-line로 전달
```bash
export FINVIZ_API_KEY=your_key_here
# OR
python3 scripts/screen_dividend_stocks.py --use-finviz --finviz-api-key your_key_here
```

**Note:** FINVIZ Elite 구독 필요(~$40/month 또는 ~$330/year)

### "ERROR: FINVIZ API authentication failed"
**Possible causes:**
1. 잘못된 FINVIZ API key
2. FINVIZ Elite 구독 만료
3. API key 포맷 오류

**Solution:**
- FINVIZ Elite 구독 활성 상태 확인
- API key 오타 확인(영숫자 문자열)
- FINVIZ Elite 계정 설정에서 API key 재확인
- 구독 상태 확인을 위해 FINVIZ Elite screener 수동 접속 테스트

### "ERROR: FINVIZ pre-screening failed or returned no results"
**Possible causes:**
1. FINVIZ API 연결 문제
2. 스크리닝 조건이 너무 엄격함(해당 종목 없음)
3. 시장 상황 영향(약세장에서는 후보가 적을 수 있음)

**Solution:**
- 인터넷 연결 확인
- FINVIZ Elite 웹사이트 접근 가능 여부 확인
- 대안으로 FMP-only 방식 사용:
  ```bash
  python3 scripts/screen_dividend_stocks.py
  ```

### "WARNING: Rate limit exceeded"
**Solution:** 스크립트는 자동으로 60초 후 재시도합니다. 반복되면:
- 다음 날까지 대기(free tier 일일 리셋)
- 분석 종목 수 축소(line 394 limit 수정)
- FMP 유료 티어 업그레이드 고려

### "No stocks found matching all criteria"
**Solution:** 기준이 과도하게 엄격할 수 있음
- P/E 임계값 완화(20보다 상향)
- 배당수익률 임계값 완화(3.5%보다 하향)
- 배당 성장 임계값 완화(5%보다 하향)
- 시장 환경 점검(약세장에서는 후보가 줄어듦)

### Script runs slowly
**Expected behavior:** rate limiting을 위해 API 호출 간 0.3s 지연 포함
- 100종목 분석 = 약 8-10분
- 최초 20-30개 통과 종목은 보통 50-70개 분석 내에 확인

## Performance & Cost Optimization

### API Call Comparison

**Two-Stage Screening (FINVIZ + FMP):**
- FINVIZ: 1 API call
- FMP Quote API: ~30-50 calls (사전 필터 symbol당 1회)
- FMP Financial Data: ~150-250 calls (5 endpoints × 30-50 symbols)
- **Total FMP calls: ~180-300**

**FMP-Only Screening:**
- FMP Stock Screener: 1 call (100-1000 stocks 반환)
- FMP Financial Data: ~500-5000 calls (5 endpoints × 100-1000 symbols)
- **Total FMP calls: ~500-5000**

**Savings: FMP API 사용량 60-94% 절감**

### Cost Analysis

**FINVIZ Elite:**
- Monthly: $39.99
- Annual: $329.99 (~$27.50/month)

**FMP API:**
- Free tier: 250 calls/day (two-stage screening에는 충분)
- Starter tier: $29.99/month for 750 calls/day
- Professional tier: $79.99/month for 2000 calls/day

**Recommendation:**
- **free FMP tier 사용자**: two-stage screening 사용(FINVIZ + FMP free tier)
- **paid FMP tier 사용자**: 두 방식 모두 가능, two-stage가 더 빠름
- **budget option**: free tier 기반 FMP-only(며칠 간격 실행)
- **optimal option**: FINVIZ Elite($330/year) + FMP free tier = 완성도 높은 조합

## Version History

- **v1.1** (November 2025): two-stage screening을 위한 FINVIZ Elite integration 추가
- **v1.0** (November 2025): 종합 multi-phase screening 초기 릴리스
