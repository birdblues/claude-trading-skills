# Pipeline Interface v1

이 문서는 `trade-strategy-pipeline` Phase I에서 사용하는
`edge-finder-candidate/v1` 계약을 요약합니다.

## 필수 산출물 레이아웃

- `strategies/<candidate_id>/strategy.yaml` (필수)
- `strategies/<candidate_id>/metadata.json` (provenance 추적 권장)
- 폴더 이름 `<candidate_id>`는 `strategy.yaml`의 `id` 필드와 일치해야 함

## `strategy.yaml` 필수 최상위 키

- `id`
- `name`
- `universe`
- `signals`
- `risk`
- `cost_model`
- `validation`
- `promotion_gates`

## Phase I 제약 조건

- `validation.method`는 반드시 `full_sample`
- `validation.oos_ratio`는 생략하거나 `null`
- `risk.risk_per_trade`는 `0 < value <= 0.10` 만족
- `risk.max_positions`는 `>= 1`
- `risk.max_sector_exposure`는 `0 < value <= 1.0` 만족
- `signals.entry.conditions`는 비어 있지 않아야 함
- `signals.exit.stop_loss`는 비어 있지 않아야 함
- `signals.exit`는 `trailing_stop` 또는 `take_profit` 포함 필수

## 지원되는 Entry Family (v1)

- `pivot_breakout` + `vcp_detection` block
- `gap_up_continuation` + `gap_up_detection` block

두 detection block이 모두 존재하면 구현체는 둘을 logical OR로 합칠 수 있습니다.

## 실행 핸드셰이크

실행:

```bash
uv run python -m pipeline.runner.cli \
  --strategy <candidate_id> \
  --data-dir data \
  --output-dir reports/<candidate_id>
```

먼저 dry-run:

```bash
uv run python -m pipeline.runner.cli --strategy <candidate_id> --dry-run
```

최소 machine-readable 출력:

- CLI exit code 기반 `run_status`
- `Promotion gate: PASSED|FAILED` 기반 `gate_status`
- `Report: ...` 기반 `report_path`
