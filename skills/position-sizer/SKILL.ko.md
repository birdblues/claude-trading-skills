---
name: position-sizer
description: 롱 주식 트레이드의 리스크 기반 포지션 사이즈를 계산합니다. 포지션 사이징, 매수 수량, 거래당 리스크, Kelly criterion, ATR 기반 sizing, 포트폴리오 리스크 배분 질문에 사용하세요. stop-loss 거리 계산, 변동성 스케일링, 섹터 집중도 점검을 지원합니다.
---

# Position Sizer

## 개요

리스크 관리 원칙에 따라 롱 주식 트레이드에서 매수할 최적 주식 수를 계산합니다.
세 가지 sizing 방법을 지원합니다:

- **Fixed Fractional**: 거래당 계좌 자본의 고정 비율을 리스크로 설정 (기본값: 1%)
- **ATR-Based**: Average True Range로 변동성 조정 stop 거리를 설정
- **Kelly Criterion**: 과거 승/패 통계로 수학적 최적 리스크 배분 계산

모든 방법은 포트폴리오 제약(max position %, max sector %)을 적용하고,
전체 리스크 분해와 함께 최종 추천 주식 수를 출력합니다.

## 사용 시점

- 사용자가 "몇 주를 사야 하나요?"라고 물을 때
- 특정 트레이드 셋업의 포지션 크기를 계산하려 할 때
- 거래당 리스크, stop-loss sizing, 포트폴리오 배분을 언급할 때
- Kelly Criterion 또는 ATR 기반 포지션 사이징을 물을 때
- 포지션이 포트폴리오 집중도 한도 안에 들어오는지 확인하려 할 때

## 사전 요구사항

- API 키 불필요
- Python 3.9+ (표준 라이브러리만 사용)

## 워크플로

### Step 1: 트레이드 파라미터 수집

사용자로부터 다음을 수집합니다:
- **필수**: 계좌 규모(총 자본)
- **Mode A (Fixed Fractional)**: 진입가, stop 가격, 리스크 비율(기본 1%)
- **Mode B (ATR-Based)**: 진입가, ATR 값, ATR multiplier(기본 2.0x), 리스크 비율
- **Mode C (Kelly Criterion)**: 승률, 평균 이익, 평균 손실
  (주식 수 계산 시 진입/stop 선택 제공)
- **선택 제약**: 계좌 대비 최대 포지션 %, 최대 섹터 %, 현재 섹터 노출

사용자가 ticker만 제공하고 구체 가격이 없으면,
사용 가능한 도구로 현재가를 조회하고 technical analysis 기반 진입/stop 레벨을 제안합니다.

### Step 2: Position Sizer 스크립트 실행

포지션 사이징 계산 실행:

```bash
# Fixed Fractional (가장 일반적)
python3 skills/position-sizer/scripts/position_sizer.py \
  --account-size 100000 \
  --entry 155 \
  --stop 148.50 \
  --risk-pct 1.0 \
  --output-dir reports/

# ATR-Based
python3 skills/position-sizer/scripts/position_sizer.py \
  --account-size 100000 \
  --entry 155 \
  --atr 3.20 \
  --atr-multiplier 2.0 \
  --risk-pct 1.0 \
  --output-dir reports/

# Kelly Criterion (budget 모드 - entry 없음)
python3 skills/position-sizer/scripts/position_sizer.py \
  --account-size 100000 \
  --win-rate 0.55 \
  --avg-win 2.5 \
  --avg-loss 1.0 \
  --output-dir reports/

# Kelly Criterion (shares 모드 - entry/stop 포함)
python3 skills/position-sizer/scripts/position_sizer.py \
  --account-size 100000 \
  --entry 155 \
  --stop 148.50 \
  --win-rate 0.55 \
  --avg-win 2.5 \
  --avg-loss 1.0 \
  --output-dir reports/
```

### Step 3: Methodology Reference 로드

