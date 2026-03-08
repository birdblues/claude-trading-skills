---
name: report-translator
description: |
  영어 리포트를 한국어로 번역하는 스킬.
  금융 용어 가이드라인에 따라 종목 티커, 숫자, 기술 지표명은 원본 유지하면서
  섹션 헤더, 설명 텍스트, 가이던스를 자연스러운 한국어로 변환.
  번역 후 data-quality-checker로 데이터 무결성을 자동 검증.
  트리거: 리포트 번역, 한글 리포트, 한국어 번역, /report-translator <파일경로>
---

# Report Translator

## Overview

영어로 생성된 분석 리포트를 한국어로 번역한다. 금융 번역 가이드라인에 따라
데이터 무결성을 유지하면서 자연스러운 한국어 리포트를 생성하고,
data-quality-checker로 번역본의 데이터 정확성을 검증한다.

## When to Use

- 스크립트가 생성한 영어 리포트를 한국어로 변환할 때
- `/report-translator reports/<file>.md` 형태로 직접 호출할 때
- 다른 스킬의 워크플로우에서 한글 리포트 생성 단계로 호출될 때

## Workflow

### Step 1: 입력 확인

번역할 리포트 파일 경로를 확인한다.
- 파일이 `reports/` 디렉토리에 존재하는지 검증
- 이미 `_ko.md`로 끝나는 파일이면 중복 번역 방지를 위해 경고

### Step 2: 번역 가이드라인 로드

`references/translation_guidelines.md`를 읽어 번역 규칙과 금융 용어 사전을 확인한다.

### Step 3: 영어 리포트 읽기

원본 영어 리포트 전체를 읽는다.

### Step 4: 한국어 번역 수행

번역 가이드라인에 따라 리포트를 한국어로 번역한다.

**번역하지 않는 항목:**
- 종목 티커 (AAPL, MSFT 등)
- 숫자, 가격, 퍼센트 데이터
- 날짜 형식 (YYYY-MM-DD)
- 기술 지표명 (RSI, MACD, EMA, SMA 등)
- 테이블 내 데이터 값
- URL, API 관련 텍스트

**번역하는 항목:**
- 섹션 헤더 및 소제목
- 설명 텍스트 및 분석 내용
- 가이던스, 추천사항, 결론
- 방법론 설명
- 면책 조항 및 부가 설명
- 테이블 컬럼 헤더 (선택적 — 기존 `.ko.md` 템플릿 패턴 따름)

**구조 보존:**
- Markdown 헤더 레벨 (##, ### 등) 유지
- 테이블 형식 유지
- 볼드/이탤릭 서식 유지
- 코드 블록 유지
- 리스트 구조 유지

### Step 5: 번역본 저장

번역된 리포트를 원본 파일명에 `_ko` 접미사를 붙여 저장한다.
- 원본: `reports/earnings_trade_analysis_2026-03-08.md`
- 번역본: `reports/earnings_trade_analysis_2026-03-08_ko.md`

원본 파일은 그대로 유지한다.

### Step 6: 데이터 무결성 검증

data-quality-checker로 번역본을 검증한다:

```bash
python3 skills/data-quality-checker/scripts/check_data_quality.py \
  --file reports/<translated_file>_ko.md --output-dir reports/
```

### Step 7: 검증 결과 처리

- ERROR가 발견되면 해당 부분을 수정하고 번역본을 재저장
- WARNING은 사용자에게 보고하되 자동 수정하지 않음
- 수정 후 재검증하여 ERROR가 없는 상태로 최종 확정

## Output Format

번역본은 원본과 동일한 Markdown 구조를 유지하며, 파일명에 `_ko` 접미사가 붙는다.
`reports/` 디렉토리에 저장된다.

## Resources

- `references/translation_guidelines.md` -- 번역 가이드라인 및 금융 용어 사전
- `skills/data-quality-checker/` -- 데이터 무결성 검증 스킬
