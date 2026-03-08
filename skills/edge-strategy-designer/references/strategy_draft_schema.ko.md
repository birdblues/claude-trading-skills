# Strategy Draft Schema

`design_strategy_drafts.py`는 concept variant마다 YAML 한 개를 생성합니다.

```yaml
id: draft_edge_concept_breakout_behavior_riskon_core
as_of: "2026-02-20"
concept_id: edge_concept_breakout_behavior_riskon
variant: core
risk_profile: balanced
name: Participation-backed trend breakout (core)
hypothesis_type: breakout
mechanism_tag: behavior
regime: RiskOn
export_ready_v1: true
entry_family: pivot_breakout
entry:
  conditions:
    - close > high20_prev
    - rel_volume >= 1.5
  trend_filter:
    - price > sma_200
exit:
  stop_loss_pct: 0.07
  take_profit_rr: 3.0
  time_stop_days: 20
risk:
  position_sizing: fixed_risk
  risk_per_trade: 0.01
  max_positions: 5
validation_plan:
  period: 2016-01-01 to latest
  hold_days: [5, 20, 60]
  success_criteria:
    - expected_value_after_costs > 0
```

`sizing/limits` 결정의 추적성을 위해 각 draft에 `risk_profile`이 저장됩니다.

## Export Ticket 출력 (선택)

`--exportable-tickets-dir`가 제공되면 export-ready draft는
`skills/edge-candidate-agent/scripts/export_candidate.py`와 호환되는 최소 ticket YAML 파일을 생성합니다.
