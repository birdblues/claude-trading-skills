# Valuation 및 One-Off 점검

이 파일은 Kanchi Step 3 및 Step 4 의사결정에 사용합니다.

## Step 3: 섹터별 Valuation 매핑

| Sector/Type | Primary metric | Secondary metric | Pass condition 예시 |
|---|---|---|---|
| Banks/Insurers | `P/TBV` | `PER x PBR` (compatibility) + historical percentile | historical fair band를 명확히 상회하면 reject |
| REIT | `P/FFO` or `P/AFFO` | peer 대비 implied cap rate | 자체 5y median multiple 이하를 선호 |
| Asset-light growth | Forward `P/E` | `P/FCF` and 5y range | valuation 지표 최소 1개는 range 하단 절반 근처여야 함 |
| Mature cash cows | `P/FCF` | Dividend yield vs 5y average | fundamentals가 유지된 상태에서 historical mean 상회 yield 선호 |

참고:
- Kanchi의 원래 Japan-style 필터는 `PER x PBR`를 사용합니다.
- US banks에서는 tangible book이 표준 anchor이므로 일반적으로 `P/TBV`가 더 견고합니다.

지표가 서로 충돌하면 `PASS`를 강제로 내기보다 `HOLD-FOR-REVIEW`를 선택하세요.

## Step 4: One-Off 이익 체크리스트

각 항목을 `YES/NO`로 표시합니다. `YES`가 2개 이상이면 downgrade 또는 reject가 필요합니다.

1. Profit jump가 asset sales 또는 disposal gains에 의해 발생.
2. EPS가 legal settlement 또는 tax one-time effects로 상승.
3. revenue quality 개선 없이 margin expansion 발생.
4. 경영진이 핵심 profit 항목을 반복적으로 "non-recurring"으로 분류.
5. dividend support가 debt 증가 또는 asset liquidation과 연결된 것으로 보임.

## Step 4 출력 형식

리포트에서는 아래 compact output을 정확히 사용합니다:

```text
Step4 verdict: FAIL
Reason: EPS uplift mostly from one-time asset sale; recurring margin trend still weak.
```

각 reason은 한 문장으로 유지하세요.
