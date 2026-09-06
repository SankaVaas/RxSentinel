"""Loads the patient's clinical context: active meds, renal/hepatic function,
age, allergies. This runs first because every downstream risk judgment
(dose-adjusted interaction severity, contraindication checks) depends on it.
"""
import logging
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.state import AgentState, PatientContext
from app.models.patient import Patient

logger = logging.getLogger(__name__)


async def run(state: AgentState, db: AsyncSession) -> dict:
    patient_id = state["patient_context"]["patient_id"]
    patient = await db.get(Patient, patient_id)
    if patient is None:
        return {"errors": [f"Patient {patient_id} not found"]}

    today = date.today()
    age = today.year - patient.date_of_birth.year - (
        (today.month, today.day) < (patient.date_of_birth.month, patient.date_of_birth.day)
    )

    active_rxcuis = [
        pm.rxcui for pm in patient.medications if pm.active
    ]

    context: PatientContext = {
        "patient_id": str(patient.id),
        "egfr": patient.egfr,
        "hepatic_impairment": patient.hepatic_impairment,
        "age": age,
        "active_rxcuis": active_rxcuis,
    }

    logger.info("Loaded patient context: %s active meds", len(active_rxcuis))
    return {"patient_context": context}
