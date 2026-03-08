---
name: sector-analyst
description: 이 스킬은 섹터 및 산업 성과 차트를 분석해 시장 포지셔닝과 순환(rotation) 패턴을 평가할 때 사용해야 합니다. 사용자가 섹터 또는 산업의 성과 차트 이미지(1주 또는 1개월 기간)를 제공하고, 성과 데이터 기반 시장 사이클 평가, 섹터 순환 분석, 전략적 포지셔닝 추천을 요청할 때 이 스킬을 사용합니다. 모든 분석과 출력은 영어로 수행됩니다.
---

# Sector Analyst

## 개요

이 스킬은 섹터 및 산업 성과 차트에 대한 종합 분석을 통해 시장 사이클 포지셔닝을 식별하고 가능성 높은 순환 시나리오를 예측할 수 있게 합니다. 분석은 관측된 성과 데이터와 확립된 섹터 순환 원칙을 결합해 객관적인 시장 평가와 확률 기반 시나리오 예측을 제공합니다.

## 이 스킬을 사용해야 할 때

다음과 같은 경우 이 스킬을 사용합니다:
- 사용자가 섹터 성과 차트(일반적으로 1주 및 1개월 기간)를 제공한 경우
- 사용자가 상대 성과 데이터가 포함된 산업 성과 차트를 제공한 경우
- 사용자가 현재 시장 사이클 포지셔닝 분석을 요청한 경우
- 사용자가 섹터 순환 평가 또는 예측을 요청한 경우
- 사용자가 시장 포지셔닝을 위한 확률 가중 시나리오를 필요로 하는 경우

사용자 요청 예시:
- "이 섹터 성과 차트들을 분석해서 우리가 시장 사이클의 어디에 있는지 알려줘"
- "이 성과 차트를 바탕으로 다음에 어떤 섹터가 아웃퍼폼할까?"
- "이 데이터 기준으로 방어적 순환(defensive rotation) 확률이 어떻게 돼?"
- "이 섹터 및 산업 차트를 검토하고 시나리오 분석을 제공해줘"

## 분석 워크플로우

섹터/산업 성과 차트를 분석할 때 아래의 구조화된 워크플로우를 따릅니다:

### 1단계: 데이터 수집 및 관찰

먼저 제공된 모든 차트 이미지를 주의 깊게 검토하여 다음을 추출합니다:
- **섹터 수준 성과**: 어떤 섹터(Technology, Financials, Consumer Discretionary 등)가 아웃퍼폼/언더퍼폼하는지 식별
- **산업 수준 성과**: 강세 또는 약세를 보이는 특정 산업 기록
- **기간 비교**: 1주 vs 1개월 성과를 비교해 추세 일관성 또는 괴리 식별
- **움직임의 크기**: 상대 성과 차이의 규모 평가
- **움직임의 폭(Breadth)**: 성과가 집중되어 있는지 광범위한지 판단

차트를 분석하는 동안에는 영어로 사고합니다. 핵심 섹터 및 산업의 구체적인 수치 성과를 문서화합니다.

### 2단계: 시장 사이클 평가

분석에 반영하기 위해 섹터 순환 지식 베이스를 로드합니다:
- 시장 사이클 및 섹터 순환 프레임워크에 접근하기 위해 `references/sector_rotation.md`를 읽습니다
- 관측된 성과 패턴을 각 사이클 국면의 기대 패턴과 비교합니다:
  - Early Cycle Recovery
  - Mid Cycle Expansion
  - Late Cycle
  - Recession

다음을 통해 현재 관측치와 가장 잘 맞는 사이클 국면을 식별합니다:
- 아웃퍼폼 섹터를 전형적인 사이클 리더에 매핑
- 언더퍼폼 섹터를 전형적인 사이클 래가드(laggard)에 매핑
- 여러 섹터 전반의 일관성 평가
- 방어주 vs 경기민감주 성과와의 정합성 평가

### 3단계: 현재 상황 분석

관측 결과를 종합해 객관적인 평가를 작성합니다:
- 현재 성과가 어떤 시장 사이클 국면과 가장 유사한지 명시
- 이를 뒷받침하는 근거(어떤 섹터/산업이 해당 관점을 확인하는지) 강조
- 상충 신호 또는 비정상 패턴 기록
- 신호 일관성 기반 신뢰도 수준 평가

데이터 기반 언어와 성과 수치에 대한 구체적 참조를 사용합니다.

### 4단계: 시나리오 개발

섹터 순환 원칙과 현재 포지셔닝을 바탕으로 다음 국면에 대한 2~4개의 잠재 시나리오를 개발합니다:

각 시나리오마다:
- 시장 사이클 전환을 설명
- 어떤 섹터가 아웃퍼폼할 가능성이 높은지 식별
- 어떤 섹터가 언더퍼폼할 가능성이 높은지 식별
- 이 시나리오를 확인해 줄 촉매 또는 조건을 명시
- 확률 할당(`sector_rotation.md`의 Probability Assessment Framework 참조)

