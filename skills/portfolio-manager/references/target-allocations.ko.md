# 목표 자산 배분 모델

이 문서는 투자자 위험 성향별 모델 포트폴리오 배분을 제공하며, 포트폴리오 분석과 리밸런싱의 벤치마크로 활용됩니다.

## 개요

목표 배분은 다음 목적의 프레임워크를 제공합니다.
1. 현재 포트폴리오가 투자자 위험 성향과 맞는지 평가
2. 배분 갭과 집중 리스크 식별
3. 리밸런싱 의사결정 가이드
4. 포지션 사이징 가이드라인 설정

**중요:** 이 문서는 템플릿이며 처방이 아닙니다. 실제 배분은 개인 상황, 목표, 투자 기간, 제약 조건에 맞춰 커스터마이즈해야 합니다.

## 투자자 위험 성향 분류

### 위험 성향을 결정하는 요인

| Factor | Conservative | Moderate | Growth | Aggressive |
|--------|-------------|----------|--------|------------|
| **Age** | 60+ | 45-60 | 30-45 | <30 |
| **Time Horizon** | 0-5 years | 5-15 years | 15-25 years | 25+ years |
| **Income Stability** | Fixed income (retired) | Stable salary | Growing career | Variable/high |
| **Net Worth** | Low to moderate | Moderate | High | Very high |
| **Loss Tolerance** | Cannot afford >10% loss | Can handle 15-25% loss | Can handle 25-35% loss | Can handle >40% loss |
| **Investment Goal** | Preserve capital, income | Balanced growth & income | Long-term growth | Maximum growth |
| **Market Experience** | Limited | Moderate | Experienced | Very experienced |

**자가 평가 방법:**
각 요인을 평가해 해당 위험 성향을 부여한 뒤, 다수 분류를 기준으로 종합 성향을 결정합니다.

## Conservative 포트폴리오 (원금 보전)

### 프로필
- **투자자:** 은퇴 임박/은퇴 상태, 낮은 위험 성향, 인컴 및 원금 보전 필요
- **투자 기간:** 0-5년
- **최대 허용 Drawdown:** -10 to -15%
- **기대 연수익률:** 4-6%
- **기대 변동성:** 6-10%

### 자산 배분

```
Total Portfolio Allocation:
├── Equities: 30%
│   ├── US Stocks: 20%
│   ├── International Developed: 7%
│   └── Emerging Markets: 3%
├── Fixed Income: 55%
│   ├── Investment Grade Bonds: 30%
│   ├── Government Bonds: 20%
│   └── High Yield Bonds: 5%
├── Cash & Equivalents: 10%
└── Alternatives (Optional): 5%
    ├── REITs: 3%
    └── Gold: 2%
```

### 주식 배분 (총 포트폴리오의 30%)

**US Stocks (총 20%, 주식 내 67%):**

| Sector | % of Total Portfolio | % of US Equity | Characteristics |
|--------|---------------------|----------------|-----------------|
| **Utilities** | 3.5% | 17.5% | High dividends, stable cash flows |
| **Consumer Staples** | 3.0% | 15.0% | Defensive, recession-resistant |
| **Healthcare** | 3.5% | 17.5% | Defensive with growth potential |
| **Financials** | 2.5% | 12.5% | Dividend income, moderate growth |
| **Technology** | 2.5% | 12.5% | Quality large-caps only (AAPL, MSFT) |
| **Communication Services** | 2.0% | 10.0% | Stable cash flows (T, VZ) |
| **Consumer Discretionary** | 1.5% | 7.5% | Underweight cyclicals |
| **Industrials** | 1.0% | 5.0% | Minimal exposure |
| **Real Estate** | 0.5% | 2.5% | Via separate REIT allocation |
| **Energy** | 0% | 0% | Avoid volatility |
| **Materials** | 0% | 0% | Avoid volatility |

**International & Emerging (총 10%, 주식 내 33%):**
- International Developed: 7% (Europe, Japan, UK - 안정적, 배당 중심)
- Emerging Markets: 3% (최소 노출, 분산 목적)

**포지션 사이징:**
- 단일 최대 포지션: 포트폴리오 총액의 5%
- 일반 포지션: 2-3%
- 포지션 수: 개별주 12-20개 또는 분산 ETF 4-6개

**선호 보유 자산:**
- 대형 배당 성장주(25년+ 배당 증가)
- 경기침체 방어 섹터
- 저베타 종목 (β < 0.8)
- 재무구조가 강한 성숙 기업

