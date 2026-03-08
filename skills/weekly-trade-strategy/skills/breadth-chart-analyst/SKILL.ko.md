---
name: breadth-chart-analyst
description: 이 스킬은 시장 breadth 차트, 특히 S&P 500 Breadth Index(200-Day MA 기반)와 US Stock Market Uptrend Stock Ratio 차트를 분석할 때 사용해야 합니다. 사용자가 breadth 차트 이미지를 제공해 분석을 요청하거나, 시장 breadth 평가, 포지셔닝 전략 추천, breadth 지표 기반의 중기 전략/단기 전술 관점을 이해하고자 할 때 사용합니다. 모든 분석과 출력은 영어로 수행됩니다.
---

# Breadth Chart Analyst

## 개요

이 스킬은 전략적(중장기) 관점과 전술적(단기) 관점을 제공하는 상호보완적 두 가지 시장 breadth 차트를 전문적으로 분석합니다. breadth 차트 이미지를 분석해 시장 건전성을 평가하고, 백테스트된 전략 기반 신호를 식별하며, 포지셔닝 권고를 제시합니다. 모든 사고 과정과 출력은 영어로만 수행합니다.

## 핵심 원칙

1. **Dual-Timeframe Analysis**: 전략(Chart 1: 200MA Breadth)과 전술(Chart 2: Uptrend Ratio) 관점을 결합
2. **Backtested Strategy Focus**: 과거 패턴에서 검증된 체계적 전략 적용
3. **Objective Signal Identification**: 명확히 정의된 임계값, 전환, 마커 중심 분석
4. **English Communication**: 모든 분석과 보고서는 영어로 수행
5. **Actionable Recommendations**: 투자자 유형별 구체적인 포지셔닝 가이드 제공

## 차트 유형과 목적

### Chart 1: S&P 500 Breadth Index (200-Day MA Based)

**목적**: 중장기 전략 시장 포지셔닝

**핵심 요소**:
- **8-Day MA (Orange Line)**: 단기 breadth 추세, 주요 진입 신호 생성기
- **200-Day MA (Green Line)**: 장기 breadth 추세, 주요 청산 신호 생성기
- **Red Dashed Line (73%)**: 평균 고점 레벨 - 시장 과열 임계값
- **Blue Dashed Line (23%)**: 평균 8MA 저점 레벨 - 극단적 과매도, 우수한 매수 기회
- **Triangles**:
  - Purple ▼ = 8MA trough (반전 시 매수 신호)
  - Blue ▼ = 200MA trough (메이저 사이클 저점)
  - Red ▲ = 200MA peak (매도 신호)
- **Pink Background**: 하락 추세 구간

**Backtested Strategy**:
- **BUY**: 8MA가 trough에서 반전할 때(특히 23% 이하)
- **SELL**: 200MA가 peak를 형성할 때(일반적으로 73% 부근/이상)
- **결과**: 역사적으로 높은 성과, bear market 회피

### Chart 2: US Stock Market - Uptrend Stock Ratio

**목적**: 단기 전술 타이밍 및 swing trading

**핵심 요소**:
- **Uptrend Stock 정의**: 200MA/50MA/20MA 위에 있고 1개월 성과가 양(+)인 종목
- **Green Regions**: 시장 uptrend 국면
- **Red Regions**: 시장 downtrend 국면
- **~10% Level (Lower Orange Dashed)**: 단기 바닥, 극단적 과매도
- **~40% Level (Upper Orange Dashed)**: 단기 천장, 시장 과열

**Swing Trading Strategy**:
- **ENTER LONG**: 색이 red에서 green으로 바뀔 때(특히 <10-15% 구간)
- **EXIT LONG**: 색이 green에서 red로 바뀔 때(특히 >35-40% 구간)
- **타임프레임**: 수일~수주

## 분석 워크플로

### Step 1: 차트 이미지 수신 및 분석 준비

사용자가 breadth 차트 이미지를 제공하면:

1. 차트 이미지 수신 확인
2. 제공된 차트 유형 식별:
   - Chart 1 only (200MA Breadth)
   - Chart 2 only (Uptrend Ratio)
   - Both charts
3. 사용자 요청의 초점 영역/질문 기록
4. 체계적 분석 진행

