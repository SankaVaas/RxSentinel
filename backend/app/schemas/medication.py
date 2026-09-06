from uuid import UUID

from pydantic import BaseModel


class MedicationAdd(BaseModel):
    rxcui: str
    dose: str | None = None
    frequency: str | None = None


class MedicationRead(BaseModel):
    id: UUID
    rxcui: str
    name: str
    dose: str | None
    frequency: str | None
    active: bool

    class Config:
        from_attributes = True
