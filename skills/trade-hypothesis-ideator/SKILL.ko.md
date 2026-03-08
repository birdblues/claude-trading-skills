---
name: trade-hypothesis-ideator
description: >
  시장 데이터, 거래 로그, 저널 스니펫에서 반증 가능한 트레이딩 전략 가설을
  생성합니다. 구조화된 입력 번들이 있고, 실험 설계, 중단 기준, 선택적
  strategy.yaml 내보내기를 포함한 우선순위 가설 카드를 원할 때 사용하세요.
  내보내기 형식은 edge-finder-candidate/v1과 호환됩니다.
---

# Trade Hypothesis Ideator

정규화된 입력 번들에서 구조화된 가설 카드 1~5개를 생성하고, 이를 비평 및 순위화한 뒤, 필요하면 `pursue` 카드를 `strategy.yaml` + `metadata.json` 아티팩트로 내보냅니다.

## 워크플로

1. 입력 JSON 번들을 받습니다.
2. 1차 패스 정규화 + 증거 추출을 실행합니다.
3. 다음 프롬프트로 가설을 생성합니다:
   - `prompts/system_prompt.md`
   - `prompts/developer_prompt_template.md` (`{{evidence_summary}}` 주입)
4. `prompts/critique_prompt_template.md`로 가설을 비평합니다.
5. 2차 패스 순위화 + 출력 포맷팅 + 가드레일을 실행합니다.
6. 필요하면 Step H strategy exporter로 `pursue` 가설을 내보냅니다.

## 스크립트

- Pass 1 (증거 요약):

```bash
python3 skills/trade-hypothesis-ideator/scripts/run_hypothesis_ideator.py \
  --input skills/trade-hypothesis-ideator/examples/example_input.json \
  --output-dir reports/
```

- Pass 2 (순위화 + 출력 + 선택적 내보내기):

```bash
python3 skills/trade-hypothesis-ideator/scripts/run_hypothesis_ideator.py \
  --input skills/trade-hypothesis-ideator/examples/example_input.json \
  --hypotheses reports/raw_hypotheses.json \
  --output-dir reports/ \
  --export-strategies
```

## 레퍼런스

- `references/hypothesis_types.md`
- `references/evidence_quality_guide.md`