**언어 참고**: 이후 모든 사고/분석/출력은 영어로 수행됩니다.

### Step 2: Breadth 차트 방법론 로드

분석 시작 전에 종합 방법론 문서를 읽습니다:

```
Read: references/breadth_chart_methodology.md
```

이 참고 문서에는 다음이 포함됩니다:
- Chart 1: 200MA 기반 breadth index 해석 및 전략
- Chart 2: uptrend stock ratio 해석 및 전략
- 신호 식별 및 임계값 의미
- 전략 규칙 및 risk management
- 두 차트 결합 의사결정
- 피해야 할 일반적인 실수

### Step 3: 샘플 차트 검토 (최초 또는 참고용)

차트 형식과 시각 요소를 이해하기 위해 포함된 샘플 차트를 확인합니다:

``` 
View: assets/SP500_Breadth_Index_200MA_8MA.jpeg
View: assets/US_Stock_Market_Uptrend_Ratio.jpeg
```

샘플 차트가 보여주는 내용:
- 각 차트 유형의 시각적 구조
- 신호와 임계값 표시 방식
- 색상 코딩 및 마커 체계
- 과거 패턴과 사이클

### Step 4: Chart 1 분석 (200MA-Based Breadth Index)

Chart 1이 제공된 경우 체계적으로 분석합니다.

#### 4.1 현재 수치 추출

차트 이미지에서 다음을 식별합니다:
- **현재 8MA 레벨** (orange line): 구체적 퍼센트
- **현재 200MA 레벨** (green line): 구체적 퍼센트
- **8MA 기울기**: 상승/하락/횡보
- **200MA 기울기**: 상승/하락/횡보
- **73% 임계값과의 거리**: 과열에 얼마나 근접했는지
- **23% 임계값과의 거리**: 극단적 과매도에 얼마나 근접했는지
- 차트에서 보이는 **최신 날짜**

#### 4.1.5 중요: 최신 데이터 포인트 상세 추세 분석

**이 단계는 최근 추세 변화를 오독하지 않기 위해 필수입니다.**

**중요 경고**: 차트는 오해를 유발할 수 있습니다. 분석 오류의 대부분은 다음 원인에서 발생합니다:
1. 8MA(orange)와 200MA(green)를 혼동
2. 가장 오른쪽의 CURRENT 데이터 포인트가 아니라 과거 추세를 읽음
3. 어느 선이 상승 중인지/하락 중인지 잘못 식별

**추세 방향을 분석하기 전에 먼저 선 색상을 확인하세요**:
- ✓ **8MA = ORANGE 선** (더 빠르게 움직이고 변동성이 큼)
- ✓ **200MA = GREEN 선** (더 느리고 부드러움)
- 어떤 선이 무엇인지 확신이 없으면 멈추고 차트 범례/색상을 다시 확인

차트의 **가장 오른쪽 3-5개 데이터 포인트**(최근 주차)에 집중합니다.

**8MA (Orange Line) - 최신 궤적 분석**:
1. **절대 최신 위치 식별**: 차트 맨 오른쪽에서 8MA가 어디에 있는가?
2. **3-5개 데이터 포인트 역추적** (약 3-5주):
   - 1주 전 8MA 레벨은?
   - 2주 전 8MA 레벨은?
   - 3주 전 8MA 레벨은?
3. **방향 변화 계산**:
   - 최신 값이 1주 전보다 HIGHER인가 LOWER인가?
   - 최신 값이 2주 전보다 HIGHER인가 LOWER인가?
   - 추세는 지속 상승/지속 하락/혼합 중 무엇인가?
4. **CURRENT 기울기 판정** (과거 기울기 아님):
   - **Rising**: 최신 값이 직전 2-3포인트보다 높고 상향 곡률
   - **Falling**: 최신 값이 직전 2-3포인트보다 낮고 하향 곡률
   - **Flat**: 최신 값이 이전 값들과 거의 동일(±2-3%)

