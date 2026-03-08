# Diversification Principles

이 문서는 포트폴리오 분산투자의 이론과 실무를 설명하며, 분산 품질 평가와 집중 리스크 식별을 위한 프레임워크를 제공합니다.

## Core Concepts

### Diversification이란?

Diversification은 여러 자산/섹터/지역에 투자를 분산해 기대수익을 비례적으로 훼손하지 않으면서 포트폴리오 리스크를 줄이는 방법입니다.

**Harry Markowitz's Key Insight (1952):**
> "Diversification is the only free lunch in finance."

상관관계가 완전하지 않은 자산을 결합하면, 단일 자산 보유보다 더 나은 위험조정수익을 얻을 수 있습니다.

### 분산의 수학

**Portfolio Risk Formula:**

2개 자산 포트폴리오:
```
σ_p = √(w₁²σ₁² + w₂²σ₂² + 2w₁w₂σ₁σ₂ρ₁₂)

Where:
σ_p = Portfolio standard deviation (risk)
w₁, w₂ = Weights of assets 1 and 2
σ₁, σ₂ = Standard deviations of assets 1 and 2
ρ₁₂ = Correlation between assets 1 and 2
```

**Key Insight:** 상관계수 < 1.0이면 포트폴리오 리스크는 개별 리스크 가중평균보다 작아집니다.

### 리스크 유형

**1. Systematic Risk (Market Risk)**
- **Definition:** 시장 전체에 내재한 리스크
- **Examples:** 경기침체, 금리 변화, 지정학 이벤트
- 분산으로 **제거 불가**
- **Beta**가 체계적 리스크 노출을 측정

**2. Unsystematic Risk (Specific Risk)**
- **Definition:** 개별 기업/섹터 고유 리스크
- **Examples:** 경영 실패, 리콜, 경쟁 열위
- 분산으로 **감소 가능**
- **분산 효과:** 15-30개 종목으로 비체계적 리스크의 약 90% 제거

**Modern Portfolio Theory Goal:** 비체계적 리스크를 제거하고 체계적 리스크(시장 리스크 프리미엄 보상)는 수용.

## Optimal Number of Holdings

### Individual Stocks

보유 종목 수가 늘어날수록 분산 효익은 체감합니다.

| Number of Stocks | % of Unsystematic Risk Eliminated |
|------------------|----------------------------------|
| 1 | 0% (all risk remains) |
| 5 | ~40% |
| 10 | ~65% |
| 15 | ~75% |
| 20 | ~85% |
| 30 | ~90% |
| 50 | ~93% |
| 100 | ~95% |

**Recommended Range: 15-30 stocks**

**왜 30개를 넘기지 않는가?**
- 한계 분산 효익이 매우 작음
- 모니터링 복잡도 증가
- 거래비용 증가
- 고확신 아이디어 희석
- 사실상 closet indexing

**왜 15개 미만은 피하는가?**
- 비체계적 리스크 제거 불충분
- 집중 리스크가 큼
- 단일 종목 이벤트의 충격이 큼
- 상관관계 과소평가 위험

### ETFs and Mutual Funds

**분산형 펀드(광범위 시장/섹터/해외)의 경우:**
- **5-10 ETFs**로도 우수한 분산 가능
- ETF 자체가 수십~수천 종목을 포함
- 중복 노출 최소화와 상호보완 노출이 핵심

**예시: 균형 잡힌 6-ETF 포트폴리오**
1. US Large Cap (S&P 500)
2. US Small/Mid Cap
3. International Developed Markets
4. Emerging Markets
5. US Bonds (Aggregate)
6. Real Estate (REITs)

## Correlation and Diversification

### Correlation 이해

**Correlation coefficient (ρ) 범위: -1.0 ~ +1.0**

| Correlation | Interpretation | Diversification Benefit |
|-------------|----------------|------------------------|
| **+1.0** | Perfect positive correlation | None (redundant holdings) |
| **+0.7 to +0.9** | Very high correlation | Minimal |
| **+0.3 to +0.7** | Moderate positive correlation | Good |
| **0 to +0.3** | Low positive correlation | Excellent |
| **0** | No correlation | Maximum benefit |
| **-0.3 to 0** | Low negative correlation | Excellent (hedging) |
| **< -0.3** | Moderate to strong negative correlation | Hedging properties |

