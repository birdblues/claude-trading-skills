---
name: skill-idea-miner
description: Claude Code 세션 로그에서 스킬 아이디어 후보를 마이닝합니다. 최근 코딩 세션에서 새 스킬 아이디어를 추출, 점수화, 백로그화하기 위해 주간 스킬 생성 파이프라인을 실행할 때 사용합니다.
---

# Skill Idea Miner

Claude Code 세션 로그에서 스킬 아이디어 후보를 자동 추출하고,
신규성, 구현 가능성, 트레이딩 가치를 기준으로 점수화한 뒤,
후속 스킬 생성을 위한 우선순위 백로그를 유지합니다.

## 사용 시점

- 주간 자동 파이프라인 실행(토요일 06:00, launchd)
- 수동 백로그 갱신: `python3 scripts/run_skill_generation_pipeline.py --mode weekly`
- LLM 점수화 없이 후보만 미리 확인하는 dry-run

## 워크플로우

### Stage 1: 세션 로그 마이닝

1. `~/.claude/projects/`의 allowlist 프로젝트에서 세션 로그를 열거
2. 파일 mtime 기준 최근 7일로 필터링하고 `timestamp` 필드로 재확인
3. 사용자 메시지 추출 (`type: "user"`, `userType: "external"`)
4. assistant 메시지에서 도구 사용 패턴 추출
5. 결정론적 시그널 감지 실행:
   - 스킬 사용 빈도 (`skills/*/` 경로 참조)
   - 에러 패턴(0이 아닌 exit code, `is_error` 플래그, exception 키워드)
   - 반복 도구 시퀀스(3개 이상 도구가 3회 이상 반복)
   - 자동화 요청 키워드(영어 및 일본어)
   - 미해결 요청(사용자 메시지 이후 5분 이상 간격)
6. 아이디어 추상화를 위해 Claude CLI headless 호출
7. `raw_candidates.yaml` 출력

### Stage 2: 점수화 및 중복 제거

1. `skills/*/SKILL.md` frontmatter에서 기존 스킬 로드
2. Jaccard similarity(임계값 > 0.5)로 다음과 중복 제거:
   - 기존 스킬 이름과 설명
   - 기존 백로그 아이디어
3. 비중복 후보를 Claude CLI로 점수화:
   - Novelty (0-100): 기존 스킬 대비 차별성
   - Feasibility (0-100): 기술적 구현 가능성
   - Trading Value (0-100): 투자자/트레이더 실무 가치
   - Composite = 0.3 * Novelty + 0.3 * Feasibility + 0.4 * Trading Value
4. 점수화된 후보를 `logs/.skill_generation_backlog.yaml`에 병합

## 출력 형식

### raw_candidates.yaml

```yaml
generated_at_utc: "2026-03-08T06:00:00Z"
period: {from: "2026-03-01", to: "2026-03-07"}
projects_scanned: ["claude-trading-skills"]
sessions_scanned: 12
candidates:
  - id: "raw_2026w10_001"
    title: "Earnings Whispers Image Parser"
    source_project: "claude-trading-skills"
    evidence:
      user_requests: ["Extract earnings dates from screenshot"]
      pain_points: ["Manual image reading"]
      frequency: 3
    raw_description: "Parse Earnings Whispers screenshots to extract dates."
    category: "data-extraction"
```

### Backlog (logs/.skill_generation_backlog.yaml)

```yaml
updated_at_utc: "2026-03-08T06:15:00Z"
ideas:
  - id: "idea_2026w10_001"
    title: "Earnings Whispers Image Parser"
    description: "Skill that parses Earnings Whispers screenshots..."
    category: "data-extraction"
    scores: {novelty: 75, feasibility: 60, trading_value: 80, composite: 73}
    status: "pending"
```

## 리소스

- `references/idea_extraction_rubric.md` — 시그널 감지 기준 및 스코어링 루브릭
- `scripts/mine_session_logs.py` — 세션 로그 파서
- `scripts/score_ideas.py` — 점수화 및 중복 제거기
