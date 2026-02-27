---
name: scenario-analyzer
description: |
  뉴스 헤드라인을 입력으로 18개월 시나리오를 분석하는 스킬.
  scenario-analyst 에이전트로 주요 분석을 실행하고,
  strategy-reviewer 에이전트로 세컨드 오피니언을 취득.
  1차·2차·3차 영향, 추천 종목, 리뷰를 포함한 포괄적 리포트를 한국어로 생성.
  사용 예: /scenario-analyzer "Fed raises rates by 50bp"
  트리거: 뉴스 분석, 시나리오 분석, 18개월 전망, 중장기 투자 전략
---

# Headline Scenario Analyzer

## Overview

이 스킬은 뉴스 헤드라인을 기점으로 중장기(18개월)의 투자 시나리오를 분석합니다.
2개의 전문 에이전트(`scenario-analyst`와 `strategy-reviewer`)를 순차적으로 호출하여,
다각적인 분석과 비판적 리뷰를 통합한 포괄적인 리포트를 생성합니다.

## When to Use This Skill

다음의 경우에 이 스킬을 사용하십시오:

- 뉴스 헤드라인에서 중장기 투자 영향을 분석하고 싶을 때
- 18개월 후의 시나리오를 복수 구축하고 싶을 때
- 섹터·종목에 대한 영향을 1차/2차/3차로 정리하고 싶을 때
- 세컨드 오피니언을 포함한 포괄적인 분석이 필요할 때
- 한국어로 리포트 출력이 필요할 때

**사용 예:**
```
/headline-scenario-analyzer "Fed raises interest rates by 50bp, signals more hikes ahead"
/headline-scenario-analyzer "China announces new tariffs on US semiconductors"
/headline-scenario-analyzer "OPEC+ agrees to cut oil production by 2 million barrels per day"
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Skill (오케스트레이터)                              │
│                                                                      │
│  Phase 1: 준비                                                       │
│  ├─ 헤드라인 해석                                                     │
│  ├─ 이벤트 타입 분류                                                  │
│  └─ 레퍼런스 읽기                                                     │
│                                                                      │
│  Phase 2: 에이전트 호출                                               │
│  ├─ scenario-analyst (주요 분석)                                     │
│  └─ strategy-reviewer (세컨드 오피니언)                              │
│                                                                      │
│  Phase 3: 통합·리포트 생성                                            │
│  └─ reports/scenario_analysis_<topic>_YYYYMMDD.md                   │
└─────────────────────────────────────────────────────────────────────┘
```

## Workflow

### Phase 1: 준비

#### Step 1.1: 헤드라인 해석

사용자가 입력한 헤드라인을 해석합니다.

1. **헤드라인 확인**
   - 인수로 헤드라인이 전달되었는지 확인
   - 전달되지 않은 경우 사용자에게 입력을 요청

2. **키워드 추출**
   - 주요 엔티티(기업명, 국가명, 기관명)
   - 수치 데이터(금리, 가격, 수량)
   - 액션(인상, 인하, 발표, 합의 등)

#### Step 1.2: 이벤트 타입 분류

헤드라인을 다음 카테고리로 분류:

| 카테고리 | 예 |
|---------|-----|
| 금융 정책 | FOMC, ECB, 한은, 금리 인상, 금리 인하, QE/QT |
| 지정학 | 전쟁, 제재, 관세, 무역 마찰 |
| 규제·정책 | 환경 규제, 금융 규제, 독점 금지법 |
| 테크놀로지 | AI, EV, 재생에너지, 반도체 |
| 커머디티 | 원유, 금, 구리, 농산물 |
| 기업·M&A | 인수, 파산, 실적, 업계 재편 |

#### Step 1.3: 레퍼런스 읽기

이벤트 타입에 기반하여 관련 레퍼런스를 읽어들입니다:

```
Read references/headline_event_patterns.md
Read references/sector_sensitivity_matrix.md
Read references/scenario_playbooks.md
```

**레퍼런스 내용:**
- `headline_event_patterns.md`: 과거 이벤트 패턴과 시장 반응
- `sector_sensitivity_matrix.md`: 이벤트 x 섹터의 영향도 매트릭스
- `scenario_playbooks.md`: 시나리오 구축 템플릿과 베스트 프랙티스

---

### Phase 2: 에이전트 호출

#### Step 2.1: scenario-analyst 호출

Task tool을 사용하여 메인 분석 에이전트를 호출합니다.

```
Task tool:
- subagent_type: "scenario-analyst"
- prompt: |
    다음 헤드라인에 대해 18개월 시나리오 분석을 실행해 주세요.

    ## 대상 헤드라인
    [입력된 헤드라인]

    ## 이벤트 타입
    [분류 결과]

    ## 레퍼런스 정보
    [읽어들인 레퍼런스 요약]

    ## 분석 요건
    1. WebSearch로 지난 2주간의 관련 뉴스를 수집
    2. Base/Bull/Bear의 3 시나리오를 구축 (확률 합계 100%)
    3. 1차/2차/3차 영향을 섹터별로 분석
    4. 포지티브/네거티브 영향 종목을 각 3-5 종목 선정 (미국 시장만)
    5. 모두 한국어로 출력
```

**기대 출력:**
- 관련 뉴스 기사 리스트
- 3 시나리오(Base/Bull/Bear)의 상세
- 섹터 영향 분석(1차/2차/3차)
- 종목 추천 리스트

#### Step 2.2: strategy-reviewer 호출

