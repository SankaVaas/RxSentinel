from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db_session
from app.models.interaction_finding import InteractionFinding
from app.schemas.interaction import InteractionCheckRequest, InteractionCheckResponse
from app.services.interaction_service import run_interaction_check

router = APIRouter()


def _is_valid_uuid(value) -> bool:
    if not value:
        return False
    try:
        UUID(str(value))
        return True
    except ValueError:
        return False


@router.post("/check", response_model=InteractionCheckResponse)
async def check_interactions(
    payload: InteractionCheckRequest,
    db: AsyncSession = Depends(get_db_session),
    user: dict = Depends(get_current_user),
) -> InteractionCheckResponse:
    """Runs the full agent graph (retrieve -> verify -> reason -> critique ->
    escalate) for a patient's current medication list and returns the
    resulting findings, each carrying its evidence and status."""
    sub = user.get("sub")
    triggered_by_user_id = sub if _is_valid_uuid(sub) else None

    agent_run = await run_interaction_check(
        db, patient_id=payload.patient_id, triggered_by_user_id=triggered_by_user_id
    )

    findings_result = await db.execute(
        select(InteractionFinding).where(InteractionFinding.agent_run_id == agent_run.id)
    )
    findings = findings_result.scalars().all()
    if not findings and getattr(agent_run, "findings", None):
        findings = agent_run.findings

    return InteractionCheckResponse(agent_run_id=agent_run.id, findings=findings)