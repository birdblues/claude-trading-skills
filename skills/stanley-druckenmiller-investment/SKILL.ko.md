---
name: stanley-druckenmiller-investment
description: Druckenmiller Strategy Synthesizer - 8개 상위 스킬 출력(Market Breadth, Uptrend Analysis, Market Top, Macro Regime, FTD Detector, VCP Screener, Theme Detector, CANSLIM Screener)을 통합해 확신도 점수(0-100), 패턴 분류, 자산 배분 권고를 생성합니다. 시장 확신도, 포트폴리오 포지셔닝, 자산 배분, 전략 통합, Druckenmiller 스타일 분석을 물을 때 사용하세요. "What is my conviction level?", "How should I position?", "Run the strategy synthesizer", "Druckenmiller analysis", "종합적인 시장 판단", "확신도 스코어", "포트폴리오 배분", "드러켄밀러 분석" 같은 질의에서 트리거됩니다.
---

# Druckenmiller Strategy Synthesizer

## 목적

8개 상위 분석 스킬(필수 5 + 선택 3)의 출력을 단일 종합 확신도 점수(0-100)로 합성하고, 시장을 4가지 Druckenmiller 패턴 중 하나로 분류하며, 실행 가능한 배분 권고를 생성합니다. 이 스킬은 다른 스킬의 구조화된 JSON 출력을 소비하는 **meta-skill**이며, 자체 API 키는 필요하지 않습니다.

## 이 스킬을 사용할 때

**English:**
- User asks "What's my overall conviction?" or "How should I be positioned?"
- User wants a unified view synthesizing breadth, uptrend, top risk, macro, and FTD signals
- User asks about Druckenmiller-style portfolio positioning
- User requests strategy synthesis after running individual analysis skills
- User asks "Should I increase or decrease exposure?"
- User wants pattern classification (policy pivot, distortion, contrarian, wait)

**Korean:**
- "종합적인 시장 판단은?" "현재 포지셔닝은?"
- 브레드스, 업트렌드, 천장 리스크, 매크로의 통합 판단
- "익스포저를 늘려야 하나? 줄여야 하나?"
- "드러켄밀러 분석을 실행해줘"
- 개별 스킬 실행 후 전략 통합 리포트

---

## 입력 요구사항

### 필수 스킬 (5)

| # | Skill | JSON Prefix | Role |
|---|-------|-------------|------|
| 1 | Market Breadth Analyzer | `market_breadth_` | 시장 참여 폭(Breadth) |
| 2 | Uptrend Analyzer | `uptrend_analysis_` | 섹터 업트렌드 비율 |
| 3 | Market Top Detector | `market_top_` | 분배/천장 리스크(방어) |
| 4 | Macro Regime Detector | `macro_regime_` | 매크로 체제 전환(1-2년 구조) |
| 5 | FTD Detector | `ftd_detector_` | 바닥 확인/재진입(공격) |

### 선택 스킬 (3)

| # | Skill | JSON Prefix | Role |
|---|-------|-------------|------|
| 6 | VCP Screener | `vcp_screener_` | 모멘텀 종목 셋업(VCP) |
| 7 | Theme Detector | `theme_detector_` | 테마/섹터 모멘텀 |
| 8 | CANSLIM Screener | `canslim_screener_` | 성장주 셋업 + M(Market Direction) |

먼저 필수 스킬을 실행하세요. synthesizer는 `reports/`의 JSON 출력을 읽습니다.

---

## 실행 워크플로우

### Phase 1: 선행조건 검증

`reports/`에 필수 5개 스킬의 JSON 리포트가 존재하고 최신(<72시간)인지 확인합니다. 누락된 것이 있으면 해당 스킬을 먼저 실행하세요.

### Phase 2: Strategy Synthesizer 실행

```bash
python3 skills/stanley-druckenmiller-investment/scripts/strategy_synthesizer.py \
  --reports-dir reports/ \
  --output-dir reports/ \
  --max-age 72
```

스크립트는 다음을 수행합니다:
1. 상위 스킬 JSON 리포트 로드 및 검증
2. 각 스킬의 정규화 신호 추출
3. 7개 컴포넌트 점수 계산(가중 0-100)
4. 종합 확신도 점수 계산
5. 4가지 Druckenmiller 패턴 중 하나로 분류
6. 목표 자산배분 및 포지션 사이징 생성
7. JSON/Markdown 리포트 출력

### Phase 3: 결과 제시

생성된 Markdown 리포트를 제시하며 다음을 강조합니다:
- 확신도 점수와 zone
- 탐지된 패턴과 match strength
- 가장 강한/약한 컴포넌트
- 목표 배분(equity/bonds/alternatives/cash)
- 포지션 사이징 파라미터
- 관련 Druckenmiller 원칙

### Phase 4: Druckenmiller 맥락 제공

