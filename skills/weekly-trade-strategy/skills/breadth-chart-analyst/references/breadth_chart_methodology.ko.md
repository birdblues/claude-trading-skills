# Breadth 차트 분석 방법론

이 레퍼런스는 시장 건전성과 추세 상태를 상호보완적으로 보여주는 두 가지 시장 breadth 차트 분석을 위한 종합 방법론을 제공합니다.

## 개요

Market breadth 지표는 시장 움직임에 참여하는 종목의 비율을 측정해, 가격 지수만으로는 드러나지 않는 추세의 강도와 지속 가능성에 대한 인사이트를 제공합니다. 이 스킬은 다음 두 가지 breadth 측정에 초점을 둡니다.

1. **200MA-Based Breadth Index**: 중장기 추세 평가 도구
2. **Uptrend Stock Ratio**: 단기 추세 및 모멘텀 지표

이 두 차트는 함께 사용될 때 전략적(중장기) 관점과 전술적(단기) 관점을 동시에 제공합니다.

---

## Chart 1: S&P 500 Breadth Index (200-Day MA Based)

### 목적 및 사용 사례

이 차트는 200-day moving average 위에서 거래되는 S&P 500 종목 비율을 측정해 시장의 중장기 건강 상태를 보여줍니다. 주요 시장 사이클을 판단하는 전략적 포지셔닝 도구로 사용됩니다.

### 차트 구성 요소

#### 주요 라인

**8-Day Moving Average (8MA) - Orange Line**
- breadth index의 단기 스무딩
- 급격한 시장 변화에 더 민감
- 반전 지점 식별에 핵심
- 진입용 주요 신호 생성기로 사용

**200-Day Moving Average (200MA) - Green Line**
- market breadth의 장기 추세
- 반응이 느려 노이즈를 걸러냄
- 시장의 구조적 건전성을 나타냄
- 청산용 주요 신호 생성기로 사용

#### 기준 레벨

**Red Dashed Line (0.73 / 73%)**
- **평균 Peak 레벨**: 200MA 상단의 역사적 평균
- **의미**: breadth index가 이 레벨을 넘으면 시장 과열 상태
- **해석**:
  - 73% 이상: 매우 bullish 하지만 소진 구간 접근
  - 73%를 크게 상회: 조정 또는 횡보 위험 상승
  - 장기간 유지되기 어려운 구간

**Blue Dashed Line (0.23 / 23%)**
- **평균 8MA Trough 레벨**: 8MA 저점의 역사적 평균
- **의미**: 8MA가 이 레벨 아래로 내려가면 극단적 과매도 상태
- **해석**:
  - 23% 이하: 심각한 시장 스트레스, capitulation 수준 매도
  - 반전 및 회복 확률 높음
  - 역사적으로 우수한 매수 기회 구간
  - 극단적 공포/비관이 동반되는 경우가 많음

#### 신호 마커 (Triangles)

**Purple/Magenta Downward Triangles (▼)**
- **8MA Troughs**: 8-day moving average의 바닥 표시
- **의미**: 잠재적 반전 지점(특히 23% 근처/이하에서 강함)
- **활용**: 8MA가 trough에서 상승 전환할 때 주요 매수 신호

**Blue Downward Triangles (▼)**
- **200MA Troughs**: 200-day moving average의 바닥 표시
- **의미**: 매우 드문 메이저 시장 사이클 저점
- **활용**: 새로운 장기 bull market 시작 신호

**Red Upward Triangles (▲)**
- **200MA Peaks**: 200-day moving average의 천장 표시
- **의미**: 추세 소진을 시사하는 메이저 사이클 고점
- **활용**: 검증된 전략의 주요 매도 신호

#### 배경 음영

**Pink Background Regions**
- **Downtrend Periods**: 시장이 확인된 downtrend에 있는 기간
- **의미**: 고위험 환경, 방어적 포지셔닝 필요
- **활용**: 불리한 시장 조건을 시각적으로 식별

