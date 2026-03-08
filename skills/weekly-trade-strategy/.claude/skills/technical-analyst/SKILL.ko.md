---
name: technical-analyst
description: 이 스킬은 주식, 주가지수, 암호화폐, 외환 페어의 주간 가격 차트를 분석할 때 사용해야 합니다. 사용자가 차트 이미지를 제공하고, 뉴스나 펀더멘털 요인 없이 차트 데이터만으로 technical analysis, 추세 식별, support/resistance 레벨, 시나리오 플래닝, 확률 평가를 요청할 때 이 스킬을 사용합니다.
---

# Technical Analyst

## Overview

이 스킬은 주간 가격 차트에 대한 종합 technical analysis를 수행합니다. 차트 이미지를 분석해 추세, support/resistance 레벨, moving average 관계, 거래량 패턴을 식별하고 향후 가격 움직임에 대한 확률 기반 시나리오를 개발합니다. 모든 분석은 뉴스, 펀더멘털, 시장 심리를 배제하고 차트 데이터만으로 객관적으로 수행합니다.

## Core Principles

1. **Pure Chart Analysis**: 차트에 보이는 technical data만으로 결론 도출
2. **Systematic Approach**: 모든 차트 분석에서 구조화된 방법론 적용
3. **Objective Assessment**: 주관적 편향을 배제하고 관측 가능한 패턴/데이터에 집중
4. **Probabilistic Scenarios**: 미래 가능성을 확률 가중 시나리오로 표현
5. **Sequential Processing**: 차트를 개별적으로 분석하고 즉시 결과 문서화

## Analysis Workflow

### Step 1: Receive Chart Images

사용자가 하나 이상의 주간 차트 이미지를 제공하면:

1. 모든 차트 이미지 수신 확인
2. 분석할 차트 개수 식별
3. 사용자 요청의 특정 포커스 영역 기록
4. 차트를 한 번에 하나씩 순차 분석 시작

### Step 2: Load Technical Analysis Framework

분석 시작 전에 종합 방법론 문서를 읽습니다:

```
Read: references/technical_analysis_framework.md
```

이 레퍼런스에는 다음에 대한 상세 가이드가 포함됩니다:
- 추세 분석 및 분류
- support/resistance 식별
- moving average 해석
- volume 분석
- chart pattern 및 candlestick 분석
- 시나리오 개발 및 확률 할당
- 분석 규율 및 객관성

### Step 3: Analyze Each Chart Systematically

각 차트 이미지에 대해 아래 순서로 체계적 분석을 수행합니다:

#### 3.1 Trend Analysis
- 추세 방향 식별(uptrend, downtrend, sideways)
- 추세 강도 평가(strong, moderate, weak)
- 추세 지속 기간 및 잠재적 exhaustion 신호 기록
- higher highs/lows 또는 lower highs/lows 패턴 점검

#### 3.2 Support and Resistance Analysis
- 중요한 수평 support 레벨 표시
- 중요한 수평 resistance 레벨 표시
- 추세선 기반 support/resistance 식별
- support-resistance role reversal 기록
- 여러 S/R 레벨이 겹치는 confluence zone 평가

#### 3.3 Moving Average Analysis
- 가격의 20-week, 50-week, 200-week MA 대비 위치 파악
- MA 정렬 상태 평가(bullish, bearish, neutral)
- MA 기울기 기록(rising, falling, flat)
- 최근 또는 예정된 MA crossover 식별
- MA가 동적 support/resistance로 작동하는지 관찰

#### 3.4 Volume Analysis
- 전반적 거래량 추세 평가(increasing, decreasing, stable)
- 거래량 스파이크 및 맥락 식별(support/resistance, breakout 구간)
- 가격과의 volume confirmation/divergence 확인
- volume climax 또는 exhaustion 패턴 기록

#### 3.5 Chart Patterns and Price Action
- reversal pattern 식별(hammer, shooting star, engulfing 등)
- continuation pattern 식별(flag, triangle 등)
- 중요한 candlestick formation 기록
- 최근 breakout/breakdown 관찰

#### 3.6 Synthesize Observations
- 모든 technical 요소를 통합해 현재 상태를 일관되게 정리
- 차트에 가장 큰 영향을 주는 핵심 요인 식별
- 상충 신호 또는 모호성 기록
- 향후 방향을 결정할 key level 설정

### Step 4: Develop Probabilistic Scenarios

각 차트에 대해 향후 가격 움직임의 2-4개 시나리오를 작성합니다:

#### Scenario Structure

각 시나리오는 반드시 포함해야 합니다:
1. **Scenario Name**: 명확한 설명형 제목(예: "Bull Case: Breakout Above Resistance")
2. **Probability Estimate**: technical factors 기반 확률(전체 시나리오 합 100%)
3. **Description**: 시나리오 전개 방식 설명
4. **Supporting Factors**: 근거 technical evidence(최소 2-3개)
5. **Target Levels**: 시나리오 실현 시 예상 가격 레벨
6. **Invalidation Level**: 시나리오를 무효화하는 구체 가격 레벨

#### Typical Scenario Framework