철학적 맥락을 제공하기 위해 적절한 참고 문서를 로드합니다:
- **High conviction:** 집중 투자와 "fat pitch" 원칙 강조
- **Low conviction:** 자본 보전과 인내 강조
- **Pattern-specific:** `references/case-studies.md`의 관련 사례 적용

---

## 7-Component 점수 체계

| # | Component | Weight | Source Skill(s) | Key Signal |
|---|-----------|--------|----------------|------------|
| 1 | Market Structure | **18%** | Breadth + Uptrend | 시장 참여 구조 건강성 |
| 2 | Distribution Risk | **18%** | Market Top (inverted) | 기관 매도 리스크 |
| 3 | Bottom Confirmation | **12%** | FTD Detector | 조정 후 재진입 신호 |
| 4 | Macro Alignment | **18%** | Macro Regime | 체제 적합도 |
| 5 | Theme Quality | **12%** | Theme Detector | 섹터 모멘텀 품질 |
| 6 | Setup Availability | **10%** | VCP + CANSLIM | 고품질 종목 셋업 |
| 7 | Signal Convergence | **12%** | All 5 required | 스킬 간 합의도 |

## 4가지 패턴 분류

| Pattern | Trigger Conditions | Druckenmiller Principle |
|---------|-------------------|----------------------|
| Policy Pivot Anticipation | Transitional regime + high transition probability | "중앙은행과 유동성에 집중하라" |
| Unsustainable Distortion | Top risk >= 60 + contraction/inflationary regime | "틀렸을 때 얼마나 잃는지가 가장 중요" |
| Extreme Sentiment Contrarian | FTD confirmed + high top risk + bearish breadth | "가장 큰 돈은 베어마켓에서 벌린다" |
| Wait & Observe | Low conviction + mixed signals (default) | "안 보이면 휘두르지 마라" |

## 확신도 Zone 매핑

| Score | Zone | Exposure | Guidance |
|-------|------|----------|----------|
| 80-100 | Maximum Conviction | 90-100% | Fat pitch - 강하게 휘두르기 |
| 60-79 | High Conviction | 70-90% | 표준 리스크 관리 |
| 40-59 | Moderate Conviction | 50-70% | 포지션 사이즈 축소 |
| 20-39 | Low Conviction | 20-50% | 자본 보전, 최소 리스크 |
| 0-19 | Capital Preservation | 0-20% | 최대 방어 |

---

## 출력 파일

- `druckenmiller_strategy_YYYY-MM-DD_HHMMSS.json` — 구조화 분석 데이터
- `druckenmiller_strategy_YYYY-MM-DD_HHMMSS.md` — 사람이 읽기 쉬운 리포트

## API Requirements

**None.** 이 스킬은 다른 스킬의 JSON 출력을 읽습니다. API 키가 필요 없습니다.

## 참고 문서

### `references/investment-philosophy.md`
- Druckenmiller 핵심 원칙: 집중, 자본 보전, 18개월 시계열
- 정량 규칙: 일일 변동성 목표, 최대 포지션 사이즈
- 확신도 평가 시 철학적 맥락 제공이 필요할 때 로드

### `references/market-analysis-guide.md`
- 시그널→액션 매핑 프레임워크
- 배분 의사결정을 위한 매크로 체제 해석
- 컴포넌트 점수 또는 배분 근거 설명 시 로드

### `references/case-studies.md`
- 역사적 사례: 1992 GBP, 2000 tech bubble, 2008 crisis
- 실제 시장 조건 기반 패턴 분류 예시
- 역사적 유사성을 묻는 질문에 로드

### `references/conviction_matrix.md`
- 정량 시그널→액션 매핑 테이블
- Market Top Zone x Macro Regime 매트릭스
- 특정 시그널 조합에서 정밀 익스포저 수치가 필요할 때 로드

### 참고 문서 로드 시점
- **첫 사용:** 프레임워크 이해를 위해 `investment-philosophy.md`
- **배분 질문:** `market-analysis-guide.md` + `conviction_matrix.md`
- **역사 맥락:** `case-studies.md`
- **정기 실행:** 참고 문서 생략 가능 — 스크립트가 점수 계산 처리

---

## 다른 스킬과의 관계

| Skill | Relationship | Time Horizon |
|-------|-------------|-------------|
| Market Breadth Analyzer | Input (required) | Current snapshot |
| Uptrend Analyzer | Input (required) | Current snapshot |
| Market Top Detector | Input (required) | 2-8 weeks tactical |
| Macro Regime Detector | Input (required) | 1-2 years structural |
| FTD Detector | Input (required) | Days-weeks event |
| VCP Screener | Input (optional) | Setup-specific |
| Theme Detector | Input (optional) | Weeks-months thematic |
| CANSLIM Screener | Input (optional) | Setup-specific |
| **This Skill** | **Synthesizer** | **Unified conviction** |
