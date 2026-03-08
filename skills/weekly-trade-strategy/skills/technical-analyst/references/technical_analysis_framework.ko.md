# Technical Analysis Framework

이 레퍼런스는 주간 가격 차트에 대해 객관적이고 차트 기반 technical analysis를 수행하는 방법론을 제공합니다.

## Core Principles

1. **Chart-Only Analysis**: 분석은 차트 데이터만으로 수행합니다. 외부 뉴스, 펀더멘털 데이터, 시장 심리는 제외합니다.
2. **Objectivity**: 주관적 해석보다 관측 가능한 패턴과 데이터에 집중합니다.
3. **Weekly Timeframe**: 모든 분석은 중장기 관점을 위해 주간 차트를 사용합니다.
4. **Probability-Based**: 미래 시나리오는 확정이 아니라 확률로 표현합니다.

## 1. Trend Analysis

### Trend Classification

**Uptrend Criteria:**
- Higher highs (HH)와 higher lows (HL) 패턴
- 가격이 핵심 moving average 위에서 거래
- moving average가 bullish 순서로 정렬(shorter MA > longer MA)

**Downtrend Criteria:**
- Lower highs (LH)와 lower lows (LL) 패턴
- 가격이 핵심 moving average 아래에서 거래
- moving average가 bearish 순서로 정렬(shorter MA < longer MA)

**Sideways/Range-bound:**
- 명확한 higher high/low 또는 lower high/low 패턴 부재
- 정의된 support/resistance 사이에서 가격 진동
- moving average가 평평하거나 서로 얽힘

### Trend Strength Assessment

**Strong Trend:**
- 연속적인 higher highs/lows(uptrend) 또는 lower highs/lows(downtrend)
- retracement가 작음
- volume이 가격 방향을 확인

**Weak Trend:**
- 불규칙한 고점/저점 패턴
- 깊은 retracement(이전 움직임의 >50%)
- 가격과 volume 사이 divergence

**Trend Exhaustion Signals:**
- 신규 고점/저점에서 모멘텀 감소
- 추세 진행 중 volume 감소
- moving average로부터 과도한 이격
- candlestick reversal pattern(예: shooting star, hammer, engulfing)

## 2. Support and Resistance Analysis

### Identifying Support Levels

Support는 과거에 매수 수요가 추가 하락을 막았던 가격 레벨입니다.

**Criteria for Valid Support:**
- 가격이 해당 레벨에서 최소 2-3회 반등
- 반등 시 volume spike 발생
- 상위 timeframe의 support일수록 중요도 상승
- 라운드 넘버(심리적 레벨)가 support로 작동하는 경우가 많음

**Support Types:**
- **Horizontal Support**: 유사 가격대의 과거 저점 정렬
- **Trendline Support**: higher lows를 잇는 우상향 선
- **Moving Average Support**: 핵심 MA(예: 20-week, 50-week)의 동적 support

### Identifying Resistance Levels

Resistance는 과거에 매도 수요가 추가 상승을 막았던 가격 레벨입니다.

**Criteria for Valid Resistance:**
- 가격이 해당 레벨에서 최소 2-3회 저항
- 저항 구간에서 volume spike
- 과거 의미 있는 고점
- 라운드 넘버가 resistance로 작동하는 경우가 많음

**Resistance Types:**
- **Horizontal Resistance**: 유사 가격대의 과거 고점 정렬
- **Trendline Resistance**: lower highs를 잇는 우하향 선
- **Moving Average Resistance**: 핵심 MA의 동적 resistance

### Support/Resistance Significance

**Strong S/R Levels:**
- 다회 테스트(3+ touches)
- 장기간 유지(수개월~수년)
- 과거 접점에서 높은 volume
- 다른 technical factors와의 confluence(Fibonacci, 라운드 넘버, moving averages)

**Weak S/R Levels:**
- 1-2회 접점만 존재
- 최근 형성
- 접점의 거래량이 낮음

### Support-Resistance Flip

돌파 후 support와 resistance는 종종 역할이 바뀝니다. 이 "role reversal"은 핵심 개념입니다:
- **Broken Support → Resistance**: 하향 이탈 후 과거 support가 재테스트 시 resistance로 작동
- **Broken Resistance → Support**: 상향 돌파 후 과거 resistance가 pullback 시 support로 작동

