# Value Dividend Stock Screening Methodology

## 개요

이 스크리닝 방법론은 다음을 결합한 고품질 배당주를 식별합니다:
- **Value characteristics**: 합리적인 밸류에이션(낮은 P/E, P/B)
- **Income generation**: 매력적인 배당수익률(>=3.5%)
- **Growth profile**: 일관된 배당, 매출, EPS 성장
- **Quality metrics**: 강한 수익성, 재무 건전성, 배당 지속가능성

## 스크리닝 기준

### Phase 1: Initial Quantitative Filters

#### 1. Dividend Yield >= 3.5%
**근거**: 일반적인 시장 수익률(S&P 500 평균: 약 1.5-2%) 대비 의미 있는 인컴 제공

**계산식**:
```
Dividend Yield = (Annual Dividends per Share / Current Stock Price) × 100
```

**임계값 논리**:
- 3.5%+는 매력적인 인컴 제공
- 과도하게 높아 배당 리스크를 시사할 수준은 아님(>8%는 대개 지속 불가능)
- 인컴과 성장 잠재력의 균형

#### 2. P/E Ratio <= 20
**근거**: 이익 대비 합리적인 multiple에 거래되는 종목 식별

**계산식**:
```
P/E Ratio = Market Price per Share / Earnings per Share (TTM)
```

**임계값 논리**:
- S&P 500 역사적 평균: 약 15-18배
- P/E <= 20은 value 영역을 시사
- 고평가 성장주 제외
- 성숙하고 수익성 있는 기업에 초점

#### 3. P/B Ratio <= 2.0
**근거**: 장부가치 대비 주가가 합리적인 수준인지 확인

**계산식**:
```
P/B Ratio = Market Price per Share / Book Value per Share
```

**임계값 논리**:
- P/B <= 2.0은 합리적인 밸류에이션을 시사
- 순자산 대비 과도한 premium 지불을 회피
- 자산 집약형 비즈니스에서 특히 중요

### Phase 2: Growth Quality Filters

#### 4. Dividend Growth: 3-Year CAGR >= 5%
**근거**: 배당 인상 track record가 일관된 기업 식별

**계산식**:
```
Dividend CAGR = [(End Dividend / Start Dividend)^(1/3) - 1] × 100
```

**임계값 논리**:
- 연 5% 성장은 시간이 지날수록 의미 있게 복리 누적
- cash flow에 대한 경영진의 자신감 반영
- 인플레이션 방어(장기 평균: 2-3%)
- 비즈니스 건전성과 주주환원 의지 신호

**일관성 체크**:
- 기간 중 배당 삭감 없음
- 배당 동결 1년은 허용(경기 사이클)
- 배당 삭감은 재무 스트레스 또는 전략 변화 신호

#### 5. Revenue Growth: Positive 3-Year Trend
**근거**: 상단 매출 성장으로 배당 지속가능성 뒷받침 여부 확인

**평가 방식**:
- 3년차 Revenue > 1년차 Revenue
- 1년 감소는 허용(경기 민감 업종, 일회성 이벤트)
- 전반적 우상향 추세 필수

**고정 %를 쓰지 않는 이유**:
- 산업별 성장률 차이
- 성숙한 배당주는 완만하지만 안정적인 성장을 보일 수 있음
- 절대 성장률보다 **추세 방향**에 초점

#### 6. EPS Growth: Positive 3-Year Trend
**근거**: 이익 창출력이 훼손되지 않고 확장되는지 확인

**평가 방식**:
- 3년차 EPS > 1년차 EPS
- 1년 감소 허용
- 전반적 우상향 추세 필수

**의미**:
- 배당의 재원은 이익
- EPS 성장 = 향후 배당 인상 여력
- quality company와 dividend trap 구분

### Phase 3: Quality & Sustainability Analysis

#### 7. Dividend Sustainability Metrics

**A. Payout Ratio**
```
Payout Ratio = (Dividends Paid / Net Income) × 100
```

**건전 구간**: 30-70%
- < 30%: 보수적, 성장 여력 큼
- 30-70%: 균형적, 지속 가능
- > 80%: 주의, 유연성 제한