**반드시 답할 핵심 질문**:
- [ ] 차트 맨 오른쪽에서 8MA가 현재 UP인가 DOWN인가?
- [ ] 최근 trough가 있었다면 8MA가 상승을 **유지**했는가, 아니면 다시 꺾였는가?
- [ ] 연속 상승 기간 수: 8MA가 몇 기간 연속 상승했는가? (확인엔 2-3기간 필요)
- [ ] 연속 하락 기간 수: 8MA가 몇 기간 연속 하락했는가? (trough 이후 하락이면 failed reversal 신호)

**200MA (Green Line) - 최신 궤적 분석**:
1. **절대 최신 위치 식별**: 맨 오른쪽에서 200MA 위치는?
2. **4-6주 역추적**:
   - 2주 전 200MA 레벨은?
   - 4주 전 200MA 레벨은?
3. **CURRENT 기울기 판정**:
   - 최신 구간에서 상승/하락/횡보 중 무엇인가?

**Failed Reversal 탐지 (중요)**:
최근 8MA trough(purple ▼)가 식별되었다면:
- [ ] 8MA가 1-2기간만 올랐다가 다시 하락했는가?
- [ ] 8MA가 60%에 도달하기 전에 하락 전환했는가?
- [ ] 반등 후 현재 8MA가 다시 하락 중인가?
- **하나라도 YES면**: **FAILED REVERSAL** - 진입 금지, 신호 무효

**예시 분석 형식**:
```
Latest 8MA Data Points (rightmost to left):
- Current (Week 0): 48%
- 1 week ago: 52%
- 2 weeks ago: 55%
- 3 weeks ago: 50%

Analysis: 8MA is FALLING. It rose from 50% to 55% (weeks 3-2), but has since declined to 48%.
This shows a failed reversal pattern - bounce was temporary, downtrend has resumed.
SLOPE: Falling (not rising!)
```

**필수 교차 점검** (오독 방지):
추세를 판단한 뒤 다음을 자문하세요:
- [ ] "내가 8MA가 RISING이라고 결론냈는데 실제로 몇 주째 FALLING이라면, 차트에서 어떻게 보여야 하는가?"
  - 답: 가장 오른쪽 데이터 포인트가 이전보다 낮아야 함(즉 FALLING 확인)
- [ ] "내 분석이 가장 오른쪽 orange 선의 시각적 기울기와 일치하는가?"
  - 오른쪽 끝에서 orange 선이 시각적으로 아래로 기울면 → FALLING
  - 오른쪽 끝에서 orange 선이 시각적으로 위로 기울면 → RISING
- [ ] "가장 오른쪽 근처에 pink background 음영(하락 추세)이 있는가?"
  - YES라면 → 하락 추세 조건을 확인하는 신호이며, 8MA가 FALLING일 가능성이 높음
- [ ] "8MA와 200MA가 수렴(가까워짐) 중인가, 발산(멀어짐) 중인가?"
  - 아래에서 수렴 → death cross 형성 가능성 → BEARISH
  - 위에서 수렴 → golden cross 형성 가능성 → BULLISH

#### 4.2 신호 마커 식별

다음을 찾고 기록합니다:
- **가장 최근 8MA trough (purple ▼)**: 날짜와 레벨
- **가장 최근 200MA trough (blue ▼)**: 날짜와 레벨(해당 기간에 보이면)
- **가장 최근 200MA peak (red ▲)**: 날짜와 레벨
- **최근 신호 이후 경과 일/주**
- **pink background 음영 여부** (하락 추세 구간)

#### 4.3 시장 국면 평가

수치와 패턴을 바탕으로 현재 시장을 분류합니다:
- Healthy Bull Market
- Overheated Bull Market
- Market Top/Distribution Phase
- Bear Market/Correction
- Capitulation/Extreme Oversold
- Early Recovery

차트의 구체적 증거로 분류를 뒷받침합니다.

#### 4.4 전략 포지션 결정

백테스트 전략 규칙을 **엄격한 확인 요건**과 함께 적용합니다.

**BUY 신호 점검** (모든 조건 충족 필요):
1. ✓ **Trough Formation**: 8MA가 명확한 trough(purple ▼)를 만들었는가?
2. ✓ **Reversal Initiated**: 8MA가 trough에서 상승하기 시작했는가?
3. ✓ **Confirmation Achieved**: trough 이후 2-3기간 연속 상승했는가?
4. ✓ **No Recent Reversal**: Step 4.1.5 기준, 현재 8MA가 상승 중인가(하락 아님)?
5. ✓ **Sustained Move**: 상승 궤적을 꺾이지 않고 유지했는가?
6. ⭐ **선택적 강한 조건**: trough 시점 8MA가 23% 이하/근처인가?

