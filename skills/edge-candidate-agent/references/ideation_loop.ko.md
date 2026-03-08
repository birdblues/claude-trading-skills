# Ideation Loop (Human + LLM)

자동 탐지를 실행하기 전에 힌트를 생성할 때 이 참고 문서를 사용하세요.

## 힌트 파일 스키마 (`hints.yaml`)

```yaml
hints:
  - title: "AI leaders breaking out after shallow pullback"
    observation: "Large-cap semis recovered above key moving averages"
    preferred_entry_family: "pivot_breakout"
    symbols: ["NVDA", "AVGO", "SMCI"]
    regime_bias: "RiskOn"
    mechanism_tag: "behavior"
```

## LLM CLI 연동 계약

`auto_detect_candidates.py --llm-ideas-cmd "<command>"`는 아래 JSON을 stdin으로 전달합니다:

```json
{
  "as_of": "YYYY-MM-DD",
  "market_summary": {...},
  "anomalies": [...],
  "instruction": "Generate concise edge hints ..."
}
```

명령은 다음 중 하나를 출력해야 합니다:

- `[{...}, {...}]` (YAML/JSON list), 또는
- `{"hints": [{...}, {...}]}`.

각 hint는 다음 필드를 지원합니다:

- `title`
- `observation`
- `preferred_entry_family` (`pivot_breakout` 또는 `gap_up_continuation`)
- `symbols` (optional)
- `regime_bias` (optional)
- `mechanism_tag` (optional)

## 권장 일일 루프

1. LLM 힌트 없이 detector를 실행하고 `anomalies.json`을 검토합니다.
2. 관측된 시장 행동을 바탕으로 `hints.yaml`을 생성하거나 수정합니다.
3. `--hints`(선택적으로 `--llm-ideas-cmd`)와 함께 detector를 다시 실행합니다.
4. 시간이 지나며 export된 티켓 품질을 비교하고 안정적인 아이디어만 유지합니다.