선택한 방법의 맥락, 리스크 가이드라인, 포트폴리오 제약 모범 사례를 제공하기 위해
`references/sizing_methodologies.md`를 읽습니다.

### Step 4: 다중 시나리오 계산

사용자가 단일 방법을 지정하지 않았다면 비교를 위해 여러 시나리오를 실행합니다:
- Fixed Fractional: 0.5%, 1.0%, 1.5% 리스크
- ATR-based: 1.5x, 2.0x, 3.0x multiplier
- 각 시나리오별 주식 수, 포지션 가치, 달러 리스크 비교표 제시

### Step 5: 포트폴리오 제약 적용 및 최종 크기 결정

사용자에게 포트폴리오 맥락이 있으면 제약을 추가합니다:

```bash
python3 skills/position-sizer/scripts/position_sizer.py \
  --account-size 100000 \
  --entry 155 \
  --stop 148.50 \
  --risk-pct 1.0 \
  --max-position-pct 10 \
  --max-sector-pct 30 \
  --current-sector-exposure 22 \
  --output-dir reports/
```

어떤 제약이 binding인지, 왜 포지션을 제한하는지 설명합니다.

### Step 6: 포지션 리포트 생성

최종 추천안에 다음을 포함해 제시합니다:
- 사용한 방법과 근거
- 정확한 주식 수와 포지션 가치
- 달러 리스크와 계좌 대비 비율
- stop-loss 가격
- binding 제약(해당 시)
- 리스크 관리 리마인더(포트폴리오 heat, 손절 규율)

## 출력 형식

### JSON 리포트

```json
{
  "schema_version": "1.0",
  "mode": "shares",
  "parameters": {
    "entry_price": 155.0,
    "account_size": 100000,
    "stop_price": 148.50,
    "risk_pct": 1.0
  },
  "calculations": {
    "fixed_fractional": {
      "method": "fixed_fractional",
      "shares": 153,
      "risk_per_share": 6.50,
      "dollar_risk": 1000.0,
      "stop_price": 148.50
    },
    "atr_based": null,
    "kelly": null
  },
  "constraints_applied": [],
  "final_recommended_shares": 153,
  "final_position_value": 23715.0,
  "final_risk_dollars": 994.50,
  "final_risk_pct": 0.99,
  "binding_constraint": null
}
```

### Markdown 리포트

JSON 리포트와 함께 자동 생성됩니다. 포함 항목:
- 파라미터 요약
- 활성 방법의 계산 상세
- 제약 분석(해당 시)
- 주식 수, 가치, 리스크를 포함한 최종 추천

리포트는 `reports/`에
`position_sizer_YYYY-MM-DD_HHMMSS.json` 및 `.md` 형식으로 저장됩니다.

## 리소스

- `references/sizing_methodologies.md`: Fixed Fractional, ATR-based, Kelly Criterion의
  종합 가이드(예시, 비교표, 리스크 관리 원칙 포함)
- `scripts/position_sizer.py`: 메인 계산 스크립트(CLI 인터페이스)

## 핵심 원칙

1. **생존 우선**: 포지션 사이징의 목적은 대박 극대화가 아니라 연속 손실 생존
2. **1% 룰**: 기본은 거래당 1% 리스크, 특별한 근거 없이는 2% 초과 금지
3. **항상 내림**: 주식 수는 반드시 정수 내림(올림 금지)
4. **가장 엄격한 제약 우선**: 여러 한도가 있으면 가장 타이트한 한도가 최종 크기를 결정
5. **Half Kelly**: 실전에서 full Kelly는 금지, Half Kelly는 훨씬 낮은 리스크로 성장률 대부분 확보
6. **Portfolio heat**: 전체 오픈 리스크는 계좌 자본의 6-8%를 넘기지 않기
7. **손실 비대칭성**: 50% 손실을 복구하려면 100% 수익이 필요하므로 사이징을 보수적으로 적용