**BUY Signal Status**:
- **CONFIRMED**: 필수 5조건 충족 → ENTER LONG
- **DEVELOPING**: trough 형성, 연속 상승 < 2-3기간 → WAIT, MONITOR
- **FAILED**: trough 형성 후 8MA 재하락 → DO NOT ENTER, 다음 trough 대기
- **NO SIGNAL**: trough 미형성 → WAIT

**SELL 신호 점검**:
- 200MA가 peak(red ▲)를 형성했는가?
- 200MA가 73% 근처/이상인가?
- 포지션 청산이 필요한 활성 매도 신호인가?

**현재 포지션 판단**:
- **Long**: BUY 신호 확인, 진입/보유 상태
- **Preparing to Enter**: BUY 신호 형성 중(확인 대기)
- **WAIT / Flat**: 유효 신호 없음 또는 failed reversal 감지
- **Preparing to Exit**: SELL 신호 형성 중(200MA peak 접근)

#### 4.5 시나리오 구성

확률 추정과 함께 2-3개 시나리오를 작성합니다:
- Base case 시나리오(최고 확률)
- 대안 시나리오
- 각 시나리오 포함 항목: 설명, 근거 요인, 전략 함의, 핵심 레벨

### Step 5: Chart 2 분석 (Uptrend Stock Ratio)

Chart 2가 제공된 경우 체계적으로 분석합니다.

#### 5.1 현재 수치 추출

차트 이미지에서 다음을 식별합니다:
- **현재 uptrend stock ratio**: 구체적 퍼센트
- **현재 색상**: Green(uptrend) 또는 Red(downtrend)
- **ratio 기울기**: 상승/하락/횡보
- **10% 임계값과의 거리**: 극단적 과매도 근접도
- **40% 임계값과의 거리**: 과매수 근접도
- 차트에 보이는 **최신 날짜**

#### 5.2 추세 전환 식별

다음을 찾고 기록합니다:
- **가장 최근 red-to-green 전환**: 전환 시 날짜 및 ratio 레벨
- **가장 최근 green-to-red 전환**: 전환 시 날짜 및 ratio 레벨
- **현재 색상 구간 지속 기간**: 현재 추세가 지속된 기간
- **최근 전환 이후 경과 일/주**

#### 5.3 시장 상태 평가

현재 ratio와 색상을 기반으로 분류합니다:
- Extreme Oversold (<10%)
- Moderate Bearish (10-20%, red)
- Neutral/Transitional (20-30%)
- Moderate Bullish (30-37%, green)
- Extreme Overbought (>37-40%)

차트의 구체적 증거로 분류를 뒷받침합니다.

#### 5.4 트레이딩 포지션 결정

swing trading 전략 규칙을 적용합니다.

**ENTER LONG 신호 점검**:
- 색이 red에서 green으로 전환되었는가?
- 전환이 과매도(<15%) 레벨에서 시작되었는가?
- 전환이 확인되었는가(2-3일 green 지속)?

**EXIT LONG 신호 점검**:
- 색이 green에서 red로 전환되었는가?
- 전환이 과매수(>35%) 레벨에서 시작되었는가?
- 모멘텀이 약화되는가?

**현재 포지션**: Long, Flat, Preparing to Enter, 또는 Preparing to Exit

#### 5.5 시나리오 구성

확률 추정과 함께 2-3개 시나리오를 작성합니다:
- Base case 시나리오(최고 확률)
- 대안 시나리오
- 각 시나리오 포함 항목: 설명, 근거 요인, 트레이딩 함의, 핵심 레벨

### Step 6: 결합 분석 (두 차트 모두 제공 시)

두 차트가 모두 제공되면 전략/전술 관점을 통합합니다.

#### 6.1 정렬(Alignment) 평가

