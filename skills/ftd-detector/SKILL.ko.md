---
name: ftd-detector
description: William O'Neil 방법론을 사용해 시장 바닥 확인을 위한 Follow-Through Day (FTD) 신호를 탐지합니다. 듀얼 인덱스 추적(S&P 500 + NASDAQ)과 state machine으로 rally attempt, FTD qualification, post-FTD health 모니터링을 수행합니다. 사용자가 시장 바닥 신호, follow-through day, rally attempt, 조정 이후 재진입 타이밍, 또는 equity exposure 확대의 안전성에 대해 물을 때 사용하세요. market-top-detector(방어적)와 상호보완적이며, 이 skill은 공격적(bottom confirmation)입니다.
---

# FTD Detector 스킬

## 목적

William O'Neil의 검증된 방법론을 사용해 시장 바닥을 확인하는 Follow-Through Day (FTD) 신호를 탐지합니다. 조정 이후 시장 재진입을 위한 exposure 가이드와 quality score(0-100)를 생성합니다.

**Market Top Detector와의 상호보완 관계:**
- Market Top Detector = 방어적(defensive, distribution/rotation/deterioration 탐지)
- FTD Detector = 공격적(offensive, rally attempts/bottom confirmation 탐지)

## 이 스킬을 사용하는 경우

**영문 표현 예시:**
- 사용자가 "Is the market bottoming?" 또는 "Is it safe to buy again?"라고 질문
- 사용자가 시장 조정(3%+ 하락)을 관찰했고 재진입 타이밍을 원함
- 사용자가 Follow-Through Days 또는 rally attempts를 질문
- 사용자가 최근 반등이 지속 가능한지 평가하려고 함
- 사용자가 조정 이후 equity exposure 확대 여부를 질문
- Market Top Detector가 위험 상승을 보였고 사용자가 바닥 신호를 원함

**한글 표현 예시:**
- "바닥을 쳤나?" "다시 매수해도 되나?"
- 조정 국면(3% 이상 하락)에서의 진입 타이밍
- 팔로스루 데이나 랠리 어템프트에 대해
- 최근 반등이 지속 가능한지 평가하고 싶다
- 조정 후 익스포저 확대 판단
- Market Top Detector가 고위험 표시 후 바닥 확인 시그널 확인

## Market Top Detector와의 차이

| 항목 | FTD Detector | Market Top Detector |
|--------|-------------|-------------------|
| 초점 | 바닥 확인 (offensive) | 천장 감지 (defensive) |
| 트리거 | 시장 조정 (3%+ 하락) | 시장이 고점 또는 고점 부근 |
| 시그널 | Rally attempt → FTD → 재진입 | Distribution → Deterioration → 이탈 |
| 점수 | 0-100 FTD quality | 0-100 top probability |
| 액션 | exposure를 늘릴 시점 | exposure를 줄일 시점 |

---

## 실행 워크플로우

### 1단계: Python 스크립트 실행

FTD detector 스크립트를 실행합니다:

```bash
python3 skills/ftd-detector/scripts/ftd_detector.py --api-key $FMP_API_KEY
```

스크립트는 다음을 수행합니다:
1. FMP API에서 S&P 500 및 QQQ 과거 데이터(60+ 거래일) 조회
2. 두 인덱스의 현재 quote 조회
3. 듀얼 인덱스 state machine 실행(correction → rally → FTD detection)
4. post-FTD health 평가(distribution days, invalidation, power trend)
5. quality score 계산(0-100)
6. JSON 및 Markdown 리포트 생성

**API Budget:** 4 calls (250/day 무료 티어 내에서 충분)

### 2단계: 결과 제시

생성된 Markdown 리포트를 사용자에게 제시하고 다음을 강조합니다:
- 현재 시장 상태(correction, rally attempt, FTD confirmed 등)
- quality score와 signal strength
- 권장 exposure 수준
- 핵심 watch level(swing low, FTD day low)
- post-FTD health(distribution days, power trend)

### 3단계: 맥락 기반 가이드

시장 상태를 기반으로 추가 가이드를 제공합니다:

**FTD Confirmed (score 60+)인 경우:**
- proper base를 형성한 leading stock 검토를 제안
- 후보 종목 확인을 위해 CANSLIM screener 참조
- position sizing 및 stop 관리 리마인드

**Rally Attempt (Day 1-3)인 경우:**
- 인내가 필요하며 FTD 이전 선매수는 피하라고 안내
- watchlist 구축 제안

**No Correction인 경우:**
- 상승 추세에서는 FTD 분석이 적용되지 않음
- 방어적 시그널 확인을 위해 Market Top Detector로 안내

---

## State Machine

```
NO_SIGNAL → CORRECTION → RALLY_ATTEMPT → FTD_WINDOW → FTD_CONFIRMED
                ↑              ↓               ↓              ↓
                └── RALLY_FAILED ←─────────────┘     FTD_INVALIDATED
```

| State | 정의 |
|-------|-----------|
| NO_SIGNAL | 상승 추세, 조건을 충족하는 조정 없음 |
| CORRECTION | 3%+ 하락과 3일+ 하락일 |
| RALLY_ATTEMPT | swing low에서 시작한 랠리의 Day 1-3 |
| FTD_WINDOW | Day 4-10, 조건을 충족하는 FTD 대기 |
| FTD_CONFIRMED | 유효한 FTD 신호 감지 |
| RALLY_FAILED | 랠리가 swing low 하향 이탈 |
| FTD_INVALIDATED | 종가가 FTD day's low 아래로 하락 |

## Quality Score (0-100)

| Score | 시그널 | Exposure |
|-------|--------|----------|
| 80-100 | Strong FTD | 75-100% |
| 60-79 | Moderate FTD | 50-75% |
| 40-59 | Weak FTD | 25-50% |
| <40 | No FTD / Failed | 0-25% |

---

## 사전 요구사항

- **FMP API Key:** 필수. `FMP_API_KEY` 환경 변수를 설정하거나 `--api-key` 플래그로 전달.
- **Python 3.8+:** `requests` 라이브러리 설치 필요.
- **API Budget:** 실행당 4 calls(FMP 무료 티어 250/day 내에서 충분).

## 출력 파일

- JSON: `ftd_detector_YYYY-MM-DD_HHMMSS.json`
- Markdown: `ftd_detector_YYYY-MM-DD_HHMMSS.md`

## 참고 문서

### `skills/ftd-detector/references/ftd_methodology.md`
- O'Neil의 FTD 규칙 상세
- rally attempt 메커니즘과 day counting
- 과거 FTD 사례(2020년 3월, 2022년 10월)

### `skills/ftd-detector/references/post_ftd_guide.md`
- post-FTD distribution day 실패율
- Power Trend 정의 및 조건
- 성공 패턴과 실패 패턴 비교

### 참고 문서를 로드해야 하는 경우
- **초기 사용:** 전체 이해를 위해 `skills/ftd-detector/references/ftd_methodology.md` 로드
- **Post-FTD 질문:** `skills/ftd-detector/references/post_ftd_guide.md` 로드
- **일반 실행:** 스크립트가 분석을 처리하므로 참고 문서 불필요
