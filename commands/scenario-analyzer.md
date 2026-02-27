---
description: "뉴스 헤드라인으로부터 18개월 시나리오를 분석. 1차/2차/3차 영향, 추천 종목, 세컨드 오피니언을 포함한 포괄적 리포트를 한국어로 생성."
argument-hint: "<headline>"
---

# Headline Scenario Analyzer

뉴스 헤드라인으로부터 18개월 시나리오를 분석하고, 섹터 및 종목에 대한 영향을 평가합니다.

## 인수

```
$ARGUMENTS
```

**인수 해석**:
- 헤드라인이 포함된 경우: 해당 헤드라인을 분석 대상으로 한다
- 인수가 비어 있는 경우: 사용자에게 헤드라인 입력을 요청한다

**사용 예시**:
- `/headline-scenario-analyzer Fed raises rates by 50bp` -> Fed 금리 인상 시나리오를 분석
- `/headline-scenario-analyzer China announces new tariffs on US semiconductors` -> 관세 시나리오를 분석
- `/headline-scenario-analyzer OPEC+ agrees to cut oil production` -> 원유 감산 시나리오를 분석
- `/headline-scenario-analyzer` -> 헤드라인 입력을 요청한 후 분석

## 분석 내용

| 항목 | 설명 |
|------|------|
| **관련 뉴스** | WebSearch로 과거 2주간의 관련 기사를 수집 |
| **시나리오** | Base/Bull/Bear의 3가지 시나리오 (확률 포함) |
| **영향 분석** | 1차/2차/3차 섹터 영향 |
| **종목 선정** | 포지티브/네거티브 각 3-5종목 (미국 시장) |
| **리뷰** | 세컨드 오피니언 (누락/편향 지적) |

## 실행 절차

1. **헤드라인 분석**:
   - 인수에서 헤드라인을 추출
   - 인수가 비어 있는 경우 사용자에게 입력을 요청
   - 이벤트 유형을 분류 (금융정책/지정학/규제/테크놀로지/원자재/기업)

2. **레퍼런스 로드**:
   ```
   Read skills/headline-scenario-analyzer/references/headline_event_patterns.md
   Read skills/headline-scenario-analyzer/references/sector_sensitivity_matrix.md
   Read skills/headline-scenario-analyzer/references/scenario_playbooks.md
   ```

3. **메인 분석 (headline-scenario-analyst 에이전트)**:
   ```
   Task tool:
   - subagent_type: "headline-scenario-analyst"
   - prompt: 헤드라인 + 이벤트 유형 + 레퍼런스 정보
   ```

   출력:
   - 관련 뉴스 기사 목록
   - 3가지 시나리오 (Base/Bull/Bear)
   - 섹터 영향 분석 (1차/2차/3차)
   - 종목 추천 목록

4. **세컨드 오피니언 (strategy-reviewer 에이전트)**:
   ```
   Task tool:
   - subagent_type: "strategy-reviewer"
   - prompt: Step 3의 분석 결과 전문
   ```

   출력:
   - 누락 지적
   - 시나리오 확률에 대한 의견
   - 편향 탐지
   - 대안 시나리오 제안

5. **리포트 생성**:
   - 양 에이전트의 결과를 통합
   - 최종 투자 판단을 추가 기술
   - `reports/YYYY-MM-DD/headline-scenario-analysis.md`에 저장

## 참조 리소스

- `skills/headline-scenario-analyzer/references/headline_event_patterns.md` - 이벤트 패턴
- `skills/headline-scenario-analyzer/references/sector_sensitivity_matrix.md` - 섹터 감응도
- `skills/headline-scenario-analyzer/references/scenario_playbooks.md` - 시나리오 템플릿

## 중요한 지시

- **언어**: 모든 분석/출력은 **한국어**로 수행
- **대상 시장**: 종목 선정은 **미국 시장 상장 종목만**
- **시간축**: 시나리오는 **18개월**을 대상
- **확률**: Base + Bull + Bear = **100%**
- **세컨드 오피니언**: **필수**로 실행 (항상 strategy-reviewer를 호출)

## 출력

최종적으로 `헤드라인 시나리오 분석 리포트`를 생성하며, 다음을 포함:
- 관련 뉴스 기사
- 예상 시나리오 개요 (18개월 후까지)
- 섹터/업종에 대한 영향 (1차/2차/3차)
- 포지티브 영향 종목 (3-5종목)
- 네거티브 영향 종목 (3-5종목)
- 세컨드 오피니언 리뷰
- 최종 투자 판단/시사점
