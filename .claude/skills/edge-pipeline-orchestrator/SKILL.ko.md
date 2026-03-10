---
name: edge-pipeline-orchestrator
description: candidate 탐지부터 strategy 설계, 리뷰, 수정, export까지 edge 연구 파이프라인 전체를 오케스트레이션합니다. 다단계 edge 연구 워크플로를 end-to-end로 조정할 때 사용하세요.
---

# Edge Pipeline Orchestrator

모든 edge 연구 단계를 하나의 자동화된 파이프라인 실행으로 조정합니다.

## 사용 시점

- tickets(또는 OHLCV)부터 export된 strategy까지 전체 edge pipeline 실행
- drafts 단계부터 부분 완료된 pipeline 재개
- 기존 strategy draft를 feedback loop로 리뷰 및 수정
- export 없이 결과 미리보기를 위한 dry-run 수행

## 워크플로

1. CLI 인자에서 pipeline configuration을 로드합니다.
2. `--from-ohlcv`가 제공되면 auto_detect 단계를 실행합니다
   (원시 OHLCV 데이터에서 tickets 생성).
3. hints 단계를 실행해 market summary와 anomaly에서 edge hints를 추출합니다.
4. concepts 단계를 실행해 tickets와 hints에서 추상 edge concept를 합성합니다.
5. drafts 단계를 실행해 concepts에서 strategy draft를 설계합니다.
6. review-revision feedback loop를 실행합니다:
   - 모든 draft 리뷰(최대 2회 iteration)
   - PASS verdict 누적, REJECT verdict 누적
   - REVISE verdict는 apply_revisions 후 재리뷰
   - 최대 iteration 이후 남은 REVISE는 research_probe로 강등
7. export 대상 draft를 내보냅니다
   (PASS + export_ready_v1 + exportable entry_family).
8. 전체 실행 추적이 담긴 pipeline_run_manifest.json을 기록합니다.

## CLI 사용법

```bash
# tickets에서 전체 pipeline 실행
python3 scripts/orchestrate_edge_pipeline.py \
  --tickets-dir path/to/tickets/ \
  --output-dir reports/edge_pipeline/

# OHLCV에서 전체 pipeline 실행
python3 scripts/orchestrate_edge_pipeline.py \
  --from-ohlcv path/to/ohlcv.csv \
  --output-dir reports/edge_pipeline/

# drafts 단계부터 재개
python3 scripts/orchestrate_edge_pipeline.py \
  --resume-from drafts \
  --drafts-dir path/to/drafts/ \
  --output-dir reports/edge_pipeline/

# review-only 모드
python3 scripts/orchestrate_edge_pipeline.py \
  --review-only \
  --drafts-dir path/to/drafts/ \
  --output-dir reports/edge_pipeline/

# Dry run (export 없음)
python3 scripts/orchestrate_edge_pipeline.py \
  --tickets-dir path/to/tickets/ \
  --output-dir reports/edge_pipeline/ \
  --dry-run
```

## 출력물

모든 아티팩트는 `--output-dir`에 기록됩니다:

```
output-dir/
├── pipeline_run_manifest.json
├── tickets/          (from auto_detect)
├── hints/hints.yaml  (from hints)
├── concepts/edge_concepts.yaml
├── drafts/*.yaml
├── exportable_tickets/*.yaml
├── reviews_iter_0/*.yaml
├── reviews_iter_1/*.yaml  (if needed)
└── strategies/<candidate_id>/
    ├── strategy.yaml
    └── metadata.json
```

## Claude Code LLM-Augmented Workflow

Claude Code 내부에서 LLM-augmented pipeline을 전체 실행합니다:

1. auto_detect를 실행해 `market_summary.json` + `anomalies.json` 생성
2. Claude Code가 데이터를 분석해 edge hints 생성
3. hints를 YAML 파일로 저장:

```yaml
- title: Sector rotation into industrials
  observation: Tech underperforming while industrials show relative strength
  symbols: [CAT, DE, GE]
  regime_bias: Neutral
  mechanism_tag: flow
  preferred_entry_family: pivot_breakout
  hypothesis_type: sector_x_stock
```

4. `--llm-ideas-file` 및 `--promote-hints`와 함께 orchestrator 실행:

```bash
python3 scripts/orchestrate_edge_pipeline.py \
  --tickets-dir path/to/tickets/ \
  --llm-ideas-file llm_hints.yaml \
  --promote-hints \
  --as-of 2026-02-28 \
  --max-synthetic-ratio 1.5 \
  --strict-export \
  --output-dir reports/edge_pipeline/
```

### Optional Flags

- `--as-of YYYY-MM-DD` — 날짜 필터링을 위해 hints 단계로 전달
- `--strict-export` — warn finding이 하나라도 있으면 PASS 대신 REVISE 처리
- `--max-synthetic-ratio N` — synthetic ticket 수를 실제 ticket 수의 N배로 제한 (최소치: 3)
- `--overlap-threshold F` — concept 중복 제거용 조건 overlap 임계값 (기본값: 0.75)
- `--no-dedup` — concept 중복 제거 비활성화

참고: `--llm-ideas-file`과 `--promote-hints`는 전체 pipeline 실행에서만 유효합니다.
`--resume-from drafts`와 `--review-only`는 hints/concepts 단계를 건너뛰므로
이 플래그들은 무시됩니다.

## 리소스

- `references/pipeline_flow.md` — Pipeline 단계, data contract, 아키텍처
- `references/revision_loop_rules.md` — Review-revision feedback loop 규칙 및 heuristic
