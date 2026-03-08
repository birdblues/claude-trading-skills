# 아이디어 추출 루브릭

Claude Code 세션 로그에서 스킬 아이디어를 마이닝하기 위한 기준 및 점수화 프레임워크입니다.

## 시그널 감지 규칙

### 1. 스킬 사용 시그널

도구 인자에서 기존 스킬에 대한 참조를 감지합니다:

- **패턴:** Read, Edit, Write, Glob, Grep, Bash 도구에서 `skills/*/`를 포함하는 파일 경로
- **임계값:** 참조가 1회라도 있으면 시그널로 집계
- **해석:** 자주 쓰이는 스킬은 인접 니즈를 시사하며, 함께 쓰이는 스킬은 워크플로우 공백을 시사

### 2. 에러 감지 시그널

실패한 작업에서 pain point를 식별합니다:

| Signal | 감지 방법 |
|--------|-----------------|
| 0이 아닌 exit code | Bash tool_result에서 `exitCode != 0` |
| 명시적 에러 플래그 | `tool_result` content block에 `is_error: true` |
| 에러 텍스트 패턴 | 정규식 일치: `Error:`, `Exception:`, `Traceback`, `FAILED`, `ModuleNotFoundError` |

- **해석:** 유사 작업에서 반복되는 에러는 자동화 또는 툴링 공백을 시사

### 3. 반복 패턴 시그널

수동 워크플로우를 시사하는 반복 도구 시퀀스를 감지합니다:

- **정의:** 도구 이름 기준 연속 3회 이상 호출 시퀀스
- **임계값:** 동일 시퀀스가 한 세션에서 3회 이상 등장
- **추출:** 도구 시퀀스와 연관 파일/명령 인자를 기록
- **해석:** 반복 시퀀스는 워크플로우 자동화의 강력한 후보

### 4. 자동화 요청 시그널

사용자 메시지의 키워드 감지:

**영어 키워드:**
- `skill`, `create`, `automate`, `workflow`, `pipeline`, `generate`, `template`, `script`

**일본어 키워드:**
- `スキル`, `作成`, `自動化`, `ワークフロー`, `パイプライン`, `生成`, `テンプレート`

- **매칭:** 대소문자 무시, 부분 단어 일치
- **해석:** 자동화에 대한 직접적 사용자 의도이며 시그널 가치가 가장 높음

### 5. 미해결 요청 시그널

도구 액션으로 이어지지 않은 사용자 메시지를 감지합니다:

- **정의:** 사용자 메시지(`type: "user"`) 뒤 5분 이상 `tool_use`가 없음
- **측정:** 사용자 메시지와 다음 tool_use 간 timestamp 비교
- **엣지 케이스:** 세션 종료 메시지(후속 엔트리 없음)는 제외
- **해석:** 현재 기능 범위를 벗어난 요청일 수 있음

## LLM 추상화 프롬프트

아이디어 추상화를 위해 Claude CLI를 호출할 때 아래 프롬프트 구조를 사용합니다:

```
You are analyzing Claude Code session logs to extract skill idea candidates
for a trading/investing skill repository.

Given the following signals detected from recent sessions:
{signals_json}

And sample user messages from these sessions:
{user_messages}

Extract 0-5 skill idea candidates. For each candidate:
1. Abstract the idea (do not copy verbatim user messages)
2. Assign a category: data-extraction, analysis, screening, reporting, workflow, monitoring
3. Describe the pain point it addresses
4. Note which signals support this idea

Return JSON with this structure:
{
  "candidates": [
    {
      "title": "Short descriptive name",
      "raw_description": "What the skill would do",
      "category": "one of the categories above",
      "evidence": {
        "user_requests": ["abstracted summaries, not verbatim"],
        "pain_points": ["what problem this solves"],
        "frequency": <number of times this pattern appeared>
      }
    }
  ]
}

Rules:
- Return 0 candidates if no clear skill ideas emerge
- Do not suggest skills that already exist (provided in context)
- Abstract user requests (e.g., "extract earnings dates from chart" not "check CRWD earnings")
- Focus on trading/investing domain relevance
```

## 점수화 루브릭

### Novelty (0-100)

| Score Range | 기준 |
|------------|---------|
| 80-100 | 기존 스킬이 이 도메인을 다루지 않으며, 명확한 공백을 메움 |
| 60-79 | 기존 스킬과 일부 겹치지만 중요한 신규 기능을 추가 |
| 40-59 | 중간 수준의 중복; 기존 스킬 기능으로 흡수 가능 |
| 20-39 | 중복도가 높아 기존 기능을 대부분 반복 |
| 0-19 | 기존 스킬과 거의 동일 |

### Feasibility (0-100)

| Score Range | 기준 |
|------------|---------|
| 80-100 | 기존 도구(WebSearch, Read, Bash)로 구현 가능, 유료 API 불필요 |
| 60-79 | 프로젝트에 이미 있는 유료 API(FMP, FINVIZ)가 필요 |
| 40-59 | 신규 API 연동 또는 복잡한 파싱 로직 필요 |
| 20-39 | 상당한 인프라(데이터베이스, 실시간 피드) 필요 |
| 0-19 | Claude 스킬로 구현 불가(지속 상태, GUI 등 필요) |

### Trading Value (0-100)

| Score Range | 기준 |
|------------|---------|
| 80-100 | 실행 가능한 시그널로 트레이드 의사결정을 직접 지원 |
| 60-79 | 가치 있는 시장 인텔리전스 또는 포트폴리오 인사이트 제공 |
| 40-59 | 리서치에는 유용하나 직접 실행 가능성은 낮음 |
| 20-39 | 트레이딩/투자와 주변적으로만 관련 |
| 0-19 | 트레이딩/투자 적용성이 명확하지 않음 |

### Composite Score

```
composite = 0.3 * novelty + 0.3 * feasibility + 0.4 * trading_value
```

저장소의 주 목적이 주식 투자자와 트레이더 지원이기 때문에 trading value 가중치(0.4)를 더 높게 둡니다.

## 카테고리 분류 체계

| Category | 설명 | 예시 |
|----------|-------------|---------|
| `data-extraction` | 비정형 소스에서 구조화 데이터 파싱/추출 | 이미지 파싱, PDF 추출 |
| `analysis` | 시장 데이터를 분석해 인사이트 생성 | 상관관계 분석, 레짐 감지 |
| `screening` | 기준 기반 종목/자산 필터링 | 모멘텀 스크리너, 가치 스크리너 |
| `reporting` | 데이터 기반 포맷된 리포트 생성 | 주간 요약, 포트폴리오 리포트 |
| `workflow` | 다단계 프로세스 자동화 | 파이프라인 오케스트레이션, 배치 처리 |
| `monitoring` | 조건 추적 및 변화 알림 | 가격 알림, 포지션 모니터링 |

## 개인정보 및 데이터 처리

- 세션 로그는 이미 Claude에 전송된 사용자 상호작용을 포함하므로, LLM 처리에 대한 추가 개인정보 우려는 없음
- 원본 사용자 메시지는 백로그 저장 전에 반드시 추상화해야 함(원문 그대로 저장 금지)
- 사용자 이름이 포함된 파일 경로는 출력 아티팩트에서 제거해야 함
- 감사 목적의 원본 세션 UUID는 `logs/`(gitignored)에만 저장
- 커밋되는 파일(SKILL.md, references)에는 개인정보가 포함되면 안 됨