포지셔닝 매트릭스를 작성합니다:
- **Chart 1 (Strategic)**: Bullish / Bearish / Neutral + 신호 상태
- **Chart 2 (Tactical)**: Bullish / Bearish / Neutral + 신호 상태
- **Combined Implication**: 두 신호가 정렬/충돌하는 방식

#### 6.2 시나리오 분류

다음 4가지 중 현재 시나리오를 판단합니다.

**Scenario 1: Both Bullish**
- Chart 1: 8MA 상승, 200MA 아직 peak 아님
- Chart 2: Green(uptrend), ratio가 과매도에서 상승
- 함의: 최대로 bullish, 공격적 포지셔닝

**Scenario 2: Strategic Bullish, Tactical Bearish**
- Chart 1: 8MA 상승, 200MA 아직 peak 아님
- Chart 2: Red(downtrend), ratio 하락 또는 높은 수준
- 함의: 핵심 long 포지션 유지, 전술 진입 대기

**Scenario 3: Strategic Bearish, Tactical Bullish**
- Chart 1: 200MA가 peak 형성 또는 하락
- Chart 2: Green(uptrend), ratio 상승
- 함의: 단기 전술 트레이드만, 타이트한 stop

**Scenario 4: Both Bearish**
- Chart 1: 두 MA 모두 하락
- Chart 2: Red(downtrend), ratio 하락
- 함의: 방어적 포지셔닝, 현금 또는 short

#### 6.3 통합 권고

다음 대상별 통합 포지셔닝 가이드를 제공합니다:
- **장기 투자자** (주로 Chart 1 기준)
- **swing trader** (주로 Chart 2 기준)
- **활동적 전술 트레이더** (결합 신호 기준)

차트 간 충돌이 있을 경우 해결 논리를 설명합니다.

### Step 7: 영어 분석 보고서 생성

아래 템플릿 구조를 사용해 종합 markdown 보고서를 생성합니다:

```
Read and use as template: assets/breadth_analysis_template.md
```

**중요**: 모든 분석과 출력은 영어여야 합니다.

보고서 구조는 분석한 차트 유형에 따라 달라집니다.

**Chart 1만 분석 시**:
- Executive Summary
- Chart 1 전체 분석 섹션
- Summary and Conclusion
- Chart 2 및 Combined Analysis 섹션 제외

**Chart 2만 분석 시**:
- Executive Summary
- Chart 2 전체 분석 섹션
- Summary and Conclusion
- Chart 1 및 Combined Analysis 섹션 제외

**두 차트 모두 분석 시**:
- Executive Summary
- Chart 1 전체 분석 섹션
- Chart 2 전체 분석 섹션
- Combined Analysis 섹션(필수)
- Summary and Conclusion

**파일명 규칙**:
- Chart 1 only: `breadth_200ma_analysis_[YYYY-MM-DD].md`
- Chart 2 only: `uptrend_ratio_analysis_[YYYY-MM-DD].md`
- Both charts: `breadth_combined_analysis_[YYYY-MM-DD].md`

### Step 8: 품질 보증

보고서 확정 전 아래를 점검합니다:

1. ✓ **Language**: 모든 내용이 영어인지(사고/출력)
2. ✓ **선 색상 검증**: 추세 분석 전 8MA = ORANGE, 200MA = GREEN을 명시적으로 확인했는지
3. ✓ **최신 데이터 추세 분석**: Step 4.1.5를 충분히 수행했는지 - 최근 3-5개 데이터 포인트로 CURRENT 추세 방향 판단
4. ✓ **추세 방향 정확성**: 명시한 8MA 기울기(Rising/Falling/Flat)가 과거 움직임이 아니라 RIGHTMOST 데이터 포인트를 반영하는지
5. ✓ **교차 점검 완료**: 필수 교차 점검 질문을 통해 시각적 기울기와 추세 판정이 일치하는지 확인했는지
6. ✓ **Death/Golden Cross 점검**: 8MA와 200MA가 수렴 중일 때 death cross/golden cross 형성 여부를 명확히 식별했는지
7. ✓ **Failed Reversal 점검**: trough 식별 시 최신 궤적으로 반전 유지/실패를 명시적으로 검증했는지
8. ✓ **구체 수치 제시**: 모든 수치가 구체적 퍼센트/레벨인지
9. ✓ **시그널 상태 명확화**: 활성 신호(CONFIRMED BUY / DEVELOPING / FAILED / SELL / WAIT)를 명확히 식별했는지
10. ✓ **전략 정합성**: 권고가 백테스트 전략 및 확인 요건과 정합적인지
11. ✓ **확률 일관성**: 시나리오 확률 합이 100%인지
12. ✓ **실행 가능성**: 트레이더 유형별로 실행 가능한 권고인지
13. ✓ **맥락 제공**: 과거 유사 상황과의 비교가 포함되었는지
14. ✓ **리스크 관리**: 무효화 레벨과 리스크 요인이 명확한지