**B. Free Cash Flow Payout Ratio**
```
FCF Payout Ratio = (Dividends Paid / Free Cash Flow) × 100
where FCF = Operating Cash Flow - Capital Expenditures
```

**건전 구간**: < 100%
- FCF는 지속 가능한 배당의 실제 원천
- < 100%: 실제 cash generation으로 배당 커버
- > 100%: 지속 불가능, 부채 또는 자산 매각으로 충당

**Sustainability Flag**: ✅ if Payout Ratio < 80% AND FCF Payout Ratio < 100%

#### 8. Financial Health Metrics

**A. Debt-to-Equity Ratio**
```
D/E Ratio = Total Debt / Shareholders' Equity
```

**건전 구간**: < 2.0
- 일반적으로 낮을수록 좋음
- 업종별 차이 존재(utilities는 일반적으로 더 높음)
- < 2.0: 합리적 레버리지, 과도한 부채 아님

**B. Current Ratio**
```
Current Ratio = Current Assets / Current Liabilities
```

**건전 구간**: > 1.0 (이상적으로 > 1.5)
- > 1.0: 단기 채무 상환 가능
- > 1.5: 유동성 완충력 우수
- < 1.0: 유동성 리스크

**Health Flag**: ✅ if D/E < 2.0 AND Current Ratio > 1.0

#### 9. Quality Score (0-100)

**구성 요소**:

**A. Return on Equity (ROE)** - Max 50 points
```
ROE = Net Income / Shareholders' Equity

Points = min((ROE% / 20%) × 50, 50)
```

- ROE 20%+ = 50점(우수한 자본 효율)
- ROE 10% = 25점(평균)
- ROE < 5% = 낮은 자본 수익성

**B. Net Profit Margin** - Max 50 points
```
Profit Margin = (Net Income / Revenue) × 100

Points = min((Margin% / 15%) × 50, 50)
```

- 마진 15%+ = 50점(높은 수익성)
- 마진 7.5% = 25점(평균)
- 마진 < 3% = 낮은 수익성

**Quality Score 해석**:
- 80-100: Excellent quality (높은 수익성, 효율성)
- 60-79: Good quality
- 40-59: Average quality
- < 40: Below average quality

## Composite Scoring System

### 목적

가치, 성장, 품질의 균형을 반영해 종목의 전체 매력도를 순위화합니다.

### 점수 구성 (총 100점)

1. **Dividend Growth** (Max 20 points)
   - 10%+ CAGR = 20점
   - 5% CAGR = 10점
   - 선형 스케일링

2. **Revenue Growth** (Max 15 points)
   - 10%+ CAGR = 15점
   - 5% CAGR = 7.5점
   - 선형 스케일링

3. **EPS Growth** (Max 15 points)
   - 15%+ CAGR = 15점
   - 7.5% CAGR = 7.5점
   - 선형 스케일링

4. **Dividend Sustainability** (10 points)
   - Pass (sustainable) = 10점
   - Fail = 0점

5. **Financial Health** (10 points)
   - Pass (healthy) = 10점
   - Fail = 0점

6. **Quality Score** (Max 30 points)
   - Quality Score × 0.3
   - quality 100 = 30점
   - quality 50 = 15점

### 해석

- **80-100**: Exceptional (높은 성장, 품질, 지속가능성)
- **60-79**: Strong (전반적으로 견고한 프로필)
- **40-59**: Good (기준 충족, 일부 trade-off 존재)
- **20-39**: Acceptable (필터 통과했지만 품질 낮음)
- **< 20**: Marginal (기준을 간신히 충족)

## 투자 철학

### 이 접근이 효과적인 이유

1. **Value + Growth + Quality**: 검증된 3개 factor premium 결합
2. **Dividend Focus**: 경영 규율과 cash generation 능력 신호
3. **Sustainability Screen**: dividend trap, value trap 회피
4. **Growth Requirements**: 하향 기업이 아닌 건전 기업 선별
5. **Quality Filters**: 지속 가능한 경쟁우위 식별