### Typical Stock Correlations

**동일 섹터 내:**
- 대형 Tech (AAPL, MSFT, GOOGL): ρ ≈ 0.6-0.8
- Banks (JPM, BAC, WFC): ρ ≈ 0.7-0.9
- Oil companies (XOM, CVX): ρ ≈ 0.8-0.9

**서로 다른 섹터 간:**
- Tech vs Healthcare: ρ ≈ 0.3-0.5
- Utilities vs Technology: ρ ≈ 0.2-0.4
- Consumer Staples vs Energy: ρ ≈ 0.3-0.5

**Defensive vs Cyclical:**
- Utilities vs Industrials: ρ ≈ 0.2-0.4
- Consumer Staples vs Consumer Discretionary: ρ ≈ 0.4-0.6

**US vs International:**
- US vs International Developed: ρ ≈ 0.7-0.9 (시간이 갈수록 상승)
- US vs Emerging Markets: ρ ≈ 0.6-0.8

**Stocks vs Bonds:**
- US Stocks vs US Treasuries: ρ ≈ -0.2 ~ +0.3 (레짐 의존)
- Stocks vs Corporate Bonds: ρ ≈ 0.4-0.6

### Correlation Pitfalls

**1. 상관관계 불안정성**
- 위기 때 상관관계가 급상승(“crisis에서는 1에 수렴”)
- 가장 필요한 시점에 분산 효과 약화
- 해결: 금/변동성 전략 등 진짜 비상관 자산 포함

**2. Hidden Correlations**
- 겉보기 업종이 달라도 공통 리스크 팩터를 공유
- 예: 은행주 + 주택건설주 = 금리 민감 노출
- 해결: 섹터 라벨이 아닌 underlying risk factor 분석

**3. Globalization Effect**
- 과거 대비 해외 분산 효과 감소
- 미국과 글로벌 시장 상관 상승
- 해결: 여전히 유효하나 과거보다 기대효과를 낮춰 가정

## Concentration Risk Measurement

### Position Concentration

**Single Position Thresholds:**

| Position Size | Risk Level | Action |
|---------------|------------|--------|
| **<5%** | Low | Acceptable for all positions |
| **5-10%** | Medium | Monitor, ensure high conviction |
| **10-15%** | High | Trim recommended unless exceptional conviction |
| **15-20%** | Very High | Trim immediately (except rare cases) |
| **>20%** | Extreme | Urgent trim required |

**Top Holdings Concentration:**

| Top 5 Holdings | Risk Assessment |
|----------------|-----------------|
| **<25%** | Well-diversified |
| **25-40%** | Moderate concentration |
| **40-60%** | High concentration |
| **>60%** | Excessive concentration |

**Example:**
- Top 5 = 55% → 높은 집중 리스크
- Largest position = 18% → 즉시 Trim 권고

### Sector Concentration

**Sector Allocation Thresholds:**

| Sector Weight | Risk Level | Guidance |
|---------------|------------|----------|
| **<15%** | Underweight | May be intentional or opportunity |
| **15-25%** | Normal | Typical for major sectors |
| **25-30%** | Moderate overweight | Monitor, ensure intentional |
| **30-40%** | High overweight | Trim recommended |
| **>40%** | Excessive concentration | Urgent diversification needed |

**S&P 500 Sector Benchmarks (approximate):**
- Technology: 25-30%
- Healthcare: 12-15%
- Financials: 10-13%
- Consumer Discretionary: 10-12%
- Communication Services: 8-10%
- Industrials: 8-10%
- Consumer Staples: 6-8%
- Energy: 3-5%
- Utilities: 2-3%
- Real Estate: 2-3%
- Materials: 2-3%

