---
name: dual-axis-skill-reviewer
description: "이중 축 방식으로 모든 프로젝트의 스킬을 리뷰합니다: (1) 결정론적 코드 기반 점검(구조, 스크립트, 테스트, 실행 안전성)과 (2) LLM 심층 리뷰 결과를 결합합니다. `skills/*/SKILL.md`에 대해 재현 가능한 품질 점수가 필요할 때, 점수 임계값(예: 90+)으로 병합을 게이트할 때, 또는 저점수 스킬의 구체적 개선 항목이 필요할 때 사용하세요. --project-root를 통해 프로젝트 전반에서 동작합니다."
---

# Dual Axis Skill Reviewer

이중 축 리뷰어 스크립트를 실행하고 보고서를 `reports/`에 저장합니다.

스크립트 지원 항목:
- 랜덤 또는 고정 스킬 선택
- 선택적 테스트 실행을 포함한 Auto-axis 점수 산정
- LLM 프롬프트 생성
- 가중 최종 점수를 위한 LLM JSON 리뷰 병합
- `--project-root`를 통한 교차 프로젝트 리뷰

## 사용 시점

- `skills/*/SKILL.md`의 단일 스킬에 대해 재현 가능한 점수가 필요할 때.
- 최종 점수가 90 미만일 때 개선 항목이 필요할 때.
- 결정론적 점검과 정성적 LLM 코드/콘텐츠 리뷰가 모두 필요할 때.
- 커맨드라인에서 **다른 프로젝트**의 스킬을 리뷰해야 할 때.

## 사전 요구사항

- Python 3.9+
- `uv` (권장 — 인라인 메타데이터로 `pyyaml` 의존성을 자동 해결)
- 테스트용: 대상 프로젝트에서 `uv sync --extra dev` 또는 동등한 설정
- LLM-axis 병합용: LLM 리뷰 스키마를 따르는 JSON 파일(리소스 참조)

## 워크플로

컨텍스트에 따라 올바른 스크립트 경로를 결정하세요:

- **같은 프로젝트**: `skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py`
- **글로벌 설치**: `~/.claude/skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py`

아래 예시는 `REVIEWER`를 플레이스홀더로 사용합니다. 한 번만 설정하세요:

```bash
# If reviewing from the same project:
REVIEWER=skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py

# If reviewing another project (global install):
REVIEWER=~/.claude/skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py
```

### 1단계: Auto Axis 실행 + LLM 프롬프트 생성

```bash
uv run "$REVIEWER" \
  --project-root . \
  --emit-llm-prompt \
  --output-dir reports/
```

다른 프로젝트를 리뷰할 때는 `--project-root`를 해당 경로로 지정합니다:

```bash
uv run "$REVIEWER" \
  --project-root /path/to/other/project \
  --emit-llm-prompt \
  --output-dir reports/
```

### 2단계: LLM 리뷰 실행
- `reports/skill_review_prompt_<skill>_<timestamp>.md`에 생성된 프롬프트 파일을 사용하세요.
- LLM이 strict JSON 출력만 반환하도록 요청하세요.
- Claude Code에서 실행 중이라면, Claude를 오케스트레이터로 사용하세요: 생성된 프롬프트를 읽고 LLM 리뷰 JSON을 만든 뒤 병합 단계에서 사용할 수 있도록 저장합니다.

### 3단계: Auto + LLM 축 병합

```bash
uv run "$REVIEWER" \
  --project-root . \
  --skill <skill-name> \
  --llm-review-json <path-to-llm-review.json> \
  --auto-weight 0.5 \
  --llm-weight 0.5 \
  --output-dir reports/
```

### 4단계: 선택적 제어

- 재현성을 위한 선택 고정: `--skill <name>` 또는 `--seed <int>`
- 모든 스킬 일괄 리뷰: `--all`
- 빠른 트리아지를 위해 테스트 건너뛰기: `--skip-tests`
- 보고서 경로 변경: `--output-dir <dir>`
- 더 엄격한 결정론적 게이팅이 필요하면 `--auto-weight` 증가.
- 정성/코드리뷰 깊이를 우선하면 `--llm-weight` 증가.

## 출력

- `reports/skill_review_<skill>_<timestamp>.json`
- `reports/skill_review_<skill>_<timestamp>.md`
- `reports/skill_review_prompt_<skill>_<timestamp>.md` (`--emit-llm-prompt` 활성화 시)

## 설치 (글로벌)

어떤 프로젝트에서든 이 스킬을 사용하려면 `~/.claude/skills/`에 심볼릭 링크를 만드세요:

```bash
ln -sfn /path/to/claude-trading-skills/skills/dual-axis-skill-reviewer \
  ~/.claude/skills/dual-axis-skill-reviewer
```

이후 Claude Code가 모든 프로젝트에서 해당 스킬을 인식하며, 스크립트는 `~/.claude/skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py`에서 접근할 수 있습니다.

## 리소스

- Auto axis는 metadata, workflow 커버리지, 실행 안전성, 산출물 존재, 테스트 상태를 점수화합니다.
- Auto axis는 `knowledge_only` 스킬을 감지하고 불공정한 감점을 피하도록 스크립트/테스트 기대치를 조정합니다.
- LLM axis는 심층 콘텐츠 품질(정확성, 리스크, 누락 로직, 유지보수성)을 점수화합니다.
- 최종 점수는 가중 평균입니다.
- 최종 점수가 90 미만이면, 개선 항목이 필수이며 markdown 보고서에 기재됩니다.
- 스크립트: `skills/dual-axis-skill-reviewer/scripts/run_dual_axis_review.py`
- LLM 스키마: `references/llm_review_schema.md`
- Rubric 상세: `references/scoring_rubric.md`
