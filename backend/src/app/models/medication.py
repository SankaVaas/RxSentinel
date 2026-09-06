from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampedBase

if TYPE_CHECKING:
    from app.models.patient import Patient


class Medication(Base):
    """Canonical drug reference, keyed by RxNorm concept ID (RxCUI)."""

    __tablename__ = "medications"

    rxcui: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    generic_name: Mapped[str | None] = mapped_column(String(256), nullable=True)
    drug_class: Mapped[str | None] = mapped_column(String(128), nullable=True)


class PatientMedication(TimestampedBase):
    """A medication currently (or historically) prescribed to a patient."""

    __tablename__ = "patient_medications"

    patient_id: Mapped[UUID] = mapped_column(ForeignKey("patients.id"))
    rxcui: Mapped[str] = mapped_column(ForeignKey("medications.rxcui"))
    dose: Mapped[str | None] = mapped_column(String(64), nullable=True)
    frequency: Mapped[str | None] = mapped_column(String(64), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    patient: Mapped["Patient"] = relationship(back_populates="medications")
    medication: Mapped["Medication"] = relationship()
