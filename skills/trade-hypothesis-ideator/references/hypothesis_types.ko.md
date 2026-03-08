# Hypothesis Types

## entry_family 매핑
- `breakout` -> `pivot_breakout` (내보내기 가능)
- `earnings_drift` / `gap_continuation` -> `gap_up_continuation` (내보내기 가능)
- `momentum` / `pullback` / `regime_shift` -> `research_only` (v1에서는 내보내기 불가)

## 참고
- `edge-finder-candidate/v1`는 `pivot_breakout`과 `gap_up_continuation`만 지원합니다.
- `gap_open_scored`는 v2 지원이 추가되기 전까지 research-only로 처리됩니다.