### 해석 프레임워크

#### 시장 국면

**Healthy Bull Market**
- 8MA와 200MA가 모두 상승
- breadth index가 40%~73% 구간
- 50-60% 구간 조정 후 8MA 위에서 지지
- 종목 전반의 폭넓은 참여

**Overheated Bull Market**
- breadth index가 73% 위에서 지속
- 8MA와 200MA 모두 매우 높은 수준
- 단기 조정 위험 높음
- 부정적 catalyst에 취약

**Market Top/Distribution Phase**
- 200MA가 peak 형성(red ▲)
- 200MA가 peak 전이라도 8MA가 먼저 꺾이기 시작
- breadth index가 고점권에서 하락
- long 포지션 청산 신호

**Bear Market/Correction**
- 8MA와 200MA 모두 하락
- pink background 음영 존재
- breadth index 50% 이하
- 높은 변동성이 일반적

**Capitulation/Extreme Oversold**
- 8MA 23% 이하(blue dashed line)
- 8MA trough 형성(purple ▼)
- 극단적 비관/공포
- 역사적으로 매우 좋은 매수 기회

**Early Recovery**
- 8MA가 trough에서 상방 전환
- 200MA는 아직 하락 중일 수 있음(후행)
- breadth index가 극저점에서 상승 시작
- 신규 상승 추세의 초기 단계

### 백테스트 전략

과거 분석 기반으로 다음 전략이 강한 성과를 보여왔습니다.

#### 진입 규칙

**BUY Signal**: 8MA Trough Reversal
- 8MA가 명확한 바닥(purple ▼)을 형성할 때까지 대기
- 특히 8MA trough가 23% 이하이면 신호 강도 상승
- 8MA가 상방 전환하기 시작할 때 S&P 500 index long 진입
- 확인 조건: 8MA가 직전 최근 고점을 상향 돌파하거나 2-3일 연속 상승

#### 상세 반전 확인 기준

**중요**: 조기 진입 금지. trough 형성만으로는 진입 충분조건이 아닙니다. 반전은 반드시 CONFIRMED 되어야 합니다.

**필수 확인 단계**:

1. **Trough 식별** (Step 1):
   - 8MA가 purple ▼ triangle로 표시된 명확한 바닥 형성
   - trough 레벨은 이상적으로 40% 이하, 선호는 30% 이하
   - 23% 이하의 극단 trough는 최고 확률 셋업

2. **초기 반전** (Step 2):
   - 8MA가 trough에서 상승 시작
   - 첫 1-2기간 상승 관찰
   - **경고**: 아직 확정 신호 아님 - 진입 금지

3. **확인 구간** (Step 3 - 필수):
   - trough 이후 8MA가 2-3기간 연속 상승
   - 각 기간은 명확한 상승(최소 2-5% 증가) 필요
   - 확인 구간 중 유의미한 되돌림/재반전 없어야 함

4. **최신 데이터 검증** (Step 4 - 중요):
   - 차트 RIGHTMOST 3-5개 데이터 포인트 분석
   - 차트 최신 구간에서 8MA가 CURRENTLY 상승 중인지 확인
   - 최근 rollover 또는 하방 전환이 없는지 확인
   - 이 단계는 failed reversal 진입을 방지

5. **저항 돌파** (Step 5 - 선택적이지만 이상적):
   - 8MA가 55-60% 레벨 상향 돌파
   - breadth 개선의 강한 확인
   - 지속 가능성에 대한 신뢰도 상승

**확인 상태 분류**:

- **CONFIRMED (Green Light)**: Step 1-4 완료, 8MA가 2-3+기간 연속 상승하며 현재도 상승 중 → ENTER
- **DEVELOPING (Yellow Light)**: Step 1-2 완료, 하지만 연속 상승 < 2기간 → WAIT, MONITOR CLOSELY
- **FAILED (Red Light)**: Step 1-2 후 8MA가 꺾여 하락 중 → DO NOT ENTER, 신호 무효
- **NO SIGNAL (Red Light)**: trough 미형성 → WAIT