- **Base Case Scenario (40-60%)**: 현재 구조 기준 가장 가능성 높은 시나리오
- **Bull Case Scenario (20-40%)**: 상방 breakout이 필요한 낙관 시나리오
- **Bear Case Scenario (20-40%)**: 하방 breakdown이 필요한 비관 시나리오
- **Alternative Scenario (5-15%)**: 가능성은 낮지만 기술적으로 타당한 시나리오

supporting technical factors 강도에 따라 확률을 조정합니다. 확률은 현실적으로 배분하고 총합은 100%여야 합니다.

### Step 5: Generate Analysis Report

분석한 각 차트에 대해 템플릿 구조를 사용해 종합 markdown 리포트를 작성합니다:

```
Read and use as template: assets/analysis_template.md
```

리포트는 모든 섹션을 포함해야 합니다:
1. Chart Overview
2. Trend Analysis
3. Support and Resistance Levels
4. Moving Average Analysis
5. Volume Analysis
6. Chart Patterns and Price Action
7. Current Market Assessment
8. Scenario Analysis (확률 포함 2-4개 시나리오)
9. Summary
10. Disclaimer

**File Naming Convention**: 각 분석을 `[SYMBOL]_technical_analysis_[YYYY-MM-DD].md`로 저장

Example: `SPY_technical_analysis_2025-11-02.md`

### Step 6: Repeat for Multiple Charts

여러 차트가 제공된 경우:

1. 첫 번째 차트에 대해 전체 워크플로우(3-5단계) 완료
2. 분석 리포트 저장
3. 다음 차트로 진행
4. 모든 차트 분석 및 문서화 완료까지 반복

분석을 배치로 묶지 마세요. 다음 차트로 넘어가기 전에 각 리포트를 완성하고 저장해야 합니다.

## Quality Standards

### Objectivity Requirements

- 모든 분석은 관측 가능한 차트 데이터에 엄격히 기반
- 외부 정보(뉴스, 펀더멘털, 심리) 반영 금지
- "I think", "I feel" 같은 주관적 표현 지양
- 신호가 모호할 때 불확실성을 명확히 표현
- confirmation bias 방지를 위해 bullish/bearish 가능성을 모두 제시

### Completeness Requirements

- 템플릿의 모든 섹션을 다룸
- support, resistance, target에 구체 가격 레벨 제시
- 확률 추정은 technical factors로 정당화
- 각 시나리오마다 invalidation level 명시
- 분석의 제한사항/주의점 기록

### Clarity Requirements

- 정확한 technical terminology 사용
- 명확하고 전문적인 문장 구성
- 정보 구조를 논리적으로 배치
- 모호한 표현 대신 구체 가격 레벨 사용
- 시나리오는 서로 구분되고 상호 배타적으로 작성

## Example Usage Scenarios

**Example 1: Single Chart Analysis**
```
User: "Please analyze this weekly chart of the S&P 500"
[Provides chart image]

Analyst:
1. Confirms receipt of chart image
2. Reads technical_analysis_framework.md for methodology
3. Conducts systematic analysis (trend, S/R, MA, volume, patterns)
4. Develops 3 scenarios with probabilities (e.g., 55% bullish continuation, 30% consolidation, 15% reversal)
5. Generates comprehensive analysis report using template
6. Saves as SPY_technical_analysis_2025-11-02.md
```

**Example 2: Multiple Chart Analysis**
```
User: "Analyze these three charts: Bitcoin, Ethereum, and Nasdaq"
[Provides 3 chart images]

Analyst:
1. Confirms receipt of 3 charts
2. Reads technical_analysis_framework.md
3. Analyzes Bitcoin chart completely → Generates report → Saves as BTC_technical_analysis_2025-11-02.md
4. Analyzes Ethereum chart completely → Generates report → Saves as ETH_technical_analysis_2025-11-02.md
5. Analyzes Nasdaq chart completely → Generates report → Saves as NDX_technical_analysis_2025-11-02.md
6. Notifies user that all three analyses are complete
```

**Example 3: Focused Analysis Request**
```
User: "I'm particularly interested in whether this stock will break above resistance. Analyze the chart."
[Provides chart image]

Analyst:
1. Conducts full systematic analysis
2. Pays special attention to resistance levels and breakout probability
3. Develops scenarios with emphasis on breakout vs. rejection possibilities
4. Assigns probabilities based on volume, trend strength, and proximity to resistance
5. Generates complete report with focused scenario analysis
```

## Resources

이 스킬에는 다음 리소스가 포함됩니다:

### references/technical_analysis_framework.md

다음을 포함한 종합 technical analysis 방법론:
- 추세 분석 기준 및 분류
- support/resistance 식별 기법
- moving average 해석 가이드라인
- volume 분석 원칙
- chart pattern 인식
- 시나리오 개발 및 확률 할당 프레임워크
- 객관성/규율 리마인더

**Usage**: 체계적이고 객관적인 분석을 위해 분석 전에 이 파일을 읽습니다.

### assets/analysis_template.md

필수 섹션이 포함된 구조화 technical analysis 리포트 템플릿입니다.

**Usage**: 모든 분석 리포트에서 이 템플릿 구조를 사용합니다. 형식을 복사해 각 차트의 구체 결과를 채워 넣습니다.