**Deviation Analysis:**
- **벤치마크 대비 +10%p 이상** = 유의미한 과대비중
- **벤치마크 대비 +20%p 이상** = 과도한 과대비중(Trim 권고)

### Herfindahl-Hirschman Index (HHI)

**Formula:**
```
HHI = Σ(w_i × 100)²

Where w_i = weight of position i (as decimal)
```

**Interpretation:**

| HHI Score | Concentration Level | Portfolio Characteristics |
|-----------|---------------------|--------------------------|
| **<1000** | Low concentration | Well-diversified (25+ equal positions) |
| **1000-1800** | Moderate concentration | Typical diversified portfolio (15-25 stocks) |
| **1800-2500** | High concentration | Concentrated portfolio (8-15 stocks) |
| **>2500** | Very high concentration | Very concentrated (5-8 stocks) |
| **>4000** | Extreme concentration | Poorly diversified (<5 stocks) |

**Example Calculation:**

포트폴리오 5개 포지션:
- Position A: 30% → (30)² = 900
- Position B: 25% → (25)² = 625
- Position C: 20% → (20)² = 400
- Position D: 15% → (15)² = 225
- Position E: 10% → (10)² = 100

HHI = 900 + 625 + 400 + 225 + 100 = **2250** (High concentration)

## Multi-Dimensional Diversification

효과적인 분산은 여러 차원에서 동시에 이뤄져야 합니다.

### 1. Number of Holdings (Quantity)
- **Target:** 15-30개 개별 종목 또는 5-10개 분산형 펀드
- **Measure:** 포지션 수
- **Risk:** 너무 적으면 집중, 너무 많으면 과다 분산

### 2. Position Sizing (Weight)
- **Target:** 단일 포지션 >10-15% 금지, Top 5 <40%
- **Measure:** HHI, top-N 집중도
- **Risk:** 종목 수가 많아도 비중 불균형이면 집중 발생

### 3. Sector Allocation (Industry)
- **Target:** 단일 섹터 >30-35% 금지, 6개+ 섹터 분산
- **Measure:** 섹터 분해, 벤치마크 비교
- **Risk:** 산업 특화 충격 (예: 2000 tech, 2008 금융위기)

### 4. Market Cap (Size)
- **Target:** Large 60-70%, Mid 20-25%, Small 10-15%
- **Measure:** 가중 평균 시총, cap별 분해
- **Risk:** Small cap 고변동, 회복기에는 large cap이 뒤처질 수 있음

### 5. Geography (Region)
- **Target:** US 60-75%, International Developed 15-25%, EM 5-15%
- **Measure:** 매출 지역, 상장 지역
- **Risk:** 국가별 정치/통화/규제 리스크

### 6. Style (Growth vs Value)
- **Target:** 균형 또는 시장 사이클에 따른 경미한 기울기
- **Measure:** 평균 P/E, P/B, 성장률
- **Risk:** 스타일 로테이션 리스크

### 7. Correlation (Independence)
- **Target:** 평균 pairwise correlation <0.6
- **Measure:** 상관행렬
- **Risk:** 고상관 = 가짜 분산

### 8. Factor Exposures (Risk Factors)
- **Target:** momentum/quality/volatility 등 팩터 균형
- **Measure:** factor loadings (고급 분석 필요)
- **Risk:** 단일 팩터 집중

## Practical Diversification Strategies

### Strategy 1: Equal Weighting

**Method:** 각 포지션 동일 비중 (예: 20종목이면 각 5%)

**Pros:**
- 단순하고 구현 용이
- 작은 포지션으로 자동 리밸런싱 유도
- 집중 리스크 완화

**Cons:**
- 확신도 반영 어려움
- 저품질 종목 과대배분 가능
- 회전율 증가

**Best for:** 수동적 투자자, 인덱스 유사 접근

### Strategy 2: Conviction Weighting

**Method:** 확신도 높은 아이디어에 더 큰 비중 배분

**Example Tiers:**
- High conviction: 7-10% (5-8개)
- Medium conviction: 4-6% (8-12개)
- Low conviction / Satellite: 2-3% (5-10개)