**시간 기반 확인**:
- 일반 확인 기간: trough 후 2-4주
- 확인에 6주 초과 시 신호 강도 약화
- trough 후 6주 내 8MA가 55%에 도달하지 못하면 유효성 재평가

#### Failed Reversal 패턴 (경고 신호)

**Failed Reversal이란?**

8MA가 trough를 만들고 상승을 시작했지만, 지속 모멘텀을 확보하기 전에 다시 하락 전환하는 경우를 말합니다. 이 경우 매수 신호는 무효화되며 더 깊은 조정으로 이어질 수 있습니다.

**Failed Reversal 식별 방법**:

1. **약한 반등 패턴**:
   - trough 이후 8MA가 1-2기간만 상승
   - 8MA가 50-55% 레벨 도달 실패
   - 이후 8MA가 다시 하락 전환
   - **결과**: false signal, 진입 금지

2. **조기 Rollover**:
   - 8MA가 50-60% 구간까지 상승
   - 상승 지속에 실패하고 하락 시작
   - 최신 데이터 포인트에서 8MA가 일관된 하락 궤적
   - **결과**: 반전 실패, 이미 진입했다면 청산하거나 신규 진입 금지

3. **Double Bottom 형성**:
   - 첫 trough 형성 후 8MA가 잠시 반등
   - 이후 8MA가 더 낮은 두 번째 trough 형성
   - **결과**: 첫 trough는 최종 바닥이 아님, 두 번째 trough 확인까지 대기

**Failed Reversal 대응 프로토콜**:
- 즉시 신호를 INVALID로 분류
- 포지션 진입 금지
- 8MA가 새로운 더 낮은 trough(대개 23% 이하)를 만들 때까지 대기
- 새 trough 기준으로 분석을 리셋하고 재확인

**과거 Failed Reversal 예시** (차트 참고):
- 빈도는 낮지만 심한 조정 구간에서 발생
- 대체로 더 깊은 하락(극단적 과매도 <23%)을 선행
- failed reversal 후 더 낮은 레벨에서 나오는 확정 반전은 종종 우수한 진입 기회를 제공

#### 최신 데이터 포인트 분석 프로토콜

**왜 최신 데이터 포인트가 가장 중요한가**

차트의 최신 3-5개 데이터 포인트(가장 오른쪽)는 CURRENT 시장 상태를 반영합니다. 과거 움직임은 맥락이며, 신호의 활성/형성/실패 여부는 최신 궤적이 결정합니다.

**프로토콜**:

1. **항상 가장 오른쪽 데이터 포인트부터 시작**:
   - 이것이 절대 최신 수치
   - 8MA의 CURRENT slope를 결정

2. **3-5개 데이터 포인트를 뒤로 추적**:
   - 현재 레벨 vs 1주 전 비교
   - 현재 레벨 vs 2주 전 비교
   - 현재 레벨 vs 3주 전 비교
   - 추세 판정: Rising / Falling / Flat

3. **연속 기간 계산**:
   - 8MA 연속 상승 기간 수 계산
   - 8MA 연속 하락 기간 수 계산
   - **확인은 2-3연속 상승 필요**
   - **trough 이후 1-2연속 하락은 failed reversal 경고**

4. **시각적 기울기 평가**:
   - 차트 오른쪽 끝의 8MA 라인을 시각적으로 추적
   - 라인이 UP / DOWN / FLAT 중 무엇인지 확인
   - 차트의 과거 구간에 의존하지 말고 오른쪽 끝에 집중

**예시 분석**:

```
Scenario: 8MA formed trough at 30% three weeks ago

Week-by-Week Analysis (from trough to present):
- Week 1 after trough: 30% → 40% (UP 10%)
- Week 2 after trough: 40% → 52% (UP 12%)
- Week 3 after trough: 52% → 48% (DOWN 4%)

Current Slope: FALLING
Consecutive Increases: 0 (last period was DOWN)
Status: FAILED REVERSAL - 8MA rolled over after initial bounce

Action: DO NOT ENTER. Signal is invalid. Wait for new trough formation.
```

