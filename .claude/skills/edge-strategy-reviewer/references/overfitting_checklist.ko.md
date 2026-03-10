# Overfitting Detection Checklist

과거 데이터에 과적합되었을 가능성이 높은 strategy draft를 식별하기 위한 heuristic입니다.

## Red Flags

### 1. 과도한 조건 개수

entry 조건이 많을수록 자유도가 줄어들고, signal보다 noise를 설명할 가능성이 커집니다.

- **총 조건 10개 이상** (entry + trend filter): 경고 임계값
- **총 조건 12개 이상**: 거의 확실한 과적합

### 2. 지나치게 정밀한 임계값

소수점 단위 임계값(예: "RSI > 30" 대신 "RSI > 33.5")은
견고한 패턴 포착보다 과거 데이터 curve-fitting을 시사합니다.

탐지 방법: condition 문자열에서 소수점이 포함된 숫자를 찾습니다.

정밀 임계값 예시:
- "RSI > 33.5" (정밀: 소수점 포함)
- "volume > 1.73 * avg" (정밀: 소수점 포함)
- "close > ma50 * 1.025" (정밀: 소수점 포함)

허용 가능한 임계값 예시:
- "RSI > 30" (round number)
- "rel_volume >= 1.5" (half-step, 흔히 사용)
- "close > ma50" (소수 임계값 숫자 없음)

### 3. 좁은 Regime 특이성

단일 market regime(예: RiskOn 전용)만 대상으로 설계되고
다른 regime 검증이 없으면 일반화 성능이 떨어질 수 있습니다.

### 4. 낮은 예상 Sample Size

조건이 너무 제한적이라 연간 기회가 10회 미만이면,
백테스트 결과는 통계적으로 신뢰하기 어렵습니다.

### 5. 비대칭 Exit 파라미터

- 15%를 넘는 stop loss는 극단적 역행을 허용한다는 뜻으로,
  진입 타이밍 부정확 또는 과적합 진입 조건을 시사할 수 있습니다.
- 1.5:1 미만 risk-reward 비율은 수익화를 위해 비현실적으로 높은 승률을 요구합니다.

## 완화 전략

1. 조건 개수를 필수 filter 중심으로 축소
2. 행동적 레벨을 포착하는 round-number 임계값 사용 (예: RSI 30/70, 50-day MA)
3. 여러 regime 및 기간에서 검증
4. 충분한 sample size 확보 (최소 연 30회 이상 기회 권장)
5. stop loss는 10% 이내로, reward-to-risk는 2:1 이상 목표
