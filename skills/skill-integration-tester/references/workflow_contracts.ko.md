# 워크플로우 계약 레퍼런스

## 개요

멀티 스킬 워크플로우는 여러 스킬을 순차적으로 연결하며,
step N의 출력이 step N+1로 전달됩니다. **데이터 계약(data contract)**은
각 스킬이 무엇을 생성하고, 다운스트림 consumer가 무엇을 기대하는지 정의합니다.
계약이 깨지면(필드 누락, 형식 비호환, 파일 패턴 오류) handoff가 조용히 실패합니다.

## 계약 스키마

각 스킬 계약은 다음을 지정합니다:

| Field | 설명 |
|-------|-------------|
| `output_format` | 생성 파일 형식: `json`, `md`, `json+md`, `yaml` |
| `output_pattern` | 출력 파일명의 Glob 패턴 |
| `output_fields` | JSON/YAML 출력의 필수 top-level 필드 |
| `api_keys` | 스킬 실행에 필요한 환경 변수 |

## Handoff 계약 스키마

producer와 consumer 간 handoff 계약은 다음을 지정합니다:

| Field | 설명 |
|-------|-------------|
| `mechanism` | 데이터 전달 방식: `file_param` (CLI arg), `directory`, `stdin` |
| `param` | consumer가 입력 수용에 사용하는 CLI 파라미터 |
| `required_fields` | consumer가 producer 출력에서 읽는 필드 |
| `description` | 데이터 흐름에 대한 사람이 읽기 쉬운 설명 |

## 알려진 Handoff 계약

### Earnings Momentum Trading Pipeline

```
earnings-trade-analyzer → pead-screener
  mechanism: file_param (--candidates-json)
  required_fields: symbol, grade, gap_pct
```

PEAD Screener의 Mode B는
`--candidates-json`을 통해 earnings-trade-analyzer JSON 출력을 읽습니다.
consumer는 `grade >= B`로 필터링하고 `symbol`을 사용해
주간 캔들 데이터를 조회합니다.

### Edge Research Pipeline

```
edge-candidate-agent → edge-hint-extractor
  mechanism: file_param (--market-summary, --anomalies)
  required_fields: market_summary, anomalies

edge-hint-extractor → edge-concept-synthesizer
  mechanism: file_param (--hints)
  required_fields: hints

edge-concept-synthesizer → edge-strategy-designer
  mechanism: file_param (--concepts)
  required_fields: concepts

edge-strategy-designer → edge-strategy-reviewer
  mechanism: file_param (--drafts-dir)
  required_fields: strategy_name, entry, exit
```

### Trade Execution Pipeline

```
screener skills → position-sizer
  mechanism: manual (user copies entry/stop from screener output)
  required_fields: (none -- user provides values)

analysis skills → data-quality-checker
  mechanism: file_param (--file)
  required_fields: (validates markdown content, not specific fields)
```

## 명시적 계약이 없는 워크플로우

일부 워크플로우(Daily Market Monitoring, Weekly Strategy Review)는
단계 간 데이터를 전달하지 않는 독립 분석 단계로 구성됩니다.
각 단계는 독립 리포트를 생성합니다. 이런 워크플로우는
스킬 존재 여부와 네이밍 규약만 검증합니다.

## 파일 네이밍 규약

| Component | 규약 | 예시 |
|-----------|-----------|---------|
| 스킬 디렉터리 | lowercase-hyphen | `earnings-trade-analyzer` |
| Python 스크립트 | snake_case.py | `analyze_earnings_trades.py` |
| 출력 파일 | `<prefix>_YYYY-MM-DD_HHMMSS.{json,md}` | `integration_test_2026-03-01_120000.json` |
| SKILL.md name | 디렉터리 이름과 일치해야 함 | `name: earnings-trade-analyzer` |

## 새 계약 추가

새 멀티 스킬 워크플로우를 만들 때:

1. 각 스킬의 출력 계약(형식, 필드, 패턴)을 정의
2. 데이터 의존성이 있는 연속 단계의 handoff 계약을 정의
3. 해당 계약을 `test_workflows.py`의 `SKILL_CONTRACTS` 및 `HANDOFF_CONTRACTS`
   딕셔너리에 추가
4. integration tester를 실행해 새 워크플로우를 검증
