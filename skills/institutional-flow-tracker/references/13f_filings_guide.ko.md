# 13F Filings 종합 가이드

## 13F Filing이란?

Form 13F는 SEC에 분기별로 제출하는 보고서이며, 최소 $100 million 이상의 운용자산(AUM)을 가진 기관 투자 운용사가 제출합니다. 이 양식은 각 캘린더 분기말 기준의 equity 보유 내역을 공시합니다.

### 법적 요구사항

**제출 의무 주체:**
- Investment advisors
- Banks
- Insurance companies
- Pension funds
- Hedge funds
- "13F securities"를 >$100M 운용하는 기타 기관

**반드시 보고해야 하는 항목:**
- 미국 상장 equities의 long positions
- Convertible bonds
- Exchange-traded options
- 분기말 기준 보유 주식 수

**보고되지 않는 항목:**
- Short positions
- Non-US securities
- Private equity investments
- Fixed income (convertibles 제외)
- Cash positions
- Derivatives (상장 options 제외)

**제출 기한:**
- 분기 종료 후 45일 이내
- Q1 (3월 31일 종료): 5월 15일까지
- Q2 (6월 30일 종료): 8월 14일까지
- Q3 (9월 30일 종료): 11월 14일까지
- Q4 (12월 31일 종료): 2월 14일까지

### 13F Filings의 핵심 데이터 포인트

**각 보유 항목별:**
1. **Issuer Name** - 회사명
2. **Ticker Symbol** - 주식 티커
3. **CUSIP** - 고유 증권 식별자
4. **Shares Held** - 보유 주식 수
5. **Market Value** - 포지션 달러 가치(주식 수 × 분기말 가격)
6. **Investment Discretion** - Sole/Shared/None
7. **Voting Authority** - Sole/Shared/None

**집계 데이터:**
- 총 보유 종목 수
- 총 포트폴리오 가치
- 포트폴리오 집중도
- 섹터 배분

## 데이터 이해하기

### 포지션 변화

**변화 유형:**
1. **New Position** - 지난 분기에는 없고 이번 분기에는 보유
2. **Increased Position** - 지난 분기보다 주식 수 증가
3. **Decreased Position** - 지난 분기보다 주식 수 감소
4. **Closed Position** - 지난 분기 보유, 이번 분기 0

**변화 계산식:**
```
Shares Change = Current Quarter Shares - Previous Quarter Shares
% Change = (Shares Change / Previous Quarter Shares) × 100
Dollar Value Change = (Shares Change) × (Current Stock Price)
```

**예시:**
```
Previous Quarter: 1,000,000 shares of AAPL @ $150 = $150M
Current Quarter:  1,200,000 shares of AAPL @ $180 = $216M

Shares Change: +200,000 shares (+20%)
Dollar Value Change: +$66M (includes price appreciation + new purchases)
```

### Aggregate Institutional Ownership

**포트폴리오 레벨 지표:**
- **Total Institutional Ownership %** = (전체 기관 보유 주식 수 / 발행주식수) × 100
- **Number of Institutional Holders** = 해당 종목으로 13F를 제출한 고유 기관 수
- **Ownership Concentration** = 상위 10개 기관 보유 비중 %
- **Ownership Trend** = 총 기관 보유율 %의 QoQ 변화

**일반적인 보유율 구간:**
- **<20%** - 기관 관심 낮음(마이크로/스몰캡, 투기적 종목)
- **20-40%** - 평균 이하(성장주, 최근 IPO)
- **40-60%** - 평균(대부분 미드/라지캡)
- **60-80%** - 평균 이상(blue chips, dividend aristocrats)
- **>80%** - 매우 높음(성숙하고 안정적인 기업)

## 데이터 품질 고려사항

### 시차(Lag)

**보고 시차:**
- 포지션 기준 시점: 분기말(예: 3월 31일)
- filing 마감: 45일 후(예: 5월 15일)
- 데이터 가용 시점: 5월 중순 이후
- **총 지연:** 포지션 시점 대비 6-7주

**실무 영향:**
- 분기말 이후 주가가 크게 움직였을 수 있음
- 기관이 이미 포지션을 변경했을 수 있음
- 13F는 실시간 신호가 아닌 확인 지표로 사용

### 기밀 처리(Confidential Treatment)

**Form 13F-NT (Notice of Confidential Treatment):**
- 기관은 특정 포지션의 공시 지연을 요청할 수 있음
- 보통 front-running 방지를 위해 1-2분기 승인
- 대규모 매집/activist 포지션에서 흔함

**레드 플래그:**
- 대규모 포지션의 갑작스러운 등장(기밀 처리였을 가능성)
- 보고 AUM이 비정상적으로 낮은 대형 기관(숨겨진 포지션 가능성)

### 집계 이슈

