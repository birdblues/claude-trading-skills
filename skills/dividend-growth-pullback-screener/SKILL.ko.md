---
name: dividend-growth-pullback-screener
description: RSI 과매도 조건(RSI ≤40)으로 식별된 일시적 눌림 구간에서, 고품질 배당 성장주(연 배당 성장률 12%+, 배당수익률 1.5%+)를 찾을 때 사용하는 스킬입니다. 이 스킬은 배당의 기초체력 분석과 기술적 타이밍 지표를 결합해 단기 약세 구간의 강한 배당 성장주 매수 기회를 식별합니다.
---

# Dividend Growth Pullback Screener

## 개요

이 스킬은 강한 펀더멘털을 갖췄지만 일시적인 기술적 약세를 보이는 배당 성장주를 스크리닝합니다. RSI 과매도 구간(≤40)까지 눌린 고성장 배당주(12%+ CAGR)를 대상으로 하며, 장기 배당 성장 투자자에게 잠재적인 진입 기회를 제공합니다.

**투자 가설:** 고품질 배당 성장주(대개 수익률 1-2.5%)는 높은 현재 배당수익률보다 배당 인상으로 자산을 복리 성장시킵니다. 이런 종목을 일시적 눌림(RSI ≤40)에서 매수하면, 강한 펀더멘털 성장과 유리한 기술적 진입 타이밍을 결합해 총수익률을 개선할 수 있습니다.

## 이 스킬을 사용할 때

다음 상황에서 사용하세요:
- 복리 잠재력이 뛰어난 배당 성장주(배당 CAGR 12%+)를 찾을 때
- 일시적 시장 약세에서 우량주 진입 기회를 찾을 때
- 더 높은 배당 성장을 위해 낮은 현재 수익률(1.5-3%)을 수용할 수 있을 때
- 현재 소득보다 5-10년 총수익률에 집중할 때
- 섹터 로테이션 또는 광범위한 조정으로 우량 종목이 함께 눌린 시장일 때

**다음 경우에는 사용하지 마세요:**
- 높은 현재 배당소득이 목적일 때(value-dividend-screener 사용)
- 즉시 배당수익률 3%+가 필요할 때
- 엄격한 P/E 또는 P/B 기준의 deep value 종목을 찾을 때
- 단기 트레이딩 중심(<6개월)일 때

## 스크리닝 워크플로

### 1단계: API Key 설정

#### Two-Stage 접근 (권장)

최적 성능을 위해 사전 스크리닝은 FINVIZ Elite API, 상세 분석은 FMP API를 사용하세요:

```bash
# Set both API keys as environment variables
export FMP_API_KEY=your_fmp_key_here
export FINVIZ_API_KEY=your_finviz_key_here
```

**왜 Two-Stage인가?**
- **FINVIZ**: RSI 필터 기반 고속 사전 스크리닝(1 API call → 약 10-50개 후보)
- **FMP**: 사전 선별된 후보에만 상세 펀더멘털 분석 수행
- **결과**: FMP API 호출을 줄이면서 더 많은 종목 분석 가능(free tier 제한 내 유지)

#### FMP-Only 접근 (기존 방식)

FINVIZ Elite 접근 권한이 없다면:

```bash
export FMP_API_KEY=your_key_here
```

**제약:** FMP free tier(250 requests/day)는 분석 대상을 약 40개로 제한합니다. 제한 내 운영을 위해 `--max-candidates 40`을 사용하세요.

### 2단계: 스크리닝 실행

**Two-Stage 스크리닝 (권장):**

```bash
cd dividend-growth-pullback-screener/scripts
python3 screen_dividend_growth_rsi.py --use-finviz
```

실행 내용:
1. FINVIZ 사전 스크린: Dividend yield 0.5-3%, Dividend growth 10%+, EPS growth 5%+, Sales growth 5%+, RSI <40
2. FMP 상세 분석: 12%+ 배당 CAGR 검증, 정확한 RSI 계산, 펀더멘털 분석

**FMP-Only 스크리닝:**

```bash
python3 screen_dividend_growth_rsi.py --max-candidates 40
```

**커스터마이징 옵션:**

```bash
# Two-stage with custom parameters
python3 screen_dividend_growth_rsi.py --use-finviz --min-yield 2.0 --min-div-growth 15.0 --rsi-max 35

# FMP-only with custom parameters
python3 screen_dividend_growth_rsi.py --min-yield 2.0 --min-div-growth 10.0 --max-candidates 30

# Provide API keys as arguments (instead of environment variables)
python3 screen_dividend_growth_rsi.py --use-finviz --fmp-api-key YOUR_FMP_KEY --finviz-api-key YOUR_FINVIZ_KEY
```

### 3단계: 결과 검토

스크립트는 두 가지 출력을 생성합니다:

1. **JSON 파일:** `dividend_growth_pullback_results_YYYY-MM-DD.json`
   - 후속 분석용 구조화 데이터(모든 지표 포함)
   - 배당 성장률, RSI 값, 재무건전성 지표 포함