시나리오는 가장 가능성 높은 것(최고 확률)부터 대안/역발상 시나리오까지 포함해야 합니다.

### 5단계: 출력 생성

다음 섹션으로 구성된 구조화된 Markdown 문서를 생성합니다:

**필수 섹션:**
1. **Executive Summary**: 핵심 결과를 2~3문장으로 요약
2. **Current Situation**: 현재 성과 패턴과 시장 사이클 포지셔닝에 대한 상세 분석
3. **Supporting Evidence**: 사이클 평가를 뒷받침하는 구체적 섹터/산업 성과 데이터
4. **Scenario Analysis**: 설명과 확률 할당이 포함된 2~4개 시나리오
5. **Recommended Positioning**: 시나리오 확률에 기반한 전략/전술 포지셔닝 추천
6. **Key Risks**: 모니터링해야 할 주요 리스크 또는 상충 신호

## 출력 형식

다음 네이밍 규칙으로 분석 결과를 Markdown 파일로 저장합니다: `sector_analysis_YYYY-MM-DD.md`

아래 구조를 사용합니다:

```markdown
# Sector Performance Analysis - [Date]

## Executive Summary

[2-3 sentences summarizing key findings]

## Current Situation

### Market Cycle Assessment
[Which cycle phase and why]

### Performance Patterns Observed

#### 1-Week Performance
[Analysis of recent performance]

#### 1-Month Performance
[Analysis of medium-term trends]

#### Sector-Level Analysis
[Detailed breakdown by sector]

#### Industry-Level Analysis
[Notable industry-specific observations]

## Supporting Evidence

### Confirming Signals
- [List data points supporting cycle assessment]

### Contradictory Signals
- [List any conflicting indicators]

## Scenario Analysis

### Scenario 1: [Name] (Probability: XX%)
**Description**: [What happens]
**Outperformers**: [Sectors/industries]
**Underperformers**: [Sectors/industries]
**Catalysts**: [What would confirm this scenario]

### Scenario 2: [Name] (Probability: XX%)
[Repeat structure]

[Additional scenarios as appropriate]

## Recommended Positioning

### Strategic Positioning (Medium-term)
[Sector allocation recommendations]

### Tactical Positioning (Short-term)
[Specific adjustments or opportunities]

## Key Risks and Monitoring Points

[What to watch that could invalidate the analysis]

---
*Analysis Date: [Date]*
*Data Period: [Timeframe of charts analyzed]*
```

## 핵심 분석 원칙

분석 수행 시:

1. **객관성 우선**: 선입견이 아니라 데이터가 결론을 이끌게 합니다
2. **확률적 사고**: 확률 범위를 통해 불확실성을 표현합니다
3. **다중 기간**: 추세 확인을 위해 1주 및 1개월 데이터를 비교합니다
4. **상대 성과**: 절대 수익률이 아닌 상대 강도에 집중합니다
5. **Breadth 중요성**: 광범위한 움직임은 고립된 움직임보다 더 중요합니다
6. **절대화 금지**: 시장은 교과서적 패턴을 정확히 따르지 않는 경우가 많습니다
7. **역사적 맥락**: 전형적 순환 패턴을 참조하되 고유성을 인정합니다

## 확률 가이드라인

증거 강도에 따라 다음 확률 범위를 적용합니다:

- **70-85%**: 여러 섹터와 기간에서 다수의 확인 신호가 있는 강한 증거
- **50-70%**: 일부 확인 신호는 있으나 혼재된 지표가 있는 중간 수준 증거
- **30-50%**: 제한적이거나 상충 신호가 있는 약한 증거
- **15-30%**: 현재 지표와 반대되지만 가능한 투기적 시나리오

모든 시나리오의 총확률은 대략 100%가 되어야 합니다.

## 리소스

### references/
- `sector_rotation.md` - 시장 사이클 국면, 전형적 섹터 성과 패턴, 확률 평가 프레임워크를 포괄하는 종합 지식 베이스

### assets/
예상 입력 형식을 보여주는 샘플 차트:
- `sector_performance.jpeg` - 섹터 수준 성과 차트 예시(1주 및 1개월)
- `industory_performance_1.jpeg` - 산업 성과 차트 예시(아웃퍼포머)
- `industory_performance_2.jpeg` - 산업 성과 차트 예시(언더퍼포머)

이 샘플들은 본 스킬이 분석하는 시각 데이터 유형을 보여줍니다. 사용자가 제공하는 차트 형식은 다를 수 있으나, 유사한 상대 성과 정보를 포함해야 합니다.

## 중요 참고사항

- 모든 분석 사고 과정은 영어로 수행해야 합니다
- 출력 Markdown 파일은 영어로 작성해야 합니다
- 각 분석마다 섹터 순환 지식 베이스를 참조합니다
- 객관성을 유지하고 확증 편향을 피합니다
- 새로운 데이터가 제공되면 확률 평가를 업데이트합니다
- 차트는 일반적으로 1주 및 1개월 기간의 성과를 보여줍니다
