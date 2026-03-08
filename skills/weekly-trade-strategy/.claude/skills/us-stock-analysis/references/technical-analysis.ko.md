# Technical Analysis 레퍼런스

## 핵심 기술적 지표

### 추세 지표

**이동평균 (Moving Averages, MA)**
- SMA (Simple Moving Average): N기간 평균 가격
- EMA (Exponential Moving Average): 최근 가격에 더 큰 가중치
- 자주 쓰는 기간: 20-day, 50-day, 200-day
- Golden Cross: 50-day MA가 200-day MA를 상향 돌파(강세)
- Death Cross: 50-day MA가 200-day MA를 하향 돌파(약세)

**MACD (Moving Average Convergence Divergence)**
- MACD Line: 12-day EMA - 26-day EMA
- Signal Line: MACD의 9-day EMA
- Histogram: MACD - Signal
- Bullish: MACD가 signal line 상향 돌파
- Bearish: MACD가 signal line 하향 돌파

### 모멘텀 지표

**RSI (Relative Strength Index)**
- Range: 0-100
- Overbought: > 70
- Oversold: < 30
- Divergence: 가격은 신고점/신저점인데 RSI는 그렇지 않음(반전 신호)

**Stochastic Oscillator**
- %K와 %D 라인
- Range: 0-100
- Overbought: > 80
- Oversold: < 20

### 변동성 지표

**Bollinger Bands**
- Middle Band: 20-day SMA
- Upper Band: Middle + (2 × standard deviation)
- Lower Band: Middle - (2 × standard deviation)
- Squeeze: 밴드 폭 축소(저변동성, 잠재적 breakout)
- Expansion: 밴드 폭 확대(고변동성)

**ATR (Average True Range)**
- 변동성을 측정
- ATR이 높을수록 변동성 큼
- stop-loss 배치에 활용

### 거래량 지표

**OBV (On-Balance Volume)**
- 누적 거래량 지표
- OBV 상승 + 주가 상승 = 강한 상승 추세
- OBV와 주가 간 divergence = 잠재적 반전

**Volume Moving Average**
- 현재 거래량을 평균 거래량과 비교
- 고거래량 breakout = 더 강한 신호

## 차트 패턴

### 반전 패턴
- Head and Shoulders (bearish)
- Inverse Head and Shoulders (bullish)
- Double Top (bearish)
- Double Bottom (bullish)

### 지속 패턴
- Flags and Pennants
- Triangles (ascending, descending, symmetrical)
- Rectangles

## 지지와 저항

**Support**: 매수 압력이 추가 하락을 막는 가격대
**Resistance**: 매도 압력이 추가 상승을 막는 가격대

**식별해야 할 핵심 레벨:**
- 이전 고점과 저점
- 라운드 넘버(심리적 가격대)
- 이동평균
- Fibonacci retracement levels (23.6%, 38.2%, 50%, 61.8%, 78.6%)

## 분석 워크플로

1. **추세 식별** (상승, 하락, 횡보)
2. **지지/저항 레벨 도출**
3. **다중 타임프레임 확인** (일봉, 주봉, 월봉)
4. **지표로 확인** (단일 지표 의존 금지)
5. **divergence 탐색** (가격 vs 지표)
6. **거래량 평가** (추세 강도 확인)
7. **차트 패턴 식별**
8. **risk/reward ratio 산정**
