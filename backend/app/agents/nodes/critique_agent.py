"""Adversarial verification step. For every reasoned finding, this node
actively tries to falsify it — checking for contradicting evidence, weak
evidence chains, or overreach given the patient's actual clinical context —
before it is allowed to reach a clinician. This is the primary defense
against LLM overreach/hallucination in a safety-critical setting.
"""
import json
import logging

import anthropic

from app.agents.state import AgentState, CritiqueResult
from app.config import get_settings

logger = logging.getLogger(__name__)

CRITIQUE_SYSTEM_PROMPT = """\
You are an adversarial clinical reviewer. Your job is to try to DISPROVE the
given interaction finding, not confirm it. Check:
1. Is the evidence actually specific to this drug pair, or generic?
2. Does the severity claim overreach what the evidence supports?
3. Given the patient's actual renal/hepatic function and age, is the
   mechanism even clinically relevant (e.g. a renally-cleared-drug
   interaction is irrelevant if eGFR is normal)?
4. Is there any evidence in the payload that contradicts the finding?

Respond with ONLY a JSON object: {"survives_critique": bool, "critique_notes": str}.
If you find any of the above problems, set survives_critique to false and
explain why in critique_notes. Be skeptical by default.
"""


async def run(state: AgentState) -> dict:
    settings = get_settings()
    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

    results: list[CritiqueResult] = []

    for finding in state["reasoned_findings"]:
        payload = {
            "finding": finding,
            "patient_context": state["patient_context"],
        }
        response = await client.messages.create(
            model=settings.anthropic_model,
            max_tokens=400,
            system=CRITIQUE_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": json.dumps(payload)}],
        )
        raw_text = response.content[0].text
        try:
            parsed = json.loads(raw_text)
        except json.JSONDecodeError:
            logger.warning("Critique agent returned non-JSON for %s", finding["drug_pair"])
            # Fail closed: if critique itself fails, don't auto-clear.
            parsed = {"survives_critique": True, "critique_notes": "Critique step failed; defaulting to human review."}

        results.append(
            {
                "drug_pair": finding["drug_pair"],
                "survives_critique": parsed["survives_critique"],
                "critique_notes": parsed["critique_notes"],
            }
        )

    logger.info(
        "Critique agent: %s/%s findings survived",
        sum(1 for r in results if r["survives_critique"]),
        len(results),
    )
    return {"critique_results": results}
