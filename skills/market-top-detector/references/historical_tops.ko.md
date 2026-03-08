# 과거 시장 고점 분석

## 개요

6-컴포넌트 Market Top Detector 프레임워크 관점에서 주요 시장 고점을 분석합니다. 이 과거 사례들은 점수 체계 캘리브레이션 데이터로 활용됩니다.

## 2000: Dot-Com Bubble Top (2000년 3월)

### 타임라인
- **S&P 500 고점:** 2000년 3월 24일 (1,527.46)
- **NASDAQ 고점:** 2000년 3월 10일 (5,048.62)
- **이후 하락:** 2.5년 동안 S&P -49%, NASDAQ -78%

### 컴포넌트 신호 (추정 점수)

| Component | Signal Level | Est. Score | Notes |
|-----------|-------------|------------|-------|
| Distribution Days | Very High | 90-100 | 2000년 3월 내내 강한 분산 |
| Leading Stocks | Critical | 85-95 | 인터넷 주식이 지수보다 수주 먼저 고점 형성 |
| Defensive Rotation | Strong | 70-80 | 수개월간 value/defensive 아웃퍼폼 |
| Breadth | Critical Divergence | 80-90 | Advance/Decline line이 1998년 4월에 이미 고점 |
| Index Technical | Breaking Down | 70-80 | NASDAQ이 50DMA를 먼저 하향 이탈 |
| Sentiment | Extreme | 90-100 | IPO 광풍, "new paradigm" 내러티브 |

**추정 Composite: 82-92 (Critical)**

### 핵심 교훈
Breadth divergence가 가장 이른 신호였습니다(고점 2년 전). Distribution days와 leading stock 붕괴는 최종 확인 신호였습니다. 6개 컴포넌트가 모두 red를 가리킬 때는 이미 하락이 시작된 뒤였습니다.

---

## 2007: Financial Crisis Top (2007년 10월)

### 타임라인
- **S&P 500 고점:** 2007년 10월 9일 (1,565.15)
- **이후 하락:** 17개월간 -57% (2009년 3월 저점)

### 컴포넌트 신호 (추정 점수)

| Component | Signal Level | Est. Score | Notes |
|-----------|-------------|------------|-------|
| Distribution Days | High | 75-85 | 2007년 9-10월 다중 분산 클러스터 |
| Leading Stocks | High | 70-80 | 주택(ITB)은 2006년 2월, 금융(XLF)은 2007년 6월 고점 |
| Defensive Rotation | Moderate | 55-65 | Utilities/Healthcare 상대강세 |
| Breadth | Diverging | 60-70 | NYSE advance/decline line이 2007년 7월 고점 |
| Index Technical | Weakening | 50-60 | S&P는 고점 근처였지만 내부 구조 악화 |
| Sentiment | Elevated | 55-65 | 2006-2007 장기간 VIX sub-12 |

**추정 Composite: 62-72 (Red Zone)**

### 핵심 교훈
2007년 고점은 슬로우모션 과정이었습니다. 선도 섹터(금융/주택)가 S&P보다 12-18개월 먼저 꺾였습니다. Composite는 Red에 진입하기 전 수개월간 Orange 구간에 머물렀고, 단일 이진 판단보다 점진적 익스포저 축소가 유효했습니다.

---

## 2018: Q4 Sell-Off (2018년 9-12월)

### 타임라인
- **S&P 500 고점:** 2018년 9월 20일 (2,930.75)
- **이후 하락:** -20% (베어마켓이 아닌 조정)
- **회복:** 2018년 12월 V자 반등, 2019년 4월 신고점

### 컴포넌트 신호 (추정 점수)

| Component | Signal Level | Est. Score | Notes |
|-----------|-------------|------------|-------|
| Distribution Days | Moderate | 55-65 | 10월에 분산 누적 |
| Leading Stocks | Moderate | 50-60 | FAANG 고점 시점 분화(FB 7월, AMZN 9월) |
| Defensive Rotation | Moderate | 45-55 | Q3 Utilities 상대강세 |
| Breadth | Mild Divergence | 40-50 | breadth 축소는 있었지만 극단 아님 |
| Index Technical | Weakening | 55-65 | 12월 50DMA가 200DMA 하향돌파 |
| Sentiment | Mixed | 35-45 | VIX 상승했지만 극단은 아님 |

**추정 Composite: 47-57 (Orange Zone)**

