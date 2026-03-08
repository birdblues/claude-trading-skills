# Market Top 탐지 방법론

## 개요

이 프레임워크는 시장의 의미 있는 하락(10-20% 조정)에 선행하는 기관 행동을 포착하기 위해, 검증된 3가지 접근법을 통합합니다.

## 세 가지 핵심 축(The Three Pillars)

### Pillar 1: O'Neil - Distribution Day 누적

**출처:** William O'Neil, "How to Make Money in Stocks"

**핵심 개념:** 기관투자자(mutual funds, hedge funds, pensions)는 대형 포지션을 하루에 처분할 수 없습니다. 이들의 매도는 독특한 패턴을 만듭니다. 즉, 지수가 전일 대비 증가한 거래량에서 하락합니다. 이런 "distribution days"가 누적되면 smart money가 체계적으로 이탈 중임을 시사합니다.

**Distribution Day 정의:**
- 지수가 전일 종가 대비 >= 0.2% 하락
- 거래량이 전일보다 증가
- 두 조건을 동시에 충족해야 함

**Stalling Day 정의:**
- 거래량이 전일 대비 증가
- 가격 상승은 미미(<0.1%)
- 강세에서 기관 매도 출회를 시사
- 반가중(0.5 distribution days)으로 계산

**25일 윈도우:**
- distribution days는 25거래일 후 만료
- 롤링 25일 카운트만 중요
- 오래된 이벤트가 현재 평가를 왜곡하지 않도록 방지

**O'Neil 경고 임계값:**
- 25거래일 내 4-5 distribution days = "market under pressure"
- 6+ distribution days = "distribution is heavy, protect capital"
- stalling days와 결합해 전체 그림을 판단

### Pillar 2: Minervini - Leading Stock 악화

**출처:** Mark Minervini, "Trade Like a Stock Market Wizard" / "Think & Trade Like a Champion"

**핵심 개념:** 시장 고점은 갑자기 나타나지 않습니다. 이전 랠리를 주도했던 선도주가 주요 지수보다 먼저 무너지며 진행됩니다. 이는 기관이 이익 실현을 위해 가장 큰 승자부터 먼저 매도하기 때문입니다.

**Monty 글의 핵심 관찰:**
> "약세장 초기 단계에서는 특정 주도주가 하락 트렌드에 저항하는 것처럼 강하게 보이며, 여전히 상승할 수 있다는 인상을 줍니다."
> (In the early stages of a bear market, certain leading stocks appear to resist the downtrend, giving the impression they can still rise.)

**탐지 방법:**
성장/혁신 ETF 바스켓을 시장 리더십 프록시로 사용:
- ARKK (Innovation), WCLD (Cloud), IGV (Software)
- XBI (Biotech), SOXX/SMH (Semiconductors)
- KWEB (China Tech), TAN (Solar)

**ETF별 악화 신호:**
1. 52주 고점 대비 괴리(>10% 경고, >25% 약세권)
2. 가격이 50일 이동평균 하회
3. 가격이 200일 이동평균 하회
4. lower highs 패턴 형성

**증폭 규칙:** leading ETFs의 60%+에서 악화가 나타나면 신호를 1.3x로 증폭. 이는 리더십 붕괴의 시스템적 성격을 반영합니다.

### Pillar 3: Monty - Defensive Sector Rotation

**출처:** monty-trader.com "미국주식 주식시장 천장 판별법과 하락 국면에서 해야 할 일"

**핵심 개념:** 시장 고점 전에 자금은 공격적/성장 섹터에서 방어적/가치 섹터로 이동합니다. 이 "rotation"은 기관이 주식 비중을 유지한 채 방어적으로 포지셔닝하고 있음을 보여주는 핵심 조기 경보입니다.

**Defensive Sectors (안전자산 성격):**
- XLU (Utilities) - 안정적 현금흐름, 채권 유사
- XLP (Consumer Staples) - 경기침체 저항 수요
- XLV (Healthcare) - 비경기민감 지출
- VNQ (Real Estate) - 인컴 중심

**Offensive Sectors (성장/리스크):**
- XLK (Technology) - 성장 의존도 높음
- XLC (Communication Services) - 광고지출 민감
- XLY (Consumer Discretionary) - 경기 민감
- QQQ (NASDAQ 100) - 테크 중심 성장 프록시

