---
name: kanchi-dividend-sop
description: Kanchi-style dividend investing을 반복 가능한 US-stock 운영 절차로 전환합니다. 사용자가 칸치식 배당 투자, dividend screening, dividend growth quality checks, US sectors에 맞춘 PERxPBR adaptation, pullback limit-order planning, one-page stock memo creation을 요청할 때 사용하세요. screening, deep dive, entry planning, post-purchase monitoring cadence를 포함합니다.
---

# Kanchi Dividend SOP

## 개요

Kanchi의 5단계 방법을 US dividend investing을 위한 결정론적 workflow로 구현합니다.
공격적인 yield 추격보다 안전성과 반복 가능성을 우선합니다.

## 사용 시점

다음이 필요할 때 이 skill을 사용합니다:
- US equities에 맞게 조정된 Kanchi-style dividend stock selection.
- 즉흥적 선택 대신 반복 가능한 screening 및 pullback-entry 프로세스.
- 명시적인 invalidation condition을 포함한 one-page underwriting memo.
- monitoring 및 tax/account-location workflow를 위한 handoff 패키지.

## 사전 준비

workflow 실행 전 아래 입력 중 하나를 준비하세요:
1. `skills/value-dividend-screener/scripts/screen_dividend_stocks.py`의 출력.
2. `skills/dividend-growth-pullback-screener/scripts/screen_dividend_growth_rsi.py`의 출력.
3. 사용자 제공 ticker 목록(브로커 export 또는 수동 목록).

결정론적 artifact 생성을 위해서는 아래처럼 ticker를 전달하세요:

```bash
python3 skills/kanchi-dividend-sop/scripts/build_sop_plan.py \
  --tickers "JNJ,PG,KO" \
  --output-dir reports/
```

Step 5 entry timing artifact를 생성하려면:

```bash
python3 skills/kanchi-dividend-sop/scripts/build_entry_signals.py \
  --tickers "JNJ,PG,KO" \
  --alpha-pp 0.5 \
  --output-dir reports/
```

## Workflow

### 1) screening 전에 mandate 정의

먼저 아래 파라미터를 수집하고 고정합니다:
- 목표: 현재 cash income vs dividend growth.
- 최대 종목 수와 포지션 크기 상한.
- 허용 instrument: stock만, 또는 REIT/BDC/ETF 포함.
- 선호 account type 맥락: taxable vs IRA-like accounts.

`references/default-thresholds.md`를 로드하고,
사용자 override가 없으면 baseline 설정을 적용합니다.

### 2) 투자 가능 universe 구성

quality 편향 universe로 시작합니다:
- Core bucket: 장기 dividend growth 종목(예: Dividend Aristocrats 스타일 quality set).
- Satellite bucket: 고배당 섹터(utilities, telecom, REITs)를 분리된 risk bucket으로 관리.

ticker 수집 시 source 우선순위를 명시적으로 사용합니다:
1. `skills/value-dividend-screener/scripts/screen_dividend_stocks.py` 출력(FMP/FINVIZ).
2. `skills/dividend-growth-pullback-screener/scripts/screen_dividend_growth_rsi.py` 출력.
3. API를 사용할 수 없을 때 사용자 제공 broker export 또는 수동 ticker 목록.

다음 단계로 넘어가기 전에 bucket별로 그룹화된 ticker 목록을 반환합니다.

### 3) Kanchi Step 1 적용 (yield filter + trap flag)

기본 규칙:
- `forward_dividend_yield >= 3.5%`

trap 통제:
- 극단적 yield(`>= 8%`)는 `deep-dive-required`로 flag 처리.
- payout 급증은 special dividend artifact 가능성으로 flag 처리.

출력:
- ticker별 `PASS` 또는 `FAIL`.
- 잠재적 yield trap용 `deep-dive-required` flag.

### 4) Kanchi Step 2 적용 (growth 및 safety)

요구 조건:
- 다년 관점에서 Revenue와 EPS trend가 양(+)의 방향.
- 검토 기간 동안 dividend trend가 감소하지 않을 것.

추가 safety check:
- payout ratio와 FCF payout ratio가 합리적인 범위.
- debt burden 및 interest coverage가 악화되지 않을 것.

