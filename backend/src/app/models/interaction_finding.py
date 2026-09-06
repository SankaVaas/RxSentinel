import enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampedBase

if TYPE_CHECKING:
    from app.models.agent_run import AgentRun


class Severity(str, enum.Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CONTRAINDICATED = "contraindicated"


class FindingStatus(str, enum.Enum):
    AUTO_CLEARED = "auto_cleared"          # critique agent falsified the risk
    PENDING_REVIEW = "pending_review"
    ESCALATED = "escalated"                # urgent, sent straight to clinician
    ACKNOWLEDGED = "acknowledged"          # clinician has reviewed


class InteractionFinding(TimestampedBase):
    """A single drug-drug interaction finding produced by an agent run."""

    __tablename__ = "interaction_findings"

    agent_run_id: Mapped[UUID] = mapped_column(ForeignKey("agent_runs.id"))
    patient_id: Mapped[UUID] = mapped_column(ForeignKey("patients.id"))

    drug_pair: Mapped[list[str]] = mapped_column(ARRAY(String(32)))  # [rxcui_a, rxcui_b]
    severity: Mapped[Severity] = mapped_column(Enum(Severity))
    status: Mapped[FindingStatus] = mapped_column(Enum(FindingStatus))

    mechanism: Mapped[str] = mapped_column(Text)
    clinical_recommendation: Mapped[str] = mapped_column(Text)

    # Structured ground-truth evidence (RxNorm/OpenFDA) + retrieved literature,
    # each with a source URL/citation — never an unattributed LLM claim.
    evidence: Mapped[dict] = mapped_column(JSONB)

    critique_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    agent_run: Mapped["AgentRun"] = relationship(back_populates="findings")