**예시 포트폴리오 (ETF 기반):**
- 10% VZ (Verizon) - Telecom, 6% yield
- 10% JNJ (Johnson & Johnson) - Healthcare, dividend aristocrat
- 10% PG (Procter & Gamble) - Consumer staples, stable
- 5% SO (Southern Company) - Utility, high yield
- 5% KO (Coca-Cola) - Consumer staples, dividend
- 5% PFE (Pfizer) - Healthcare, value
- (또는 배당 ETF 대체: VYM, SCHD, DVY)

### 채권 배분 (총 포트폴리오의 55%)

| Bond Type | % of Total Portfolio | Purpose |
|-----------|---------------------|---------|
| **Investment Grade Corporate** | 30% | Income, moderate risk |
| **US Treasury Bonds** | 15% | Safety, low risk |
| **TIPS (Inflation-Protected)** | 5% | Inflation hedge |
| **High Yield (Junk Bonds)** | 5% | Higher income, higher risk |

**Duration:** 금리 리스크를 낮추기 위해 단기~중기(3-7년)

**예시 보유 자산:**
- AGG (Core Bond ETF)
- BND (Total Bond Market)
- LQD (Investment Grade Corporate)
- TIP (TIPS)
- HYG (High Yield - 소규모 비중)

### 현금성 자산 (10%)

**목적:**
- 비상 유동성
- 하락 시 기회 매수
- 포트폴리오 전체 변동성 완화

**보유 수단:**
- 머니마켓 펀드
- 단기 미 국채
- 고금리 예금 계좌

---

## Moderate 포트폴리오 (균형 성장 & 인컴)

### 프로필
- **투자자:** 경력 중반, 균형 목표, 중간 위험 성향
- **투자 기간:** 5-15년
- **최대 허용 Drawdown:** -15 to -25%
- **기대 연수익률:** 6-8%
- **기대 변동성:** 10-14%

### 자산 배분

```
Total Portfolio Allocation:
├── Equities: 60%
│   ├── US Stocks: 42%
│   ├── International Developed: 12%
│   └── Emerging Markets: 6%
├── Fixed Income: 32%
│   ├── Investment Grade Bonds: 20%
│   ├── Government Bonds: 7%
│   └── High Yield Bonds: 5%
├── Cash & Equivalents: 5%
└── Alternatives (Optional): 3%
    ├── REITs: 2%
    └── Commodities/Gold: 1%
```

### 주식 배분 (총 포트폴리오의 60%)

**US Stocks (총 42%, 주식 내 70%):**

| Sector | % of Total Portfolio | % of US Equity | Benchmark (S&P 500) |
|--------|---------------------|----------------|---------------------|
| **Technology** | 11.0% | 26% | 28% |
| **Healthcare** | 7.0% | 17% | 13% |
| **Financials** | 6.0% | 14% | 13% |
| **Consumer Discretionary** | 5.5% | 13% | 11% |
| **Industrials** | 4.0% | 10% | 9% |
| **Consumer Staples** | 3.5% | 8% | 7% |
| **Communication Services** | 2.5% | 6% | 9% |
| **Energy** | 1.0% | 2% | 4% |
| **Utilities** | 1.0% | 2% | 3% |
| **Real Estate** | 0.5% | 1% | 3% |
| **Materials** | 0.5% | 1% | 3% |

**섹터 전략:**
- Technology, Healthcare 소폭 오버웨이트(성장 + 퀄리티)
- Financials와 소비 섹터는 균형 노출
- Energy, Materials는 언더웨이트(변동성 고려)
- 방어 섹터(Utilities, Staples) 비중은 Conservative보다 낮음

**International & Emerging (총 18%, 주식 내 30%):**
- International Developed: 12% (Europe, Japan, UK, Canada)
- Emerging Markets: 6% (China, India, Brazil - 성장 노출)

**포지션 사이징:**
- 단일 최대 포지션: 총 포트폴리오의 8%
- High conviction: 6-8%
- Medium conviction: 4-6%
- Low conviction: 2-3%
- 포지션 수: 개별주 15-25개 또는 ETF 6-10개

**시가총액 분포:**
- Large-cap (>$10B): US equity의 70%
- Mid-cap ($2-10B): 20%
- Small-cap (<$2B): 10%

**예시 포트폴리오 (개별주):**
- 8% MSFT - Technology, quality growth
- 7% AAPL - Technology, ecosystem
- 6% GOOGL - Technology, advertising
- 6% JNJ - Healthcare, defensive
- 5% JPM - Financials, dividend
- 5% UNH - Healthcare, growth
- 4% V - Financials, payments
- 4% HD - Consumer Discretionary, housing
- 4% DIS - Communication, entertainment
- 3% BA - Industrials, aerospace
- (추가 15%는 8-10개 소규모 포지션)
- 18% International (VEA, VWO 또는 개별주)

