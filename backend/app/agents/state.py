"""Shared state passed between LangGraph nodes.

Every node reads from and writes to this object. Keeping it a single typed
schema (rather than a free-form dict) is what makes the audit trail
(AgentRunStep.input_payload / output_payload) meaningful — each step's diff
against this state is exactly what a reviewer or the AgentTraceViewer needs.
"""
from typing import Annotated, TypedDict
from uuid import UUID

import operator


class PatientContext(TypedDict):
    patient_id: str
    egfr: float | None
    hepatic_impairment: str | None
    age: int | None
    active_rxcuis: list[str]


class RetrievedEvidence(TypedDict):
    source: str
    citation: str
    url: str | None
    excerpt: str | None


class InteractionCandidate(TypedDict):
    drug_pair: tuple[str, str]
    ground_truth_severity: str | None   # from RxNorm/OpenFDA, if found
    llm_flagged: bool                   # did retrieval/reasoning surface this pair
    evidence: list[RetrievedEvidence]


class ReasonedFinding(TypedDict):
    drug_pair: tuple[str, str]
    severity: str
    mechanism: str
    clinical_recommendation: str
    evidence: list[RetrievedEvidence]
    confidence: float


class CritiqueResult(TypedDict):
    drug_pair: tuple[str, str]
    survives_critique: bool             # False => critique agent falsified it
    critique_notes: str


class AgentState(TypedDict):
    agent_run_id: str
    patient_context: PatientContext
    interaction_candidates: Annotated[list[InteractionCandidate], operator.add]
    reasoned_findings: Annotated[list[ReasonedFinding], operator.add]
    critique_results: Annotated[list[CritiqueResult], operator.add]
    final_findings: list[dict]
    escalation_queue: list[dict]
    errors: Annotated[list[str], operator.add]
