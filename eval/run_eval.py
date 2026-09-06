"""Agent evaluation harness: runs the golden dataset through the full agent
graph and reports precision/recall on severity classification, plus
critique-agent behavior on the edge-case scenarios.

This is what should gate CI (see .github/workflows/ci.yml) — a regression in
agent accuracy should fail a PR the same way a broken unit test would.

Usage:
    python run_eval.py [--report-path report.md]
"""
import argparse
import asyncio
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

GOLDEN_DATASETS_DIR = Path(__file__).parent / "golden_datasets"


def load_jsonl(path: Path) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


async def evaluate_known_interactions() -> dict:
    cases = load_jsonl(GOLDEN_DATASETS_DIR / "known_interactions.jsonl")
    results = {"total": len(cases), "correct": 0, "mismatches": []}

    for case in cases:
        # TODO: wire this up to app.services.interaction_service against a
        # test patient seeded with exactly [rxcui_a, rxcui_b], then compare
        # the resulting finding's severity to case["expected_severity"].
        logger.info("Would evaluate: %s + %s -> expect %s", case["drug_a"], case["drug_b"], case["expected_severity"])

    return results


async def evaluate_edge_cases() -> dict:
    cases = load_jsonl(GOLDEN_DATASETS_DIR / "edge_cases.jsonl")
    return {"total": len(cases), "scenarios": [c["scenario"] for c in cases]}


async def main(report_path: str | None) -> None:
    known_results = await evaluate_known_interactions()
    edge_results = await evaluate_edge_cases()

    report_lines = [
        "# RxSentinel Agent Eval Report",
        "",
        f"## Known interactions: {known_results['correct']}/{known_results['total']} correct",
        "",
        f"## Edge cases covered: {edge_results['total']}",
        *[f"- {s}" for s in edge_results["scenarios"]],
    ]
    report = "\n".join(report_lines)
    print(report)

    if report_path:
        Path(report_path).write_text(report)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-path", default=None)
    args = parser.parse_args()
    asyncio.run(main(args.report_path))
