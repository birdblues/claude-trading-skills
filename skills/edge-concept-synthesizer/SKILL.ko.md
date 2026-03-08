---
name: edge-concept-synthesizer
description: detector 티켓과 힌트를 추상화해 재사용 가능한 edge concept(논지, 무효화 시그널, 전략 플레이북 포함)으로 합성한 뒤 전략 설계/export 이전 단계에 제공합니다.
---

# Edge Concept Synthesizer

## 개요

탐지(detection)와 전략 구현(strategy implementation) 사이에 추상화 레이어를 만듭니다.
이 스킬은 티켓 증거를 클러스터링하고 반복 조건을 요약해, 명시적 thesis와 invalidation logic를 가진 `edge_concepts.yaml`을 출력합니다.

## 사용 시점

- 원시 ticket이 많아 메커니즘 수준의 구조화가 필요할 때
- ticket에서 strategy로 바로 넘어가며 발생하는 overfitting을 피하고 싶을 때
- strategy draft 전에 concept 단위 리뷰가 필요할 때

## 사전 요구사항

- Python 3.9+
- `PyYAML`
- detector 출력 ticket YAML 디렉터리 (`tickets/exportable`, `tickets/research_only`)
- 선택 입력 `hints.yaml`

## 출력물

- `edge_concepts.yaml` (포함 내용):
  - concept cluster
  - support 통계
  - 추상 thesis
  - invalidation signal
  - export readiness flag

## 워크플로

1. auto-detection 출력에서 ticket YAML 파일을 수집합니다.
2. 선택적으로 `hints.yaml`을 제공해 컨텍스트 매칭을 강화합니다.
3. `scripts/synthesize_edge_concepts.py`를 실행합니다.
4. concept 중복 제거: 동일 hypothesis를 가진 concept 중 조건이 겹치는 것(containment > threshold)을 병합합니다.
5. concept를 검토하고 support가 높은 concept만 strategy drafting으로 승격합니다.

## 빠른 명령

```bash
python3 skills/edge-concept-synthesizer/scripts/synthesize_edge_concepts.py \
  --tickets-dir /tmp/edge-auto/tickets \
  --hints /tmp/edge-hints/hints.yaml \
  --output /tmp/edge-concepts/edge_concepts.yaml \
  --min-ticket-support 2

# hint 승격 및 synthetic 비율 제한
python3 skills/edge-concept-synthesizer/scripts/synthesize_edge_concepts.py \
  --tickets-dir /tmp/edge-auto/tickets \
  --hints /tmp/edge-hints/hints.yaml \
  --output /tmp/edge-concepts/edge_concepts.yaml \
  --promote-hints \
  --max-synthetic-ratio 1.5

# 사용자 정의 중복 제거 임계값 (또는 중복 제거 비활성화)
python3 skills/edge-concept-synthesizer/scripts/synthesize_edge_concepts.py \
  --tickets-dir /tmp/edge-auto/tickets \
  --output /tmp/edge-concepts/edge_concepts.yaml \
  --overlap-threshold 0.6

python3 skills/edge-concept-synthesizer/scripts/synthesize_edge_concepts.py \
  --tickets-dir /tmp/edge-auto/tickets \
  --output /tmp/edge-concepts/edge_concepts.yaml \
  --no-dedup
```

## 리소스

- `skills/edge-concept-synthesizer/scripts/synthesize_edge_concepts.py`
- `references/concept_schema.md`