**최종 상식 점검**:
- [ ] 보고서가 "BUY signal" 또는 "8MA rising"을 주장한다면, 사용자 차트의 death cross/하락 추세와 모순되지 않는지 확인
- [ ] 보고서가 "bullish"를 주장한다면, pink background 음영 또는 death cross가 보이지 않는지 확인
- [ ] 추세 방향에 대해 ANY 항목이라도 불확실하면 추측하지 말고 불확실성을 명시

## 품질 기준

### 객관성 요구사항

- 모든 분석은 관측 가능한 차트 데이터에만 기반
- 특별히 breadth 해석에 필요한 경우가 아니면 외부 정보(뉴스, 펀더멘털) 배제
- 기술 용어를 일관되게 정밀하게 사용
- 사실 관측과 확률 예측을 명확히 구분
- 신호가 모호할 때 불확실성을 명시

### 완결성 요구사항

- 분석 템플릿의 관련 섹션을 모두 다룰 것
- 핵심 메트릭은 모두 구체적 수치로 제시
- 확률 추정은 기술적 근거로 정당화
- 각 시나리오의 무효화 레벨 포함
- 현재 수치를 차트의 과거 패턴과 비교

### 명확성 요구사항

- 전문적이고 분석적인 영어로 작성
- 명확한 섹션 헤딩과 구조 사용
- 필요한 경우 표로 정보 제시
- 권고는 구체적이고 실행 가능해야 함
- 설명 없는 jargon 사용 지양

### 전략 준수 요구사항

- 백테스트 전략 규칙을 정확히 적용
- 전략(Chart 1)과 전술(Chart 2) 신호를 구분
- 포지션 상태(Long/Flat/Entering/Exiting)를 명확히 제시
- 해당 시 구체적 진입/청산 레벨 포함
- risk management(stop loss, 포지션 사이징) 반영

## 사용 예시 시나리오

### Example 1: 전략 Breadth 분석 (Chart 1만)

```
User: "Please analyze this S&P 500 breadth chart and tell me where we are in the market cycle."
[Provides Chart 1 image: 200MA Breadth Index]

Breadth Analyst (thinking in English):
1. Confirms receipt of Chart 1 (200MA-based breadth index)
2. Reads breadth_chart_methodology.md for Chart 1 guidance
3. Views sample chart for format reference
4. Extracts current readings:
   - 8MA: 68%
   - 200MA: 75%
   - 8MA slope: Flat to slightly declining
   - 200MA slope: Rising but may be forming peak
   - Distance from 73% threshold: +2% (above threshold = overheated)
5. Identifies signals:
   - Most recent 8MA trough: 3 months ago at 25%
   - Most recent 200MA peak: None visible yet, but 200MA at 75% suggests potential peak forming
6. Assesses regime: Overheated Bull Market approaching Distribution Phase
7. Determines strategy position: Long position should prepare to exit; watch for 200MA peak confirmation
8. Develops scenarios:
   - Base Case (55%): 200MA forms peak in next 1-2 weeks, sell signal activates
   - Alternative (35%): Further consolidation at elevated levels before eventual peak
   - Bear Case (10%): Immediate rollover without clear peak formation
9. Generates comprehensive report in English: breadth_200ma_analysis_2025-11-02.md
```

### Example 2: 전술 Uptrend Ratio 분석 (Chart 2만)

