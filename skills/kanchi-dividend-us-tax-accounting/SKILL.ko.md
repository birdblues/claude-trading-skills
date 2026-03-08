---
name: kanchi-dividend-us-tax-accounting
description: Kanchi 스타일 소득 포트폴리오를 위한 미국 배당세 및 계좌 배치(account-location) 워크플로우를 제공합니다. qualified vs ordinary dividend, 1099-DIV 해석, REIT/BDC 분배금 처리, 보유기간 점검, 배당 자산의 taxable-vs-IRA 배치 결정을 요청할 때 사용합니다.
---

# Kanchi Dividend Us Tax Accounting

## 개요

감사 가능성을 유지하면서 배당 투자자를 위한 실무형 US tax 워크플로우를 적용합니다.
법률/세무 자문 대체가 아니라 분류 및 계좌 배치 의사결정 지원에 집중합니다.

## 사용 시점

다음이 필요할 때 이 스킬을 사용합니다:
- 미국 배당세 분류 계획(qualified vs ordinary 가정).
- 연말 세무 계획 전 보유기간(holding period) 점검.
- 주식/REIT/BDC/MLP 소득 자산의 계좌 배치(account location) 결정.
- 표준화된 연간 배당세 메모 형식.

## 사전 준비

종목 단위 입력을 준비합니다:
- `ticker`
- `instrument_type`
- `account_type`
- `hold_days_in_window` (가능한 경우)

결정론적 출력 artifact를 위해 JSON 입력을 제공하고 다음을 실행합니다:

```bash
python3 skills/kanchi-dividend-us-tax-accounting/scripts/build_tax_planning_sheet.py \
  --input /path/to/tax_input.json \
  --output-dir reports/
```

## 가드레일

항상 명확히 고지합니다: 세무 결과는 개인별 사실관계와 관할에 따라 달라집니다.
이 스킬은 계획 지원으로 사용하고, 최종 신고 판단은 세무 전문가에게 이관합니다.

## 워크플로우

### 1) 분배금 스트림별 분류

각 보유 종목의 예상 현금흐름을 다음으로 분류합니다:
- qualified dividend 가능 항목.
- ordinary dividend/non-qualified distribution 항목.
- 해당되는 경우 REIT/BDC 특화 분배금 구성요소.

보유기간 및 분류 점검은 `references/qualified-dividend-checklist.md`를 사용합니다.

### 2) 보유기간 적격성 가정 검증

qualified 처리 가능 항목에 대해:
- ex-dividend date window 확인.
- 측정 구간 내 최소 보유일수 요건 확인.
- 보유기간 요건 미충족 위험 포지션 표시.

데이터가 불완전하면 상태를 `ASSUMPTION-REQUIRED`로 표시합니다.

### 3) 보고 필드 매핑

계획 가정을 예상 세무 양식 버킷으로 매핑합니다:
- Ordinary dividend total.
- Qualified dividend subset.
- 별도 보고되는 경우 REIT 관련 구성요소.

연말 정합(reconciliation)이 쉽도록 양식 용어를 일관되게 사용합니다.

### 4) 계좌 배치 권고안 작성

`references/account-location-matrix.md`를 사용해
세무 프로필 기준으로 자산을 배치합니다:
- qualified 중심 유지 가능성이 높은 종목은 taxable account.
- ordinary-income 성격이 높은 분배금은 tax-advantaged account.

유동성, 전략, 집중도 등 제약이 충돌하면 트레이드오프를 명시적으로 설명합니다.

### 5) 연간 계획 메모 작성

`references/annual-tax-memo-template.md`를 사용하고 다음을 포함합니다:
- 사용한 가정.
- 분배금 분류 요약.
- 수행한 계좌 배치 조치.
- CPA/세무자문 검토용 open item.

## 출력

항상 다음을 출력합니다:
1. 종목 단위 분배금 분류 테이블.
2. 근거를 포함한 계좌 배치 권고 테이블.
3. 미해결 세무 가정을 위한 open-risk 체크리스트.
4. 선택적으로 `skills/kanchi-dividend-us-tax-accounting/scripts/build_tax_planning_sheet.py`에서 생성된 artifact.

## 멀티 스킬 핸드오프

- `kanchi-dividend-sop`로부터 후보/보유 종목 리스트를 입력받음.
- `kanchi-dividend-review-monitor`로부터 리스크 이벤트(`WARN/REVIEW`) 맥락을 입력받음.
- 신규 진입 전에 계좌 배치 제약을 `kanchi-dividend-sop`로 반환.

## 리소스

- `skills/kanchi-dividend-us-tax-accounting/scripts/build_tax_planning_sheet.py`: 세무 계획 시트 생성기.
- `skills/kanchi-dividend-us-tax-accounting/scripts/tests/test_build_tax_planning_sheet.py`: 세무 계획 출력 테스트.
- `references/qualified-dividend-checklist.md`: 분류 및 보유기간 점검.
- `references/account-location-matrix.md`: 계좌 유형/상품별 배치 매트릭스.
- `references/annual-tax-memo-template.md`: 재사용 가능한 메모 구조.