### 채권 배분 (총 포트폴리오의 32%)

| Bond Type | % of Total Portfolio | Purpose |
|-----------|---------------------|---------|
| **Investment Grade Corporate** | 20% | Core income, moderate risk |
| **US Treasury Bonds** | 5% | Safety ballast |
| **TIPS** | 2% | Inflation hedge |
| **High Yield Bonds** | 5% | Enhanced income |

**Duration:** 중기(5-10년)

---

## Growth 포트폴리오 (장기 자본 성장)

### 프로필
- **투자자:** 젊은 투자자, 긴 투자기간, 성장 중심
- **투자 기간:** 15-25년
- **최대 허용 Drawdown:** -25 to -35%
- **기대 연수익률:** 8-10%
- **기대 변동성:** 14-18%

### 자산 배분

```
Total Portfolio Allocation:
├── Equities: 80%
│   ├── US Stocks: 52%
│   ├── International Developed: 18%
│   └── Emerging Markets: 10%
├── Fixed Income: 15%
│   ├── Investment Grade Bonds: 8%
│   └── High Yield Bonds: 7%
├── Cash & Equivalents: 3%
└── Alternatives: 2%
    └── REITs or Commodities: 2%
```

### 주식 배분 (총 포트폴리오의 80%)

**US Stocks (총 52%, 주식 내 65%):**

| Sector | % of Total Portfolio | % of US Equity | Notes |
|--------|---------------------|----------------|-------|
| **Technology** | 16.0% | 31% | Growth focus, secular trends |
| **Healthcare** | 8.0% | 15% | Innovation, demographics |
| **Consumer Discretionary** | 7.5% | 14% | Economic growth exposure |
| **Communication Services** | 6.0% | 12% | Digital transformation |
| **Financials** | 5.5% | 11% | Economic expansion |
| **Industrials** | 5.0% | 10% | Capital spending cycles |
| **Consumer Staples** | 2.0% | 4% | Underweight defensive |
| **Energy** | 1.0% | 2% | Minimal exposure |
| **Materials** | 0.5% | 1% | Minimal exposure |
| **Utilities** | 0.5% | 1% | Minimal exposure |
| **Real Estate** | 0% | 0% | Separate REIT allocation |

**섹터 전략:**
- Technology 대폭 오버웨이트(혁신, 구조적 성장)
- Healthcare 오버웨이트(인구구조, 혁신)
- 성장/경기민감 섹터 비중 확대
- 방어 섹터는 최소화(안정성 수요 낮음)

**International & Emerging (총 28%, 주식 내 35%):**
- International Developed: 18% (우량 해외 성장)
- Emerging Markets: 10% (더 높은 성장 잠재력)

**포지션 사이징:**
- 단일 최대 포지션: 총 포트폴리오의 10%
- High conviction: 8-10%
- Medium conviction: 5-7%
- Low conviction: 2-4%
- 포지션 수: 개별주 15-30개

**시가총액 분포:**
- Large-cap: US equity의 60%
- Mid-cap: 25%
- Small-cap: 15% (성장 잠재력)

**Growth vs Value 기울기:** 균형~소폭 Growth tilt(극단적 아님)

**예시 포트폴리오:**
- 10% NVDA - Technology, AI leadership
- 9% MSFT - Technology, cloud + AI
- 8% AAPL - Technology, ecosystem
- 7% GOOGL - Technology, AI + advertising
- 6% AMZN - Consumer Discretionary, AWS
- 6% META - Communication, digital advertising
- 5% TSLA - Consumer Discretionary, EV + energy
- 5% UNH - Healthcare, managed care
- 4% V - Financials, payments
- 4% MA - Financials, payments
- (나머지 36%는 15-20개 소규모 포지션 + 해외 노출)

### 채권 배분 (총 포트폴리오의 15%)

| Bond Type | % of Total Portfolio | Purpose |
|-----------|---------------------|---------|
| **Investment Grade Corporate** | 8% | Moderate income, volatility dampening |
| **High Yield Bonds** | 7% | Enhanced returns, equity-like exposure |

**Duration:** 중기~장기(7-15년) - 금리 리스크 감내 가능

---

## Aggressive 포트폴리오 (최대 성장)

### 프로필
- **투자자:** 젊고 고소득, 매우 높은 위험 성향, 장기 투자기간
- **투자 기간:** 20년+
- **최대 허용 Drawdown:** -35 to -50%
- **기대 연수익률:** 9-12%
- **기대 변동성:** 18-22%

### 자산 배분

