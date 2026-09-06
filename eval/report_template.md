# RxSentinel Agent Eval Report — {date}

## Summary
- Known interactions: {correct}/{total} correct severity classification
- False positive rate (auto-cleared incorrectly): {fp_rate}
- False negative rate (should have escalated, didn't): {fn_rate}
- Edge cases covered: {edge_case_count}

## Notes
Regressions in false-negative rate should block merge — a missed
contraindicated interaction is the failure mode this whole system exists to
prevent.
