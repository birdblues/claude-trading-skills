---
name: edge-strategy-designer
description: 추상 edge concept를 전략 draft 변형으로 변환하고, 필요 시 edge-candidate-agent의 export/validation에 사용할 export 가능한 ticket YAML을 생성합니다.
---

# Edge Strategy Designer

## 개요

concept 수준 가설을 구체적인 strategy draft 스펙으로 변환합니다.
이 스킬은 concept synthesis 이후, pipeline export validation 이전 단계에 위치합니다.

## 사용 시점

- `edge_concepts.yaml`은 있는데 strategy candidate가 필요할 때
- concept별로 다중 변형(core/conservative/research-probe)을 만들고 싶을 때
- interface v1 family용 exportable ticket 파일을 선택적으로 만들고 싶을 때

## 사전 요구사항

- Python 3.9+
- `PyYAML`
- concept synthesis로 생성된 `edge_concepts.yaml`

## 출력물

- `strategy_drafts/*.yaml`
- `strategy_drafts/run_manifest.json`
- 선택: 후속 `export_candidate.py`용 `exportable_tickets/*.yaml`

## 워크플로

1. `edge_concepts.yaml`을 로드합니다.
2. risk profile(`conservative`, `balanced`, `aggressive`)을 선택합니다.
3. concept별 변형을 생성합니다.
4. 해당 시 v1-ready ticket YAML을 export합니다.
5. exportable ticket을 `skills/edge-candidate-agent/scripts/export_candidate.py`로 전달합니다.

## 빠른 명령

draft만 생성:

```bash
python3 skills/edge-strategy-designer/scripts/design_strategy_drafts.py \
  --concepts /tmp/edge-concepts/edge_concepts.yaml \
  --output-dir /tmp/strategy-drafts \
  --risk-profile balanced
```

draft + exportable ticket 생성:

```bash
python3 skills/edge-strategy-designer/scripts/design_strategy_drafts.py \
  --concepts /tmp/edge-concepts/edge_concepts.yaml \
  --output-dir /tmp/strategy-drafts \
  --exportable-tickets-dir /tmp/exportable-tickets \
  --risk-profile conservative
```

## 리소스

- `skills/edge-strategy-designer/scripts/design_strategy_drafts.py`
- `references/strategy_draft_schema.md`
- `skills/edge-candidate-agent/scripts/export_candidate.py`