### 이 전략이 회피하는 것

1. **Dividend Traps**: 부진 기업의 고배당(성장 필터가 포착)
2. **Value Traps**: 싸지만 계속 싼 종목(품질 지표가 포착)
3. **Overvaluation**: 비싼 multiple의 성장주(P/E, P/B 필터)
4. **Financial Risk**: 과도한 레버리지 또는 유동성 취약 기업(건전성 지표)

### 이상적인 후보 프로필

이 스크린에서 높은 점수를 받는 종목은 일반적으로:
- 안정적이고 성숙한 산업에서 영업
- 지속 가능한 경쟁우위(moat) 보유
- 일관된 free cash flow 창출
- 주주환원(배당)에 대한 확고한 의지
- 합리적 밸류에이션에서 거래(과열 아님)
- 완만하지만 일관된 성장
- 강한 재무상태와 수익성

예시: Dividend Aristocrats, quality REITs(포함 시), 안정적 utilities, consumer staples 리더

## 사용 시 유의사항

### 한계

1. **Market Cap Bias**: 대체로 대형/중형주를 더 많이 찾음(소형주는 전 기준 충족 가능성 낮음)
2. **Sector Bias**: 특정 섹터 비중이 높아질 수 있음(utilities, consumer staples, REITs)
3. **Excludes High Growth**: 테크/고성장주는 일반적으로 제외됨(의도된 설계)
4. **Historical Performance**: 과거 성장이 미래 성과를 보장하지 않음
5. **Economic Sensitivity**: 조건 충족 종목 일부는 경기 민감 가능

### Best Practices

1. **Diversification**: 상위 5개에 집중하지 말고 상위 20개에 분산
2. **Sector Balance**: 섹터 노출 모니터링, 과집중 회피
3. **Rescreen Regularly**: 분기 또는 반기 재스크리닝(펀더멘털 변화)
4. **Valuation Check**: 통과했다고 무조건 매수하지 말 것
5. **Dividend Safety**: payout ratios와 cash flow를 분기마다 점검
6. **Hold for Long Term**: 트레이딩이 아닌 quality dividend growth 전략

### 매도 시점

1. **Dividend Cut**: 즉각적인 red flag, 사업 건전성 재검토
2. **Deteriorating Fundamentals**: 매출/EPS가 여러 분기 하락
3. **Payout Ratio > 100%**: 배당 지속 불가능
4. **Debt Spike**: 명확한 사유 없이 레버리지 급증
5. **Better Opportunities**: 더 높은 점수 종목으로 자본 재배치
6. **Valuation Extreme**: 종목이 과도하게 고평가됨(예: P/E > 30)

## Historical Context

### 왜 3.5% Yield 임계값인가?

- **US 10-Year Treasury**: 역사적으로 2-4%
- **S&P 500 Dividend Yield**: 1.5-2%
- **Equity Risk Premium**: 3.5%는 국채 대비 약 1.5-2% 프리미엄 제공
- **Tax Efficiency**: qualified dividends는 채권 대비 세제상 유리

### 왜 P/E <= 20인가?

- **S&P 500 Historical Average**: 약 15-18배
- **Fair Value Range**: 성숙하고 안정적인 기업의 15-20배
- **Margin of Safety**: multiple compression 여지 확보
- **Cyclically Adjusted**: peak earnings에서 과지불 방지

### 왜 5% Dividend CAGR인가?

- **Inflation Protection**: 장기 인플레이션(2-3%) 상회
- **Real Income Growth**: 구매력 증가를 동반한 인컴 성장
- **Achievable**: quality company에 현실적인 지속 가능 수준
- **Compound Power**: 5%는 14.4년 내 2배

## 참고 자료

- Benjamin Graham: "The Intelligent Investor" (value investing principles)
- Jeremy Siegel: "The Future for Investors" (dividend growth research)
- CFA Institute: Equity Valuation standards
- S&P Dow Jones Indices: Dividend Aristocrats methodology
- Morningstar: Dividend Sustainability Research
