"""Drug reference lookup — powers the medication search/typeahead in the
frontend so clinicians search by drug name rather than typing raw RxCUI
codes. Separate from patients.py/medications.py since this endpoint has no
patient context; it's a pure reference-data lookup.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db_session
from app.models.medication import Medication
from app.tools.rxnorm_client import approximate_search

router = APIRouter()


@router.get("/search")
async def search_drugs(
    q: str = Query(..., min_length=2, description="Drug name, partial or misspelled"),
    db: AsyncSession = Depends(get_db_session),
    _user: dict = Depends(get_current_user),
) -> list[dict]:
    """Searches RxNorm by drug name and upserts results into the local
    `medications` reference table, so the returned RxCUIs can immediately
    be attached to a patient via POST /patients/{id}/medications without a
    separate sync step.
    """
    candidates = await approximate_search(q)

    for candidate in candidates:
        stmt = (
            pg_insert(Medication)
            .values(rxcui=candidate["rxcui"], name=candidate["name"])
            .on_conflict_do_nothing(index_elements=["rxcui"])
        )
        await db.execute(stmt)
    await db.commit()

    return candidates