trend가 혼재되어도 깨지지 않았다면 hard reject 대신 `HOLD-FOR-REVIEW`로 분류합니다.

### 5) Kanchi Step 3 적용 (valuation) + US sector 매핑

`references/valuation-and-one-off-checks.md`를 사용하고
섹터별 valuation 로직을 적용합니다:
- Financials: `PER x PBR`를 주요 지표로 유지 가능.
- REITs: 단순 `P/E` 대신 `P/FFO` 또는 `P/AFFO` 사용.
- Asset-light sectors: forward `P/E`, `P/FCF`, historical range를 결합.

각 ticker마다 어떤 valuation method를 사용했는지 반드시 보고합니다.

### 6) Kanchi Step 4 적용 (one-off event filter)

최근 이익이 일회성 효과에 의존한 종목은 reject 또는 downgrade합니다:
- Asset sale gains, litigation settlement, tax effect spikes.
- sales trend로 뒷받침되지 않는 margin spike.
- 반복되는 "one-time/non-recurring" 조정.

auditability 유지를 위해 각 `FAIL`에 대해 한 줄 근거를 기록합니다.

### 7) Kanchi Step 5 적용 (규칙 기반 약세 매수)

entry trigger를 기계적으로 설정합니다:
- Yield trigger: 현재 yield가 5y 평균 yield + alpha(기본 `+0.5pp`)보다 높음.
- Valuation trigger: 목표 multiple 도달(`P/E`, `P/FFO`, 또는 `P/FCF`).

실행 패턴:
- 분할 주문: `40% -> 30% -> 30%`.
- 각 추가 매수 전 한 문장 sanity check 필수: "thesis intact vs structural break".

### 8) 표준화된 출력물 생성

항상 아래 3개 artifact를 생성합니다:
1. Screening table (`PASS`, `HOLD-FOR-REVIEW`, `FAIL` + evidence).
2. One-page stock memo (`references/stock-note-template.md` 사용).
3. 분할 수량과 invalidation condition이 포함된 limit-order plan.

## 출력

반환 및/또는 생성:
1. markdown 형식 SOP screening summary.
2. `references/stock-note-template.md` 기반 underwriting memo 세트.
3. 선택 사항: `skills/kanchi-dividend-sop/scripts/build_sop_plan.py`가 `reports/`에 생성하는 plan artifact 파일.
4. 선택 사항: `skills/kanchi-dividend-sop/scripts/build_entry_signals.py`가 `reports/`에 생성하는 Step 5 entry-signal artifact.

## Cadence

최소 주기는 아래를 사용합니다:
- Weekly (15 min): dividend 및 business-news 변경만 점검.
- Monthly (30 min): screening 재실행 및 주문 레벨 갱신.
- Quarterly (60 min): 최신 filings/earnings 기반 심층 safety review.

## Multi-Skill Handoff

이 skill을 먼저 실행한 뒤 결과를 전달합니다:
1. 일/주/분기 이상 징후 탐지를 위해 `kanchi-dividend-review-monitor`로 전달.
2. account-location 및 tax classification 계획을 위해 `kanchi-dividend-us-tax-accounting`으로 전달.

## Guardrails

- Step 4 및 safety check 없이 무근거 buy call을 내리지 마세요.
- coverage quality 검증 전 high yield를 value로 간주하지 마세요.
- 데이터가 누락되면 가정을 명시적으로 유지하세요.

## 리소스

- `skills/kanchi-dividend-sop/scripts/build_sop_plan.py`: 결정론적 SOP plan generator.
- `skills/kanchi-dividend-sop/scripts/tests/test_build_sop_plan.py`: plan generation 테스트.
- `skills/kanchi-dividend-sop/scripts/build_entry_signals.py`: Step 5 target-buy calculator (`5y avg yield + alpha`).
- `skills/kanchi-dividend-sop/scripts/tests/test_build_entry_signals.py`: signal calculation 테스트.
- `references/default-thresholds.md`: baseline threshold 및 profile tuning.
- `references/valuation-and-one-off-checks.md`: sector valuation map 및 one-off checklist.
- `references/stock-note-template.md`: 후보별 one-page memo 템플릿.
