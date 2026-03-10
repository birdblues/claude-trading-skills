# Revision Loop Rules

## 개요

review-revision feedback loop는 strategy draft가 export 전에
품질 기준을 충족하도록 보장합니다.
draft는 최대 반복 횟수까지 review와 선택적 revision 단계를 순환합니다.

## Verdict 카테고리

| Verdict | Meaning                                      | Next Action                  |
|---------|----------------------------------------------|------------------------------|
| PASS    | Draft meets quality standards                | Accumulated; eligible for export |
| REJECT  | Draft has fundamental flaws                  | Accumulated; no further action   |
| REVISE  | Draft needs specific improvements            | Apply revisions, re-review       |

## Loop 메커니즘

1. 모든 draft가 첫 번째 review iteration(iter 0)에 들어갑니다.
2. 각 review 이후:
   - PASS draft는 passed list에 누적됩니다(재리뷰하지 않음).
   - REJECT draft는 rejected list에 누적됩니다(재검토하지 않음).
   - REVISE draft는 revision 단계로 진행합니다.
3. 수정된 draft는 다음 iteration의 review 단계로 재진입합니다.
4. `max_review_iterations`(기본값: 2) 이후에도 REVISE가 남으면
   `research_probe` variant로 강등하고 export 불가로 표시합니다.

## 누적 규칙

- PASS/REJECT 목록은 iteration 전체에 걸쳐 append-only입니다.
- iteration 0에서 PASS한 draft는 iteration 1이 실행되어도 PASS 상태를 유지합니다.
- iteration 0에서 REJECT된 draft는 다시 검토하지 않습니다.
- REVISE draft만 다음 iteration으로 전달됩니다.

## Revision Heuristic (apply_revisions)

draft가 REVISE verdict와 revision instruction을 받으면:

| Instruction Pattern             | Action                                          |
|---------------------------------|-------------------------------------------------|
| "Reduce entry conditions"       | Keep only the first 5 entry conditions           |
| "Add volume filter"             | Append "avg_volume > 500000" to conditions       |
| "Round precise thresholds"      | Round decimal numbers in conditions to integers  |

revision 이후:
- `variant`는 변경하지 않음
- `export_ready_v1`는 변경하지 않음

## 강등 규칙 (downgrade_to_research_probe)

REVISE draft가 모든 iteration을 소진하면:
- `variant` = "research_probe"로 설정
- `export_ready_v1` = False로 설정
- downgraded list에 draft_id 기록

## Export 자격

다음 조건을 모두 만족할 때 draft를 export할 수 있습니다:
1. Verdict가 PASS
2. `export_ready_v1`가 True
3. `entry_family`가 EXPORTABLE_FAMILIES에 포함
   (pivot_breakout, gap_up_continuation)

## Export용 Ticket 생성

- **사전 생성 ticket**: designer 단계에서 `--exportable-tickets-dir`에
  export 가능한 ticket YAML을 기록할 수 있습니다. 가능하면 이를 우선 사용합니다.
- **수정 draft ticket**: 수정된 draft에 사전 생성 ticket이 없으면
  `build_export_ticket()`이 draft 데이터에서 ticket을 생성합니다.
- export는 `--ticket PATH --strategies-dir DIR` CLI 인터페이스를 사용합니다.
