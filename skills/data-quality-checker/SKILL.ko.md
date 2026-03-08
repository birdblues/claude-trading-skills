---
name: data-quality-checker
description: 발행 전 시장 분석 문서와 블로그 글의 데이터 품질을 검증합니다. 가격 스케일 불일치(ETF vs futures), 종목 표기 오류, 날짜/요일 불일치, 배분 합계 오류, 단위 불일치를 점검할 때 사용하세요. 영어와 일본어 콘텐츠를 지원합니다. Advisory mode로 동작하며, 차단이 아닌 사람 검토용 경고를 표시합니다.
---

## 개요

발행 전에 시장 분석 문서에서 자주 발생하는 데이터 품질 이슈를 탐지합니다.
체커는 다섯 가지 카테고리를 검증합니다: 가격 스케일 일관성, 종목 표기법,
날짜/요일 정확도, 배분 합계, 단위 사용.
모든 결과는 advisory 성격이며, 발행을 차단하지 않고 사람 검토가 필요한
잠재 이슈를 표시합니다.

## 사용 시점

- 주간 전략 블로그나 시장 분석 리포트를 발행하기 전
- 자동 생성된 시장 요약을 만든 직후
- 번역 문서(영어/일본어)의 데이터 정확도를 검토할 때
- 여러 데이터 소스(FRED, FMP, FINVIZ)를 하나의 리포트로 통합할 때
- 금융 데이터가 포함된 모든 문서의 pre-flight 점검으로 사용할 때

## 사전 요구사항

- Python 3.9+
- 외부 API 키 불필요
- 서드파티 Python 패키지 불필요(표준 라이브러리만 사용)

## 워크플로

### Step 1: 입력 문서 수신

대상 markdown 파일 경로와 선택 파라미터를 받습니다:
- `--file`: 검증할 markdown 문서 경로 (필수)
- `--checks`: 실행할 점검 항목의 콤마 구분 목록 (선택, 기본값: all)
- `--as-of`: 연도 추론 기준일, YYYY-MM-DD 형식 (선택)
- `--output-dir`: 리포트 출력 디렉터리 (선택, 기본값: `reports/`)

### Step 2: 검증 스크립트 실행

데이터 품질 체커 스크립트를 실행합니다:

```bash
python3 skills/data-quality-checker/scripts/check_data_quality.py \
  --file path/to/document.md \
  --output-dir reports/
```

특정 점검만 실행하려면:

```bash
python3 skills/data-quality-checker/scripts/check_data_quality.py \
  --file path/to/document.md \
  --checks price_scale,dates,allocations
```

연도 추론용 기준일을 제공하려면(문서에 연도가 명시되지 않은 경우 유용):

```bash
python3 skills/data-quality-checker/scripts/check_data_quality.py \
  --file path/to/document.md \
  --as-of 2026-02-28
```

### Step 3: 참조 표준 로드

결과를 맥락화하기 위해 관련 reference 문서를 읽습니다:

- `references/instrument_notation_standard.md` -- 표준 ticker 표기,
  자릿수 힌트, 종목 클래스별 명명 규칙
- `references/common_data_errors.md` -- 자주 관찰되는 오류 카탈로그
  (FRED 데이터 지연, ETF/futures 스케일 혼동, 휴장일 누락,
  배분 합계 함정, 단위 혼동 패턴 포함)

결과 설명과 수정 제안에 이 reference를 활용하세요.

### Step 4: 결과 검토

출력의 각 finding을 점검합니다:

- **ERROR** -- 높은 확신의 이슈
  (예: 캘린더 계산으로 검증된 날짜-요일 불일치). 수정 강력 권장.
- **WARNING** -- 사람 판단이 필요한 가능성 높은 이슈
  (예: 가격 스케일 이상치, 표기 불일치, 배분 합계가 0.5% 이상 벗어남).
- **INFO** -- 정보성 메모
  (예: bp/% 혼용이 의도되었을 수 있는 경우).

### Step 5: 품질 리포트 생성

스크립트는 두 개의 출력 파일을 생성합니다:

1. **JSON report** (`data_quality_YYYY-MM-DD_HHMMSS.json`):
   severity, category, message, line number, context를 포함한
   machine-readable finding 목록.
2. **Markdown report** (`data_quality_YYYY-MM-DD_HHMMSS.md`):
   severity별로 그룹화된 human-readable 리포트.

knowledge base를 참조해 설명과 함께 finding을 사용자에게 제시하세요.
이슈별로 구체적인 수정안을 제안하세요.

## 출력 형식

### JSON Finding 구조

```json
{
  "severity": "WARNING",
  "category": "price_scale",
  "message": "GLD: $2,800 has 4 digits (expected 2-3 digits)",
  "line_number": 5,
  "context": "GLD: $2,800"
}
```

### Markdown Report 구조

```markdown
# Data Quality Report
**Source:** path/to/document.md
**Generated:** 2026-02-28 14:30:00
**Total findings:** 3

## ERROR (1)
- **[dates]** (line 12): Date-weekday mismatch: January 1, 2026 (Monday) -- actual weekday is Thursday

## WARNING (2)
- **[price_scale]** (line 5): GLD: $2,800 has 4 digits (expected 2-3 digits)
  > `GLD: $2,800`
- **[allocations]**: Allocation total: 110.0% (expected ~100%)
```

## 리소스

- `scripts/check_data_quality.py` -- 메인 검증 스크립트
- `references/instrument_notation_standard.md` -- 표기/가격 스케일 reference
- `references/common_data_errors.md` -- 공통 오류 패턴 및 예방 가이드

## 핵심 원칙

1. **Advisory mode**: 모든 finding은 사람 검토용 경고입니다.
   finding이 있어도 스크립트가 정상 실행되면 항상 exit code 0을 반환합니다.
   exit code 1은 스크립트 실패(파일 없음, parse 오류)에만 사용됩니다.

2. **섹션 인식 배분 점검**: 배분 섹션(예: "配分", "Allocation" 헤더,
   "ウェイト", "目安比率" 같은 테이블 컬럼) 내부의 퍼센트만 검사합니다.
   본문의 일반 퍼센트(확률, RSI, YoY 성장률)는 무시합니다.

3. **이중 언어 지원**: 영어/일본어 날짜 형식, 요일 이름, 섹션 헤더를 처리합니다.
   전각 문자(％, 〜, en-dash)는 처리 전에 정규화합니다.

4. **연도 추론**: 연도가 없는 날짜는 우선순위에 따라 추론합니다:
   `--as-of` 옵션, 문서 제목/메타데이터의 YYYY 패턴,
   또는 현재 연도 + 6개월 cross-year heuristic.

5. **자릿수 heuristic**: 가격 스케일 검증은 절대 가격 범위 대신
   자릿수(소수점 앞 숫자 개수)를 사용합니다.
   이 방식은 시간 경과에 따른 가격 변화에 강건하면서 ETF/futures 혼동을
   효과적으로 탐지합니다.
