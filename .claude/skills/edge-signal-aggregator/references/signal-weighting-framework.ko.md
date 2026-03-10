# Signal Weighting Framework

이 문서는 기본 signal weight의 근거, 점수 계산 방법론,
그리고 트레이딩 스타일에 맞춰 weight를 커스터마이즈하는 가이드를 설명합니다.

## 기본 Skill Weight

| Skill | Default Weight | Rationale |
|-------|----------------|-----------|
| edge-candidate-agent | 0.25 | Primary quantitative signal source with OHLCV anomaly detection |
| edge-concept-synthesizer | 0.20 | Synthesizes multiple inputs into coherent concepts |
| theme-detector | 0.15 | Identifies cross-sector thematic patterns |
| sector-analyst | 0.15 | Provides rotation and relative strength context |
| institutional-flow-tracker | 0.15 | Tracks smart money positioning via 13F filings |
| edge-hint-extractor | 0.10 | Supplementary hints that support other signals |

**합계: 1.00**

## Weight 근거

### edge-candidate-agent (0.25)

가장 높은 weight를 두는 이유:
- 정량적이며 데이터 기반 anomaly 탐지
- 구체적인 entry/exit 레벨이 있는 실행 가능한 ticket 생성
- 내러티브 편향에 가장 덜 취약
- signal에 타임스탬프가 있어 검증 가능

### edge-concept-synthesizer (0.20)

두 번째로 높은 이유:
- 여러 upstream 입력을 통합
- 테스트 가능한 hypothesis를 가진 구조화 edge concept 생성
- 다중 source corroboration이 필요

### theme-detector, sector-analyst, institutional-flow-tracker (각 0.15)

동일한 중간 weight를 주는 이유:
- 각각 서로 다른 분석 렌즈를 제공
- themes는 내러티브 모멘텀 포착
- sectors는 rotation flow 포착
- institutional flow는 smart money 포지셔닝 포착
- 셋 중 하나가 본질적으로 더 신뢰할 만하다고 단정하기 어려움

### edge-hint-extractor (0.10)

가장 낮은 weight를 두는 이유:
- hints는 제안적(suggestive)이지 결정적(definitive)이지 않음
- 다른 skill의 검증이 필요한 경우가 많음
- 아이디어 생성에는 유용하지만 conviction 용도로는 상대적으로 약함

## Composite Score 계산

집계된 signal의 composite conviction score는 다음과 같이 계산됩니다:

```
base_score = Σ(skill_weight × normalized_score) / Σ(skill_weight)
composite  = min(max_score, (base_score + agreement_bonus + merge_bonus) × recency_factor)
```

### 정규화 (Normalization)

서로 다른 skill의 raw score를 [0, 1]로 정규화합니다:
- 0-1 스케일 입력 (value <= 1.0): 그대로 사용
- 0-100 스케일 입력 (value <= 100.0): 100으로 나눔
- 범주형 grade: A=1.0, B=0.8, C=0.6, D=0.4, F=0.2
- 결측값: 0.0 (기여 없음)

### Agreement Bonus (가산)

dedup merge 후 여러 skill이 동일 signal에 동의하면:
- 2개 skill 동의: base_score에 +0.10
- 3개 이상 skill 동의: base_score에 +0.20

### Merge Bonus (가산)

중복이 병합될 때, 병합된 중복 1개당 base_score에 +0.05를 더합니다.

### Recency Factor (곱셈)

결합 점수에 multiplier로 적용:
- 24시간 이내: ×1.00
- 1-3일 경과: ×0.95
- 3-7일 경과: ×0.90
- 7일 이상: ×0.85

최종 composite는 1.0으로 상한 처리됩니다.

## Deduplication 로직

### 유사도 탐지

두 signal은 **direction이 같고** 아래 조건 중 **하나라도** 만족하면 중복으로 간주:
1. **Ticker overlap >= 30%** -- ticker 집합의 Jaccard overlap (기본값 0.30)
2. **Title similarity >= 0.60** -- title 단어 기반 Jaccard similarity (기본값 0.60)