2. **Markdown 보고서:** `dividend_growth_pullback_screening_YYYY-MM-DD.md`
   - 사람이 읽기 쉬운 종목별 분석
   - 시나리오 기반 확률 평가
   - 진입 타이밍 권고

### 4단계: 통과 종목 분석

각 통과 종목에 대해 보고서는 다음을 제공합니다:

**Dividend Growth 프로필:**
- 현재 수익률 및 연 배당금
- 3년 배당 CAGR 및 일관성
- payout ratio 및 지속 가능성 평가

**기술적 타이밍:**
- 현재 RSI 값(≤40 = 과매도)
- RSI 맥락(극단 과매도 <30 vs 초기 눌림 30-40)
- 최근 추세 대비 가격 흐름

**품질 지표:**
- 매출 및 EPS 성장(사업 모멘텀 확인)
- 재무건전성(부채 수준, 유동성 비율)
- 수익성(ROE, 이익률)

**투자 권고:**
- 진입 타이밍 평가(즉시 진입 vs 확인 후 진입)
- 종목별 리스크 요인
- 배당 성장 복리 기반 업사이드 시나리오

## 스크리닝 기준 상세

### 1단계: 펀더멘털 스크리닝 (FMP API)

**초기 필터:**
- Dividend Yield ≥ 1.5% (실제 배당 지급 데이터 기준 계산)
- Market Cap ≥ $2 billion (유동성/안정성)
- 거래소: NYSE, NASDAQ (OTC/pink sheet 제외)

**배당 성장 분석:**
- 3-Year Dividend CAGR ≥ 12% (6년 내 배당 2배)
- 배당 일관성: 최근 4년 배당 삭감 없음
- Payout Ratio < 100% (지속 가능성 점검)

**재무건전성:**
- 3년 매출 성장 양수
- 3년 EPS 성장 양수
- Debt-to-Equity < 2.0 (관리 가능한 레버리지)
- Current Ratio > 1.0 (유동성)

### 2단계: 기술적 스크리닝 (RSI 계산)

**RSI 계산:**
- 일간 종가 기준 14-period RSI
- 공식: RSI = 100 - (100 / (1 + RS))
  - RS = 14기간 평균 상승폭 / 평균 하락폭
- 데이터 소스: FMP 과거 가격(최근 30일)

**RSI 필터:**
- RSI ≤ 40 (과매도/눌림 조건)
- RSI 해석:
  - < 30: 극단 과매도(반등 가능성)
  - 30-40: 초기 눌림(상승추세 조정)
  - > 40: 과매도 아님(제외)

### 3단계: 랭킹 및 출력

**종합 점수 (0-100):**
- Dividend Growth (40%): 높은 CAGR와 일관성 가점
- Financial Quality (30%): ROE, 이익률, 부채 수준
- Technical Setup (20%): RSI가 낮을수록 진입 기회 우수
- Valuation (10%): P/E, P/B는 참고용(배제 기준 아님)

종합 점수로 종목을 정렬합니다. 상위 종목은 뛰어난 배당 성장과 매력적인 기술적 진입 지점을 동시에 갖습니다.

## 결과 해석

### RSI 구간 해석

**RSI 25-30 (극단 과매도):**
- 공포성 매도 또는 부정적 뉴스 반영이 잦음
- 위험은 높지만 잠재 보상도 큼
- 권장: RSI 반등 전환(안정화 신호) 확인 후 진입
- 진입: 50% 선진입, RSI >30에서 추가 매수

**RSI 30-35 (강한 과매도):**
- 강한 상승추세 내 정상 조정 구간
- 극단 과매도 대비 위험 낮음
- 권장: 즉시 포지션 진입 가능
- 진입: 풀 포지션 가능, 손절은 진입가 대비 5-8% 하단

**RSI 35-40 (초기 눌림):**
- 상승추세 내 완만한 약세
- 추가 하락 위험이 가장 낮은 구간
- 권장: 확신 높은 종목에 보수적 진입
- 진입: 풀 포지션, 타이트한 손절(3-5% 하단)

### 배당 성장 복리 예시

**12% Dividend CAGR (최소 기준):**
- 시작 수익률: 1.5%
- 6년차: 원가 기준 수익률 2.96% (2배)
- 12년차: 원가 기준 수익률 5.85% (4배)
- 예시: Visa (V), Mastercard (MA) 과거 프로필

**15% Dividend CAGR (우수):**
- 시작 수익률: 1.8%
- 6년차: 원가 기준 수익률 4.08% (2.3배)
- 12년차: 원가 기준 수익률 9.22% (5.1배)
- 예시: Microsoft (MSFT) 2010-2020 구간

**20% Dividend CAGR (탁월):**
- 시작 수익률: 2.0%
- 6년차: 원가 기준 수익률 6.00% (3배)
- 12년차: 원가 기준 수익률 18.0% (9배)
- 예시: Apple (AAPL) 2012-2020 구간