```
Total Portfolio Allocation:
├── Equities: 95%
│   ├── US Stocks: 57%
│   ├── International Developed: 23%
│   └── Emerging Markets: 15%
├── Fixed Income: 0-5%
└── Cash & Equivalents: 0-5%
```

### 주식 배분 (총 포트폴리오의 95%)

**US Stocks (총 57%, 주식 내 60%):**

| Sector | % of Total Portfolio | % of US Equity | Strategy |
|--------|---------------------|----------------|----------|
| **Technology** | 20.0% | 35% | Maximum exposure to innovation |
| **Healthcare** | 9.0% | 16% | Biotech, medical devices, innovation |
| **Consumer Discretionary** | 9.0% | 16% | E-commerce, luxury, travel |
| **Communication Services** | 6.0% | 11% | Digital platforms, streaming |
| **Financials** | 6.0% | 11% | Fintechs, growth-oriented |
| **Industrials** | 4.0% | 7% | Aerospace, automation |
| **Consumer Staples** | 1.0% | 2% | Minimal |
| **Energy** | 1.0% | 2% | Renewables focus |
| **Materials** | 0.5% | 1% | Minimal |
| **Utilities** | 0.5% | 1% | Minimal |

**섹터 전략:**
- Technology 극단적 오버웨이트(벤치마크 28% 대비 35%)
- 성장 섹터가 포트폴리오의 80%+
- 방어 섹터 최소 노출
- 높은 변동성을 수용

**International & Emerging (총 38%, 주식 내 40%):**
- International Developed: 23% (유럽 tech, 아시아 성장)
- Emerging Markets: 15% (중국 tech, 인도 성장, 중남미)

**포지션 사이징:**
- 단일 최대 포지션: 총 포트폴리오의 12%
- High conviction: 10-12%
- Medium conviction: 6-9%
- Low conviction: 3-5%
- 포지션 수: 개별주 12-25개(집중형)

**시가총액 분포:**
- Large-cap: 55%
- Mid-cap: 30%
- Small-cap: 15% (고성장/고위험)

**Growth vs Value:** 강한 Growth tilt

**스타일 특성:**
- 높은 P/E 허용(성장 프리미엄)
- 일부 포지션은 수익성보다 매출 성장 중시
- 구조적 테마: AI, cloud, EVs, fintech, biotech
- 투기적 포지션(총 5-10%) 포함 가능

**예시 포트폴리오:**
- 12% NVDA - Technology, AI chips
- 10% TSLA - Consumer Discretionary, EVs + autonomy
- 9% MSFT - Technology, cloud + AI
- 8% GOOGL - Technology, AI + advertising
- 8% META - Communication, VR/AI
- 7% AMZN - Consumer Discretionary, AWS
- 6% AAPL - Technology, ecosystem
- 5% SHOP - Technology, e-commerce platform
- 5% SQ - Fintech, payments
- 4% CRSP - Healthcare, gene editing
- 4% ENPH - Energy, solar
- (나머지 22%는 소규모 성장 포지션 + 해외 노출)

### 채권 배분 (총 포트폴리오의 0-5%)

**최소 또는 미보유:**
- 유동성 목적의 0-5% investment grade 또는 현금
- 긴 투자기간을 전제로 변동성 완화 자산 필요성이 낮음
- 이 프로필은 100% 주식도 허용 가능

---

## 특수 목적 배분 고려사항

### Dividend Income 포트폴리오

**목표:** 원금 보전을 유지하면서 현재 인컴 극대화

**배분:**
- Equities: 60% (배당 중심)
  - High-yield stocks (4-7% yields): 40%
  - Dividend growth stocks: 20%
- Fixed Income: 30% (인컴 중심)
  - Investment grade corporate: 15%
  - High yield bonds: 10%
  - Preferred stocks: 5%
- REITs: 10% (고배당, 인플레이션 헤지)

**목표 Yield:** 총 포트폴리오 기준 4-6%

### Tax-Efficient 포트폴리오 (과세계좌)

**고려사항:**
- 회전율 최소화(양도차익 과세 축소)
- 적격배당/장기자본이득 선호
- Tax-loss harvesting 기회 활용
- 고세율 구간이라면 지방채(Municipal bonds) 고려

**배분 조정:**
- Growth stocks(저배당/무배당): 비중 확대
- Municipal bonds: 회사채 일부 대체
- Index funds: 액티브 대비 비중 확대
- International: 해외 세금 복잡성을 고려해 비중 축소 가능

### Retirement 포트폴리오 (은퇴 이후)

**목표:** 인컴 창출, 원금 보전, 장수 리스크 관리

