# 스킬 품질 체크리스트

dual-axis-skill-reviewer 스코어링 루브릭(총 100점)에서 도출되었습니다.

## 1. 메타데이터 및 사용 사례 (20점)

- [ ] YAML frontmatter의 `name:`이 디렉터리 이름과 일치함
- [ ] `description:`이 명확하고 간결한 트리거 조건임
- [ ] "When to Use" 섹션에 구체적인 트리거 시나리오가 나열됨
- [ ] "Prerequisites" 섹션에 Python 버전, API 키, 의존성이 문서화됨
- [ ] 스킬이 언제 활성화되어야 하는지 모호함이 없음

## 2. 워크플로우 커버리지 (25점)

- [ ] "Overview" 섹션이 스킬의 기능을 설명함 (2-3문장)
- [ ] "Workflow"에 명령형 동사가 포함된 번호 단계가 있음
- [ ] 각 단계가 구체적 행동을 포함함(모호한 가이드 금지)
- [ ] Bash 명령 예시가 전체 상대 경로를 사용함
- [ ] "Output Format" 섹션이 JSON/Markdown 구조를 보여줌
- [ ] "Resources" 섹션이 모든 참고 파일과 스크립트를 나열함

## 3. 실행 안전성 및 재현성 (25점)

- [ ] Bash 명령을 그대로 복붙 실행 가능함(올바른 경로, 플래그)
- [ ] 스크립트가 기본값으로 `--output-dir reports/`를 사용함
- [ ] 하드코딩된 절대 경로가 없음(상대 경로 또는 동적 해석 사용)
- [ ] API 키를 우선 환경 변수에서 읽고, CLI 인자를 fallback으로 사용함
- [ ] 적절한 종료 코드가 포함된 에러 처리 문서화됨
- [ ] 모든 출력 파일에 날짜/시간 스탬프 포함

## 4. 보조 아티팩트 (10점)

- [ ] `references/`에 최소 1개 참고 문서 존재
- [ ] `scripts/`에 최소 1개 실행 스크립트 존재 (`knowledge_only` 제외)
- [ ] 스크립트에 `#!/usr/bin/env python3` shebang 존재
- [ ] `__init__.py`는 필수 아님(스크립트는 standalone)

## 5. 테스트 건전성 (20점)

- [ ] 테스트 디렉터리 존재: `scripts/tests/`
- [ ] sys.path 설정이 있는 `conftest.py` 존재
- [ ] 핵심 로직을 다루는 의미 있는 테스트 최소 3개
- [ ] 테스트가 pytest fixtures와 tmp_path를 사용함
- [ ] `python -m pytest scripts/tests/ -v`로 테스트 통과

## 임계값 정책

| Score | Status |
|-------|--------|
| 90+   | Production-ready |
| 80-89 | 목표 지점 개선 후 사용 가능 |
| 70-79 | 눈에 띄는 공백 존재; 정기 사용 전 보강 필요 |
| <70   | 고위험; 초안으로 취급하고 수정 우선순위 상향 |

## Knowledge-Only 스킬

실행 스크립트 없이 참고 문서만 있는 스킬의 경우:
- `knowledge_only`로 분류
- 누락된 bash 명령 예시에 대한 감점 적용 안 함
- `supporting_artifacts`와 `test_health` 기대치를 조정
- 그래도 명확한 "When to Use", "Prerequisites", 워크플로우 구조는 필수