```
Scenario: 8MA formed trough at 25% four weeks ago

Week-by-Week Analysis (from trough to present):
- Week 1 after trough: 25% → 35% (UP 10%)
- Week 2 after trough: 35% → 45% (UP 10%)
- Week 3 after trough: 45% → 55% (UP 10%)
- Week 4 after trough: 55% → 60% (UP 5%)

Current Slope: RISING
Consecutive Increases: 4 (all periods UP)
Status: CONFIRMED - Strong sustained reversal

Action: ENTER LONG. Signal is confirmed and robust.
```

#### 청산 규칙

**SELL Signal**: 200MA Peak Detection
- 200MA가 peak(red ▲)를 형성하면 long 포지션 청산
- 200MA peak는 보통 breadth index가 73% 근처/이상에서 발생
- 200MA 하락 전환을 기다리지 말고 peak 부근에서 청산
- 이는 bull market 구간 종료 신호

#### Risk Management

- **Stop Loss**: 8MA가 최근 trough 아래로 결정적으로 이탈하면 청산 고려
- **부분 익절**: breadth index가 73%를 초과하면(과열) 부분 익절 고려
- **재진입**: 동일 사이클에서는 새 8MA trough가 형성되지 않는 한 재진입 금지

#### 전략 성과 특성

- **Win Rate**: 극단 과매도 매수 + 강세 구간 매도로 역사적으로 높음
- **보유 기간**: 보통 수개월~1년 이상
- **Drawdown 관리**: 대형 bear market 보유를 회피
- **False Signal**: 지표 스무딩이 강해 상대적으로 드묾

### 분석 체크리스트

이 차트를 분석할 때 다음을 체계적으로 평가합니다:

1. ✓ **현재 8MA 레벨**: 과거 trough 및 23% 임계값 대비 위치는?
2. ✓ **현재 200MA 레벨**: 과거 peak 및 73% 임계값 대비 위치는?
3. ✓ **8MA 기울기**: 상승/하락/횡보 중 무엇인가?
4. ✓ **200MA 기울기**: 상승/하락/횡보 중 무엇인가?
5. ✓ **최근 신호 마커**: 최근 trough/peak triangle 존재 여부?
6. ✓ **시장 국면**: 현재 상태를 가장 잘 설명하는 국면은?
7. ✓ **전략 포지션**: 백테스트 전략 기준으로 long/flat/진입 준비/청산 준비 중 무엇인가?
8. ✓ **임계값 거리**: 핵심 레벨(23%, 73%)과 얼마나 가까운가?

---

## Chart 2: US Stock Market - Uptrend Stock Ratio

### 목적 및 사용 사례

이 차트는 미국 주식시장 전체에서 확인된 uptrend 상태 종목 비율을 측정해, 시장 모멘텀과 참여도를 실시간에 가깝게 보여줍니다. 단기 swing trading 및 시장 움직임 강도 확인을 위한 전술 도구입니다.

### "Uptrend Stock"의 정의

다음 조건을 **모두** 만족하면 uptrend stock으로 분류합니다:

1. **Price above 200-day MA**: 장기 uptrend
2. **Price above 50-day MA**: 중기 uptrend
3. **Price above 20-day MA**: 단기 uptrend
4. **Positive 1-month performance**: 최근 1개월 수익 양(+)

이 다중 조건 정의는 여러 타임프레임에서 모멘텀이 확인된 종목만 집계되도록 보장합니다.

### 차트 구성 요소

#### 주요 시각화

**색상 기반 추세 식별**

**Green Regions**
- 시장이 **uptrend**인 구간
- uptrend stock ratio가 대체로 상승
- 긍정적 시장 모멘텀
- long 포지션에 유리한 환경

