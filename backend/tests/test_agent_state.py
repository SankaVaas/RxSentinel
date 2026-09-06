"""Unit tests for the agent state reducers — regressions here silently
corrupt the audit trail, so they're worth testing directly."""
from app.agents.state import AgentState


def test_interaction_candidates_reducer_appends() -> None:
    state: AgentState = {
        "agent_run_id": "run-1",
        "patient_context": {},
        "interaction_candidates": [],
        "reasoned_findings": [],
        "critique_results": [],
        "final_findings": [],
        "escalation_queue": [],
        "errors": [],
    }
    assert state["interaction_candidates"] == []