**배분(연령별):**
- Age 65: 40/60 stocks/bonds
- Age 75: 30/70 stocks/bonds
- Age 85: 20/80 stocks/bonds

**인컴 전략:**
- 4% 인출률(지속 가능성 기준)
- 버킷 전략:
  - Bucket 1 (0-2 years expenses): Cash
  - Bucket 2 (3-7 years): Bonds
  - Bucket 3 (8+ years): Stocks

---

## 위험 성향별 포지션 사이징 가이드

| Risk Profile | Max Single Position | Typical Position | Min # of Stocks | Max # of Stocks |
|--------------|--------------------|--------------------|----------------|----------------|
| **Conservative** | 5% | 2-3% | 12 | 20 |
| **Moderate** | 8% | 4-6% | 15 | 25 |
| **Growth** | 10% | 5-7% | 15 | 30 |
| **Aggressive** | 12% | 6-9% | 12 | 25 |

**단일 섹터 최대치:**

| Risk Profile | Max Single Sector |
|--------------|------------------|
| **Conservative** | 25% |
| **Moderate** | 30% |
| **Growth** | 35% |
| **Aggressive** | 40% |

---

## 위험 성향별 리밸런싱 트리거

| Risk Profile | Rebalancing Frequency | Asset Class Drift Trigger | Position Drift Trigger |
|--------------|----------------------|--------------------------|------------------------|
| **Conservative** | Quarterly | >3% | >2% |
| **Moderate** | Quarterly | >5% | >3% |
| **Growth** | Semi-Annually | >7% | >4% |
| **Aggressive** | Annually | >10% | >5% |

---

## 생애주기 배분 (연령 기반)

**전통적 경험칙:** 주식 비중 = "120 - 나이"

| Age | Stock % | Bond % | Formula |
|-----|---------|--------|---------|
| 25 | 95% | 5% | 120 - 25 |
| 35 | 85% | 15% | 120 - 35 |
| 45 | 75% | 25% | 120 - 45 |
| 55 | 65% | 35% | 120 - 55 |
| 65 | 55% | 45% | 120 - 65 |
| 75 | 45% | 55% | 120 - 75 |

**현대적 조정:** "130 - 나이" (수명 증가, 저금리 환경 반영)

---

## 포트폴리오 분석에서 목표 배분 활용

### 1. 현재 배분 식별
실제 포트폴리오 비중을 다음 기준으로 계산합니다.
- 자산군(stocks/bonds/cash)
- 섹터(주식 내)
- 지역(geographic)
- 시가총액 구간

### 2. 목표 모델과 비교
다음 기준으로 적절한 모델을 선택합니다.
- 투자자 위험 성향 평가 결과
- 투자 기간
- 재무 상황
- 목표

### 3. 이탈도 계산
```
Deviation = Current % - Target %

Example:
Target (Moderate): 60% stocks
Current: 68% stocks
Deviation: +8% (overweight stocks)
```

### 4. 리밸런싱 계획 수립
- 오버웨이트 포지션/섹터 축소
- 언더웨이트 포지션/섹터 확대
- 이탈 폭이 큰 항목부터 우선 처리

### 5. 개인 상황 반영
템플릿은 출발점이며 고정 규칙이 아닙니다.
- 세금 환경에 따라 특정 보유 자산 선호 가능
- 전문성이 있는 섹터는 오버웨이트가 정당화될 수 있음
- 회사 주식 보유는 집중 리스크를 만들 수 있음
- 부동산(자가 포함) 보유가 전체 배분에 영향

---

## 요약

**핵심 포인트:**

1. **목표 배분은 가이드라인**이며 강제 규칙이 아닙니다. 개인 상황에 맞춰 조정해야 합니다.
2. **위험 성향이 배분을 결정**합니다. 주식/채권 비중은 위험 성향과 투자 기간에 맞아야 합니다.
3. **섹터 배분이 중요**합니다. 주식 내 섹터 믹스가 위험과 수익에 큰 영향을 줍니다.
4. **포지션 사이징 규율**이 필요합니다. 최대 비중 규칙으로 집중 리스크를 통제해야 합니다.
5. **체계적 리밸런싱**을 수행해야 합니다. 무의식적 drift를 방치하지 말아야 합니다.
6. **생애주기를 반영**해야 합니다. 나이와 상황 변화에 따라 배분을 조정해야 합니다.

**기억할 점:** 시장 하락 30% 구간에서 공포 매도할 배분이라면 그 배분은 본인에게 맞지 않습니다. 이상적인 위험 성향이 아니라 실제 위험 성향에 맞는 배분을 선택해야 장기적으로 유지할 수 있습니다.
