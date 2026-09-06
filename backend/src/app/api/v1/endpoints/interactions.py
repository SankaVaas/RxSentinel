from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db_session
from app.schemas.interaction import InteractionCheckRequest, InteractionCheckResponse
from app.services.interaction_service import run_interaction_check

router = APIRouter()


@router.post("/check", response_model=InteractionCheckResponse)
async def check_interactions(
    payload: InteractionCheckRequest,
    db: AsyncSession = Depends(get_db_session),
    user: dict = Depends(get_current_user),
) -> InteractionCheckResponse:
    """Runs the full agent graph (retrieve -> verify -> reason -> critique ->
    escalate) for a patient's current medication list and returns the
    resulting findings, each carrying its evidence and status."""
    agent_run = await run_interaction_check(
        db, patient_id=payload.patient_id, triggered_by_user_id=user.get("sub")
    )
    return InteractionCheckResponse(agent_run_id=agent_run.id, findings=agent_run.findings)