**중복 집계(Double Counting):**
- 같은 조직 내 복수 엔티티가 동일 주식을 중복 보고할 수 있음
- 예: Vanguard Group + Vanguard Index Funds + Vanguard ETF Trust
- 정확한 기관 보유율 계산을 위해 관련 엔티티 통합 필요

**Custodial vs Beneficial Ownership:**
- 일부 기관은 실질 소유자가 아닌 custodian으로 보유
- 예: State Street가 pension funds의 custodian 역할
- "voting authority", "investment discretion" 필드 확인 필요

## 흔한 함정과 회피 방법

### Pitfall 1: 가격 변화를 무시

**문제:**
- 기관이 동일 주식 수를 보유해도 기관 보유율 %는 감소할 수 있음
- 발생 조건: 주가 하락, 기관 AUM이 보고 임계치 하회

**해결:**
- 주식 수 변화와 보유율 % 변화를 함께 추적
- 더 정확한 신호를 위해 주식 수 변화에 집중

**예시:**
```
Q1: Institution holds 1M shares, stock at $100, ownership = 5%
Q2: Institution holds 1M shares, stock at $50, ownership = 2.5%
Interpretation: No actual selling, just price decline affecting percentage
```

### Pitfall 2: Passive Index Funds 해석 오류

**문제:**
- Index funds는 펀더멘털 판단이 아니라 index 구성에 따라 기계적으로 매매
- Index funds 대규모 유입은 기관 보유율을 기계적으로 증가시킴

**해결:**
- active managers와 passive funds를 분리
- active manager 변화를 더 높은 가중치로 반영
- 추적 우선순위: ARK, Berkshire, Baupost > Vanguard Index Funds

**Active vs Passive 지표:**
- Active: 집중 포트폴리오(20-50종목), 고확신 베팅
- Passive: 분산 포트폴리오(500+종목), index 비중 추종

### Pitfall 3: 기관 품질 무시

**문제:**
- 모든 기관투자자가 동일하지 않음
- 100개 소형 펀드 매수 ≠ Warren Buffett 매수

**해결:**
- 트랙레코드와 전략 정합성으로 기관 Tier 분류
- Tier 1(우량 장기 투자자)에 높은 가중치 부여

**Institutional Tiers:**
- **Tier 1** (High conviction): Berkshire, Appaloosa, Baupost, Pershing Square
- **Tier 2** (Quality active): Fidelity, T. Rowe Price, Wellington
- **Tier 3** (Passive/momentum): Vanguard Index, State Street, momentum funds

### Pitfall 4: 단일 분기 변화에 과잉 반응

**문제:**
- 한 분기의 매수/매도만으로 추세 판단이 어려움
- 포트폴리오 리밸런싱, 환매, 일시적 요인일 수 있음

**해결:**
- 다분기 추세(3+분기) 확인
- 누적/분산이 지속될 때 확신도 상승
- 한 분기 = 노이즈, 세 분기 = 신호

**추세 품질:**
```
Strong Signal (3+ quarters same direction):
Q1: +10% institutional ownership
Q2: +8% institutional ownership
Q3: +12% institutional ownership
Interpretation: Sustained accumulation, high conviction

Noise (inconsistent):
Q1: +10% institutional ownership
Q2: -5% institutional ownership
Q3: +3% institutional ownership
Interpretation: No clear trend, likely portfolio adjustments
```

## 고급 분석 기법

### Flow Analysis

모든 기관의 순증/순감 주식 수를 추적:

```
Net Institutional Flow = Sum(All Institutional Share Changes)
Flow Ratio = (Shares Added by Buyers) / (Shares Sold by Sellers)

Flow Ratio > 2.0 = Strong accumulation
Flow Ratio 1.5-2.0 = Moderate accumulation
Flow Ratio 0.8-1.2 = Neutral/Balanced
Flow Ratio 0.5-0.8 = Moderate distribution
Flow Ratio < 0.5 = Strong distribution
```

### Concentration Risk Analysis

**Herfindahl-Hirschman Index (HHI):**
```
HHI = Sum of (Each Institution's Ownership %)²

HHI < 1000 = Diversified ownership (low concentration risk)
HHI 1000-1800 = Moderate concentration
HHI > 1800 = High concentration (risk if top holder sells)
```

**예시:**
```
Top 3 holders: 15%, 12%, 10% of institutional ownership
HHI = 15² + 12² + 10² = 225 + 144 + 100 = 469 (low concentration)

Top 3 holders: 40%, 30%, 20% of institutional ownership
HHI = 40² + 30² + 20² = 1600 + 900 + 400 = 2900 (high concentration)
```

### New Buyers vs Sellers Analysis

**분기별 코호트 추적:**
```
New Buyers = Institutions with zero shares last Q, non-zero this Q
Increasers = Institutions with more shares this Q
Decreasers = Institutions with fewer shares this Q
Exited = Institutions with shares last Q, zero this Q

Bull Signal: New Buyers > Exited AND Increasers > Decreasers
Bear Signal: Exited > New Buyers AND Decreasers > Increasers
```

