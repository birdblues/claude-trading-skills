# Qualified Dividend Checklist (US)

계획 가정 수립 시 이 체크리스트를 사용합니다.

## 분류 점검

각 보유 종목마다 다음을 검증합니다:
1. 상품/유형 기준으로 분배금이 qualified 처리 가능성이 있는지.
2. ex-dividend date window 주변에서 필요한 보유기간 테스트를 충족하는지.
3. 현재 사실관계에서 알려진 결격 사유가 없는지.

하나라도 불확실하면 `ASSUMPTION-REQUIRED`로 표시합니다.

## 보유기간 규칙 (US Federal, 일반 계획 기준)

- 보통주 기준: ex-dividend date **60일 전**부터 시작하는 **121일 기간** 중 **61일 초과** 보유.
- 우선주(특정 장기 배당): ex-dividend date **90일 전**부터 시작하는 **181일 기간** 중 **91일 초과** 보유를 자주 사용.

최신 IRS 가이드를 기준 출처로 사용합니다:
- IRS Publication 550.
- IRS Form 1099-DIV instructions.

## 실무 데이터 필드

포지션별로 다음 필드를 추적합니다:
- Ticker
- Account type
- Ex-dividend date
- Purchase date(s)
- Disposal date(s), if any
- Days held in required window
- Preliminary classification (`qualified-likely`, `ordinary-likely`, `unknown`)

## 흔한 함정

- 보유기간 검증 없이 보통주 배당은 모두 qualified라고 가정하는 실수.
- 잦은 전술 매매로 보유기간이 짧아진 점을 무시하는 실수.
- REIT/BDC 분배금을 표준 qualified-dividend 흐름과 동일하게 취급하는 실수.

## 권장 출처 우선순위

1. 브로커 세무 문서 및 분배금 breakdown.
2. 해당 연도 최신 IRS 공식 문서(Publication 550, 1099-DIV instructions).
3. 분류가 수정된 경우 발행사/펀드 공지.
