# Stagnation Triggers

4개의 deterministic trigger가 전략의 백테스트 반복 루프 정체를 감지합니다. 각 trigger는 iteration history에 누적된 `evaluate_backtest.py` 출력 필드에 직접 매핑됩니다.

## 필드 참조 매핑

| Data Point | JSON Path | Type |
|---|---|---|
| total_score | `eval.total_score` | int |
| Expectancy dim score | `eval.dimensions` (lookup by `name == "Expectancy"`) | int |
| Risk Management dim score | `eval.dimensions` (lookup by `name == "Risk Management"`) | int |
| Robustness dim score | `eval.dimensions` (lookup by `name == "Robustness"`) | int |
| red_flag IDs | `[f["id"] for f in eval.red_flags]` | list[str] |
| expectancy | `eval.expectancy` | float |
| profit_factor | `eval.profit_factor` | float |
| slippage_tested | `eval.inputs.slippage_tested` | bool |
| max_drawdown_pct | `eval.inputs.max_drawdown_pct` | float |

**참고**: Dimension 점수는 배열 인덱스가 아니라 `name` 필드로 조회합니다. 이 방식은 향후 dimension 재정렬/추가에도 견고합니다.

---

## Trigger 1: Improvement Plateau

**ID**: `improvement_plateau`
**Severity**: high

**조건**: 최근 K회 반복(default K=3)에서 `total_score` 값 범위가 임계값(default 3)보다 작다.

**근거**: 파라미터를 바꿔도 점수가 움직이지 않으면 전략 아키텍처 자체가 local maximum에 도달한 것입니다.

**증거 필드**:
- `last_k_scores`: 최근 K회 total_score 리스트
- `score_range`: last_k_scores의 max - min
- `threshold`: 설정된 임계값

**최소 반복 수**: K (기본 3). 반복 수가 부족하면 발화 불가.

---

## Trigger 2: Overfitting Proxy

**ID**: `overfitting_proxy`
**Severity**: medium

**조건**: 아래를 모두 만족해야 함:
1. Expectancy dimension score >= 15
2. Risk Management dimension score >= 15
3. Robustness dimension score < 10
4. red_flags ID에 `over_optimized` 또는 `short_test_period` 포함

**근거**: in-sample 성과는 높지만 robustness가 낮고 curve-fitting 경고가 있으면, 진짜 edge가 아니라 과거 노이즈에 최적화되었을 가능성이 큽니다.

**최소 반복 수**: 2 (의미 있는 판단을 위해 최소 이력 필요).

---

## Trigger 3: Cost Defeat

**ID**: `cost_defeat`
**Severity**: medium

**조건**: 아래를 모두 만족해야 함:
1. `eval.expectancy` < 0.3
2. `eval.profit_factor` < 1.3
3. `eval.inputs.slippage_tested` == True

**근거**: expectancy와 profit factor가 얇고 슬리피지가 이미 반영되었다면, 실제 실행 비용을 견딜 edge가 없습니다. 추가 파라미터 튜닝으로 없는 edge를 만들 수는 없습니다.

**최소 반복 수**: 2 (슬리피지 테스트는 최소 1회 개선 사이클을 전제).

---

## Trigger 4: Tail Risk

**ID**: `tail_risk`
**Severity**: high

**조건**: 아래 중 하나:
1. `eval.inputs.max_drawdown_pct` > 35
2. Risk Management dimension score <= 5

**근거**: 극단적 drawdown 또는 매우 낮은 리스크 관리 점수는 파라미터 튜닝만으로 해결할 수 없는 구조적 리스크 문제를 뜻합니다. 리스크 모듈의 아키텍처 변경이 필요합니다.

**최소 반복 수**: 1 (첫 평가에서도 발화 가능 — drawdown이 극단적이면 조기 pivot이 타당).

---

## 권고 결정 테이블

우선순위 순으로 평가 (첫 매칭 우선):

| Priority | Condition | Recommendation |
|----------|-----------|---------------|
| 1 | Latest `total_score` < 30 AND `iterations >= 3` AND score trajectory (last 3) is monotonically non-increasing | `abandon` |
| 2 | `triggers_fired` has at least 1 entry | `pivot` |
| 3 | None of the above | `continue` |

**참고**: `abandon`을 먼저 평가합니다. 이는 특정 trigger 임계값은 넘지 않더라도 점수가 지속적으로 매우 낮은 케이스(예: 25 부근 횡보)를 포착하기 위함입니다.
