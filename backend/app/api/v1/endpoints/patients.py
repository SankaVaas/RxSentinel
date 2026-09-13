from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_current_user, get_db_session, require_role
from app.models.medication import PatientMedication
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientListResponse, PatientRead

router = APIRouter()


async def _to_patient_read(db: AsyncSession, patient: Patient) -> PatientRead:
    count_stmt = select(func.count()).select_from(PatientMedication).where(
        PatientMedication.patient_id == patient.id, PatientMedication.active.is_(True)
    )
    active_count = (await db.execute(count_stmt)).scalar_one()
    return PatientRead.model_validate({**patient.__dict__, "active_medication_count": active_count})


@router.get("", response_model=PatientListResponse)
async def list_patients(
    q: str | None = Query(None, description="Search by name or MRN"),
    limit: int = Query(25, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db_session),
    _user: dict = Depends(get_current_user),
) -> PatientListResponse:
    stmt = select(Patient)
    count_stmt = select(func.count()).select_from(Patient)

    if q:
        pattern = f"%{q}%"
        search_filter = or_(
            Patient.mrn.ilike(pattern),
            Patient.first_name.ilike(pattern),
            Patient.last_name.ilike(pattern),
        )
        stmt = stmt.where(search_filter)
        count_stmt = count_stmt.where(search_filter)

    total = (await db.execute(count_stmt)).scalar_one()
    stmt = stmt.order_by(Patient.last_name, Patient.first_name).limit(limit).offset(offset)
    patients = (await db.execute(stmt)).scalars().all()

    results = [await _to_patient_read(db, p) for p in patients]
    return PatientListResponse(total=total, results=results)


@router.post("", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
async def create_patient(
    payload: PatientCreate,
    db: AsyncSession = Depends(get_db_session),
    _user: dict = Depends(require_role("clinician")),
) -> PatientRead:
    existing = (
        await db.execute(select(Patient).where(Patient.mrn == payload.mrn))
    ).scalar_one_or_none()
    if existing:
        raise HTTPException(status.HTTP_409_CONFLICT, f"MRN {payload.mrn} already exists")

    patient = Patient(**payload.model_dump())
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    return await _to_patient_read(db, patient)


@router.get("/{patient_id}", response_model=PatientRead)
async def get_patient(
    patient_id: UUID,
    db: AsyncSession = Depends(get_db_session),
    _user: dict = Depends(get_current_user),
) -> PatientRead:
    patient = await db.get(Patient, patient_id)
    if patient is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Patient not found")
    return await _to_patient_read(db, patient)