### 핵심 교훈
이 국면은 전형적 "조정" 사례였습니다(베어마켓 아님). Composite가 Orange 구간에 머무르는 것은 약한 포지션 차익실현을 정당화하되 전면 방어까지는 아님을 의미했습니다. 빠른 V자 회복은 다중 컴포넌트 극단값 없이 Critical로 올리지 않는 현재 설계의 타당성을 보여줍니다.

---

## 2022: Fed Tightening Bear Market (2022년 1월)

### 타임라인
- **S&P 500 고점:** 2022년 1월 3일 (4,796.56)
- **NASDAQ 고점:** 2021년 11월 19일 (16,057.44)
- **이후 하락:** S&P -25%, NASDAQ -33%

### 컴포넌트 신호 (2022년 1월 기준 추정)

| Component | Signal Level | Est. Score | Notes |
|-----------|-------------|------------|-------|
| Distribution Days | High | 75-90 | 2021년 12월 말~2022년 1월 초 강한 분산 |
| Leading Stocks | Critical | 80-90 | ARKK는 2021년 2월 고점(11개월 선행), 다수 성장주 고점 대비 -50%+ |
| Defensive Rotation | Strong | 65-75 | XLU, XLP 강한 아웃퍼폼 |
| Breadth | Severe Divergence | 70-80 | NASDAQ 신고점/신저점 구조 급격한 괴리 |
| Index Technical | Breaking | 60-70 | NASDAQ 200DMA 하향, S&P 핵심 레벨 테스트 |
| Sentiment | Elevated | 50-60 | Margin debt 사상 고점, 크립토 투기 |

**추정 Composite: 68-78 (Red Zone)**

### 핵심 교훈
ARKK(leading stock 프록시)는 S&P보다 11개월 먼저 고점 형성. 이는 Minervini 신호의 전형으로, 선도주 악화가 지수보다 훨씬 먼저 발생합니다. 2022년 1월 시점 Composite는 Red zone에 확실히 위치해 공격적 차익실현 신호를 정당화했습니다. 2022년 사례는 "Leading Stock Health" 컴포넌트의 조기 경보력을 검증합니다.

---

## 크로스 케이스 패턴

### 모든 고점의 공통점:
1. 하락 직전 수주 동안 distribution days가 **클러스터링**
2. **Leading stocks가 지수보다 먼저 고점 형성**(수주~수개월)
3. **Breadth가 지수 가격과 괴리**(랠리 폭이 점점 좁아짐)
4. 고점 형성과 함께 **defensive rotation 가속**

### 케이스별로 달랐던 점:
1. **하락 강도:** -20%(2018)부터 NASDAQ -78%(2000)까지
2. **속도:** 2018은 급락(3개월), 2000-2002는 장기 하락(2.5년)
3. **회복 시간:** 2018은 4개월, 2000은 NASDAQ 7년
4. **Breadth divergence 타이밍:** 2000은 2년, 2022는 수개월

### 점수 캘리브레이션:
- **Orange Zone (41-60):** 조정 가능성 높음(2018형, -10-20%)
- **Red Zone (61-80):** 큰 하락 가능성 높음(2007/2022형, -20-35%)
- **Critical (81-100):** 극단 버블 고점(2000형, -40%+)

### 중요한 주의사항:
과거 기반 캘리브레이션은 완벽하지 않습니다. 각 시장 환경은 고유합니다. Composite score는 투자 판단의 하나의 입력값으로 사용해야 하며 확정적 예측 도구가 아닙니다. 시장은 실제 하락 전에 warning zone에 오래 머물 수 있습니다.

---

## 패턴: Leading Stocks의 조기 경보

Monty 글에서:
> 약세장 초기 단계에서는 특정 주도주가 하락 트렌드에 저항하는 것처럼 강하게 보이며,
> 여전히 상승할 수 있다는 인상을 줍니다.

이 패턴은 모든 과거 고점에서 나타났습니다.
- **2000:** 닷컴이 무너질 때 대형 기술주(MSFT, INTC)는 상대적으로 버팀
- **2007:** 금융 붕괴 와중에 에너지 섹터는 랠리
- **2022:** ARKK 계열 붕괴 중 AAPL, MSFT는 상대 안정
- **현재 유사 패턴:** 일부 메가캡은 버티지만 성장/투기 종목은 악화

그래서 Component 2(Leading Stock Health)는 S&P 500 구성주만 보지 않고 성장 ETF 바스켓을 사용합니다. 지수가 가리는 내부 악화를 포착하기 위함입니다.
