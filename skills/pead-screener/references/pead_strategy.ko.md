# PEAD Strategy - Post-Earnings Announcement Drift

## What is PEAD

Post-Earnings Announcement Drift (PEAD)는 금융시장에서 가장 견고한 anomaly 중 하나입니다. 긍정적 earnings surprise를 발표해 공시 직후 gap-up한 종목은, 이후 수주~수개월 동안 추가 상승 drift를 이어가는 경향이 있습니다. 이 drift는 새로운 실적 정보에 대한 시장의 체계적인 underreaction을 반영합니다.

## Academic Foundation

### Ball & Brown (1968)
Ray Ball과 Philip Brown의 기념비적 논문은 실적 발표 후 최대 60일 동안 주가가 earnings surprise 방향으로 계속 drift한다는 사실을 처음 문서화했습니다. 이는 효율적 시장 가설(Efficient Market Hypothesis)에 대한 초기 도전 중 하나였습니다.

### Bernard & Thomas (1989)
Victor Bernard와 Jacob Thomas는 PEAD에 대한 가장 포괄적인 분석을 제시했습니다. 핵심 결과는 다음과 같습니다:
- earnings surprise 상위 decile 종목은 발표 후 60일 동안 하위 decile 대비 약 4% 아웃퍼폼
- drift는 발표 후 첫 2-3주에 가장 강함
- 더 작은 규모, 유동성이 낮은 종목에서 drift가 더 강함
- anomaly는 다양한 기간과 시장 환경에서 지속적으로 관찰됨

### Foster, Olsen & Shevlin (1984)
drift 크기가 earnings surprise 크기에 비례함을 확인했습니다. 즉 surprise가 클수록 drift도 더 지속적입니다.

## Why It Works: Market Underreaction

PEAD가 존재하는 이유는 행동적/구조적 요인이 결합되기 때문입니다:

1. **Anchoring Bias**: 애널리스트와 투자자는 기존 실적 추정치에 고정되어 새로운 정보 반영이 불충분
2. **Gradual Information Diffusion**: 모든 참여자가 동시에 정보를 처리하지 않음; 기관, 개인, 알고리즘 시스템의 반응 속도가 다름
3. **Confirmation Bias**: 실적 전 약세 시각을 가진 투자자는 긍정 surprise를 일회성으로 치부할 수 있음
4. **Liquidity Constraints**: 대형 기관은 시장 충격 없이 즉시 풀 포지션을 구축하기 어려움
5. **Post-Earnings Volatility Risk**: 많은 트레이더가 실적 직후 높은 내재변동성을 피해 반응이 지연됨

## Weekly Candle Approach

이 screener는 일봉 대신 주봉 캔들 분석을 사용합니다. 이유는 다음과 같습니다:

### Why Weekly Candles

1. **Noise Reduction**: 주봉은 intraday/일간 노이즈를 걸러 실적 이후 실제 추세를 더 잘 보여줌
2. **Institutional Footprints**: 기관은 며칠이 아닌 수주에 걸쳐 포지션을 구축하는 경우가 많고, 주봉이 이를 포착
3. **Clear Pattern Recognition**: red/green 주봉은 매수·매도 우위 신호를 명확하게 제공
4. **Manageable Monitoring**: 주간 주기로도 체계적 모니터링이 가능해 운영 부담 감소

### Red Candle Pullback Pattern

이 screener가 식별하는 핵심 패턴:

1. **Earnings Gap-Up**: 실적 발표로 주가가 3%+ gap-up(green weekly candle)
2. **Post-Earnings Drift**: 1-2주 추가 상승 가능(green candles)
3. **Red Candle Pullback**: 질서 있는 조정으로 red weekly candle(close < open) 형성
4. **Breakout Signal**: 다음 green candle이 red candle high 위에서 마감하면 조정 종료 및 PEAD 추세 재개 신호

이 패턴이 작동하는 이유:
- red candle은 단기 트레이더의 이익실현을 반영
- red candle의 아래 꼬리는 기관 매수 지지 구간을 드러냄
- red candle high 상향 돌파는 수요가 공급을 초과함을 확인

## Stage-Based Monitoring System

screener는 각 종목을 4개 stage 중 하나로 분류합니다:

### MONITORING
- watch window 내에서 earnings gap-up 발생
- 아직 red weekly candle 미형성
- Action: watchlist에 추가하고 주간으로 red candle 형성 점검

### SIGNAL_READY
- earnings gap-up 이후 red weekly candle 형성 완료
- 아직 red candle high 상향 breakout 미발생
- Action: red candle high에 알림 설정, breakout 주문 준비

### BREAKOUT
- 현재 주봉이 green이고 가격이 red candle high 위
- 실제 진입 가능한 트레이드 신호
- Action: red candle low 하단 stop과 함께 진입

### EXPIRED
- earnings 이후 5주(설정 가능) 초과
- 이 구간 이후 PEAD 효과는 의미 있게 약화
- Action: watchlist에서 제거

## Historical Performance Characteristics

학술 연구와 실무 관찰 기반 특성:

- **Win Rate**: PEAD 전략의 역사적 승률은 55-65% 수준
- **Average Winner vs. Loser**: 승리 거래 크기가 손실 거래의 1.5-2.5배
- **Optimal Holding Period**: 핵심 PEAD drift는 진입 후 2-6주가 최적
- **Sector Sensitivity**: Technology 및 growth 섹터에서 효과가 더 강한 경향
- **Market Cap Effect**: mid-cap($2B-$20B)에서 analyst coverage gap으로 drift가 강한 경우가 많음
- **Earnings Quality**: EPS beat뿐 아니라 revenue beat 동반 시 drift가 더 강함

## Key Differences from Other Momentum Strategies

순수 price momentum 전략과 달리 PEAD는 펀더멘털 촉발형입니다:
- 특정 catalyst(earnings announcement)가 필요
- 단순 추세 추종이 아니라 정보 underreaction 가설에 기반
- 진입 가능 구간(post-earnings)과 모니터링 기간이 명확
- risk management가 임의 stop이 아니라 red candle 패턴에 anchored됨