**Red Regions**
- 시장이 **downtrend**인 구간
- uptrend stock ratio가 대체로 하락
- 부정적 시장 모멘텀
- long에 불리하며 방어적 자세 적합

**색상 전환**
- **Red-to-Green Transition**: downtrend 종료, uptrend 시작(BUY signal)
- **Green-to-Red Transition**: uptrend 종료, downtrend 시작(SELL signal)

#### 기준 레벨

**Lower Orange Dashed Line (~10%)**
- **단기 시장 바닥**: uptrend ratio가 약 10%까지 하락
- **의미**: 극단적 과매도 상태
- **해석**:
  - 10% 이하: 극단적 bearish 심리, capitulation 구간
  - 단기 반전 확률 높음
  - 이 레벨에서 단기 바닥이 자주 형성
  - long 진입의 risk/reward 우수

**Upper Orange Dashed Line (~37-40%)**
- **단기 시장 천장**: uptrend ratio가 약 40%에 접근
- **의미**: 과매수 상태, 시장 과열
- **해석**:
  - 40% 근처: 단기 과매수
  - 되돌림/횡보 확률 높음
  - 이 레벨에서 반전이 시작되기 쉬움
  - long 포지션 익절 또는 stop 타이트닝 고려

### 해석 프레임워크

#### 시장 상태

**Extreme Oversold (Ratio < 10%)**
- uptrend 참여 종목이 매우 적음
- 시장 전반 매도 압력
- 공포/비관 심리 고조
- 역발상 매수 기회
- VIX 급등과 동반되는 경우 많음
- red-to-green 전환 관찰 필요

**Moderate Bearish (Ratio 10-20%)**
- 평균 이하 참여도
- downtrend(red) 지속
- 선택적 종목 강세만 존재
- 확인 전 진입 대기

**Neutral/Transitional (Ratio 20-30%)**
- 평균적 시장 참여도
- uptrend 초기 또는 downtrend 말기일 수 있음
- 문맥 판단에서 색상(green vs red)이 핵심
- 추세 전환 여부 관찰

**Moderate Bullish (Ratio 30-37%)**
- 건강한 uptrend 참여도
- green 구간 우세
- 지속 가능한 모멘텀
- long 포지션에 우호적

**Extreme Overbought (Ratio > 37-40%)**
- uptrend 참여도 매우 높음
- 시장 단기 과열
- 되돌림에 취약
- green-to-red 전환 관찰
- 익절 고려

#### 추세 전환

**Red-to-Green (Downtrend to Uptrend)**
- **진입 신호**: 새로운 uptrend 구간 시작
- **특징**:
  - uptrend ratio가 바닥을 만들고 상승 시작
  - 대개 극단 과매도(<10-15%)에서 발생
  - MA 상향 돌파 종목 수 증가
  - 모멘텀이 bearish에서 bullish로 전환
- **행동**: index 또는 강한 개별 종목 long 진입

**Green-to-Red (Uptrend to Downtrend)**
- **청산 신호**: uptrend 구간 종료
- **특징**:
  - uptrend ratio가 고점을 만들고 하락 시작
  - 대개 과매수(>35-40%)에서 발생
  - 종목들이 핵심 moving average 하향 이탈
  - 모멘텀이 bullish에서 bearish로 전환
- **행동**: long 청산, 현금/방어 포지션 전환

### 트레이딩 전략

#### 단기 Swing Trading 전략

**진입 규칙**

1. **과매도 구간 대기**:
   - uptrend ratio가 10-15% 구간으로 하락
   - 시장이 red(downtrend) 구간

2. **추세 반전 식별**:
   - 색상이 red에서 green으로 전환
   - uptrend ratio가 저점에서 상승 시작
   - 확인 조건: ratio 2-3회 연속 상승

3. **Long 포지션 진입**:
   - S&P 500 index(SPY, ES futures) 또는 리더 종목 바스켓 매수
   - 리스크 허용도 기반 포지션 사이즈 조절

