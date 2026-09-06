from sqlalchemy import Date, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampedBase


class Patient(TimestampedBase):
    """Minimal clinical demographic record needed for risk-scoring.

    NOTE: in a real deployment this would sit behind a de-identification /
    tokenization boundary and be linked to an EHR via MRN, not stored raw.
    """

    __tablename__ = "patients"

    mrn: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    date_of_birth: Mapped[Date] = mapped_column(Date)
    sex: Mapped[str] = mapped_column(String(16))

    # Renal/hepatic function drive dose-adjusted interaction risk.
    egfr: Mapped[float | None] = mapped_column(Float, nullable=True)  # mL/min/1.73m2
    hepatic_impairment: Mapped[str | None] = mapped_column(String(32), nullable=True)

    allergies: Mapped[str | None] = mapped_column(String(512), nullable=True)

    medications: Mapped[list["PatientMedication"]] = relationship(
        back_populates="patient", cascade="all, delete-orphan"
    )