### Smart Money Clustering

여러 우량 투자자가 동시에 매집하는 상황을 식별:

**Clustering Score:**
```
Score = Sum of (Institution Tier × % Position Change)

Tier 1 institutions: Weight = 3.0
Tier 2 institutions: Weight = 2.0
Tier 3 institutions: Weight = 1.0

Example:
Berkshire (Tier 1) +10% position = 3.0 × 10 = 30 points
Fidelity (Tier 2) +5% position = 2.0 × 5 = 10 points
Index Fund (Tier 3) +2% position = 1.0 × 2 = 2 points
Total Clustering Score = 42

Score > 50 = Strong smart money accumulation
Score 25-50 = Moderate accumulation
Score < 25 = Weak/no clustering
```

## 과거 성공 패턴

### 돌파 전 매집(Pre-Breakout Accumulation)

**패턴:**
- 종목이 2-4분기 동안 박스권 횡보
- 기관 보유율이 조용히 상승(10-20% 증가)
- 13F에서 매집이 확인된 1-2분기 뒤 돌파

**예시 종목:**
- NVDA (2019): AI 붐 이전 기관 매집
- TSLA (2019-2020): 500% 상승 전 점진적 기관 매수

### 조기 분산 경고(Early Distribution Warning)

**패턴:**
- 종목이 상승 추세
- 기관 보유율이 2+분기 하락
- top-tier 기관 이탈
- 분산 시작 후 1-2분기에 고점 형성

**예시 종목:**
- Dot-com 종목(1999-2000): 폭락 전 smart money 이탈
- 주택 관련 종목(2006-2007): 위기 전 기관 분산

## Fundamental Analysis와의 통합

**Bullish 확인:**
- 강한 펀더멘털(매출 성장, 마진 확장)
- 기관 보유율 상승
- 우량 투자자의 포지션 추가
- **Action:** 고확신 매수

**Bearish 경고:**
- 펀더멘털은 강하나 기관 보유율 하락
- 숫자가 좋아도 우량 투자자 이탈
- **Action:** 추가 조사(숨은 리스크 가능성)

**가치 기회(Value Opportunity):**
- 단기 펀더멘털 약세
- 기관 보유율 안정/상승(value 투자자 매집)
- **Action:** 펀더멘털 반등이 보이면 contrarian 기회

**회피:**
- 약한 펀더멘털
- 하락하는 기관 보유율
- 우량 투자자 이탈
- **Action:** 접근 금지

## 규제 변경 및 업데이트

**2025년 기준 현재:**
- 보고 임계치: $100M AUM
- filing 마감: 분기 종료 후 45일
- 정정(amendment) 규칙: filing 기간 내 허용

**제안 변경사항(모니터링 필요):**
- filing 마감 30일 단축 가능성
- short positions 공시 요구 가능성
- AUM 임계치 $50M 하향 가능성

**업데이트 확인 경로:**
- SEC website: https://www.sec.gov/rules
- 업계 뉴스: 규제 공지 추적

## 도구 및 리소스

**공식 소스:**
- SEC EDGAR Database: https://www.sec.gov/edgar/searchedgar/companysearch.html
- Form 13F instructions: https://www.sec.gov/pdf/form13f.pdf

**서드파티 집계 서비스:**
- WhaleWisdom: https://whalewisdom.com (free tier 제공)
- DataRoma: https://www.dataroma.com (superinvestors 추적)
- Fintel: https://fintel.io (institutional ownership 데이터)

**API 접근:**
- FMP API: Institutional ownership endpoints
- SEC API: filings 직접 접근(무료, rate-limited)

## 요약: 13F 데이터 효과적으로 사용하기

**Best Practices:**
1. ✅ 단일 분기보다 다분기 추세를 추적
2. ✅ 보유율 %만 보지 말고 주식 수 변화 중심으로 분석
3. ✅ 우량 기관에 더 높은 가중치 적용
4. ✅ fundamental analysis와 결합
5. ✅ 단독 신호가 아닌 확인 지표로 사용
6. ✅ filing 마감 이후 분기별 업데이트

**피해야 할 것:**
1. ❌ 13F를 실시간 포지션으로 가정하지 말 것
2. ❌ passive fund flows를 무시하지 말 것
3. ❌ 단일 기관 움직임을 과대평가하지 말 것
4. ❌ 단기 트레이딩에 사용하지 말 것
5. ❌ 보유율 계산 시 가격 변화 무시 금지
6. ❌ confidential treatment 요청 가능성 간과 금지

**기대 수익:**
- 학술 연구상 13F 기반 전략은 연 2-4% alpha 가능성이 보고됨
- momentum, value factor와 결합 시 성과가 가장 좋음
- 정보 비대칭이 큰 small/mid caps에서 효과가 높음
