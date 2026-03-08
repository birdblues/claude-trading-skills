# Pivot Report: {strategy_id}

**Generated**: {generated_at_utc}
**Source Strategy**: {source_strategy_id}
**Diagnosis**: {diagnosis_summary}

---

## Stagnation Diagnosis

**Triggers Fired**: {triggers_count}
**Recommendation**: {recommendation}

{triggers_detail}

### Score Trajectory

{score_trajectory}

---

## Pivot Proposals

{pivot_proposals}

### Proposal: {proposal_id}

**Technique**: {pivot_technique}
**Target Archetype**: {target_archetype}
**Category**: {category}

**What Changed**:
- Signal: {signal_change}
- Horizon: {horizon_change}
- Risk: {risk_change}

**Why**: {why_explanation}

**Targeted Triggers**: {targeted_triggers}

**Scores**:
- Quality Potential: {quality_potential}
- Novelty: {novelty}
- Combined: {combined}

**Expected Failure Modes**:
{failure_modes}

---

## Summary

| Rank | Proposal | Archetype | Combined | Category |
|------|----------|-----------|----------|----------|
{summary_table}

---

## Next Steps

1. 제안을 검토하고 가장 유망한 pivot 방향을 선택
2. **exportable** 제안: `edge-candidate-agent` 파이프라인용 ticket YAML 즉시 사용 가능
3. **research_only** 제안: 파이프라인 통합 전 수동 전략 설계 필요
4. 선택한 pivot draft로 backtest-expert를 실행해 다음 반복 사이클 시작
