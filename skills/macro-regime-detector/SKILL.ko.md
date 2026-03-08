---
name: macro-regime-detector
description: 교차자산 비율 분석으로 구조적 매크로 레짐 전환(1-2년)을 탐지합니다. RSP/SPY 집중도, 수익률 곡선, 신용 여건, size factor, 주식-채권 관계, 섹터 로테이션을 분석해 Concentration, Broadening, Contraction, Inflationary, Transitional 상태 변화를 식별합니다. 매크로 레짐, 시장 레짐 변화, 구조적 로테이션, 장기 포지셔닝 질문 시 실행합니다.
---

# Macro Regime Detector

월간 주기의 교차자산 비율 분석으로 구조적 매크로 레짐 전환을 탐지합니다. 이 스킬은 전략적 포트폴리오 포지셔닝에 영향을 주는 1-2년 레짐 변화를 식별합니다.

## 사용 시점

- 사용자가 현재 매크로 레짐 또는 레짐 전환을 묻는 경우
- 사용자가 구조적 시장 로테이션(집중화 vs 확산)을 이해하려는 경우
- 사용자가 수익률 곡선, 신용, 교차자산 시그널 기반 장기 포지셔닝을 묻는 경우
- 사용자가 RSP/SPY, IWM/SPY, HYG/LQD 등 교차자산 비율을 언급한 경우
- 사용자가 레짐 변화 진행 여부를 평가하려는 경우

## 워크플로우

1. 방법론 맥락을 위해 참고 문서를 로드:
   - `references/regime_detection_methodology.md`
   - `references/indicator_interpretation_guide.md`

2. 메인 분석 스크립트 실행:
   ```bash
   python3 skills/macro-regime-detector/scripts/macro_regime_detector.py
   ```
   이 스크립트는 9개 ETF + 미국채 금리의 600일 데이터를 가져옵니다(총 10 API 호출).

3. 생성된 Markdown 리포트를 읽고 결과를 사용자에게 전달.

4. 사용자가 역사적 유사 사례를 요청하면 `references/historical_regimes.md`로 추가 맥락 제공.

## 사전 요구사항

- **FMP API Key** (필수): `FMP_API_KEY` 환경변수 설정 또는 `--api-key` 전달
- 무료 티어(250 calls/day)로 충분함(스크립트 약 10회 호출)

## 6개 구성요소

| # | 구성요소 | 비율/데이터 | 가중치 | 탐지 대상 |
|---|-----------|------------|--------|-----------------|
| 1 | 시장 집중도 | RSP/SPY | 25% | 메가캡 집중 vs 시장 확산 |
| 2 | 수익률 곡선 | 10Y-2Y spread | 20% | 금리 사이클 전환 |
| 3 | 신용 여건 | HYG/LQD | 15% | 신용 사이클 리스크 선호 |
| 4 | Size Factor | IWM/SPY | 15% | 소형주 vs 대형주 로테이션 |
| 5 | 주식-채권 | SPY/TLT + correlation | 15% | 주식-채권 관계 레짐 |
| 6 | 섹터 로테이션 | XLY/XLP | 10% | 경기순환 vs 방어 선호 |

## 5개 레짐 분류

- **Concentration**: 메가캡 주도, 좁은 시장.
- **Broadening**: 시장 참여 확장, 소형/가치 로테이션.
- **Contraction**: 신용 긴축, 방어 로테이션, risk-off.
- **Inflationary**: 주식-채권 양(+) 상관, 전통적 헤지 약화.
- **Transitional**: 시그널은 다수이나 패턴이 명확하지 않음.

## 출력

- `macro_regime_YYYY-MM-DD_HHMMSS.json` — 프로그램용 구조화 데이터
- `macro_regime_YYYY-MM-DD_HHMMSS.md` — 사람이 읽는 리포트:
  1. Current Regime Assessment
  2. Transition Signal Dashboard
  3. Component Details
  4. Regime Classification Evidence
  5. Portfolio Posture Recommendations

## 다른 스킬과의 관계

| Aspect | Macro Regime Detector | Market Top Detector | Market Breadth Analyzer |
|--------|----------------------|--------------------|-----------------------|
| Time Horizon | 1-2 years (structural) | 2-8 weeks (tactical) | Current snapshot |
| Data Granularity | Monthly (6M/12M SMA) | Daily (25 business days) | Daily CSV |
| Detection Target | Regime transitions | 10-20% corrections | Breadth health score |
| API Calls | ~10 | ~33 | 0 (Free CSV) |

## 스크립트 인자

```bash
python3 macro_regime_detector.py [options]

Options:
  --api-key KEY       FMP API key (default: $FMP_API_KEY)
  --output-dir DIR    Output directory (default: current directory)
  --days N            Days of history to fetch (default: 600)
```
