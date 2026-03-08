# Research Ticket Schema

이 schema를 `scripts/export_candidate.py`의 입력으로 사용합니다.

## 필수 필드

- `id`: 고유 ticket 식별자
- `hypothesis_type`: edge library 라벨 중 하나
- `entry_family`: export 대상 (`pivot_breakout` 또는 `gap_up_continuation`)

## 선택 필드

- `name`, `description`
- `mechanism_tag`
- `regime`
- `holding_horizon`
- `universe`, `data`
- `entry`, `exit`
- `risk`, `cost_model`, `promotion_gates`
- `detection.vcp_detection` 또는 `detection.gap_up_detection`
- `strategy_overrides`

## 최소 예시 (pivot breakout)

```yaml
id: edge_vcp_breakout_v1
hypothesis_type: breakout
entry_family: pivot_breakout
name: VCP Breakout Candidate v1
description: Relative strength leaders breaking above pivot with volume.
mechanism_tag: behavior
regime: RiskOn
holding_horizon: 20D
```

## 최소 예시 (gap continuation)

```yaml
id: edge_gap_followthrough_v1
hypothesis_type: earnings_drift
entry_family: gap_up_continuation
name: Gap-Up Continuation Candidate v1
description: Earnings gap-up with follow-through above gap-day high.
mechanism_tag: structure
regime: Neutral
holding_horizon: 20D
```

## Export 규칙

Phase I 호환성을 유지하세요:

- `validation.method`를 `walk_forward`로 설정하지 말 것
- `validation.oos_ratio`를 설정하지 말 것
