# PEAD Entry and Exit Rules

## Entry Rules

### Primary Entry: Red Candle Breakout
- **Trigger**: 주봉이 green candle(close >= open)로 red candle의 high 위에서 마감
- **Entry Price**: red candle high 부근 또는 소폭 상단
- **Confirmation**: breakout 주간 거래량이 4주 평균 거래량보다 높아야 함
- **Timing**: 주간 마감으로 breakout이 확정된 후 진입(금요일 세션 종료 시점)

### Gap Minimum Requirement
- PEAD 후보로 인정하려면 실적 당일 최소 3% gap-up 필요
- 더 큰 갭(5%+)은 일반적으로 더 강한 earnings surprise와 더 지속적인 drift를 시사
- 3% 미만 갭은 진짜 surprise보다 노이즈일 가능성

### Pre-Entry Checklist
1. Earnings gap-up이 최소 3%였는가
2. 명확한 red weekly candle이 형성되었는가(doji/inside bar 제외)
3. 현재 주봉이 green이며 종가가 red candle high 위인가
4. 유동성 확보를 위해 ADV20(20일 평균 거래대금)이 최소 $25M인가
5. penny stock 변동성 회피를 위해 주가가 $10 이상인가
6. earnings date 기준 5주 모니터링 윈도우 이내인가

## Exit Rules

### Stop-Loss
- **Level**: red candle low 하단
- **Type**: hard stop(mental stop 아님)
- **Rationale**: red candle low 하향 이탈 시 pullback 패턴 실패 및 기관 수급 지지 붕괴로 판단

### Profit Target
- **Primary Target**: 2R (entry-stop 리스크의 2배)
- **Calculation**: Target = Entry + (Entry - Stop) x 2.0
- **Example**: Entry $100, Stop $95(리스크 5%) -> Target $110(수익 10%, 2:1 R:R)

### Trailing Stop (Optional)
- 1R 수익 도달 후 stop을 breakeven으로 이동
- 1.5R 수익 도달 후 현재가 대비 1R 아래로 trailing
- PEAD drift가 이어질 때 수익을 잠그면서 추세 추종 가능

### Time-Based Exit
- 진입 후 4주 내 목표가 미도달 시, 본전 또는 소폭 손익에서 청산 고려
- PEAD drift는 실적 후 6-8주 이후 유의미하게 약해짐

## Position Sizing

### Risk-Based Sizing
- 거래당 포트폴리오 가치의 1-2% 이상 리스크를 지지 않음
- Position size = (Portfolio x Risk%) / (Entry - Stop)
- Example: $100K 포트폴리오, 1% risk = $1,000 risk budget
  - Entry $100, Stop $95 = 주당 $5 리스크
  - Position = $1,000 / $5 = 200 shares ($20,000 포지션)

### Liquidity-Based Constraints
- 포지션 크기를 ADV20의 1%를 넘기지 않음
- 이렇게 하면 큰 시장 충격 없이 하루 내 청산 가능
- Example: ADV20 = $50M -> Max position = $500K

### Portfolio-Level Constraints
- 동시 보유 PEAD 포지션 최대 3-5개
- 상관된 실적 리스크를 피하기 위해 섹터 분산
- 다수 PEAD 거래가 열려 있으면 포지션 크기 축소

## Monitoring Window

### Duration
- 기본값: earnings date부터 5주
- PEAD 효과는 1-3주차가 가장 강하고 4-5주차에 약화
- 5주 내 breakout 신호가 없으면 모니터링 대상에서 제거

### Weekly Review Process
1. red candle 형성 여부 확인(MONITORING -> SIGNAL_READY)
2. breakout 발생 여부 확인(SIGNAL_READY -> BREAKOUT)
3. breakout 캔들의 거래량 확인
4. 현재 red candle 레벨 기준 risk/reward 계산
5. 진입 가능한 유동성 유지 여부 확인

## Special Situations

### Multiple Red Candles
- red candle이 여러 개면 가장 최근 candle 기준으로 entry/stop 레벨 설정
- red candle 반복은 모멘텀 약화를 시사할 수 있으므로 포지션 크기 축소

### Gap-and-Go (No Red Candle)
- 일부 종목은 gap-up 후 의미 있는 pullback 없이 바로 진행
- 이런 경우는 PEAD screener 후보가 아님(정의된 리스크를 위해 red candle 필요)
- 확신이 높다면 대체 진입 전략 고려

### Earnings in Consecutive Quarters
- 2개 분기 이상 연속 실적 gap-up 종목은 지속적 펀더멘털 강세를 시사
- red candle 패턴이 형성되면 더 높은 확신의 PEAD 후보
