---
name: edge-strategy-reviewer
description: >
  edge-strategy-designer가 생성한 strategy draft를 edge 개연성, overfitting
  리스크, sample size 적정성, 실행 현실성 관점에서 비판적으로 리뷰합니다.
  strategy_drafts/*.yaml이 존재하고 pipeline export 전 품질 게이트가 필요할 때
  사용하세요. PASS/REVISE/REJECT verdict와 confidence score를 출력합니다.
---

# Edge Strategy Reviewer

`edge-strategy-designer`가 생성한 strategy draft를 위한 deterministic 품질 게이트입니다.

## 사용 시점

- `edge-strategy-designer`가 `strategy_drafts/*.yaml`를 생성한 이후
- pipeline을 통해 draft를 `edge-candidate-agent`로 export하기 전
- draft strategy의 edge 개연성을 수동 검증할 때

## 사전 요구사항

- Strategy draft YAML 파일 (`edge-strategy-designer` 출력물)
- Python 3.10+ 및 PyYAML

## 워크플로

1. `--drafts-dir` 또는 단일 `--draft` 파일에서 draft YAML 로드
2. 각 draft를 8개 기준(C1-C8)으로 가중 점수 평가
3. confidence score 계산(모든 기준의 가중 평균)
4. verdict 결정: PASS / REVISE / REJECT
5. export 자격 평가(PASS + export_ready_v1 + exportable family)
6. 리뷰 출력(YAML 또는 JSON) 및 선택적 markdown summary 작성

## 리뷰 기준

| # | Criterion | Weight | Key Checks |
|---|-----------|--------|------------|
| C1 | Edge Plausibility | 20 | Thesis 품질, 도메인 용어, 메커니즘 키워드 (연속 점수 50-95) |
| C2 | Overfitting Risk | 20 | 5단계 filter count 점수화 (90/80/60/40/10), 정밀 임계값 패널티 |
| C3 | Sample Adequacy | 15 | 연간 기회 수 추정 기반 연속 점수 (10-95) |
| C4 | Regime Dependency | 10 | Cross-regime 검증 |
| C5 | Exit Calibration | 10 | Stop-loss, reward-to-risk |
| C6 | Risk Concentration | 10 | Position sizing 한도 |
| C7 | Execution Realism | 10 | Volume filter, export 일관성 |
| C8 | Invalidation Quality | 5 | Signal 개수 및 구체성 |

## Verdict 로직

- C1 또는 C2 severity=fail -> 즉시 REJECT
- confidence >= 70, fail finding 없음 -> PASS
- confidence < 35 -> REJECT
- 그 외 -> REVISE (revision instruction 포함)

## 스크립트 실행

```bash
# 디렉터리의 모든 draft 리뷰
python3 skills/edge-strategy-reviewer/scripts/review_strategy_drafts.py \
  --drafts-dir reports/edge_strategy_drafts/ \
  --output-dir reports/

# 단일 draft 리뷰
python3 skills/edge-strategy-reviewer/scripts/review_strategy_drafts.py \
  --draft reports/edge_strategy_drafts/draft_xxx.yaml \
  --output-dir reports/

# markdown summary와 함께 JSON 출력
python3 skills/edge-strategy-reviewer/scripts/review_strategy_drafts.py \
  --drafts-dir reports/edge_strategy_drafts/ \
  --output-dir reports/ \
  --format json \
  --markdown-summary

# Strict export mode: warn finding이 하나라도 있으면 REVISE 처리
python3 skills/edge-strategy-reviewer/scripts/review_strategy_drafts.py \
  --drafts-dir reports/edge_strategy_drafts/ \
  --output-dir reports/ \
  --strict-export
```

## 출력 형식

주 출력물: `review.yaml` (또는 `review.json`)

```yaml
generated_at_utc: "2026-02-28T12:00:00+00:00"
source:
  drafts_dir: "/path/to/strategy_drafts"
  draft_count: 4
summary:
  total: 4
  PASS: 1
  REVISE: 2
  REJECT: 1
  export_eligible: 1
reviews:
  - draft_id: "draft_xxx_core"
    verdict: "PASS"
    confidence_score: 80
    export_eligible: true
    findings: [...]
    revision_instructions: []
```

## 리소스

- `references/review_criteria.md` -- C1-C8 상세 점수 rubric
- `references/overfitting_checklist.md` -- overfitting 탐지 heuristic