scenario-analyst의 분석 결과를 받아 리뷰 에이전트를 호출합니다.

```
Task tool:
- subagent_type: "strategy-reviewer"
- prompt: |
    다음 시나리오 분석을 리뷰해 주세요.

    ## 대상 헤드라인
    [입력된 헤드라인]

    ## 분석 결과
    [scenario-analyst의 출력 전문]

    ## 리뷰 요건
    다음 관점에서 리뷰를 실시:
    1. 누락된 섹터/종목
    2. 시나리오 확률 배분의 타당성
    3. 영향 분석의 논리적 정합성
    4. 낙관/비관 바이어스 검출
    5. 대안 시나리오 제안
    6. 타임라인의 현실성

    건설적이고 구체적인 피드백을 한국어로 출력해 주세요.
```

**기대 출력:**
- 누락 사항 지적
- 시나리오 확률에 대한 의견
- 바이어스 지적
- 대안 시나리오 제안
- 최종 추천 사항

---

### Phase 3: 통합·리포트 생성

#### Step 3.1: 결과 통합

양 에이전트의 출력을 통합하여 최종 투자 판단을 작성합니다.

**통합 포인트:**
1. 리뷰에서 지적된 누락 사항을 보완
2. 확률 배분 조정(필요한 경우)
3. 바이어스를 고려한 최종 판단
4. 구체적인 액션 플랜 수립

#### Step 3.2: 리포트 생성

다음 형식으로 최종 리포트를 생성하고 파일에 저장합니다.

**저장 위치:** `reports/scenario_analysis_<topic>_YYYYMMDD.md`

```markdown
# 헤드라인·시나리오 분석 리포트

**분석 일시**: YYYY-MM-DD HH:MM
**대상 헤드라인**: [입력된 헤드라인]
**이벤트 타입**: [분류 카테고리]

---

## 1. 관련 뉴스 기사
[scenario-analyst가 수집한 뉴스 리스트]

## 2. 예상 시나리오 개요 (18개월 후까지)

### Base Case (XX% 확률)
[시나리오 상세]

### Bull Case (XX% 확률)
[시나리오 상세]

### Bear Case (XX% 확률)
[시나리오 상세]

## 3. 섹터·업종에 대한 영향

### 1차적 영향 (직접적)
[영향 테이블]

### 2차적 영향 (밸류체인·관련 산업)
[영향 테이블]

### 3차적 영향 (매크로·규제·기술)
[영향 테이블]

## 4. 포지티브 영향이 예상되는 종목 (3-5 종목)
[종목 테이블]

## 5. 네거티브 영향이 예상되는 종목 (3-5 종목)
[종목 테이블]

## 6. 세컨드 오피니언·리뷰
[strategy-reviewer의 출력]

## 7. 최종 투자 판단·시사점

### 추천 액션
[리뷰를 반영한 구체적 액션]

### 리스크 요인
[주요 리스크 열거]

### 모니터링 포인트
[팔로우해야 할 지표·이벤트]

---
**생성**: scenario-analyzer skill
**에이전트**: scenario-analyst, strategy-reviewer
```

#### Step 3.3: 리포트 저장

1. `reports/` 디렉토리가 존재하지 않는 경우 생성
2. `scenario_analysis_<topic>_YYYYMMDD.md`로 저장 (예: `scenario_analysis_venezuela_20260104.md`)
3. 저장 완료를 사용자에게 알림
4. **프로젝트 루트에 직접 저장하지 않을 것**

---

## Resources

### References
- `references/headline_event_patterns.md` - 이벤트 패턴과 시장 반응
- `references/sector_sensitivity_matrix.md` - 섹터 민감도 매트릭스
- `references/scenario_playbooks.md` - 시나리오 구축 템플릿

### Agents
- `scenario-analyst` - 메인 시나리오 분석
- `strategy-reviewer` - 세컨드 오피니언·리뷰

---

## Important Notes

### 언어
- 모든 분석·출력은 **한국어**로 수행
- 종목 티커는 영어 표기를 유지

### 대상 시장
- 종목 선정은 **미국 시장 상장 종목만**
- ADR 포함

### 시간축
- 시나리오는 **18개월**을 대상
- 0-6개월/6-12개월/12-18개월의 3페이즈로 기술

### 확률 배분
- Base + Bull + Bear = **100%**
- 각 시나리오의 확률은 근거와 함께 기술

### 세컨드 오피니언
- **필수**로 실행 (strategy-reviewer를 항상 호출)
- 리뷰 결과는 최종 판단에 반영

### 출력 위치 (중요)
- **반드시** `reports/` 디렉토리 하위에 저장할 것
- 경로: `reports/scenario_analysis_<topic>_YYYYMMDD.md`
- 예: `reports/scenario_analysis_fed_rate_hike_20260104.md`
- `reports/` 디렉토리가 존재하지 않는 경우 생성할 것
- **프로젝트 루트에 직접 저장해서는 안 됨**

---

## Quality Checklist

리포트 완성 전에 다음을 확인:

- [ ] 헤드라인이 정확하게 해석되었는가
- [ ] 이벤트 타입 분류가 적절한가
- [ ] 3 시나리오의 확률 합계가 100%인가
- [ ] 1차/2차/3차 영향의 논리적 연결이 있는가
- [ ] 종목 선정에 구체적인 근거가 있는가
- [ ] strategy-reviewer의 리뷰가 포함되어 있는가
- [ ] 리뷰를 반영한 최종 판단이 기재되어 있는가
- [ ] 리포트가 올바른 경로에 저장되었는가
