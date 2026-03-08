---
name: skill-integration-tester
description: CLAUDE.md에 정의된 멀티 스킬 워크플로우를 검증합니다. 스킬 존재 여부, 스킬 간 데이터 계약(JSON schema 호환성), 파일 네이밍 규약, handoff 무결성을 점검합니다. 새 워크플로우 추가, 스킬 출력 수정, 릴리스 전 파이프라인 상태 점검 시 사용합니다.
---

# Skill Integration Tester

## 개요

CLAUDE.md에 정의된 멀티 스킬 워크플로우(Daily Market Monitoring,
Weekly Strategy Review, Earnings Momentum Trading 등)를 각 단계를
순차 실행해 검증합니다. step N의 출력과 step N+1의 입력 간 JSON schema
호환성을 확인하는 스킬 간 데이터 계약 점검, 파일 네이밍 규약 검증,
그리고 깨진 handoff를 리포트합니다. synthetic fixture를 이용한 dry-run
모드를 지원합니다.

## 사용 시점

- CLAUDE.md에 멀티 스킬 워크플로우를 추가하거나 수정한 뒤
- 스킬 출력 형식(JSON schema, 파일 네이밍)을 변경한 뒤
- 새 스킬 릴리스 전 파이프라인 호환성 검증 시
- 연속 워크플로우 단계 간 깨진 handoff 디버깅 시
- 스킬 스크립트를 건드리는 pull request의 CI 사전 점검으로

## 사전 요구사항

- Python 3.9+
- API 키 불필요
- 서드파티 Python 패키지 불필요(표준 라이브러리만 사용)

## 워크플로우

### Step 1: 통합 검증 실행

프로젝트의 CLAUDE.md를 대상으로 검증 스크립트를 실행합니다:

```bash
python3 skills/skill-integration-tester/scripts/test_workflows.py \
  --output-dir reports/
```

이 스크립트는 Multi-Skill Workflows 섹션의 모든 `**Workflow Name:**`
블록을 파싱하고, 각 step display name을 스킬 디렉터리로 해석한 뒤
존재 여부, 계약, 네이밍을 검증합니다.

### Step 2: 특정 워크플로우 검증

이름 부분 문자열로 단일 워크플로우를 지정합니다:

```bash
python3 skills/skill-integration-tester/scripts/test_workflows.py \
  --workflow "Earnings Momentum" \
  --output-dir reports/
```

### Step 3: Synthetic Fixture로 Dry-Run

각 스킬의 예상 출력에 대한 synthetic fixture JSON 파일을 만들고,
실데이터 없이 계약 호환성을 검증합니다:

```bash
python3 skills/skill-integration-tester/scripts/test_workflows.py \
  --dry-run \
  --output-dir reports/
```

fixture 파일은 `_fixture` 플래그가 설정된 상태로 `reports/fixtures/`에 저장됩니다.

### Step 4: 결과 검토

사람이 읽기 쉬운 요약은 생성된 Markdown 리포트를 열어 확인하고,
프로그램에서 소비할 때는 JSON 리포트를 파싱합니다. 각 워크플로우는 다음을 보여줍니다:
- 단계별 스킬 존재 여부 점검
- Handoff 계약 검증 (PASS / FAIL / N/A)
- 파일 네이밍 규약 위반
- 워크플로우 전체 상태 (valid / broken / warning)

### Step 5: 깨진 Handoff 수정

각 `FAIL` handoff에 대해 다음을 확인합니다:
1. producer 스킬 출력에 모든 필수 필드가 포함되어 있는지
2. consumer 스킬 입력 파라미터가 producer 출력 형식을 받을 수 있는지
3. producer 출력과 consumer 입력 간 파일 네이밍 패턴이 일관적인지

## 출력 형식

### JSON Report

```json
{
  "schema_version": "1.0",
  "generated_at": "2026-03-01T12:00:00+00:00",
  "dry_run": false,
  "summary": {
    "total_workflows": 8,
    "valid": 6,
    "broken": 1,
    "warnings": 1
  },
  "workflows": [
    {
      "workflow": "Daily Market Monitoring",
      "step_count": 4,
      "status": "valid",
      "steps": [...],
      "handoffs": [...],
      "naming_violations": []
    }
  ]
}
```

### Markdown Report

워크플로우별 섹션에 step 검증, handoff 상태, 네이밍 위반을 표시하는 구조화 리포트입니다.

리포트는 `reports/`에
`integration_test_YYYY-MM-DD_HHMMSS.{json,md}`
파일명으로 저장됩니다.

## 리소스

- `scripts/test_workflows.py` -- 메인 검증 스크립트
- `references/workflow_contracts.md` -- 계약 정의 및 handoff 패턴

## 핵심 원칙

1. API 키 불필요 -- 모든 검증은 로컬 오프라인에서 수행
2. Non-destructive -- SKILL.md와 CLAUDE.md만 읽고, 스킬을 수정하지 않음
3. Deterministic -- 동일 입력은 항상 동일 검증 결과를 생성
