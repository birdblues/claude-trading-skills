# Kanchi Dividend Skills Runbook

이 문서는 아래 3개 스킬의 실운용 순서를 고정하기 위한 절차서입니다.

- `kanchi-dividend-sop`
- `kanchi-dividend-review-monitor`
- `kanchi-dividend-us-tax-accounting`

## 결론

시작점은 `kanchi-dividend-sop`이 맞습니다.
기본 플로우는 `SOP -> 모니터링 -> 세무/계좌 배치`입니다.

## 표준 플로우

1. 종목 선정과 매수 조건을 만든다
사용 스킬: `kanchi-dividend-sop`
실행 타이밍: 신규 검토 시, 월간 재검토 시
산출물:
- Screening 결과 (`PASS/HOLD-FOR-REVIEW/FAIL`)
- 1페이지 종목 메모
- 지정가 분할 플랜

2. 보유 종목의 이상 탐지를 실행한다
사용 스킬: `kanchi-dividend-review-monitor`
실행 타이밍:
- 일간: T1, T4
- 주간: T3
- 분기: T2, T5
산출물:
- `OK/WARN/REVIEW` 큐
- REVIEW 티켓

3. 세무 구분과 계좌 배치를 최적화한다
사용 스킬: `kanchi-dividend-us-tax-accounting`
실행 타이밍: 신규 채용 시, 대규모 교체 시, 연간 점검 시
산출물:
- 배당 구분 서머리
- 계좌 배치 제안
- 세무 전제의 미확정 사항 리스트

## 운용 리듬

- 일간: `kanchi-dividend-review-monitor`의 T1/T4만 확인
- 주간: REVIEW/WARN 종목의 수동 확인
- 월간: `kanchi-dividend-sop`으로 후보 업데이트와 매수 조건 업데이트
- 분기: T2/T5 재평가 + SOP 메모 업데이트
- 연간: `kanchi-dividend-us-tax-accounting`으로 세무 메모 확정

## 스킬 간 인계

1. `kanchi-dividend-sop`에서 `kanchi-dividend-review-monitor`로
인계 항목:
- 채용/보유 티커 목록
- 배당 안전성 기준값
- 실효 조건

2. `kanchi-dividend-review-monitor`에서 `kanchi-dividend-sop`으로
인계 항목:
- `REVIEW` 판정 사유
- 전제 붕괴 의심
- 재평가 대상 우선순위

3. `kanchi-dividend-us-tax-accounting`에서 `kanchi-dividend-sop`으로
인계 항목:
- 계좌 제약
- 세무상 우선 배치
- 신규 매수 시 배치 규칙

## 최소 실행 예시

`kanchi-dividend-review-monitor`의 룰 엔진은 아래와 같이 실행할 수 있습니다.

```bash
python3 skills/kanchi-dividend-review-monitor/scripts/build_review_queue.py \
  --input /path/to/monitor_input.json \
  --output /path/to/review_queue.json \
  --markdown /path/to/review_queue.md
```

입력 형식은 `skills/kanchi-dividend-review-monitor/references/input-schema.md`를 참조하십시오.