**청산 규칙**

1. **과매수 상태 감시**:
   - uptrend ratio가 37-40%에 접근
   - 시장이 오랜 기간 green 상태 유지

2. **추세 소진 식별**:
   - 색상이 green에서 red로 전환
   - uptrend ratio가 고점에서 하락 시작
   - 모멘텀 둔화

3. **Long 포지션 청산**:
   - index 포지션 매도
   - 현금 또는 방어 자산으로 이동

**Risk Management**

- **Stop Loss**: uptrend로 간주하던 구간에서 ratio가 최근 저점 아래로 이탈하면 청산
- **부분 청산**: ratio가 35-37%에 접근하면 분할 청산 고려
- **포지션 사이징**: 극단 과매도(<10%) 진입 시 크게, 중간 레벨 진입 시 작게
- **False Signal**: 며칠 내 급격한 red-green-red 또는 green-red-green 전환은 허위 신호일 수 있으므로 확인 필요

#### 전략 성과 특성

- **타임프레임**: 수일~수주(swing trading)
- **Win Rate**: 확인 기준에 따라 중간~높음
- **보유 기간**: 일반적으로 1-4주
- **최적 성과**: 진입이 극단 과매도(<10%)와 정렬될 때
- **리스크**: 횡보/무추세 장에서 whipsaw 발생

### 두 차트 결합 활용

최적 의사결정을 위해 두 breadth 차트를 함께 사용합니다.

#### 전략 포지셔닝 (Chart 1: 200MA Breadth)

- 전체 시장 국면(bull, bear, neutral) 판단
- 전략적 자산 배분 가이드
- 코어 포지션의 주요 진입/청산 지점 식별
- 긴 보유 기간(수개월~1년+)

#### 전술 포지셔닝 (Chart 2: Uptrend Ratio)

- 단기 모멘텀과 타이밍 판단
- 전술 트레이드 및 포지션 사이징 가이드
- swing trade용 단기 진입/청산 지점 식별
- 짧은 보유 기간(수일~수주)

#### 정렬 시나리오

**Scenario 1: Both Bullish**
- Chart 1: 8MA 상승, 200MA 상승 또는 횡보, breadth < 73%
- Chart 2: Green(uptrend), ratio가 과매도에서 상승
- **Action**: 최대로 bullish, 공격적 long 포지셔닝

**Scenario 2: Strategic Bullish, Tactical Bearish**
- Chart 1: 8MA 상승, 200MA 아직 peak 아님
- Chart 2: Red(downtrend), ratio 고점권 또는 하락
- **Action**: 코어 long 유지, 신규 전술 long 보류, 과매도 대기

**Scenario 3: Strategic Bearish, Tactical Bullish**
- Chart 1: 200MA가 peak 형성 또는 하락
- Chart 2: Green(uptrend), ratio가 극단 과매도에서 상승
- **Action**: 단기 전술 long만, 타이트한 stop, 전략적 청산 준비

**Scenario 4: Both Bearish**
- Chart 1: 두 MA 하락, pink background
- Chart 2: Red(downtrend), ratio 하락
- **Action**: 방어적 포지셔닝, 현금 또는 short, 8MA trough 대기

### Chart 2 분석 체크리스트

uptrend stock ratio 차트 분석 시 체계적으로 평가합니다:

1. ✓ **현재 Ratio 레벨**: 현재 uptrend stock 퍼센트는?
2. ✓ **현재 색상**: 시장이 green(uptrend)인가 red(downtrend)인가?
3. ✓ **임계값 근접도**: ratio가 10%(바닥), 40%(천장)에 얼마나 가까운가?
4. ✓ **추세 방향**: ratio는 상승/하락/횡보 중 무엇인가?
5. ✓ **최근 전환**: red-to-green 또는 green-to-red 전환이 있었는가?
6. ✓ **현재 추세 지속 기간**: 현재 색상 구간은 얼마나 지속되었는가?
7. ✓ **전략 포지션**: swing trading 전략 기준으로 long/flat/진입 준비/청산 준비 중 무엇인가?
8. ✓ **과거 맥락**: 현재 수치가 최근 극단값 대비 어떤 위치인가?