**신호:** 20일 롤링 구간에서 defensive가 offensive를 아웃퍼폼하면 자금이 방어적으로 이동 중입니다. 상대성과 스프레드 +3% 이상은 강한 경고 신호입니다.

---

## 보조 컴포넌트

### Component 4: Market Breadth Divergence

**개념:** 지수는 신고점을 가는데 참여 종목 수가 줄면 랠리 폭이 좁아져 취약해집니다. 지수 가격과 breadth 사이의 이 "divergence"는 전형적 고점 신호입니다.

**핵심 지표:** S&P 500 구성 종목 중 200-day moving average 위에 있는 비율.
- 건강한 시장: >70%
- 경고 구간: 50-70% + 지수는 고점 근처
- 위험 구간: <50% + 지수는 고점

**중요한 뉘앙스:** breadth divergence는 지수가 52주 고점 근처(고점 대비 -5% 이내)일 때 가장 의미가 큽니다. 지수가 이미 크게 조정된 뒤라면 약한 breadth는 덜 유의미합니다.

### Component 5: Index Technical Condition

**이동평균 구조:**
- 건강: Price > 21 EMA > 50 EMA > 200 SMA
- 악화: 위 관계 중 일부 역전
- 약세: 가격이 주요 이동평균 전부 하회

**패턴 인식:**
- Failed Rally: 반등했지만 직전 고점 돌파 실패
- Lower Highs: 스윙 고점이 순차적으로 낮아짐
- 거래량 동반 Gap Down: 기관 패닉 매도

### Component 6: Sentiment & Speculation

**VIX (공포 지수):**
- <12: 극단적 안도(경고)
- 12-16: 낮은 변동성(약한 경고)
- 16-20: 정상
- >25: 공포 고조(고점 형성보다 조정 진행 가능성)

**Put/Call Ratio:**
- <0.60: 극단적 콜 매수(최대 안도)
- 0.60-0.70: 낙관 과열
- 0.70-0.80: 완만한 bullish
- >0.80: 건강한 경계심

**VIX Term Structure:**
- Steep Contango: 시장이 평온을 기대(안도 신호)
- Backwardation: 헤지 수요 증가(공포 신호)

---

## Follow-Through Day (FTD) 모니터

Composite score > 40 구간에서 바닥 확인용으로 중요한 O'Neil 개념:

1. **Rally Attempt Day:** 하락 후 지수가 처음 상승 마감한 날
2. **카운팅 시작:** 잠재 상승 추세 Day 1
3. **Follow-Through Day:** Rally attempt의 day 4-7 사이, 강한 상승(1.5%+) + 전일 대비 거래량 증가
4. **의미:** "The most powerful uptrends usually begin with a Follow-Through Day on day 4-7"

**False FTD 비율:** 약 25% FTD는 실패. 다중 FTD 출현 시 신뢰도 상승.

---

## 점수 철학

### 왜 가중 Composite인가?

단일 지표로 시장 고점을 완벽히 예측할 수 없습니다. 각 축은 서로 다른 차원을 포착합니다.
- Distribution Days: 기관 매도의 직접 측정
- Leading Stocks: 시장 리더십의 질
- Defensive Rotation: 기관 포지셔닝 변화
- Breadth: 시장 참여도 건강성
- Technicals: 가격 구조 건전성
- Sentiment: 심리 극단

### 가중치 근거

- **Distribution Days (25%):** 기관 행동의 가장 직접적 측정치
- **Leading Stocks (20%):** Minervini식 핵심 선행 신호
- **Defensive Rotation (15%):** Monty 방법론의 차별 포인트
- **Breadth (15%):** 고전적 확인 신호
- **Technicals (15%):** 구조적 무결성 점검
- **Sentiment (10%):** 맥락/극단 확인(단독 신뢰도는 낮음)

### 캘리브레이션 원칙

점수는 다음과 같이 해석되도록 보정됩니다.
- 정상 건강장: 10-20
- 조기 경고장: 25-40
- 고점 형성 초기~중기: 40-55
- 명확한 고점 형성: 60-80
- 붕괴 동반 고점 완료: 80+
