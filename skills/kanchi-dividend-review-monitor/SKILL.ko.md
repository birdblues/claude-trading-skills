---
name: kanchi-dividend-review-monitor
description: Kanchi 스타일의 강제 리뷰 트리거(T1-T5)로 배당 포트폴리오를 모니터링하고, 이상 징후를 자동 매도 없이 OK/WARN/REVIEW 상태로 변환합니다. 배당 삭감 감지, 8-K 거버넌스 감시, 배당 안전성 모니터링, REVIEW 큐 자동화, 주기적 배당 리스크 점검 요청 시 사용합니다.
---

# Kanchi Dividend Review Monitor

## 개요

비정상적인 배당 리스크 시그널을 감지해 사람 검토 큐로 라우팅합니다.
자동화는 자동 매매가 아니라 이상 징후 탐지로 다룹니다.

## 사용 시점

다음이 필요할 때 이 스킬을 사용합니다:
- 배당 보유 종목의 일간/주간/분기 이상 징후 탐지.
- T1-T5 리스크 트리거 기반 강제 리뷰 큐잉.
- 포트폴리오 티커와 연계된 8-K/거버넌스 키워드 스캔.
- 수동 의사결정 전에 결정론적 `OK/WARN/REVIEW` 출력.

## 사전 요구사항

다음 스키마를 따르는 정규화 입력 JSON을 제공합니다:
- `references/input-schema.md`

상위 데이터가 불완전한 경우에도 최소한 아래는 제공해야 합니다:
- `ticker`
- `instrument_type`
- `dividend.latest_regular`
- `dividend.prior_regular`

## 비타협 규칙

머신 트리거만으로 자동 매도하지 않습니다.
항상 먼저 사람 확인을 위한 `WARN` 또는 `REVIEW` 근거를 생성합니다.

## 상태 머신

- `OK`: 조치 없음.
- `WARN`: 다음 점검 주기에 추가하고 선택적 추가매수 일시 중지.
- `REVIEW`: 즉시 사람 리뷰 티켓 생성 + 추가매수 중지.

트리거 임계값과 조치는 `references/trigger-matrix.md`를 사용합니다.

## 모니터링 주기

- Daily:
  - T1 배당 삭감/중단.
  - T4 SEC 공시 키워드 스캔(8-K 중심).
- Weekly:
  - T3 프록시 신용 스트레스 점검.
- Quarterly:
  - T2 커버리지 악화 및 T5 구조적 둔화 점수화.

## 워크플로우

### 1) 입력 데이터셋 정규화

티커별 필드를 하나의 JSON 문서로 수집합니다:
- 배당 포인트(최신 정기배당, 이전 정기배당, 누락/0 플래그).
- 커버리지 필드(FCF 또는 FFO 또는 NII, 지급배당, 비율 이력).
- 재무상태표 추세 필드(순부채, 이자보상배율, 자사주/배당).
- 공시 텍스트 스니펫(특히 최근 8-K 또는 동등한 알림 텍스트).
- 영업 추세 필드(매출 CAGR, 마진 추세, 가이던스 추세).

필드 정의와 샘플 payload는 `references/input-schema.md`를 사용합니다.

### 2) 규칙 엔진 실행

실행:

```bash
python3 skills/kanchi-dividend-review-monitor/scripts/build_review_queue.py \
  --input /path/to/monitor_input.json \
  --output /path/to/review_queue.json \
  --markdown /path/to/review_queue.md
```

스크립트는 T1-T5 기준으로 각 티커를 `OK/WARN/REVIEW`에 매핑합니다.

### 3) 우선순위 지정 및 중복 제거

여러 트리거가 동시에 발생하면:
- 감사 추적(audit trail)을 위해 모든 발견 사항을 유지.
- 최종 상태는 가장 높은 심각도로만 승격.
- 트리거 사유는 한 줄 근거로 저장.

### 4) 사람 리뷰 티켓 생성

각 `REVIEW` 티커에 다음을 포함합니다:
- 트리거 ID와 근거.
- 추정 실패 모드.
- 다음 의사결정을 위한 수동 확인 항목.

출력 형식은 `references/review-ticket-template.md`를 사용합니다.

## SEC Filing 가드레일

실시간 SEC fetcher 구현 시:
- 준수 가능한 `User-Agent` 문자열(이름 + 이메일) 포함.
- 캐싱 및 스로틀링 적용.
- SEC 공정 접근 가이드 준수.

## 출력 계약

항상 다음을 반환합니다:
1. 요약 카운트와 티커별 발견 사항이 포함된 Queue JSON.
2. 빠른 트리아지를 위한 Markdown 대시보드.
3. 즉시 처리해야 할 `REVIEW` 티켓 목록.

## 멀티 스킬 핸드오프

- `kanchi-dividend-sop`에서 티커 유니버스와 기준 가정을 입력받음.
- `REVIEW` 결과를 `kanchi-dividend-sop`로 되돌려 재언더라이팅 및 포지션 크기 재검토.
- 리스크 이벤트가 계좌 이동 결정을 시사할 때 계좌 유형 맥락을 `kanchi-dividend-us-tax-accounting`과 공유.

## 리소스

- `scripts/build_review_queue.py`: T1-T5용 로컬 규칙 엔진.
- `scripts/tests/test_build_review_queue.py`: T1-T5 및 리포트 렌더링 단위 테스트.
- `references/trigger-matrix.md`: 트리거 정의, 주기, 조치.
- `references/input-schema.md`: 정규화 입력 스키마 및 샘플 JSON.
- `references/review-ticket-template.md`: 표준 수동 리뷰 티켓 레이아웃.