---

## 출력 요구사항

### 언어 및 스타일

- **분석 언어**: 모든 사고 및 분석은 영어로 수행
- **출력 형식**: 모든 보고서는 영어 markdown으로 생성
- **톤**: 전문적, 객관적, 분석적
- **용어**: 정확한 기술 용어를 일관되게 사용

### 분석 구조

각 breadth 차트 분석 보고서에는 다음이 포함되어야 합니다:

1. **Current Readings**: 핵심 메트릭의 구체적 값
2. **Signal Status**: 활성 신호(troughs, peaks, transitions)의 명확한 식별
3. **Market Regime Assessment**: 현재 시장 환경 분류
4. **Strategy Implications**: 백테스트 전략 기반 구체적 포지셔닝 권고
5. **Key Levels to Watch**: 분석이 바뀔 수 있는 다음 임계값/레벨
6. **Risk Considerations**: 잠재적 무효화 시나리오 및 대안 해석
7. **Combined Analysis** (두 차트 분석 시): 전략+전술 관점 통합

### 객관성 기준

- 관측 가능한 차트 데이터에만 근거
- breadth 해석과 직접 관련되지 않으면 외부 정보(뉴스, 펀더멘털) 배제
- 사실 관측과 확률 예측을 명확히 구분
- 신호가 모호하면 불확실성 인정
- 필요 시 bullish/bearish 시나리오를 모두 제시

---

## 피해야 할 일반적 실수

### Chart 1 (200MA Breadth) 실수

- **최근 추세 방향 오독** (가장 흔한 오류): 차트의 과거 움직임만 보고, 오른쪽 끝의 **최신 3-5개 데이터 포인트**를 보지 않는 것. 이로 인해 실제로는 하락인데 "8MA 상승"으로 판단하거나 반대로 판단하게 됩니다. CURRENT slope 판정은 항상 오른쪽 끝 데이터로 하세요.

- **성급한 진입**: 8MA 반전 확인(2-3연속 상승) 전에 매수하는 것. trough 형성만으로 진입하면 failed reversal 손실 가능성이 큽니다.

- **Failed Reversal 무시**: trough 이후 잠시 반등한 8MA가 다시 꺾인 상황을 인식하지 못하는 것. 8MA가 잠깐 오르고 다시 하락하면 신호는 INVALID입니다.

- **늦은 청산**: peak 형성에서 청산하지 않고 200MA 하락 확인을 기다리는 것. peak 자체가 매도 신호이며 하락 확인을 기다리면 늦습니다.

- **임계값 무시**: 23%, 73% 레벨의 의미를 무시하는 것. 이 임계값은 진입/청산 타이밍에 핵심 맥락을 제공합니다.

- **과도한 매매**: 8MA의 모든 흔들림을 거래하려는 것. 이 전략은 명확히 확인된 trough 반전까지 기다리는 인내가 필수입니다.

### Chart 2 (Uptrend Ratio) 실수

- **추격 매수**: ratio가 과매도에서 이미 크게 오른 후 진입
- **색상 무시**: ratio 수준만 보고 추세 방향(색상)을 고려하지 않음
- **False Breakout**: 색상 전환 확인 없이 성급히 대응
- **극단값 간과**: ratio가 <10% 또는 >40%에 도달한 의미를 놓침

### 일반 실수

- **단독 분석**: 한 차트만 보고 다른 차트를 고려하지 않음
- **과복잡화**: 핵심 신호를 흐리는 추가 indicator 과다 사용
- **Recency Bias**: 가장 최근 움직임에 과도한 가중치
- **과거 맥락 무시**: 현재 수치를 차트의 역사적 패턴과 비교하지 않음
