# 문서 디렉토리 (Documentation Directory)

이 디렉토리는 프로젝트 전반의 문서, 리비전(수정) 내역 및 개선 기록을 포함합니다.

## 디렉토리 구조

```
docs/
├── README.md (현재 문서)
├── edge_candidate_agent_design.md
├── edge-institutionalization-process.md
├── kanchi-dividend-skills-runbook.md
└── revisions/
    ├── bubble-detector-v2.0-revision.md
    └── Breadth Chart Analyst Skill_IMPROVEMENTS_v2.0.md
```

## `revisions/` 폴더

각 스킬의 상세한 리비전 및 개선 기록을 포함합니다.

### 파일 목록:

- **`bubble-detector-v2.0-revision.md`** - 버블 감지기(Bubble Detector) 스킬 v2.0에 대한 종합적인 개선 요약
  - 발견된 문제점 (4가지 핵심 이슈)
  - 적용된 해결책
  - 개선 전/후 비교 (10포인트 → 3포인트 케이스 스터디)
  - 주요 배운 점 (Lessons learned)
  - 향후 단계 (Next steps)

## 사용 방법

스킬에 중요한 개선 사항을 적용할 때:

1. `docs/revisions/[스킬명]-[버전]-revision.md` 파일에 리비전 내역을 문서화합니다.
2. 다음 내용을 포함해야 합니다:
   - 발견된 문제점
   - 적용된 해결책
   - 개선 전/후 비교
   - 배운 점 (Lessons learned)
3. 필요한 경우 스킬의 메인 문서에서 리비전 문서를 참조(링크)합니다.

## 관련 디렉토리

- `/[스킬명]/references/` - 특정 스킬과 관련된 참고 자료
- `/[스킬명]/SKILL.md` - 메인 스킬 정의 문서 (Claude Code가 자동 로드함)

## 런북 (Runbooks)

- **`kanchi-dividend-skills-runbook.md`** - 운용 순서 고정용 절차서
  - 3가지 스킬의 매뉴얼화된 실행 순서 (`SOP -> 모니터링 -> 세무/계좌 배치`)
  - 일간/주간/월간/분기/연간 운용 리듬
  - 스킬 간 입력/출력 데이터 인계
- **`edge-institutionalization-process.md`** - 엣지(Edge)의 제도화(Institutionalization) 절차
  - `관찰 -> 추상화 -> 전략화 -> 파이프라인`의 분업 워크플로우
  - 승급 단계 (Hint/Ticket/Concept/Draft/Candidate/Live)
  - Concept/Draft/Pipeline/Promotion 승급을 위한 게이트(통과) 기준