## 3. Moving Average Analysis

### Key Moving Averages for Weekly Charts

- **20-week MA**: 단기 추세 지표(약 4개월)
- **50-week MA**: 중기 추세 지표(약 1년)
- **200-week MA**: 장기 추세 지표(약 4년)

### Moving Average Interpretations

**Price Position Relative to MAs:**
- **Above all MAs**: 강한 bullish 구조
- **Below all MAs**: 강한 bearish 구조
- **Between MAs**: 전환 구간, 추세 불명확

**Moving Average Crossovers:**
- **Golden Cross**: 20-week MA가 50-week MA 상향 돌파(bullish signal)
- **Death Cross**: 20-week MA가 50-week MA 하향 돌파(bearish signal)

**Moving Average Slope:**
- **Rising MAs**: bullish momentum
- **Falling MAs**: bearish momentum
- **Flat MAs**: 횡보, 방향성 모멘텀 부족

**Moving Average as Support/Resistance:**
- uptrend에서는 MA(특히 20-week, 50-week)가 동적 support 역할
- downtrend에서는 MA가 동적 resistance 역할
- MA에서 반복 반등/저항이 나타날수록 중요도 증가

### Moving Average Confluence

여러 MA가 모이거나 정렬될 때:
- **Bullish Alignment**: 20-week > 50-week > 200-week (모두 상승)
- **Bearish Alignment**: 20-week < 50-week < 200-week (모두 하락)
- **Compressed/Converging MAs**: 큰 방향성 움직임의 전조가 되기 쉬움

## 4. Volume Analysis

Volume은 가격 움직임의 강도/약세를 확인하는 요소입니다.

### Volume Interpretation Principles

**Volume Confirms Price:**
- **Rising prices + Rising volume**: 건강한 uptrend, 강한 매수
- **Falling prices + Rising volume**: 건강한 downtrend, 강한 매도
- **Rising prices + Falling volume**: 약한 상승, 신뢰도 부족
- **Falling prices + Falling volume**: 약한 하락, 매도 소진 가능

### Key Volume Patterns

**Volume Spikes:**
- **At Support**: 고거래량 반등은 강한 매수 수요 시사(bullish)
- **At Resistance**: 고거래량 저항은 강한 매도 압력 시사(bearish)
- **On Breakout**: 고거래량 돌파는 움직임 유효성 강화
- **Low Volume Breakout**: 실패 돌파(false signal)로 이어지기 쉬움

**Volume Trends:**
- **Increasing Volume in Trend Direction**: 추세 강도 확인
- **Decreasing Volume in Trend Direction**: 추세 소진 경고
- **Volume Climax**: 극단적 거래량은 추세 극점(투매/과열) 시사 가능

**Volume Divergence:**
- **Bullish Divergence**: 가격은 신저점인데 volume 감소(매도 소진)
- **Bearish Divergence**: 가격은 신고점인데 volume 감소(매수 소진)

## 5. Chart Patterns and Candlestick Analysis

### Reversal Patterns

**Bullish Reversal:**
- **Hammer**: 긴 아래 꼬리, 상단 작은 몸통, support에서 출현
- **Bullish Engulfing**: 이전 red candle을 완전히 감싸는 큰 green candle
- **Morning Star**: 3개 캔들 패턴(하락, 작은 몸통, 상승)
- **Double/Triple Bottom**: support 2-3회 테스트 후 반전

**Bearish Reversal:**
- **Shooting Star**: 긴 위 꼬리, 하단 작은 몸통, resistance에서 출현
- **Bearish Engulfing**: 이전 green candle을 완전히 감싸는 큰 red candle
- **Evening Star**: 3개 캔들 패턴(상승, 작은 몸통, 하락)
- **Double/Triple Top**: resistance 2-3회 테스트 후 반전

### Continuation Patterns

**Bullish Continuation:**
- **Bull Flag**: 강한 상승 후 조정, 이후 상방 돌파
- **Ascending Triangle**: higher lows + 수평 resistance, 상방 이탈

**Bearish Continuation:**
- **Bear Flag**: 강한 하락 후 조정, 이후 하방 이탈
- **Descending Triangle**: lower highs + 수평 support, 하방 이탈