```
User: "Should I be buying or selling here? Analyze this uptrend ratio chart."
[Provides Chart 2 image: Uptrend Stock Ratio]

Breadth Analyst (thinking in English):
1. Confirms receipt of Chart 2 (Uptrend stock ratio)
2. Reads breadth_chart_methodology.md for Chart 2 guidance
3. Views sample chart for format reference
4. Extracts current readings:
   - Current ratio: 12%
   - Current color: Green (uptrend)
   - Ratio slope: Rising sharply
   - Just transitioned from red to green 3 days ago at 11%
5. Identifies transitions:
   - Most recent red-to-green: 3 days ago at 11% (from extreme oversold)
   - Prior green-to-red: 2 weeks ago at 28%
6. Assesses condition: Early in new uptrend from extreme oversold
7. Determines trading position: ENTER LONG signal active, excellent risk/reward
8. Develops scenarios:
   - Base Case (65%): Ratio continues higher to 30-35% over next 2-3 weeks
   - Alternative (25%): Choppy advance, consolidates around 20% before next leg
   - Bear Case (10%): False breakout, returns to red quickly
9. Generates tactical report in English: uptrend_ratio_analysis_2025-11-02.md
```

### Example 3: 결합 전략+전술 분석 (두 차트)

```
User: "Analyze both of these breadth charts and give me your overall market view."
[Provides both Chart 1 and Chart 2 images]

Breadth Analyst (thinking in English):
1. Confirms receipt of both charts
2. Reads full breadth_chart_methodology.md
3. Views both sample charts
4. Analyzes Chart 1:
   - 8MA: 55%, rising from trough 2 weeks ago at 30%
   - 200MA: 60%, still rising
   - Regime: Early Recovery to Healthy Bull Market
   - Strategy: Long position, hold
5. Analyzes Chart 2:
   - Ratio: 22%, green (uptrend)
   - Transitioned red-to-green 10 days ago from 14%
   - Condition: Moderate Bullish, building momentum
   - Trading: Hold long, entered on transition
6. Combined assessment:
   - Scenario 1: Both Bullish ✓
   - Strategic: Bullish (8MA reversal confirmed)
   - Tactical: Bullish (uptrend established from oversold)
   - Alignment: Strong alignment = Maximum conviction
7. Unified recommendation:
   - Long-term investors: Aggressive long positioning, core holdings
   - Swing traders: Hold longs entered on red-to-green, target 35%+
   - Active traders: Full position, favorable environment for longs
8. Develops integrated scenarios with probabilities
9. Generates comprehensive combined report in English: breadth_combined_analysis_2025-11-02.md
```

## 자주 발생하는 분석 오류와 예방법

### 오류 1: 8MA와 200MA 혼동

**증상**: 실제로는 200MA가 오르는 상황인데 보고서가 8MA 상승으로 잘못 판단

**예방법**:
- ALWAYS verify: 8MA = ORANGE, 200MA = GREEN
- 선의 변동성 점검: 8MA는 더 빠르고 변동성이 큼
- 확신이 없으면 다음처럼 명시: "선 색상을 기준으로 [orange/green] 선을 [8MA/200MA]로 식별했습니다."

### 오류 2: 현재 방향 대신 과거 추세를 읽음

**증상**: 지금의 움직임이 아니라 1-2개월 전 상황을 중심으로 서술

**예방법**:
- 가장 오른쪽 3-5개 데이터 포인트에만 집중
- 다음 문장을 명시적으로 작성: "CURRENT 오른쪽 끝에서 8MA는 X%이며 [rising/falling]입니다."
- 11월 분석이라면 9월의 움직임에 과도하게 끌려가지 않기

### 오류 3: Death Cross 또는 Golden Cross 형성 누락

**증상**: 8MA와 200MA가 death cross 직전(약세)인데도 강세로 판단

**예방법**:
- 항상 점검: "8MA와 200MA가 수렴(converging)하는가, 발산(diverging)하는가?"
- 8MA가 200MA 위에서 수렴 → death cross 가능성 → BEARISH
- 8MA가 200MA 아래에서 수렴 → golden cross 가능성 → BULLISH
- 다음을 명시적으로 기재: "현재 8MA는 200MA [above/below]에 있고, 두 선은 [converging/diverging] 중입니다."

### 오류 4: Pink Background 음영 무시

**증상**: 차트에 pink 하락 추세 배경이 보이는데도 강세 셋업으로 판단