참고: OR 로직을 사용하므로 ticker overlap이 높거나 title similarity가 높기만 해도 충분합니다.

### 병합 전략

중복이 감지되면:
1. raw score가 가장 높은 signal을 primary로 유지
2. 모든 중복의 contributing skill을 집계
3. 병합된 중복 1개당 composite score를 5% 가산(합의 신호)
4. 감사 추적을 위해 병합된 모든 signal을 로그에 기록

## Contradiction 탐지

### 정의

다음 조건에서 contradiction이 존재합니다:
1. 동일 ticker 또는 sector가 여러 signal에 등장
2. direction이 반대 (LONG vs SHORT)
3. time horizon이 겹침

### 심각도 레벨

| Level | Criteria | Action |
|-------|----------|--------|
| LOW | Different time horizons (e.g., short-term SHORT vs long-term LONG) | Log, no penalty |
| MEDIUM | Same horizon, different skills | Flag for review, -10% to both scores |
| HIGH | Same skill, opposite signals | Critical alert, exclude from ranking |

### 해결 힌트

aggregator는 다음 해결 힌트를 제공합니다:
- **Timeframe mismatch** -- 서로 다른 horizon에 적용되는 signal인지 확인
- **Sector vs stock** -- sector는 bearish지만 해당 sector 내 특정 종목은 bullish일 수 있음
- **Flow vs price** -- 기관 매수는 강한데 가격은 하락 중인지(축적 구간 가능성)

## Weight 커스터마이즈

### Momentum Traders용

단기 움직임을 포착하는 skill weight를 높입니다:
```yaml
weights:
  edge_candidate_agent: 0.30
  theme_detector: 0.25
  sector_analyst: 0.20
  edge_concept_synthesizer: 0.15
  institutional_flow_tracker: 0.05
  edge_hint_extractor: 0.05
```

### Value/Position Traders용

장기 포지셔닝을 포착하는 skill weight를 높입니다:
```yaml
weights:
  institutional_flow_tracker: 0.30
  edge_concept_synthesizer: 0.25
  edge_candidate_agent: 0.20
  sector_analyst: 0.15
  theme_detector: 0.05
  edge_hint_extractor: 0.05
```

### Thematic Investors용

내러티브 및 theme 탐지 weight를 높입니다:
```yaml
weights:
  theme_detector: 0.30
  edge_concept_synthesizer: 0.25
  sector_analyst: 0.20
  edge_candidate_agent: 0.15
  institutional_flow_tracker: 0.05
  edge_hint_extractor: 0.05
```

## 품질 지표

### Signal Confidence Factor

각 집계 signal은 다음 confidence breakdown을 포함합니다:

| Factor | Weight | Description |
|--------|--------|-------------|
| multi_skill_agreement | 0.35 | How many skills corroborate the signal |
| signal_strength | 0.40 | Average normalized score across contributing skills |
| recency | 0.25 | Time decay adjustment |

### 최소 임계값

권장 최소 conviction threshold:

| Trading Style | Min Conviction | Rationale |
|---------------|----------------|-----------|
| Aggressive | 0.50 | More signals, higher risk |
| Moderate | 0.65 | Balanced approach |
| Conservative | 0.80 | Fewer, higher-quality signals |

## 한계

1. **Garbage In, Garbage Out** -- 집계 품질은 upstream skill 품질에 의존
2. **Weight Sensitivity** -- 작은 weight 변경도 순위를 크게 바꿀 수 있음
3. **No Fundamental Override** -- aggregator는 fundamental thesis를 검증하지 않음
4. **Temporal Lag** -- 일부 skill(institutional flow)은 보고 지연이 본질적으로 존재

## Best Practices

1. **정기 Weight 튜닝** -- 백테스트 성과를 바탕으로 분기마다 weight를 점검/조정
2. **Contradiction 검토** -- HIGH 심각도 contradiction은 반드시 수동 검토
3. **Provenance 감사** -- 고신뢰 signal을 원본 source data까지 주기적으로 추적
4. **다양한 입력 확보** -- 의미 있는 합의를 위해 최소 3개 이상 upstream skill 실행 후 집계
