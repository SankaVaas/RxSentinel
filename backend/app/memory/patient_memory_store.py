"""Long-term memory: the patient's persisted medication history and prior
finding outcomes (e.g. "clinician previously acknowledged and accepted this
interaction risk"). This is what lets the agent avoid re-flagging a
risk the clinician has already reviewed and consciously accepted, while
still re-flagging it if the patient's clinical context has materially
changed (e.g. eGFR dropped).
"""
import logging
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.interaction_finding import FindingStatus, InteractionFinding

logger = logging.getLogger(__name__)


async def get_acknowledged_pairs(db: AsyncSession, patient_id: UUID) -> set[tuple[str, str]]:
    stmt = select(InteractionFinding.drug_pair).where(
        InteractionFinding.patient_id == patient_id,
        InteractionFinding.status == FindingStatus.ACKNOWLEDGED,
    )
    rows = (await db.execute(stmt)).scalars().all()
    return {tuple(sorted(pair)) for pair in rows}
