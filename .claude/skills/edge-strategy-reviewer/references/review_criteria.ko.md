# Strategy Draft Review Criteria

각 strategy draft에는 8개 기준(C1-C8)을 적용합니다.
각 기준은 점수(0-100), severity 레벨, 선택적 revision instruction을 생성합니다.

## Severity 레벨

- **pass**: 점수 >= 60, 이슈 없음
- **warn**: 점수 30-59, 수정 권장되는 경미한 우려
- **fail**: 점수 < 30, 반드시 해결해야 하는 치명적 이슈

## Verdict 로직

1. C1 또는 C2 severity가 "fail"이면 즉시 REJECT
2. 모든 기준에 대해 가중 confidence_score 계산
3. confidence_score >= 70이고 "fail" finding이 없으면 PASS
4. confidence_score < 35이면 REJECT
5. 그 외는 REVISE (revision instruction 포함)

## C1: Edge Plausibility (Weight: 20)

전략이 일관되고 테스트 가능한 edge hypothesis를 갖는지 평가합니다.

| Condition | Severity | Score |
|-----------|----------|-------|
| thesis is empty or fewer than 5 words | fail | 10 |
| thesis is generic (no causal mechanism described) | warn | 40 |
| thesis contains specific causal reasoning | pass | 80 |

Generic thesis 지표:
"momentum", "reversion", "drift", "earnings", "breakout", "gap", "volume", "sentiment"
같은 도메인 용어 없이 10단어 미만.

## C2: Overfitting Risk (Weight: 20)

실용적인 sample size 대비 entry 조건 복잡도를 평가합니다.

| Condition | Severity | Score |
|-----------|----------|-------|
| conditions + trend_filter total > 12 | fail | 10 |
| conditions + trend_filter total > 10 | warn | 40 |
| conditions + trend_filter total <= 10 | pass | 80 |

추가 패널티: 정밀 임계값 1개당 -10
(예: "RSI > 33.5", "volume > 1.73"처럼 소수점 숫자).

패널티 적용 후 최소 점수는 0입니다.

## C3: Sample Adequacy (Weight: 15)

연간 트레이딩 기회를 추정해 지나치게 제한적인 전략을 표시합니다.

추정 공식:
```
base = 252 (trading days)
if sector filter in conditions: base //= 3
if regime is not Neutral/Unknown/empty: base //= 2
base *= 0.8 ^ len(conditions)
base *= 0.85 ^ len(trend_filter)
result = max(base, 1)
```

| Estimated Opportunities | Severity | Score |
|------------------------|----------|-------|
| < 10 per year | fail | 10 |
| < 30 per year | warn | 40 |
| >= 30 per year | pass | 80 |

## C4: Regime Dependency (Weight: 10)

전략이 다양한 market regime를 고려하는지 확인합니다.

| Condition | Severity | Score |
|-----------|----------|-------|
| Single regime with no cross-regime validation plan | warn | 40 |
| Otherwise | pass | 80 |

validation_plan 값 중 하나라도 "regime" 또는 "regimes"
(대소문자 무시)를 언급하면 cross-regime validation이 있다고 봅니다.

## C5: Exit Calibration (Weight: 10)

stop-loss, take-profit 파라미터를 검증합니다.

| Condition | Severity | Score |
|-----------|----------|-------|
| stop_loss_pct > 0.15 | fail | 10 |
| take_profit_rr < 1.5 | fail | 10 |
| Both within range | pass | 80 |

두 fail 조건이 동시에 성립해도 점수는 최소값 10을 사용합니다.

## C6: Risk Concentration (Weight: 10)

position sizing 및 집중도 제한을 평가합니다.

| Condition | Severity | Score |
|-----------|----------|-------|
| risk_per_trade > 0.02 | fail | 10 |
| risk_per_trade > 0.015 | warn | 40 |
| max_positions > 10 | fail | 10 |
| All within range | pass | 80 |

여러 fail 조건이 동시에 있으면 가장 낮은 점수를 사용합니다.

## C7: Execution Realism (Weight: 10)

실전 집행 가능성 관련 우려를 점검합니다.

| Condition | Severity | Score |
|-----------|----------|-------|
| No volume filter in conditions | warn | 50 |
| export_ready_v1=true but entry_family not in EXPORTABLE_FAMILIES | fail | 10 |
| Otherwise | pass | 80 |

EXPORTABLE_FAMILIES = {"pivot_breakout", "gap_up_continuation"}

두 조건이 모두 트리거되면 더 낮은 점수/심각도를 적용합니다.

## C8: Invalidation Quality (Weight: 5)

invalidation signal 품질을 평가합니다.

| Condition | Severity | Score |
|-----------|----------|-------|
| invalidation_signals is empty | fail | 10 |
| invalidation_signals has fewer than 2 entries | warn | 40 |
| 2 or more entries | pass | 80 |

## 가중치 요약

| Criterion | Weight |
|-----------|--------|
| C1 Edge Plausibility | 20 |
| C2 Overfitting Risk | 20 |
| C3 Sample Adequacy | 15 |
| C4 Regime Dependency | 10 |
| C5 Exit Calibration | 10 |
| C6 Risk Concentration | 10 |
| C7 Execution Realism | 10 |
| C8 Invalidation Quality | 5 |
| **Total** | **100** |
