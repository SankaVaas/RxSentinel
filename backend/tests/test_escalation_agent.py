import pytest

from app.agents.nodes import escalation_agent


@pytest.mark.asyncio
async def test_finding_falsified_by_critique_is_auto_cleared() -> None:
    state = {
        "reasoned_findings": [
            {
                "drug_pair": ("111", "222"),
                "severity": "high",
                "mechanism": "m",
                "clinical_recommendation": "r",
                "evidence": [],
                "confidence": 0.8,
            }
        ],
        "critique_results": [
            {"drug_pair": ("111", "222"), "survives_critique": False, "critique_notes": "Not clinically relevant"}
        ],
    }
    result = await escalation_agent.run(state)
    assert result["final_findings"][0]["status"] == "auto_cleared"
    assert result["escalation_queue"] == []


@pytest.mark.asyncio
async def test_high_severity_surviving_critique_is_escalated() -> None:
    state = {
        "reasoned_findings": [
            {
                "drug_pair": ("111", "222"),
                "severity": "contraindicated",
                "mechanism": "m",
                "clinical_recommendation": "r",
                "evidence": [],
                "confidence": 0.9,
            }
        ],
        "critique_results": [
            {"drug_pair": ("111", "222"), "survives_critique": True, "critique_notes": "Confirmed"}
        ],
    }
    result = await escalation_agent.run(state)
    assert result["final_findings"][0]["status"] == "escalated"
    assert len(result["escalation_queue"]) == 1
