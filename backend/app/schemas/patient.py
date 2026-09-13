from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field


class PatientBase(BaseModel):
    mrn: str = Field(..., description="Medical record number")
    first_name: str
    last_name: str
    date_of_birth: date
    sex: str
    egfr: float | None = Field(None, description="Estimated GFR, mL/min/1.73m2")
    hepatic_impairment: str | None = None
    allergies: str | None = None


class PatientCreate(PatientBase):
    pass


class PatientRead(PatientBase):
    id: UUID
    active_medication_count: int = 0

    class Config:
        from_attributes = True


class PatientListResponse(BaseModel):
    total: int
    results: list[PatientRead]
