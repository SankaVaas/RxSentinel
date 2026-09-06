from uuid import UUID

from pydantic import BaseModel

from app.models.interaction_finding import FindingStatus, Severity


class InteractionCheckRequest(BaseModel):
    patient_id: UUID


class EvidenceItem(BaseModel):
    source: str  # "rxnorm" | "openfda" | "literature"
    citation: str
    url: str | None = None
    excerpt: str | None = None


class InteractionFindingRead(BaseModel):
    id: UUID
    drug_pair: list[str]
    severity: Severity
    status: FindingStatus
    mechanism: str
    clinical_recommendation: str
    evidence: list[EvidenceItem]
    critique_notes: str | None = None

    class Config:
        from_attributes = True


class InteractionCheckResponse(BaseModel):
    agent_run_id: UUID
    findings: list[InteractionFindingRead]
