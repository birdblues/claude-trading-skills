# Documentation Directory

This directory contains project-wide documentation, revision histories, and improvement records.

## Directory Structure

```
docs/
├── README.md (this file)
├── edge_candidate_agent_design.md
├── edge-institutionalization-process.md
├── kanchi-dividend-skills-runbook.md
└── revisions/
    ├── bubble-detector-v2.0-revision.md
    └── Breadth Chart Analyst Skill_IMPROVEMENTS_v2.0.md
```

## `revisions/`

Contains detailed revision and improvement records for each skill.

### Files:

- **`bubble-detector-v2.0-revision.md`** - Comprehensive improvement summary for Bubble Detector skill v2.0
  - Problems identified (4 key issues)
  - Solutions implemented
  - Comparison of improvements (10 points → 3 points case study)
  - Important lessons learned
  - Next steps

## Usage

When making significant improvements to a skill:

1. Document the revision in `docs/revisions/[skill-name]-[version]-revision.md`
2. Include:
   - Problems identified
   - Solutions implemented
   - Before/after comparison
   - Lessons learned
3. Reference the revision document in the skill's main documentation if needed

## Related Directories

- `/[skill-name]/references/` - Skill-specific reference materials
- `/[skill-name]/SKILL.md` - Main skill definition (auto-loaded by Claude Code)

## Runbooks

- **`kanchi-dividend-skills-runbook.md`** - 운용 순서 고정용 절차서
  - 3스킬의 실행 순서 (`SOP -> 모니터링 -> 세무/계좌 배치`)
  - 일간/주간/월간/분기/연간 운용 리듬
  - 스킬 간 입력/출력 인계
- **`edge-institutionalization-process.md`** - 에지의 인스티튜셔널라이제이션 절차
  - `관찰 -> 추상화 -> 전략화 -> 파이프라인`의 분업 플로우
  - 승급 스테이트 (Hint/Ticket/Concept/Draft/Candidate/Live)
  - Concept/Draft/Pipeline/Promotion의 게이트 기준
