---
name: edge-candidate-agent
description: 일일 EOD 관측값으로부터 미국 주식 롱 전략용 edge 리서치 티켓을 생성·우선순위화하고, trade-strategy-pipeline Phase I에 바로 투입 가능한 후보 스펙으로 내보냅니다. 가설/이상징후를 재현 가능한 리서치 티켓으로 전환하거나, 검증된 아이디어를 `strategy.yaml` + `metadata.json`으로 변환하거나, 파이프라인 백테스트 전 인터페이스 호환성(`edge-finder-candidate/v1`) 사전 점검이 필요할 때 사용합니다.
---

# Edge Candidate Agent

## 개요

일일 시장 관측값을 재현 가능한 리서치 티켓과 Phase I 호환 후보 스펙으로 변환합니다.
공격적인 전략 확장보다 시그널 품질과 인터페이스 호환성을 우선합니다.
이 스킬은 단독으로 end-to-end 실행 가능하지만, 분리 워크플로에서는 주로 최종 export/validation 단계에 사용됩니다.

## 사용 시점

- 시장 관측, 이상징후, 가설을 구조화된 리서치 티켓으로 변환해야 할 때
- EOD OHLCV와 선택적 힌트를 기반으로 일일 자동 탐지로 새 edge 후보를 찾고 싶을 때
- 검증된 티켓을 `trade-strategy-pipeline` Phase I용 `strategy.yaml` + `metadata.json`으로 export할 때
- 파이프라인 실행 전에 `edge-finder-candidate/v1` 사전 호환성 점검이 필요할 때

## 사전 요구사항

- `PyYAML`이 설치된 Python 3.9+
- schema/stage 검증을 위해 대상 `trade-strategy-pipeline` 저장소 접근 가능
- `--pipeline-root` 기반 파이프라인 관리 검증 시 `uv` 사용 가능

## 출력물

- `strategies/<candidate_id>/strategy.yaml`: Phase I 호환 전략 스펙
- `strategies/<candidate_id>/metadata.json`: 인터페이스 버전/티켓 컨텍스트를 포함한 provenance metadata
- `scripts/validate_candidate.py` 검증 상태 (pass/fail + 사유)
- 일일 탐지 산출물:
  - `daily_report.md`
  - `market_summary.json`
  - `anomalies.json`
  - `watchlist.csv`
  - `tickets/exportable/*.yaml`
  - `tickets/research_only/*.yaml`

## 분리 워크플로에서의 위치

권장 분리 워크플로:

1. `skills/edge-hint-extractor`: observations/news -> `hints.yaml`
2. `skills/edge-concept-synthesizer`: tickets/hints -> `edge_concepts.yaml`
3. `skills/edge-strategy-designer`: concepts -> `strategy_drafts` + exportable ticket YAML
4. `skills/edge-candidate-agent` (이 스킬): export + validate 후 pipeline handoff

## 워크플로

1. EOD OHLCV에서 자동 탐지 실행:
   - `skills/edge-candidate-agent/scripts/auto_detect_candidates.py`
   - 선택: 사람 아이데이션 입력용 `--hints`
   - 선택: 외부 LLM ideation loop용 `--llm-ideas-cmd`
2. 계약/매핑 참고 문서 로드:
   - `references/pipeline_if_v1.md`
   - `references/signal_mapping.md`
   - `references/research_ticket_schema.md`
   - `references/ideation_loop.md`
3. `references/research_ticket_schema.md`를 사용해 리서치 티켓을 생성 또는 업데이트
4. `skills/edge-candidate-agent/scripts/export_candidate.py`로 후보 산출물 export
5. `skills/edge-candidate-agent/scripts/validate_candidate.py`로 인터페이스 및 Phase I 제약 검증
6. 후보 디렉터리를 `trade-strategy-pipeline`으로 handoff하고 먼저 dry-run 실행

## 빠른 명령

일일 자동 탐지 (선택적으로 export/validation 포함):

```bash
python3 skills/edge-candidate-agent/scripts/auto_detect_candidates.py \
  --ohlcv /path/to/ohlcv.parquet \
  --output-dir reports/edge_candidate_auto \
  --top-n 10 \
  --hints path/to/hints.yaml \
  --export-strategies-dir /path/to/trade-strategy-pipeline/strategies \
  --pipeline-root /path/to/trade-strategy-pipeline
```

티켓에서 candidate 디렉터리 생성:

```bash
python3 skills/edge-candidate-agent/scripts/export_candidate.py \
  --ticket path/to/ticket.yaml \
  --strategies-dir /path/to/trade-strategy-pipeline/strategies
```

인터페이스 계약만 검증:

```bash
python3 skills/edge-candidate-agent/scripts/validate_candidate.py \
  --strategy /path/to/trade-strategy-pipeline/strategies/my_candidate_v1/strategy.yaml
```

인터페이스 계약 + 파이프라인 schema/stage 규칙 동시 검증:

```bash
python3 skills/edge-candidate-agent/scripts/validate_candidate.py \
  --strategy /path/to/trade-strategy-pipeline/strategies/my_candidate_v1/strategy.yaml \
  --pipeline-root /path/to/trade-strategy-pipeline \
  --stage phase1
```

## Export 규칙

- `validation.method: full_sample` 유지
- `validation.oos_ratio`는 생략하거나 `null` 유지
- v1에서 지원되는 entry family만 export:
  - `pivot_breakout` + `vcp_detection`
  - `gap_up_continuation` + `gap_up_detection`
- 미지원 가설 family는 export 후보가 아니라 티켓 메모에서 research-only로 표시

## 가드레일

- schema 범위를 위반하는 후보(risk, exits, 빈 conditions)는 거부
- 폴더 이름과 `id` 불일치 시 후보 거부
- `interface_version: edge-finder-candidate/v1`가 포함된 결정적 metadata 필수
- 전체 실행 전 파이프라인에서 `--dry-run` 필수

## 리소스

### `skills/edge-candidate-agent/scripts/export_candidate.py`
리서치 티켓 YAML에서 `strategies/<candidate_id>/strategy.yaml` 및 `metadata.json` 생성.

### `skills/edge-candidate-agent/scripts/validate_candidate.py`
`trade-strategy-pipeline` 대상 인터페이스 점검 및 선택적 `StrategySpec`/`validate_spec` 검증 수행.

### `skills/edge-candidate-agent/scripts/auto_detect_candidates.py`
EOD OHLCV에서 edge 아이디어를 자동 탐지하고 export/research 티켓을 생성하며, 선택적으로 자동 export/validation까지 수행.

### `references/pipeline_if_v1.md`
`edge-finder-candidate/v1`용 축약 통합 계약 문서.

### `references/signal_mapping.md`
가설 family와 현재 export 가능한 signal family의 매핑.

### `references/research_ticket_schema.md`
`export_candidate.py`가 사용하는 티켓 schema.

### `references/ideation_loop.md`
힌트 schema와 외부 LLM ideation command 계약.