**핵심 인사이트:** 낮은 시작 수익률 + 높은 성장률은 10년+ 구간에서 높은 시작 수익률 + 낮은 성장률보다 유리합니다.

## 문제 해결

### 결과가 없을 때

**가능한 원인:**
1. **시장 환경:** 강한 bull market으로 과매도 종목이 적음
2. **기준 과도:** 12% 배당 성장은 희소(보통 5-10개 종목만 통과)
3. **RSI 임계값 과도:** 후보 확대를 위해 RSI ≤45 고려

**해결 방법:**
- RSI 완화: `--rsi-max 45` (초기 눌림 구간 포함)
- 배당 성장 기준 완화: `--min-div-growth 10.0` (여전히 우수한 성장)
- 최소 수익률 완화: `--min-yield 1.0` (성장주 더 포괄)

### API Rate Limit 도달

**FMP Free Tier 제한:**
- 250 requests/day
- 종목당 분석에 6 API calls 필요(quote, dividend, prices, income, balance, cashflow, metrics)
- FMP-only 모드에서 하루 최대 약 40종목

**해결 방법:**

**1. FINVIZ Two-Stage 접근 사용 (권장)**
```bash
python3 screen_dividend_growth_rsi.py --use-finviz
```
- FINVIZ 사전 스크리닝: 1 API call → 10-50 후보(RSI 기준 선별 완료)
- FMP 분석: 6 calls × 10-50 종목 = 60-300 FMP calls
- **장점**: FINVIZ RSI 필터로 후보 수를 크게 줄여 FMP 한도 내 유지 용이

**2. FMP-Only 후보 수 제한**
```bash
python3 screen_dividend_growth_rsi.py --max-candidates 40
```

**3. 24시간 후 limit reset 대기**
- FMP는 UTC 자정에 리셋

**4. FMP 유료 플랜 업그레이드**
- Starter ($14/month): 500 requests/day
- Professional ($29/month): 1,000 requests/day

**참고:** 이 사용 사례에서는 FINVIZ Elite($40/month) + FMP free tier 조합이 FMP 단독 유료 플랜보다 비용 효율적인 경우가 많습니다.

### RSI 계산 오류

**문제:** "Insufficient price data for RSI calculation"

**원인:** 상장 초기 또는 비활성 종목으로 30일 미만 거래 이력

**해결:** 스크립트가 데이터 부족 종목을 자동으로 건너뜁니다. 별도 조치 불필요.

## 다른 스킬과 결합

**사전 스크리닝 컨텍스트:**
1. **Market News Analyst** → 섹터 로테이션/시장 조정 여부 파악
2. **Breadth Chart Analyst** → 시장 전반 과매도 확인
3. **Economic Calendar Fetcher** → 금리결정/매크로 이벤트 일정 확인

**스크리닝 후 분석:**
1. **Technical Analyst** → 통과 종목 개별 차트 분석
2. **US Stock Analysis** → 진입 전 종목 심층 분석
3. **Backtest Expert** → RSI + 배당 성장 전략 히스토리 검증

**예시 워크플로:**
```
1. Market News Analyst: "Market pulled back 5% this week on Fed hawkish comments"
2. Breadth Chart Analyst: Confirms market oversold (S&P breadth weak)
3. Dividend Growth Pullback Screener: Finds 8 quality dividend growers with RSI <35
4. Technical Analyst: Analyze top 3 candidates for support levels and entry timing
5. Execute: Enter scaled positions with 6-12 month time horizon
```

## 리소스

### scripts/

**screen_dividend_growth_rsi.py** - 메인 스크리닝 스크립트
- 펀더멘털 데이터용 FMP API 연동
- 과거 가격으로 14-period RSI 계산
- 다단계 필터링 및 랭킹 적용
- JSON/markdown 보고서 출력

### references/

**rsi_oversold_strategy.md** - RSI 지표 설명
- RSI가 과매도 구간을 식별하는 방식
- 극단 과매도(<30)와 초기 눌림(30-40)의 차이
- RSI와 펀더멘털 분석 결합 방법
- false positive 관리 및 리스크 완화

**dividend_growth_compounding.md** - 배당 성장 수학
- 12%+ 배당 CAGR의 장기 복리 효과
- 수익률 vs 성장 트레이드오프
- 과거 사례(MSFT, V, MA, AAPL)
- 배당 성장주의 품질 특성

**fmp_api_guide.md** - API 사용 문서
- API key 설정 및 관리
- 스크리닝용 endpoint 문서
- rate limiting 전략
- 오류 처리 및 트러블슈팅

---

**면책 조항:** 이 스크리닝 도구는 정보 제공 목적입니다. 과거 배당 성장률은 미래 성과를 보장하지 않습니다. 투자 의사결정 전에 충분한 실사를 수행하세요. RSI 과매도 조건은 가격 반등을 보장하지 않으며, 종목은 장기간 과매도 상태를 유지할 수 있습니다.
