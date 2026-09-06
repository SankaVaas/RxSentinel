from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db_session, require_role
from app.models.medication import Medication, PatientMedication
from app.models.patient import Patient
from app.schemas.medication import MedicationAdd, MedicationRead

router = APIRouter()


@router.post(
    "/{patient_id}/medications",
    response_model=MedicationRead,
    status_code=status.HTTP_201_CREATED,
)
async def add_medication(
    patient_id: UUID,
    payload: MedicationAdd,
    db: AsyncSession = Depends(get_db_session),
    _user: dict = Depends(require_role("clinician")),
) -> PatientMedication:
    patient = await db.get(Patient, patient_id)
    if patient is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Patient not found")

    medication = await db.get(Medication, payload.rxcui)
    if medication is None:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"Unknown RxCUI {payload.rxcui}. Sync the medication reference table first.",
        )

    patient_med = PatientMedication(
        patient_id=patient_id,
        rxcui=payload.rxcui,
        dose=payload.dose,
        frequency=payload.frequency,
    )
    db.add(patient_med)
    await db.commit()
    await db.refresh(patient_med)

    return MedicationRead(
        id=patient_med.id,
        rxcui=patient_med.rxcui,
        name=medication.name,
        dose=patient_med.dose,
        frequency=patient_med.frequency,
        active=patient_med.active,
    )


@router.get("/{patient_id}/medications", response_model=list[MedicationRead])
async def list_medications(
    patient_id: UUID,
    db: AsyncSession = Depends(get_db_session),
) -> list[MedicationRead]:
    patient = await db.get(Patient, patient_id)
    if patient is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Patient not found")

    results = []
    for pm in patient.medications:
        med = await db.get(Medication, pm.rxcui)
        results.append(
            MedicationRead(
                id=pm.id, rxcui=pm.rxcui, name=med.name if med else pm.rxcui,
                dose=pm.dose, frequency=pm.frequency, active=pm.active,
            )
        )
    return results
