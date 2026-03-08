# Account Location Matrix

taxable 계좌와 tax-advantaged 계좌 간 배치를 제안할 때 이 매트릭스를 사용합니다.

## 기본 배치 로직

| Instrument profile | Taxable account | Tax-advantaged account | Rationale |
|---|---|---|---|
| Qualified-dividend-heavy US equity | 일반적으로 선호 | 선택 사항 | taxable 계좌에서 지속적 세후 효율이 더 좋을 수 있음 |
| REIT-heavy income holdings | 상대적으로 비선호 | 자주 선호 | 분배금에 ordinary-income 성분이 더 높을 수 있음 |
| BDC/high-distribution structures | 상대적으로 비선호 | 자주 선호 | taxable 계좌에서 세무 처리상 불리할 수 있음 |
| MLP (partnership units) | 사안별 판단 | tax-advantaged 계좌에서는 주의 | UBTI 및 K-1 복잡성으로 배치가 비자명할 수 있음 |
| Broad index ETF with low turnover | 대체로 허용 가능 | 또한 허용 가능 | 전체 자산 배치 설계에 따라 달라짐 |

MLP가 투자 mandate 밖이라면 `OUT-OF-SCOPE`로 명시하고 기본 배치 로직에서 제외합니다.

## 충돌 해결 규칙

계좌 배치 권고가 다른 요구와 충돌할 때:
1. 먼저 집중도와 리스크 통제를 우선.
2. 다음으로 유동성/인출 제약을 우선.
3. 마지막으로 세금 최적화를 우선.

## 출력 형식

보유 종목당 한 줄로 반환:

```text
[Ticker] -> [Recommended Account] | Why: [one sentence]
```