**예방법**:
- 가장 오른쪽 영역의 pink 음영 유무 확인
- pink background = 하락 추세 구간 = 약세 조건
- pink 음영이 보이면 보고서에서 반드시 약세 조건을 언급

### 오류 5: 반전 시그널을 너무 일찍 확정

**증상**: 1주 상승만으로 "BUY signal confirmed"라고 결론

**예방법**:
- 확인에는 8MA 2-3주 CONSECUTIVE 상승이 필요
- 1주 상승만이면 "CONFIRMED"가 아니라 "DEVELOPING"
- 8MA가 올랐다가 다시 하락하면 신호는 "FAILED"로 처리

## 리소스

이 스킬에는 다음 리소스가 포함됩니다.

### references/breadth_chart_methodology.md

다음을 다루는 종합 방법론:
- **Chart 1 (200MA Breadth)**: 구성요소, 해석, 시장 국면, 백테스트 전략, 분석 체크리스트
- **Chart 2 (Uptrend Ratio)**: 구성요소, 해석, 시장 상태, swing trading 전략, 분석 체크리스트
- **Combined Analysis**: 정렬 시나리오, 통합 의사결정
- **Common Pitfalls**: 차트 유형별로 피해야 할 실수

**사용법**: breadth 차트 분석 전 이 파일을 읽어 체계적이고 정확한 해석을 보장합니다.

### assets/breadth_analysis_template.md

영어 breadth 분석 보고서용 구조화 템플릿:
- Executive Summary
- Chart 1 분석 섹션(해당 시)
- Chart 2 분석 섹션(해당 시)
- Combined Analysis 섹션(두 차트 분석 시)
- Summary and Conclusion
- 모든 섹션에 표/체크리스트/구조화 형식 포함

**사용법**: 모든 분석 보고서에서 이 템플릿 구조를 사용하고, 분석 대상 차트에 따라 섹션을 조정합니다.

### assets/SP500_Breadth_Index_200MA_8MA.jpeg

다음을 보여주는 Chart 1 샘플 이미지:
- 8-day MA(orange), 200-day MA(green) 라인
- 임계값 레벨(73% red dashed, 23% blue dashed)
- 신호 마커(trough/peak triangles)
- pink background 하락 추세 음영
- 2016-2025 과거 패턴

**사용법**: 사용자 차트에서 유사 패턴을 식별할 수 있도록 Chart 1 시각 형식을 이해하는 참고 자료로 사용합니다.

### assets/US_Stock_Market_Uptrend_Ratio.jpeg

다음을 보여주는 Chart 2 샘플 이미지:
- green/red 색상 추세 구간
- y축 uptrend ratio 퍼센트
- 임계값(~10%, ~40% orange dashed lines)
- 단기 모멘텀 패턴
- 2023-2025 과거 패턴

**사용법**: 사용자 차트에서 유사 패턴을 식별할 수 있도록 Chart 2 시각 형식을 이해하는 참고 자료로 사용합니다.

## 특별 참고

### 언어 요구사항

**중요**: 모든 분석, 사고, 출력은 반드시 영어여야 합니다. 포함 항목:
- 내부 분석 및 추론
- 보고서 생성
- 표 및 데이터 제시
- 시나리오 설명
- 권고안

번역하거나 다른 언어를 사용하지 마세요. 사용자는 영어 전용 출력을 기대합니다.

### 전략 초점

이 스킬은 재량 해석보다 백테스트된 체계적 전략을 중시합니다. 항상:
- 문서화된 전략 규칙 적용
- 과거 성과 패턴 참조
- 구체적 진입/청산 기준 제시
- risk management 가이드 포함

### 실전 적용

목표는 실행 가능한 인사이트입니다. 모든 분석은 다음 질문에 답해야 합니다:
- **전략적**: 중기 관점에서 시장에 long/flat/short 중 무엇이어야 하는가?
- **전술적**: 단기적으로 포지션에 진입/청산해야 하는가?
- **타이밍**: 언제, 어떤 레벨에서 행동해야 하는가?
- **리스크**: 어떤 조건에서 관점이 무효화되며 stop은 어디에 둘 것인가?
