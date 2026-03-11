---
name: edge-hint-extractor
description: Extract edge hints from daily market observations and news reactions, with optional LLM ideation, and output canonical hints.yaml for downstream concept synthesis and auto detection.
---

# Edge Hint Extractor

## Overview

Convert raw observation signals (`market_summary`, `anomalies`, `news reactions`) into structured edge hints.
This skill is the first stage in the split workflow: `observe -> abstract -> design -> pipeline`.

## When to Use

- You want to turn daily market observations into reusable hint objects.
- You want LLM-generated ideas constrained by current anomalies/news context.
- You need a clean `hints.yaml` input for concept synthesis or auto detection.

## Prerequisites

- Python 3.9+
- `PyYAML`
- Optional inputs from detector run:
  - `market_summary.json`
  - `anomalies.json`
  - `news_reactions.csv` or `news_reactions.json`

## Output

- `hints.yaml` containing:
  - `hints` list
  - generation metadata
  - rule/LLM hint counts

## Workflow

### Step 0.5: Supabase Breaking News Context (Optional)

**Prerequisite:** Check if `mcp__supabase__execute_sql` tool is available.
If not available, skip directly to Step 1.

Invoke the `supabase-news-summarizer` agent:

```
Agent tool:
  subagent_type: "supabase-news-summarizer"
  prompt: |
    최근 10일간 Supabase public.news 테이블의 속보를 전량 수집하여
    에지 힌트 추출에 특화된 요약을 생성해주세요.

    분석 기간: [현재 날짜 - 10일] ~ [현재 날짜]

    다음을 반환해주세요:
    1. 시장 이상 현상 (비정상적 가격 반응, 예상 밖 실적)
    2. 섹터 디커플링 (상관관계 붕괴, 비동조화)
    3. 크레딧·유동성 스트레스 초기 신호
    4. 내러티브 전환점 (컨센서스 변화 징후)
    5. 크로스테마 상호작용
    6. 블라인드 스팟 경보 (사모/크레딧/시스템 리스크)
```

**Why agent:** 10일간 중요 속보 800+건 × detail 평균 824자 = ~665K자로 메인 컨텍스트에 직접 로드 불가. 에이전트가 자체 컨텍스트 윈도우에서 전량 처리 후 3,000자 이내 압축 요약을 반환.

**Agent output → Step 1 input:**
- `news_reactions.csv`가 없을 때 뉴스 컨텍스트 보충용으로 활용
- `news_reactions.csv`가 있어도 추가 컨텍스트로 에지 힌트 품질 향상에 기여

1. Gather observation files (`market_summary`, `anomalies`, optional news reactions).
2. Run `scripts/build_hints.py` to generate deterministic hints.
3. Optionally augment hints with LLM ideas via one of two methods:
   - a. `--llm-ideas-cmd` — pipe data to an external LLM CLI (subprocess).
   - b. `--llm-ideas-file PATH` — load pre-written hints from a YAML file (for Claude Code workflows where Claude generates hints itself).
4. Pass `hints.yaml` into concept synthesis or auto detection.

Note: `--llm-ideas-cmd` and `--llm-ideas-file` are mutually exclusive.

## Quick Commands

Rule-based only (default output to `reports/edge_hint_extractor/hints.yaml`):

```bash
python3 skills/edge-hint-extractor/scripts/build_hints.py \
  --market-summary /tmp/edge-auto/market_summary.json \
  --anomalies /tmp/edge-auto/anomalies.json \
  --news-reactions /tmp/news_reactions.csv \
  --as-of 2026-02-20 \
  --output-dir reports/
```

Rule + LLM augmentation (external CLI):

```bash
python3 skills/edge-hint-extractor/scripts/build_hints.py \
  --market-summary /tmp/edge-auto/market_summary.json \
  --anomalies /tmp/edge-auto/anomalies.json \
  --llm-ideas-cmd "python3 /path/to/llm_ideas_cli.py" \
  --output-dir reports/
```

Rule + LLM augmentation (pre-written file, for Claude Code):

```bash
python3 skills/edge-hint-extractor/scripts/build_hints.py \
  --market-summary /tmp/edge-auto/market_summary.json \
  --anomalies /tmp/edge-auto/anomalies.json \
  --llm-ideas-file /tmp/llm_hints.yaml \
  --output-dir reports/
```

## Resources

- `skills/edge-hint-extractor/scripts/build_hints.py`
- `references/hints_schema.md`
