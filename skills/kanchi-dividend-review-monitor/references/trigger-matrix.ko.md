# Trigger Matrix (T1-T5)

아래 규칙을 적용해 티커를 `OK`, `WARN`, `REVIEW`로 라우팅합니다.

## 심각도 정책

- `OK`: 강제 조치 없음.
- `WARN`: 다음 점검 체크포인트 큐에 추가하고 선택적 추가매수 중지.
- `REVIEW`: 즉시 사람 리뷰 티켓 생성 및 추가매수 중지.

## 트리거 정의

| Trigger | 핵심 시그널 | 기본 머신 규칙 | 주기 | 기본 조치 |
|---|---|---|---|---|
| T1 | 배당 삭감 또는 중단 | `latest_regular < prior_regular * 0.99` OR `latest_regular <= 0` OR 배당 피드 누락 | Daily | `REVIEW` |
| T2 | 커버리지 악화 | 양(+)의 배당이 있는데 `denominator <= 0` OR 2기간 연속 커버리지 비율 `>1.0` | Quarterly | `WARN/REVIEW` |
| T3 | 신용 스트레스 프록시 | 3기간 순부채 증가 + 이자보상배율 약화 and/or 과도한 자본환원 | Weekly + Quarterly confirm | `WARN/REVIEW` |
| T4 | 거버넌스/회계 레드플래그 | 공시 텍스트에 Item 4.02, non-reliance, restatement, material weakness, SEC investigation 키워드 | Daily | `REVIEW` |
| T5 | 구조적 둔화 | 동시 2개 이상 음(-) 조건: 매출 CAGR <0, 마진 하락 추세, 가이던스 하향, 배당 성장 정체 | Quarterly | `WARN/REVIEW` |

## T2 분모 매핑

| Instrument | Denominator |
|---|---|
| Stock | FCF (`CFO - CapEx`) |
| REIT | FFO/AFFO |
| BDC | NII |
| ETF | 펀드 레벨 커버리지가 없으면 보유종목 품질 프록시 사용 |

## 승격 규칙

여러 트리거가 동시에 발생하면 모든 발견사항을 유지하고, 최종 상태는 가장 높은 심각도로 설정합니다:
- `OK < WARN < REVIEW`.

T2 내부에서는 단일 기간 위반보다 2기간 지속 위반(`>1.0` for 2 periods)을 우선합니다.
