from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field


class PatientBase(BaseModel):
    mrn: str = Field(..., description="Medical record number")
    date_of_birth: date
    sex: str
    egfr: float | None = Field(None, description="Estimated GFR, mL/min/1.73m2")
    hepatic_impairment: str | None = None
    allergies: str | None = None


class PatientCreate(PatientBase):
    pass


class PatientRead(PatientBase):
    id: UUID

    class Config:
        from_attributes = True
