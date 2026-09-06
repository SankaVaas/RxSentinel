from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db_session
from app.models.agent_run import AgentRun

router = APIRouter()


@router.get("/{agent_run_id}/trace")
async def get_agent_run_trace(
    agent_run_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: dict = Depends(get_current_user),
) -> dict:
    """Returns the full step-by-step trace for an agent run — this is what
    the frontend's AgentTraceViewer renders, and what a clinician or auditor
    uses to see exactly why a finding was surfaced or cleared."""
    agent_run = await db.get(AgentRun, agent_run_id)
    if agent_run is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Agent run not found")

    return {
        "agent_run_id": str(agent_run.id),
        "status": agent_run.status,
        "steps": [
            {
                "step_index": step.step_index,
                "node_name": step.node_name,
                "input": step.input_payload,
                "output": step.output_payload,
                "duration_ms": step.duration_ms,
            }
            for step in agent_run.steps
        ],
    }
