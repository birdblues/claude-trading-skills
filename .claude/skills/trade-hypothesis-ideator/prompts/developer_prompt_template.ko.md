## 목표
반복 테스트를 위한 고품질 trade hypothesis card 1~5개를 생성합니다.

## 증거 요약
{{evidence_summary}}

## 출력 요구사항
최상위 키가 `hypotheses`인 JSON을 반환하세요.
각 hypothesis는 `schemas/hypothesis_card.schema.json`의 모든 필수 필드를 포함해야 합니다.
다음에 집중하세요:
- 명확한 메커니즘
- 사용 가능한 feature로 검증 가능한 testability
- 명시적인 invalidation 및 제약 인식(constraints-awareness)
