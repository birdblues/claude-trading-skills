# VCP 방법론 - Minervini의 Volatility Contraction Pattern

## 개요

Volatility Contraction Pattern(VCP)은 미국 투자 챔피언십 2회 우승자인 Mark Minervini가 개발한 패턴입니다. 잠재적 breakout 이전에 점진적으로 더 타이트한 박스권을 형성하는 Stage 2 상승 추세 종목을 식별합니다.

## Stage 분석 기반

### 4단계 (Stan Weinstein / Minervini)

1. **Stage 1 - Accumulation/Basing:** 하락 이후 주가가 횡보합니다. Smart money가 매집합니다.
2. **Stage 2 - Advancing/Uptrend:** 주가가 확인된 상승 추세에 있습니다. VCP는 이 구간에서 형성됩니다. **매수 가능한 유일한 stage입니다.**
3. **Stage 3 - Distribution/Topping:** 상승 이후 주가가 정체됩니다. Smart money가 분산 매도합니다.
4. **Stage 4 - Declining/Downtrend:** 주가가 확인된 하락 추세에 있습니다. 회피 또는 공매도 구간입니다.

### Minervini의 7-Point Trend Template (Stage 2 확인)

종목이 확인된 Stage 2에 있으려면 아래 기준을 모두(또는 대부분) 충족해야 합니다:

| # | Criterion | Purpose |
|---|-----------|---------|
| 1 | Price > 150-day SMA AND Price > 200-day SMA | 주요 추세선 상단 |
| 2 | 150-day SMA > 200-day SMA | 단기 MA가 장기 MA 위(강세 정렬) |
| 3 | 200-day SMA trending up for 22+ trading days | 장기 추세 상승 |
| 4 | Price > 50-day SMA | 중기 추세선 상단 |
| 5 | Price at least 25% above 52-week low | 저점 대비 충분한 거리 |
| 6 | Price within 25% of 52-week high | 깊은 조정 구간 아님 |
| 7 | Relative Strength rating > 70 | 대부분 종목 대비 아웃퍼폼 |

**통과 기준:** VCP 탐지로 진행하려면 7개 중 6개 이상 충족(score >= 85).

## VCP 패턴 메커니즘

### VCP란?

VCP는 Stage 2 상승 추세 종목이 조정 후 반등을 반복하는 과정에서, 각 조정폭이 이전 조정보다 **더 얕아지는**(변동성 축소) 패턴입니다. 이 변동성 축소는 다음을 시사합니다:

1. 매도 압력이 흡수되고 있음
2. 잔존 매도 세력이 소진되고 있음
3. 공급이 마르고 있음
4. breakout 확률이 높아지고 있음

### 수축 구조

```
        H1 (Highest swing high)
       / \
      /   \  T1 (First contraction: deepest)
     /     \
    /       L1
   /       / \
  /       /   \ T2 (Second contraction: tighter)
         H2    \
          \    L2
           \  / \
            \/   \ T3 (Third contraction: tightest)
            H3    L3
             \   /
              \ /  ← PIVOT POINT (buy here on volume)
               P
```

### 수축 규칙

- **T1 (첫 조정):** S&P 500 대형주의 경우 depth 8-35%(소형주는 최대 50%)
- **T2:** T1보다 최소 25% 더 타이트해야 함(ratio <= 0.75)
- **T3:** (있다면) T2보다 최소 25% 더 타이트해야 함
- **T4:** 매우 타이트하며 보통 < 5%(드물지만 매우 강세)
- **최소:** 수축 2회 필요
- **이상적:** 점진적 타이트닝이 있는 3-4회 수축
- **기간:** 전체 패턴 기준 15-325 거래일

### Pivot Point

**pivot**은 마지막 수축의 고점입니다. 이 구간이 매수 지점입니다:

- 가격이 pivot 위로 돌파하고 거래량이 50일 평균 대비 1.5x+일 때 매수
- stop-loss는 마지막 수축 저점 아래 1-2%에 배치
- 진입가 대비 stop까지 종목당 리스크는 5-8% 권장

### 거래량 시그니처

VCP에서 이상적인 거래량 흐름:

1. **조정 구간:** 거래량 감소(매도자 소진)
2. **pivot 근처:** 거래량 dry up(극도로 낮은 거래량, 폭풍 전 고요)
3. **breakout 시점:** 거래량이 50일 평균의 1.5-2x로 급증

**Dry-up ratio** = 평균 거래량(피벗 근처 최근 10개 봉) / 50일 평균 거래량
- < 0.30: Exceptional (textbook)
- 0.30-0.50: Strong
- 0.50-0.70: Adequate
- \> 0.70: Weak (caution)

## 과거 VCP 예시

### 클래식 3-Contraction VCP
- T1: 6주 동안 20% 조정
- T2: 3주 동안 12% 조정(40% 더 타이트)
- T3: 2주 동안 5% 조정(58% 더 타이트)
- 2x 거래량 breakout 후 50%+ 상승

### 타이트한 2-Contraction VCP (Large-Cap)
- T1: 4주 동안 12% 조정
- T2: 2주 동안 5% 조정(58% 더 타이트)
- 1.8x 거래량 breakout 후 25-30% 상승

## 흔한 실수

1. **pivot 이전 매수:** 셋업이 아니라 breakout을 기다릴 것
2. **거래량 무시:** 거래량 없는 breakout은 실패 확률이 높음
3. **넓은 손절:** 손절은 마지막 수축 저점 아래로 타이트하게
4. **잘못된 stage:** VCP는 Stage 2에서만 유효, 먼저 Trend Template로 확인
5. **깊은 T1:** 대형주에서 T1 > 35%면 패턴 신뢰도가 낮아짐
6. **확장형 수축:** T2 > T1이면 VCP가 아님

## VCP 품질별 포지션 사이징

| Rating | Position Size | Risk Budget |
|--------|---------------|-------------|
| Textbook (90+) | 1.5-2x normal | Full |
| Strong (80-89) | 1x normal | Full |
| Good (70-79) | 0.75x normal | Standard |
| Developing (60-69) | Wait/Watch | Reduced |
