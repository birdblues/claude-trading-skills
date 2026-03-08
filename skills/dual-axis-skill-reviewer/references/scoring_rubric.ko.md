# 점수 산정 Rubric 근거

이 문서는 각 auto-axis 구성 요소에 현재 가중치를 부여한 이유를 설명합니다.

## 가중치

- `metadata_use_case` (20)
이유: frontmatter가 부정확하거나 트리거 조건이 불명확하면 스킬을 올바르게 호출하기 어렵습니다.

- `workflow_coverage` (25)
이유: 운영자는 실행 가능한 흐름이 필요합니다. 핵심 섹션이 빠지면 실제 사용에서 모호성이 커집니다.

- `execution_safety_reproducibility` (25)
이유: 명령 예시와 경로 위생이 결과의 재현성과 안전성을 좌우합니다.

- `supporting_artifacts` (10)
이유: scripts/references/tests는 기본 유지보수성을 제공하지만, 점수를 과도하게 지배해서는 안 됩니다.

- `test_health` (20)
이유: 런타임 신뢰도가 중요하며, 테스트 통과는 자동화 신뢰도를 크게 높입니다.

## 임계값 정책

- `90+`: 프로덕션 준비 기준 충족
- `80-89`: 목표 개선을 거치면 사용 가능
- `70-79`: 눈에 띄는 공백 존재, 정기 사용 전 보강 필요
- `<70`: 고위험, 초안으로 간주하고 수정 우선

## 개선 트리거

최종 점수가 `< 90`이면 보고서 출력에 개선 항목이 필수입니다.

## Knowledge-Only Skill 처리

실행 가능한 스크립트가 없고(`scripts/*.py` 부재) 참조 문서만 있는 스킬의 경우:

- `knowledge_only`로 분류합니다.
- bash 명령 예시 누락으로 감점하지 않습니다.
- 스크립트/테스트 산출물은 대부분 비해당으로 처리합니다(`supporting_artifacts`, `test_health` 조정).
- 그래도 명확한 `When to Use`, `Prerequisites`, 워크플로 구조는 필수입니다.