**Pros:**
- 분석 우위 반영
- 실력이 있으면 위험조정수익 개선 가능
- 분산 유지 가능

**Cons:**
- 확신도 평가의 정직성이 필요
- 과신 리스크
- 집중도로 기울 가능성

**Best for:** 리서치 역량 있는 액티브 투자자

### Strategy 3: Risk Parity

**Method:** 달러 비중이 아니라 리스크 기여도로 배분

**Example:**
- Volatile stock (beta 1.8): 3%
- Moderate stock (beta 1.0): 5%
- Stable stock (beta 0.6): 8%

**Pros:**
- 리스크 관점의 진짜 분산
- 포트폴리오 안정성 향상
- 체계적 리스크 관리

**Cons:**
- 구현 복잡
- 변동성 추정 필요
- 저변동 저품질 자산 과대비중 우려

**Best for:** 정교한 리스크 중심 투자자

### Strategy 4: Core-Satellite

**Method:**
- **Core (60-80%)**: 분산된 저비용 인덱스
- **Satellite (20-40%)**: 고확신 개별 종목/섹터 베팅

**Pros:**
- 패시브 분산 + 액티브 업사이드 결합
- 종목선정 실수 리스크 축소
- 비용 효율

**Cons:**
- 위성 포트폴리오 품질에 성과 의존
- 관리 복잡도
- 계좌별 세금 효율 차이

**Best for:** 분산과 액티브를 함께 원하는 투자자

## Diversification Quality Checklist

포트폴리오 분산 점검 체크리스트:

**Position Diversification:**
- [ ] 포트폴리오가 15-30개 종목(또는 5-10개 분산형 펀드)으로 구성
- [ ] 단일 포지션이 10%를 넘지 않음
- [ ] 단일 포지션이 15%를 넘지 않음
- [ ] Top 5 비중이 40% 미만
- [ ] HHI < 1800

**Sector Diversification:**
- [ ] 단일 섹터 비중이 주식의 30% 초과하지 않음
- [ ] 최소 6개 이상의 섹터 포함
- [ ] 벤치마크 대비 섹터 편차가 합리적(±15% 이내)
- [ ] 성장/방어/경기민감 섹터 균형
- [ ] 단일 하위 산업 과집중 없음

**Correlation Diversification:**
- [ ] 서로 다른 드라이버의 산업으로 분산
- [ ] 평균 상관 <0.6 수준
- [ ] 전부 고베타 성장주로 구성되지 않음
- [ ] 경기민감 + 방어 혼합
- [ ] 저상관 포지션 일부 포함

**Geographic Diversification:**
- [ ] 해외 노출 존재(주식의 15-30%)
- [ ] 미국 경기 단일 의존 아님
- [ ] 위험 성향에 맞는 EM 노출
- [ ] 상장지뿐 아니라 매출 지역 고려

**Market Cap Diversification:**
- [ ] Large/Mid/Small 혼합
- [ ] 메가캡(>$500B) 전용 포트폴리오 아님
- [ ] 소형주(<$2B) 전용 포트폴리오 아님
- [ ] 위험 성향에 맞는 평균 시총

**Asset Class Diversification:**
- [ ] 주식 비중이 위험 성향과 일치
- [ ] 매우 공격적 배분이 아니면 채권 포함
- [ ] 기회/유동성용 현금 버퍼 보유
- [ ] 필요 시 대체자산 포함

## Common Diversification Mistakes

### Mistake 1: False Diversification

**Problem:** 고상관 종목을 많이 보유해 분산된 것처럼 보임

**Example:**
- AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA
- 겉보기에는 7종목 분산
- 실제로는 섹터/팩터 집중

**Solution:** 종목 수가 아니라 섹터/리스크 드라이버 분산

### Mistake 2: Over-Diversification ("Diworsification")

**Problem:** 위험 감소 없이 수익만 희석

**Example:**
- 100개 개별 종목
- 인덱스와 중복
- 높은 비용의 closet indexing

**Solution:** 최선의 15-30개 아이디어 또는 저비용 인덱스

