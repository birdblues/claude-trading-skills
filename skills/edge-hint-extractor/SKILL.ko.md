---
name: edge-hint-extractor
description: 일일 시장 관측값과 뉴스 반응에서 edge hint를 추출하고(선택적으로 LLM ideation 포함), 후속 concept synthesis 및 auto detection에 사용할 표준 `hints.yaml`을 생성합니다.
---

# Edge Hint Extractor

## 개요

원시 관측 신호(`market_summary`, `anomalies`, `news reactions`)를 구조화된 edge hint로 변환합니다.
이 스킬은 분리 워크플로 `observe -> abstract -> design -> pipeline`의 첫 단계입니다.

## 사용 시점

- 일일 시장 관측을 재사용 가능한 hint 객체로 바꾸고 싶을 때
- 현재 anomalies/news 컨텍스트에 제약된 LLM 아이디어가 필요할 때
- concept synthesis 또는 auto detection용 깔끔한 `hints.yaml` 입력이 필요할 때

## 사전 요구사항

- Python 3.9+
- `PyYAML`
- detector 실행의 선택 입력:
  - `market_summary.json`
  - `anomalies.json`
  - `news_reactions.csv` 또는 `news_reactions.json`

## 출력물

- `hints.yaml` (포함 내용):
  - `hints` list
  - 생성 metadata
  - rule/LLM hint 개수

## 워크플로

1. 관측 파일(`market_summary`, `anomalies`, 선택적 news reactions)을 수집합니다.
2. `scripts/build_hints.py`를 실행해 결정적(deterministic) 힌트를 생성합니다.
3. 선택적으로 `--llm-ideas-cmd`를 추가해 힌트를 보강합니다.
4. 생성된 `hints.yaml`을 concept synthesis 또는 auto detection에 전달합니다.

## 빠른 명령

Rule 기반만 사용 (`reports/edge_hint_extractor/hints.yaml`에 기본 출력):

```bash
python3 skills/edge-hint-extractor/scripts/build_hints.py \
  --market-summary /tmp/edge-auto/market_summary.json \
  --anomalies /tmp/edge-auto/anomalies.json \
  --news-reactions /tmp/news_reactions.csv \
  --as-of 2026-02-20 \
  --output-dir reports/
```

Rule + LLM 보강:

```bash
python3 skills/edge-hint-extractor/scripts/build_hints.py \
  --market-summary /tmp/edge-auto/market_summary.json \
  --anomalies /tmp/edge-auto/anomalies.json \
  --llm-ideas-cmd "python3 /path/to/llm_ideas_cli.py" \
  --output-dir reports/
```

## 리소스

- `skills/edge-hint-extractor/scripts/build_hints.py`
- `references/hints_schema.md`
