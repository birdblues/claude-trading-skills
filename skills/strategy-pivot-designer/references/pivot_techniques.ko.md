# Pivot Techniques

백테스트 반복 루프가 정체될 때 구조적으로 다른 전략 제안을 생성하기 위한 3가지 체계적 기법입니다.

---

## Technique 1: Assumption Inversion

**원칙**: 현재 전략의 핵심 가정을 식별하고, 어떤 정체 트리거가 발생했는지에 따라 그 가정을 뒤집습니다.

### Trigger별 Inversion 규칙

| Trigger | Module | Inversion |
|---------|--------|-----------|
| `cost_defeat` | horizon | 보유 기간 단축 (마찰 비용 노출 감소) |
| `cost_defeat` | universe | 더 높은 유동성 종목으로 이동 (슬리피지 감소) |
| `tail_risk` | risk | 스탑 강화, 포지션 축소, max drawdown cap 추가 |
| `tail_risk` | structure | market-neutral 또는 hedged 접근으로 이동 |
| `improvement_plateau` | signal | 시그널 소스 변경 (price-based → volume/fundamental) |
| `improvement_plateau` | entry | 진입 타이밍 메커니즘 변경 |
| `overfitting_proxy` | complexity | 파라미터 축소, 단순 진입 모델 사용 |
| `overfitting_proxy` | validation | 테스트 기간 확장, regime subsample 추가 |

### 적용 절차

1. diagnosis에서 발생한 trigger를 읽습니다.
2. 해당 inversion 규칙을 조회합니다.
3. 현재 전략의 각 모듈에 inversion을 적용합니다.
4. 뒤집힌 가정으로 새 draft를 생성합니다.

---

## Technique 2: Archetype Switch

**원칙**: 동일한 시장 비효율을 다른 각도에서 공략하는 구조적으로 다른 전략 archetype으로 점프합니다.

### 절차

1. 현재 전략의 `hypothesis_type`, `mechanism_tag`, `entry_family`에서 archetype을 식별합니다.
2. archetype catalog의 `compatible_pivots_from` 매핑에서 호환 pivot target을 찾습니다.
3. 각 호환 target에 대해 target archetype의 기본 모듈로 draft를 생성합니다.
4. 가능한 경우 원래 concept_id와 thesis를 유지합니다.

### Archetype 식별 규칙

| hypothesis_type | mechanism_tag | entry_family | Archetype |
|----------------|---------------|--------------|-----------|
| breakout | behavior | pivot_breakout | trend_following_breakout |
| breakout | structural | pivot_breakout | volatility_contraction |
| mean_reversion | statistical | * | mean_reversion_pullback OR statistical_pairs |
| mean_reversion | information | * | event_driven_fade |
| earnings_drift | information | gap_up_continuation | earnings_drift_pead |
| momentum | behavior | * | sector_rotation_momentum |
| regime | macro | * | regime_conditional_carry |

여러 archetype이 매칭되면 현재 draft와 `entry_family`가 일치하는 쪽을 우선합니다.

---

## Technique 3: Objective Reframe

**원칙**: 전략의 "성공" 정의를 바꿔 최적화 타깃 자체를 전환합니다.

### Reframe 옵션

| Current Objective | Reframed To | Rationale |
|-------------------|-------------|-----------|
| Maximize Sharpe ratio | Minimize max drawdown | tail risk 제어 강화 |
| Maximize expectancy | Maximize win rate | 더 일관된 성과(작지만 빈번한 승리) |
| Maximize total return | Maximize risk-adjusted return per unit exposure | 자본 효율성 중심 |

### 적용

1. 현재 전략의 `validation_plan`에서 `success_criteria`를 읽습니다.
2. trigger에 따라 reframe을 선택합니다:
   - `tail_risk` → drawdown 최소화
   - `cost_defeat` → win rate 최대화 (작은 목표, 타이트한 스탑)
   - `improvement_plateau` → risk-adjusted return (다른 효율 렌즈)
   - `overfitting_proxy` → 더 단순한 기준 (최적화 타깃 축소)
3. 새 objective에 맞게 exit 규칙과 risk 파라미터를 조정합니다.
4. 생성 draft의 `success_criteria`를 업데이트합니다.

---

## Trigger별 Technique 선택

| Trigger | Primary Technique | Secondary Technique |
|---------|-------------------|---------------------|
| `improvement_plateau` | Archetype Switch | Assumption Inversion |
| `overfitting_proxy` | Assumption Inversion | Objective Reframe |
| `cost_defeat` | Assumption Inversion | Archetype Switch |
| `tail_risk` | Assumption Inversion | Objective Reframe |

`generate_pivots` 스크립트는 적용 가능한 모든 기법을 실행하고, scoring으로 최적 후보를 선택합니다.

---

## Scoring

### Quality Potential (0-1)

target archetype이 해당 trigger를 얼마나 잘 해결하는지에 대한 휴리스틱 점수입니다. `QUALITY_TABLE` 딕셔너리의 `(trigger, archetype) → score` 매핑으로 정의됩니다.

### Novelty (0-1)

원본 전략과 제안 pivot의 모듈 집합 간 Jaccard distance:

```
novelty = 1 - |A ∩ B| / |A ∪ B|
```

여기서 A, B는 다음 (key, value) 쌍 집합으로 구성됩니다:
- `("hypothesis_type", <value>)`
- `("mechanism_tag", <value>)`
- `("regime", <value>)`
- `("entry_family", <value>)`
- `("horizon", <"short"|"medium"|"long">)` — time_stop_days ≤ 7: short, ≤ 30: medium, 그 외: long
- `("risk_style", <"tight"|"normal"|"wide">)` — stop_loss_pct ≤ 0.04: tight, ≤ 0.08: normal, 그 외: wide

### Combined Score

```
combined = 0.6 * quality_potential + 0.4 * novelty
```

### Tiebreak 규칙 (deterministic)

1. Combined score 내림차순
2. Novelty 내림차순 (더 새로운 제안 우선)
3. Proposal ID 알파벳 오름차순 (최종 정렬 결정성 확보)

### Diversity 제약

target archetype당 최대 1개 제안만 허용합니다. 여러 technique이 동일 archetype 후보를 만들면 combined score가 가장 높은 제안만 유지합니다.
