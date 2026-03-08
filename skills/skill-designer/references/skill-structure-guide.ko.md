# 스킬 구조 가이드

## 디렉터리 레이아웃

모든 스킬은 다음 표준 구조를 따릅니다:

```
<skill-name>/
├── SKILL.md              # 필수: YAML frontmatter가 포함된 스킬 정의
├── references/           # Claude 컨텍스트에 로드되는 지식 베이스
├── scripts/             # 실행 가능한 Python 스크립트(자동 로드되지 않음)
│   └── tests/           # 스크립트 테스트 파일
└── assets/              # 출력 생성용 템플릿과 리소스
```

## SKILL.md 형식

### YAML Frontmatter (필수)

```yaml
---
name: <skill-name>
description: <one-line trigger description>
---
```

- `name`은 디렉터리 이름과 정확히 일치해야 함
- `description`은 스킬이 트리거되어야 하는 시점을 정의하며, 간결하게 작성

### 본문 섹션 (필수)

1. **Overview** -- 스킬이 수행하는 작업 (2-3문장)
2. **When to Use** -- 트리거 조건 불릿 리스트
3. **Prerequisites** -- Python 버전, API 키, 의존성
4. **Workflow** -- 단계별 실행 지침(명령형)
5. **Output Format** -- JSON 및/또는 Markdown 리포트 구조
6. **Resources** -- 참고 파일과 스크립트 목록

## 작성 스타일

- 명령형/부정사 동사 형태 사용: "Analyze the chart", "Generate report"
- 사용자 지침이 아니라 Claude가 실행할 지침으로 작성
- "You should..." 또는 "Claude will..."을 피하고, 행동을 직접 서술
- 전체 경로를 포함한 구체적 bash 명령 예시 포함

## 네이밍 규약

- 디렉터리 이름: 소문자, 하이픈 구분 (예: `position-sizer`)
- SKILL.md frontmatter `name:`은 디렉터리 이름과 일치해야 함
- 스크립트: `snake_case.py` (예: `check_data_quality.py`)
- 리포트: `<skill>_<analysis-type>_<date>.{md,json}`
- 출력 디렉터리: 기본값 `reports/`

## 점진적 로딩

1. 스킬 탐지를 위해 메타데이터(YAML frontmatter)를 먼저 로드
2. 스킬 호출 시 SKILL.md 본문 로드
3. 분석 필요에 따라 references를 조건부 로드
4. scripts는 필요 시 실행되며, 컨텍스트에 자동 로드되지 않음

## 스크립트 요구사항

- 요청 전 API 키 존재 여부 확인
- 날짜 범위와 입력 파라미터 검증
- stderr에 유용한 에러 메시지 제공
- 올바른 종료 코드 반환(성공 0, 에러 1)
- rate limit 대응을 위한 exponential backoff 재시도 로직 지원
- 상대 경로 또는 동적 경로 해석 사용(절대 경로 하드코딩 금지)
- 기본 `--output-dir`을 `reports/`로 설정

## 참고 문서 패턴

- 사실에 대한 선언적 문장 사용
- 해당되는 경우 역사적 예시와 사례 연구 포함
- 의사결정 프레임워크와 체크리스트 제공
- 계층 구조로 구성(H2: 대섹션, H3: 하위 섹션)

## 분석 출력 요구사항

모든 출력은 다음을 충족해야 합니다:
- `reports/` 디렉터리에 저장
- 날짜/시간 스탬프 포함
- 영어 사용
- 해당되는 경우 확률 평가 제공
- 실행 가능한 시나리오를 위한 구체적 트리거 레벨 포함
