# Hints Schema

이 schema를 후속 concept synthesis와 auto detection의 입력으로 사용합니다.

```yaml
generated_at_utc: "2026-02-22T12:00:00+00:00"
as_of: "2026-02-20"
meta:
  rule_hints: 6
  llm_hints: 3
  total_hints: 9
  regime: RiskOn
hints:
  - title: "Breadth-supported breakout regime"
    observation: "Risk-on regime with pct_above_ma50=0.65"
    preferred_entry_family: "pivot_breakout"  # optional
    symbols: ["NVDA", "AVGO"]              # optional
    regime_bias: "RiskOn"                    # optional
    mechanism_tag: "behavior"                # optional
```

## 필드 노트

- `preferred_entry_family`: optional. 제공 시 `pivot_breakout` 또는 `gap_up_continuation`이어야 함.
- `symbols`: optional 집중 목록. 비어 있으면 광범위한 시장 힌트.
- `regime_bias`: optional regime gate (`RiskOn`, `Neutral`, `RiskOff`).
- `mechanism_tag`: optional 메커니즘 라벨 (`behavior`, `flow`, `structure` 등).

## LLM CLI 계약

`build_hints.py --llm-ideas-cmd "<command>"`는 JSON을 stdin으로 전송합니다:

```json
{
  "as_of": "YYYY-MM-DD",
  "market_summary": {...},
  "anomalies": [...],
  "news_reactions": [...],
  "instruction": "Generate concise edge hints ..."
}
```

명령은 다음 중 하나를 출력해야 합니다:

- `[{...}, {...}]`
- `{"hints": [{...}, {...}]}`
