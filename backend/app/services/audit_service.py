"""Writes immutable AgentRunStep rows — the append-only audit trail that
powers both the frontend AgentTraceViewer and the eval harness."""
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent_run import AgentRunStep


async def record_step(
    db: AsyncSession,
    *,
    agent_run_id: UUID,
    step_index: int,
    node_name: str,
    input_payload: dict,
    output_payload: dict,
    duration_ms: int,
) -> None:
    db.add(
        AgentRunStep(
            agent_run_id=agent_run_id,
            step_index=step_index,
            node_name=node_name,
            input_payload=input_payload,
            output_payload=output_payload,
            duration_ms=duration_ms,
        )
    )
    await db.flush()
