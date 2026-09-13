"""Orchestrates a full agent run: builds the LangGraph, executes it, persists
every step to AgentRunStep for audit purposes, and materializes findings.

This is the single call site the API layer uses — endpoints should never
import from app.agents directly.
"""
import logging
import time
from uuid import UUID, uuid4

from app.core.metrics import agent_findings_total, agent_runs_total

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.agents.graph import build_graph
from app.models.agent_run import AgentRun, AgentRunStep, RunStatus
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
        agent_runs_total.labels(status="completed").inc()

    except Exception:
        logger.exception("Agent run %s failed", agent_run.id)
        agent_run.status = RunStatus.FAILED
        agent_runs_total.labels(status="failed").inc()
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
        agent_findings_total.labels(severity=finding["severity"], status=finding["status"]).inc()

    await db.commit()
    result = await db.execute(
        select(AgentRun)
        .options(selectinload(AgentRun.findings))
        .where(AgentRun.id == agent_run.id)
    )
    loaded_agent_run = result.scalar_one_or_none()
    return loaded_agent_run or agent_run
