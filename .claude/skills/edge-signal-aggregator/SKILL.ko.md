---
name: edge-signal-aggregator
description: 여러 edge 탐색 스킬(edge-candidate-agent, theme-detector, sector-analyst, institutional-flow-tracker)의 signal을 가중치 점수화, 중복 제거, 모순 탐지를 통해 통합하고 우선순위 conviction dashboard로 정렬합니다.
---

# Edge Signal Aggregator

## 개요

여러 upstream edge-finding skill의 출력을 단일 weighted conviction dashboard로 통합합니다.
이 스킬은 설정 가능한 signal weight를 적용하고, 겹치는 theme를 dedup하며,
skill 간 모순을 표시하고, aggregate confidence score 기준으로 composite edge idea를
순위화합니다.
결과물은 각 기여 skill에 대한 provenance 링크를 포함한 우선순위 edge shortlist입니다.

## 사용 시점

- 여러 edge-finding skill을 실행한 뒤 통합 뷰가 필요할 때
- edge-candidate-agent, theme-detector, sector-analyst,
  institutional-flow-tracker signal을 통합할 때
- 다중 signal source 기반으로 포트폴리오 배분 결정을 내리기 전
- 서로 다른 분석 접근 간 모순을 식별할 때
- 어떤 edge idea를 더 깊게 연구할지 우선순위를 정할 때

## 사전 요구사항

- Python 3.9+
- API 키 불필요(다른 skill의 로컬 JSON/YAML 파일 처리)
- 의존성: `pyyaml` (대부분 환경에서 기본 제공)

## 워크플로

### Step 1: Upstream Skill 출력 수집

집계하려는 upstream skill의 출력 파일을 모읍니다:
- edge-candidate-agent의 `reports/edge_candidate_*.json`
- edge-concept-synthesizer의 `reports/edge_concepts_*.yaml`
- theme-detector의 `reports/theme_detector_*.json`
- sector-analyst의 `reports/sector_analyst_*.json`
- institutional-flow-tracker의 `reports/institutional_flow_*.json`
- edge-hint-extractor의 `reports/edge_hints_*.yaml`

### Step 2: Signal 집계 실행

upstream 출력 경로를 전달해 aggregator 스크립트를 실행합니다:

```bash
python3 skills/edge-signal-aggregator/scripts/aggregate_signals.py \
  --edge-candidates reports/edge_candidate_agent_*.json \
  --edge-concepts reports/edge_concepts_*.yaml \
  --themes reports/theme_detector_*.json \
  --sectors reports/sector_analyst_*.json \
  --institutional reports/institutional_flow_*.json \
  --hints reports/edge_hints_*.yaml \
  --output-dir reports/
```

선택 사항: 커스텀 weight 설정 사용

```bash
python3 skills/edge-signal-aggregator/scripts/aggregate_signals.py \
  --edge-candidates reports/edge_candidate_agent_*.json \
  --weights-config skills/edge-signal-aggregator/assets/custom_weights.yaml \
  --output-dir reports/
```

### Step 3: 집계 Dashboard 검토

생성된 리포트를 열어 다음을 검토합니다:
1. **Ranked Edge Ideas** - composite conviction score 기준 정렬
2. **Signal Provenance** - 각 아이디어에 어떤 skill이 기여했는지
3. **Contradictions** - 수동 검토가 필요한 상충 signal
4. **Deduplication Log** - 병합된 중복 theme

### Step 4: 고신뢰 Signal 실행

최소 conviction 임계값으로 shortlist를 필터링합니다:

```bash
python3 skills/edge-signal-aggregator/scripts/aggregate_signals.py \
  --edge-candidates reports/edge_candidate_agent_*.json \
  --min-conviction 0.7 \
  --output-dir reports/
```

## 출력 형식

### JSON 리포트

