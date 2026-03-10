---
name: skill-designer
description: 구조화된 아이디어 명세에서 새로운 Claude 스킬을 설계합니다. 스킬 자동 생성 파이프라인이 저장소 규약에 맞는 완전한 스킬 디렉터리(SKILL.md, references, scripts, tests)를 만드는 Claude CLI 프롬프트를 생성해야 할 때 사용합니다.
---

# Skill Designer

## 개요

구조화된 스킬 아이디어 명세로부터 포괄적인 Claude CLI 프롬프트를 생성합니다. 이 프롬프트는 저장소 규약에 맞는 완전한 스킬 디렉터리 생성 작업을 Claude에 지시합니다: YAML frontmatter가 포함된 SKILL.md, 참고 문서, 헬퍼 스크립트, 테스트 스캐폴딩.

## 사용 시점

- 스킬 자동 생성 파이프라인이 백로그에서 아이디어를 선택했고 `claude -p`용 설계 프롬프트가 필요할 때
- 개발자가 JSON 아이디어 명세로 새로운 스킬을 부트스트랩하고 싶을 때
- 생성된 스킬의 품질 리뷰에서 스코어링 루브릭 이해가 필요할 때

## 사전 요구사항

- Python 3.9+
- 외부 API 키 불필요
- 참고 파일은 `skills/skill-designer/references/` 하위에 존재해야 함

## 워크플로우

### Step 1: 아이디어 명세 준비

다음 필드를 포함하는 JSON 파일(`--idea-json`)을 받습니다:
- `title`: 사람이 읽을 수 있는 아이디어 이름
- `description`: 스킬이 수행하는 작업
- `category`: 스킬 카테고리(예: trading-analysis, developer-tooling)

디렉터리 이름과 YAML frontmatter `name:` 필드에 사용될 정규화된 스킬 이름(`--skill-name`)을 받습니다.

### Step 2: 설계 프롬프트 생성

프롬프트 빌더를 실행합니다:

```bash
python3 skills/skill-designer/scripts/build_design_prompt.py \
  --idea-json /tmp/idea.json \
  --skill-name "my-new-skill" \
  --project-root .
```

스크립트 동작:
1. 아이디어 JSON 로드
2. 세 개의 참고 파일(구조 가이드, 품질 체크리스트, 템플릿) 모두 읽기
3. 중복 방지를 위해 기존 스킬 목록(최대 20개) 조회
4. 완전한 프롬프트를 stdout으로 출력

### Step 3: Claude CLI에 프롬프트 전달

호출 파이프라인은 프롬프트를 `claude -p`로 파이프합니다:

```bash
python3 skills/skill-designer/scripts/build_design_prompt.py \
  --idea-json /tmp/idea.json \
  --skill-name "my-new-skill" \
  --project-root . \
| claude -p --allowedTools Read,Edit,Write,Glob,Grep
```

### Step 4: 출력 검증

Claude가 스킬을 생성한 뒤 다음을 확인합니다:
- 올바른 frontmatter를 갖춘 `skills/<skill-name>/SKILL.md` 존재
- 디렉터리 구조가 규약을 따름
- dual-axis-skill-reviewer 점수가 임계값 충족

## 출력 형식

스크립트는 일반 텍스트 프롬프트를 stdout으로 출력합니다. 성공 시 종료 코드 0, 필수 참고 파일 누락 시 1을 반환합니다.

## 리소스

- `references/skill-structure-guide.md` -- 디렉터리 구조, SKILL.md 형식, 네이밍 규약
- `references/quality-checklist.md` -- dual-axis reviewer 5개 카테고리 체크리스트 (100점)
- `references/skill-template.md` -- YAML frontmatter와 표준 섹션을 포함한 SKILL.md 템플릿
- `scripts/build_design_prompt.py` -- 프롬프트 빌더 스크립트 (CLI 인터페이스)
