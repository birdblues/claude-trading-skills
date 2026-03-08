# Signal Mapping

리서치 티켓을 interface v1 기준으로
`trade-strategy-pipeline`에 export할 수 있는지 판단할 때 이 매핑을 사용합니다.

| Hypothesis Type | Export Status | Entry Family | Notes |
|---|---|---|---|
| `breakout` | exportable | `pivot_breakout` | `vcp_detection` block 필수. |
| `earnings_drift` | exportable | `gap_up_continuation` | gap continuation config 사용, Phase I에서 walk-forward 금지. |
| `momentum` | research-only | n/a | pipeline이 전용 momentum entry를 지원할 때까지 ticket으로 유지. |
| `pullback` | research-only | n/a | pullback signal family가 추가될 때까지 ticket으로 유지. |
| `sector_x_stock` | research-only | n/a | sector-relative filter가 strategy spec의 first-class가 될 때까지 ticket으로 유지. |
| `panic_reversal` | research-only | n/a | reversal signal family 구현 전까지 ticket으로 유지. |
| `low_vol_quality` | research-only | n/a | quality/risk filter가 signal 입력으로 지원될 때까지 ticket으로 유지. |
| `regime_shift` | research-only | n/a | pipeline에서 regime transition entry를 지원할 때까지 ticket으로 유지. |

## 규칙

티켓이 `research-only`이면 `strategy.yaml`을 생성하지 않습니다.
티켓을 기록해 두고 향후 interface/version 확장을 위한 큐에 넣습니다.