```json
{
  "schema_version": "1.0",
  "generated_at": "2026-03-02T07:00:00Z",
  "config": {
    "weights": {
      "edge_candidate_agent": 0.25,
      "edge_concept_synthesizer": 0.20,
      "theme_detector": 0.15,
      "sector_analyst": 0.15,
      "institutional_flow_tracker": 0.15,
      "edge_hint_extractor": 0.10
    },
    "min_conviction": 0.5,
    "dedup_similarity_threshold": 0.8
  },
  "summary": {
    "total_input_signals": 42,
    "unique_signals_after_dedup": 28,
    "contradictions_found": 3,
    "signals_above_threshold": 12
  },
  "ranked_signals": [
    {
      "rank": 1,
      "signal_id": "sig_001",
      "title": "AI Infrastructure Capex Acceleration",
      "composite_score": 0.87,
      "contributing_skills": [
        {
          "skill": "edge_candidate_agent",
          "signal_ref": "ticket_2026-03-01_001",
          "raw_score": 0.92,
          "weighted_contribution": 0.23
        },
        {
          "skill": "theme_detector",
          "signal_ref": "theme_ai_infra",
          "raw_score": 0.85,
          "weighted_contribution": 0.13
        }
      ],
      "tickers": ["NVDA", "AMD", "AVGO"],
      "direction": "LONG",
      "time_horizon": "3-6 months",
      "confidence_breakdown": {
        "multi_skill_agreement": 0.30,
        "signal_strength": 0.35,
        "recency": 0.22
      }
    }
  ],
  "contradictions": [
    {
      "contradiction_id": "contra_001",
      "description": "Conflicting sector view on Energy",
      "skill_a": {
        "skill": "sector_analyst",
        "signal": "Energy sector bearish rotation",
        "direction": "SHORT"
      },
      "skill_b": {
        "skill": "institutional_flow_tracker",
        "signal": "Heavy institutional buying in XLE",
        "direction": "LONG"
      },
      "resolution_hint": "Check timeframe mismatch (short-term vs long-term)"
    }
  ],
  "deduplication_log": [
    {
      "merged_into": "sig_001",
      "duplicates_removed": ["theme_detector:ai_compute", "edge_hints:datacenter_demand"],
      "similarity_score": 0.92
    }
  ]
}
```

### Markdown 리포트

markdown 리포트는 사람이 읽기 쉬운 dashboard를 제공합니다:

```markdown
# Edge Signal Aggregator Dashboard
**Generated:** 2026-03-02 07:00 UTC

## Summary
- Total Input Signals: 42
- Unique After Dedup: 28
- Contradictions: 3
- High Conviction (>0.7): 12

## Top 10 Edge Ideas by Conviction

### 1. AI Infrastructure Capex Acceleration (Score: 0.87)
- **Tickers:** NVDA, AMD, AVGO
- **Direction:** LONG | **Horizon:** 3-6 months
- **Contributing Skills:**
  - edge-candidate-agent: 0.92 (ticket_2026-03-01_001)
  - theme-detector: 0.85 (theme_ai_infra)
- **Confidence Breakdown:** Agreement 0.30 | Strength 0.35 | Recency 0.22

...

## Contradictions Requiring Review

### Energy Sector Conflict
- **sector-analyst:** Bearish rotation (SHORT)
- **institutional-flow-tracker:** Heavy buying XLE (LONG)
- **Hint:** Check timeframe mismatch

## Deduplication Summary
- 14 signals merged into 8 unique themes
- Average similarity of merged signals: 0.89
```

리포트는 `reports/`에 다음 파일명으로 저장됩니다:
- `edge_signal_aggregator_YYYY-MM-DD_HHMMSS.json`
- `edge_signal_aggregator_YYYY-MM-DD_HHMMSS.md`

## 리소스

- `scripts/aggregate_signals.py` -- CLI 인터페이스를 포함한 메인 집계 스크립트
- `references/signal-weighting-framework.md` -- 기본 weight 및 점수화 방법론의 근거
- `assets/default_weights.yaml` -- 기본 skill weight 설정

## 핵심 원칙

1. **Provenance Tracking** -- 모든 집계 signal은 source skill과 원본 reference로 역추적 가능
2. **Contradiction Transparency** -- 상충 signal을 숨기지 않고 표시해 정보에 근거한 판단 지원
3. **Configurable Weights** -- 기본 weight는 일반적 신뢰도를 반영하되 사용자별 커스터마이즈 가능
4. **Deduplication Without Loss** -- 병합 signal에도 모든 원본 source reference를 유지
5. **Actionable Output** -- 각 아이디어별 ticker, direction, time horizon이 명확한 ranked list 제공