### Pattern Significance

패턴의 신뢰도는 다음일 때 더 높습니다:
- 핵심 support/resistance 레벨에서 형성
- 적절한 volume 동반(돌파 시 거래량 증가)
- moving average 및 추세 구조와 정합
- 더 긴 timeframe에서 발생(weekly > daily)

## 6. Scenario Development and Probability Assignment

### Scenario Development Process

각 차트 분석에서 2-4개 시나리오를 개발합니다:

1. **Base Case Scenario**: 현재 구조 기준 가장 가능성 높은 결과
2. **Bull Case Scenario**: 핵심 resistance 돌파 시 낙관 시나리오
3. **Bear Case Scenario**: 핵심 support 붕괴 시 비관 시나리오
4. **Alternative Scenario** (optional): 확률은 낮지만 타당한 시나리오

### Probability Assignment Framework

확률은 아래를 기반으로 할당합니다:

**High Probability (50-70%):**
- 현재 추세와 정합
- 다중 확인 요소 존재(추세, S/R, MA, volume)
- 최근 price action이 시나리오를 지지
- 명확한 invalidation level 존재

**Medium Probability (25-45%):**
- 추세 전환 또는 큰 breakout 필요
- 지지 요인이 일부만 존재
- 핵심 레벨 유지/이탈 여부에 의존

**Low Probability (5-20%):**
- 대부분 technical factors와 반대
- 구조적 큰 변화 필요
- 근거는 제한적이나 기술적으로 가능

### Probability Assignment Example

Current Structure: Uptrend, above all MAs, holding support

- **Bull Case (60%)**: support pullback 후 상승 추세 지속
  - Reasoning: 추세 유지, 핵심 support 방어, volume 확인

- **Base Case (30%)**: 다음 방향성 전 범위 박스 consolidation
  - Reasoning: resistance 접근, 일부 이익실현 신호

- **Bear Case (10%)**: support 하향 이탈, 추세 반전
  - Reasoning: 아직 뚜렷한 반전 신호는 없지만 가능성은 존재

**Note**: 확률 총합은 100%여야 하며, 근거 강도에 따라 조정합니다.

### Invalidation Levels

각 시나리오마다 무효화 가격을 명시합니다:
- **Bull Scenario Invalidation**: 핵심 support 하향 이탈
- **Bear Scenario Invalidation**: 핵심 resistance 상향 돌파
- **Base Case Invalidation**: range 상하단 돌파

## 7. Analysis Structure and Discipline

### Analysis Checklist

각 차트에서 체계적으로 평가:

1. ✓ **Current Trend**: 방향, 강도, 기간 식별
2. ✓ **Support Levels**: 주요 수평/동적 support 표시
3. ✓ **Resistance Levels**: 주요 수평/동적 resistance 표시
4. ✓ **Moving Averages**: 위치, 기울기, crossover 확인
5. ✓ **Volume Pattern**: volume이 가격을 확인/모순하는지 평가
6. ✓ **Chart Patterns**: 형성 중/완료된 유의미 패턴 식별
7. ✓ **Scenarios**: 확률 포함 2-4개 시나리오 개발
8. ✓ **Invalidation Levels**: 시나리오 무효화 조건 정의

### Objectivity Reminders

- confirmation bias 회피: bullish/bearish 시나리오를 모두 고려
- 차트가 말하게 하기: 없는 패턴을 억지로 만들지 않기
- 신규 데이터에 따라 분석 업데이트: 차트는 동적
- 불확실성 인정: 모든 차트가 명확한 신호를 주지는 않음
- 예측이 아닌 확률에 집중: 어떤 시나리오도 100% 확실하지 않음

### Common Pitfalls to Avoid

- **Overcomplicating**: 지표 과다 사용은 분석 마비를 유발
- **Ignoring Volume**: volume 없는 가격 해석은 불완전
- **Forcing Patterns**: 명확하지 않은 패턴을 억지로 인식
- **Disregarding Timeframe**: weekly와 daily 해석 차이 무시
- **Neglecting Context**: 차트 단독 분석이 원칙이지만 시장 맥락도 유의
- **Being Too Certain**: 시장은 결정론이 아니라 확률론
