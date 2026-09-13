"""Adversarial verification step. For every reasoned finding, this node
actively tries to falsify it — checking for contradicting evidence, weak
evidence chains, or overreach given the patient's actual clinical context —
before it is allowed to reach a clinician. This is the primary defense
against LLM overreach/hallucination in a safety-critical setting.
"""
import json
import logging

from groq import AsyncGroq

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
Keep critique_notes to one or two sentences. If you find any of the above
problems, set survives_critique to false and explain why in critique_notes.
Be skeptical by default.
"""


async def run(state: AgentState) -> dict:
    settings = get_settings()
    client = AsyncGroq(api_key=settings.groq_api_key)

    results: list[CritiqueResult] = []

    for finding in state["reasoned_findings"]:
        payload = {"finding": finding, "patient_context": state["patient_context"]}

        try:
            response = await client.chat.completions.create(
                model=settings.groq_model,
                max_tokens=800,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": CRITIQUE_SYSTEM_PROMPT},
                    {"role": "user", "content": json.dumps(payload)},
                ],
            )
            raw_text = response.choices[0].message.content
            parsed = json.loads(raw_text)
            survives = bool(parsed["survives_critique"])
            notes = str(parsed["critique_notes"])
        except Exception:  # noqa: BLE001
            # Fail closed: if the critique step itself errors (truncated
            # JSON, API error, malformed response), do NOT auto-clear --
            # default to human review.
            logger.exception("Critique agent failed for %s", finding["drug_pair"])
            survives, notes = True, "Critique step failed; defaulting to human review."

        results.append(
            {
                "drug_pair": finding["drug_pair"],
                "survives_critique": survives,
                "critique_notes": notes,
            }
        )

    logger.info(
        "Critique agent: %s/%s findings survived",
        sum(1 for r in results if r["survives_critique"]),
        len(results),
    )
    return {"critique_results": results}