---
name: strategy-pivot-designer
description: 파라미터 튜닝이 local optimum에 갇혔을 때 백테스트 반복 정체를 감지하고 구조적으로 다른 전략 pivot 제안을 생성합니다.
---

# Strategy Pivot Designer

## 개요

전략의 백테스트 반복 루프가 정체된 시점을 감지하고, 구조적으로 다른 전략 아키텍처를 제안합니다. 이 스킬은 Edge 파이프라인(hint-extractor -> concept-synthesizer -> strategy-designer -> candidate-agent)의 피드백 루프로 동작하며, 파라미터 미세조정이 아니라 전략 골격 자체를 재설계해 local optimum에서 탈출합니다.

## 사용할 때

- 여러 번 개선했지만 백테스트 점수가 plateau에 머물 때
- 전략이 overfitting 징후를 보일 때 (in-sample 높고 robustness 낮음)
- 거래 비용 때문에 얇은 edge가 사라질 때
- tail risk 또는 drawdown이 허용 임계값을 초과할 때
- 동일 시장 가설에서 근본적으로 다른 전략 아키텍처를 탐색하고 싶을 때

## 선행조건

- Python 3.9+
- `PyYAML`
- Iteration history JSON (누적된 backtest-expert 평가)
- Source strategy draft YAML (edge-strategy-designer 산출물)

## 출력

- `pivot_drafts/research_only/*.yaml` — strategy_draft 호환 YAML 제안
- `pivot_drafts/exportable/*.yaml` — export 준비 draft + candidate-agent용 ticket YAML
- `pivot_report_*.md` — 사람이 읽는 pivot 분석 리포트
- `pivot_manifest_*.json` — 생성 파일 메타데이터
- `pivot_diagnosis_*.json` — 정체 감지 결과

## 워크플로우

1. `--append-eval`로 백테스트 평가 결과를 iteration history 파일에 누적합니다.
2. history에서 정체 트리거(plateau, overfitting, cost defeat, tail risk)를 감지합니다.
3. 정체가 감지되면 3가지 기법(assumption inversion, archetype switch, objective reframe)으로 pivot 제안을 생성합니다.
4. 순위화된 제안을 검토합니다(quality potential + novelty 점수).
5. exportable 제안은 edge-candidate-agent 파이프라인용 ticket YAML을 바로 사용합니다.
6. research_only 제안은 파이프라인 통합 전에 수동 전략 설계가 필요합니다.
7. 선택된 pivot draft를 backtest-expert로 되돌려 다음 반복 사이클을 시작합니다.

## Quick Commands

백테스트 평가를 history에 추가(없으면 생성):

```bash
python3 skills/strategy-pivot-designer/scripts/detect_stagnation.py \
  --append-eval reports/backtest_eval_2026-02-10_120000.json \
  --history reports/iteration_history.json \
  --strategy-id draft_edge_concept_breakout_behavior_riskon_core \
  --changes "Widened stop_loss from 5% to 7%"
```

정체 감지:

```bash
python3 skills/strategy-pivot-designer/scripts/detect_stagnation.py \
  --history reports/iteration_history.json \
  --output-dir reports/
```

pivot 제안 생성:

```bash
python3 skills/strategy-pivot-designer/scripts/generate_pivots.py \
  --diagnosis reports/pivot_diagnosis_*.json \
  --strategy reports/edge_strategy_drafts/draft_*.yaml \
  --max-pivots 3 \
  --output-dir reports/
```

## 리소스

- `skills/strategy-pivot-designer/scripts/detect_stagnation.py`
- `skills/strategy-pivot-designer/scripts/generate_pivots.py`
- `references/stagnation_triggers.md`
- `references/strategy_archetypes.md`
- `references/pivot_techniques.md`
- `references/pivot_proposal_schema.md`
- `skills/backtest-expert/scripts/evaluate_backtest.py`
- `skills/edge-strategy-designer/scripts/design_strategy_drafts.py`
