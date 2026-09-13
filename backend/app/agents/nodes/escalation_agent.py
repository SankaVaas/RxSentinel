"""Routes surviving findings to the appropriate workflow lane:
auto_cleared (critique falsified it), pending_review (needs a clinician's eyes),
or escalated (high/contraindicated severity — urgent notification).
"""
import logging

from app.agents.state import AgentState

logger = logging.getLogger(__name__)

URGENT_SEVERITIES = {"high", "contraindicated"}


async def run(state: AgentState) -> dict:
    critique_by_pair = {tuple(r["drug_pair"]): r for r in state["critique_results"]}

    final_findings = []
    escalation_queue = []

    for finding in state["reasoned_findings"]:
        pair = tuple(finding["drug_pair"])
        critique = critique_by_pair.get(pair)

        if critique and not critique["survives_critique"]:
            status = "auto_cleared"
        elif finding["severity"] in URGENT_SEVERITIES:
            status = "escalated"
        else:
            status = "pending_review"

        record = {
            **finding,
            "status": status,
            "critique_notes": critique["critique_notes"] if critique else None,
        }
        final_findings.append(record)

        if status == "escalated":
            escalation_queue.append(record)

    logger.info(
        "Escalation: %s total findings, %s escalated urgently",
        len(final_findings),
        len(escalation_queue),
    )
    return {"final_findings": final_findings, "escalation_queue": escalation_queue}
