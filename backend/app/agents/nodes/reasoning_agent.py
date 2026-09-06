"""Reconciles literature context + structured ground truth into a
patient-specific severity judgment and clinical recommendation. Only
candidates with *some* signal (ground truth OR retrieved evidence) reach this
node — pure noise is dropped upstream implicitly by having empty evidence.
"""
import json
import logging

import anthropic

from app.agents.state import AgentState, ReasonedFinding
from app.config import get_settings

logger = logging.getLogger(__name__)

REASONING_SYSTEM_PROMPT = """\
You are a clinical pharmacology reasoning assistant. You are given:
- a candidate drug-drug interaction pair
- structured ground-truth severity (if available)
- retrieved literature/label excerpts
- patient-specific factors (age, eGFR, hepatic impairment)

Produce a JSON object with: severity (low|moderate|high|contraindicated),
mechanism (1-2 sentences), clinical_recommendation (1-2 sentences), and
confidence (0-1 float). Ground every claim in the provided evidence. If the
evidence is insufficient to support a specific severity, say so and default
to "low" with confidence <= 0.4 rather than guessing.
Respond with ONLY the JSON object, no other text.
"""


async def run(state: AgentState) -> dict:
    settings = get_settings()
    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    findings: list[ReasonedFinding] = []

    for candidate in state["interaction_candidates"]:
        if not candidate["ground_truth_severity"] and not candidate["evidence"]:
            continue  # no signal at all — skip rather than fabricate

        user_payload = {
            "drug_pair": candidate["drug_pair"],
            "ground_truth_severity": candidate["ground_truth_severity"],
            "evidence": candidate["evidence"],
            "patient_context": state["patient_context"],
        }

        response = await client.messages.create(
            model=settings.anthropic_model,
            max_tokens=500,
            system=REASONING_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": json.dumps(user_payload)}],
        )
        raw_text = response.content[0].text
        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError:
            logger.warning("Reasoning agent returned non-JSON for %s", candidate["drug_pair"])
            continue

        findings.append(
            {
                "drug_pair": candidate["drug_pair"],
                "severity": parsed["severity"],
                "mechanism": parsed["mechanism"],
                "clinical_recommendation": parsed["clinical_recommendation"],
                "evidence": candidate["evidence"],
                "confidence": float(parsed["confidence"]),
            }
        )

    logger.info("Reasoning agent produced %s findings", len(findings))
    return {"reasoned_findings": findings}
