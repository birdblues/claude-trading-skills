# Edge Pipeline Flow

## Pipeline 단계

```
OHLCV / Tickets
       |
       v
 [auto_detect] ───> tickets/
       |
       v
 [hints]       ───> hints.yaml
       |
       v
 [concepts]    ───> edge_concepts.yaml
       |
       v
 [drafts]      ───> drafts/*.yaml  +  exportable_tickets/*.yaml
       |
       v
 [review]  <──────────────────────┐
       |                          |
       ├── PASS   → accumulated   |
       ├── REJECT → accumulated   |
       └── REVISE → [revision] ───┘  (max 2 iterations)
                          |
                   remaining REVISE → research_probe downgrade
       |
       v
 [export]      ───> strategies/<candidate_id>/
```

## 단계별 스크립트 매핑

| Stage       | Script Path                                                        |
|-------------|--------------------------------------------------------------------|
| auto_detect | skills/edge-candidate-agent/scripts/auto_detect_candidates.py      |
| hints       | skills/edge-hint-extractor/scripts/build_hints.py                  |
| concepts    | skills/edge-concept-synthesizer/scripts/synthesize_edge_concepts.py |
| drafts      | skills/edge-strategy-designer/scripts/design_strategy_drafts.py    |
| review      | skills/edge-strategy-reviewer/scripts/review_strategy_drafts.py    |
| export      | skills/edge-candidate-agent/scripts/export_candidate.py            |

## Data Contract

### auto_detect 출력 (tickets/)

각 ticket은 최소 다음 필드를 갖는 YAML 파일입니다:
- `id`: 고유 ticket 식별자
- `hypothesis_type`: breakout, earnings_drift 등
- `entry_family`: pivot_breakout, gap_up_continuation, 또는 research_only
- `priority_score`: 0-100 숫자 점수

### hints 출력 (hints.yaml)

```yaml
generated_at_utc: "2026-01-01T00:00:00+00:00"
hints:
  - title: "Breadth-supported breakout regime"
    observation: "..."
    symbols: [AAPL, MSFT]
    regime_bias: "RiskOn"
    mechanism_tag: "behavior"
```

### concepts 출력 (edge_concepts.yaml)

```yaml
concept_count: 3
concepts:
  - id: edge_concept_breakout_behavior_riskon
    hypothesis_type: breakout
    strategy_design:
      recommended_entry_family: pivot_breakout
      export_ready_v1: true
```

### drafts 출력 (drafts/*.yaml)

각 draft YAML 파일은 다음을 포함합니다:
- `id`: draft 식별자 (`draft_<concept_id>_<variant>`)
- `concept_id`: 원본 concept
- `variant`: core, conservative, 또는 research_probe
- `entry_family`: pivot_breakout, gap_up_continuation, 또는 research_only
- `export_ready_v1`: boolean
- `entry.conditions`: 조건 문자열 목록
- `entry.trend_filter`: trend filter 문자열 목록
- `exit`: stop_loss_pct, take_profit_rr
- `risk`: position sizing 파라미터

### review 출력 (reviews/*.yaml)

각 review YAML은 다음을 포함합니다:
- `draft_id`: 대응되는 draft 식별자
- `verdict`: PASS, REVISE, 또는 REJECT
- `revision_instructions`: 문자열 목록 (REVISE verdict용)
- `confidence_score`: 0-100

### export 출력 (strategies/<candidate_id>/)

- `strategy.yaml`: Phase I 호환 strategy specification
- `metadata.json`: provenance 및 연구 컨텍스트

## Export 가능한 Entry Family

trade-strategy-pipeline으로 export 가능한 family는 다음 둘뿐입니다:
- `pivot_breakout`
- `gap_up_continuation`

다른 family(research_only 등)는 research probe로 유지됩니다.