### Mistake 3: Home Country Bias

**Problem:** 국내 주식 과대 비중으로 글로벌 기회 상실

**Example:**
- US 투자자가 US 95%
- 글로벌 시총 대비 과대 노출

**Solution:** 해외 주식 15-30% 배분

### Mistake 4: Employer Stock Concentration

**Problem:** 직장/포트폴리오 리스크가 동일 기업에 결합

**Example:**
- 자사주 40%
- 회사 부진 시 소득+자산 동시 타격

**Solution:** 자사주를 포트폴리오 10% 미만으로 축소

### Mistake 5: Sector Drift

**Problem:** 승자 방치로 의도치 않은 섹터 집중

**Example:**
- Tech 상승으로 포트폴리오의 50%
- 의도한 오버웨이트가 아님

**Solution:** 정기 리밸런싱으로 분산 유지

### Mistake 6: Forgetting About Bonds

**Problem:** 변동성 감내가 어려운 투자자가 100% 주식 보유

**Example:**
- 30% 하락 시 패닉매도

**Solution:** 위험 성향/기간에 맞는 stock/bond 믹스

### Mistake 7: Low-Quality Diversification

**Problem:** 종목 수를 늘리기 위해 품질 낮은 종목 추가

**Example:**
- 질 좋은 20종목 + 투기 10종목
- 리스크 감소 없이 수익 저하

**Solution:** 품질 기준을 유지한 상태에서 분산

## Advanced Topics

### Factor-Based Diversification

전통적 분산 외에 팩터 노출도 고려합니다.

**Common Factors:**
- **Value:** 저 P/E, 저 P/B
- **Growth:** 고매출/고이익 성장
- **Momentum:** 최근 가격 강세
- **Quality:** 높은 ROE, 안정 이익
- **Low Volatility:** 낮은 beta, 안정 수익
- **Size:** Small vs Large

**Factor Diversification:**
- 단일 팩터 집중 회피
- 의도적 균형 또는 의도적 Tilt
- 팩터 사이클 인식 필요

### Tail Risk and Black Swans

**Problem:** 극단적 이벤트에서는 일반 분산이 약화

**2008 금융위기 예시:**
- 주식 50%+ 하락
- 상관계수 급등
- 전통적 분산 보호 제한

**Solutions:**
- **비상관 자산 포함:** Gold, long-vol, managed futures
- **Tail hedge:** Put option, VIX call
- **구성 방식:** Barbell (안전 코어 + 공격 위성)

### Dynamic Diversification

**Concept:** 시장 환경에 따라 분산 강도 조정

**High Volatility Regimes:**
- 포지션 수 확대/집중도 축소
- 방어 자산 확대
- 상관 낮은 조합 강화

**Low Volatility Regimes:**
- 약간 높은 집중 허용 가능
- 고확신 아이디어 중심
- 다소 높은 상관 수용 가능

**Implementation Challenge:** 레짐 판단과 규율이 필요

## Summary

**Key Principles:**

1. **분산은 비체계적 리스크를 줄인다** (체계적 리스크는 남음)
2. **적정 범위:** 개별 15-30종목 또는 5-10개 분산형 펀드
3. **다차원 접근:** 종목 수/비중/섹터/지역/상관
4. **가짜 분산 경계:** 종목은 많아도 상관이 높을 수 있음
5. **과다 분산 경계:** 너무 많으면 수익 희석
6. **정기 리밸런싱**으로 집중 드리프트 예방
7. **위험 성향 매칭:** 보수적일수록 분산 강도 강화

**Practical Guidelines:**

- 단일 종목 >10-15% 금지
- 단일 섹터 >30-35% 금지
- Top 5 <40%
- 6개+ 섹터
- 해외 노출 15-30%
- 자산배분은 투자 기간/위험 성향과 정합

**Remember:** 분산의 목표는 수익 극대화가 아니라 리스크 관리입니다. 잘 분산된 포트폴리오는 일부 상방을 포기하는 대신 치명적 손실을 방지해 시장에 오래 남게 해줍니다.
