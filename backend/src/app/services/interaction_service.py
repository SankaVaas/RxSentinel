"""Orchestrates a full agent run: builds the LangGraph, executes it, persists
every step to AgentRunStep for audit purposes, and materializes findings.

This is the single call site the API layer uses — endpoints should never
import from app.agents directly.
"""
import logging
import time
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.graph import build_graph
from app.models.agent_run import AgentRun, RunStatus
from app.models.interaction_finding import InteractionFinding
from app.services.audit_service import record_step

logger = logging.getLogger(__name__)


async def run_interaction_check(db: AsyncSession, patient_id: UUID, triggered_by_user_id: UUID | None) -> AgentRun:
    agent_run = AgentRun(patient_id=patient_id, status=RunStatus.RUNNING, triggered_by_user_id=triggered_by_user_id)
    db.add(agent_run)
    await db.flush()  # get agent_run.id without committing yet

    graph = build_graph(db)
    initial_state = {
        "agent_run_id": str(agent_run.id),
        "patient_context": {"patient_id": str(patient_id)},
        "interaction_candidates": [],
        "reasoned_findings": [],
        "critique_results": [],
        "final_findings": [],
        "escalation_queue": [],
        "errors": [],
    }

    step_index = 0
    final_state = initial_state

    try:
        # `astream` yields the state after each node executes — this is what
        # lets us persist a step-by-step audit trail rather than only the
        # final result.
        async for node_output in graph.astream(initial_state):
            for node_name, output in node_output.items():
                start = time.monotonic()
                await record_step(
                    db,
                    agent_run_id=agent_run.id,
                    step_index=step_index,
                    node_name=node_name,
                    input_payload=final_state,
                    output_payload=output,
                    duration_ms=int((time.monotonic() - start) * 1000),
                )
                final_state = {**final_state, **output}
                step_index += 1

        agent_run.status = RunStatus.COMPLETED

    except Exception:
        logger.exception("Agent run %s failed", agent_run.id)
        agent_run.status = RunStatus.FAILED
        await db.commit()
        raise

    for finding in final_state.get("final_findings", []):
        db.add(
            InteractionFinding(
                agent_run_id=agent_run.id,
                patient_id=patient_id,
                drug_pair=list(finding["drug_pair"]),
                severity=finding["severity"],
                status=finding["status"],
                mechanism=finding["mechanism"],
                clinical_recommendation=finding["clinical_recommendation"],
                evidence=finding["evidence"],
                critique_notes=finding.get("critique_notes"),
            )
        )

    await db.commit()
    await db.refresh(agent_run)
    return agent_run
