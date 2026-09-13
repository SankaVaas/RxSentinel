from datetime import date
from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.api.v1.endpoints import interactions as interactions_endpoint
from app.dependencies import get_current_user, get_db_session
from app.main import app
from app.models.agent_run import AgentRun
from app.models.medication import Medication, PatientMedication
from app.models.patient import Patient


class FakeSession:
    def __init__(self):
        self.patients = {}
        self.medications = {}
        self.agent_runs = {}

    async def get(self, model, identifier):
        if model is Patient:
            return self.patients.get(identifier)
        if model is Medication:
            return self.medications.get(identifier)
        if model is AgentRun:
            return self.agent_runs.get(identifier)
        return None

    def add(self, obj):
        if isinstance(obj, Patient):
            if obj.id is None:
                obj.id = uuid4()
            self.patients[obj.id] = obj
            if obj.medications is None:
                obj.medications = []
        elif isinstance(obj, Medication):
            self.medications[obj.rxcui] = obj
        elif isinstance(obj, PatientMedication):
            if obj.id is None:
                obj.id = uuid4()
            if obj.active is None:
                obj.active = True
            patient = self.patients.get(obj.patient_id)
            if patient is not None:
                if patient.medications is None:
                    patient.medications = []
                if obj not in patient.medications:
                    patient.medications.append(obj)
        elif isinstance(obj, AgentRun):
            if obj.id is None:
                obj.id = uuid4()
            self.agent_runs[obj.id] = obj

    async def commit(self):
        return None

    async def refresh(self, obj):
        return None


@pytest.fixture
def fake_session():
    return FakeSession()


@pytest.fixture
def sample_user():
    return {"sub": "sample-user-123", "roles": ["clinician"]}


@pytest.fixture
def client(fake_session, sample_user):
    async def override_get_db_session():
        yield fake_session

    async def override_get_current_user():
        return sample_user

    app.dependency_overrides[get_db_session] = override_get_db_session
    app.dependency_overrides[get_current_user] = override_get_current_user

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def seeded_patient(fake_session):
    patient_id = uuid4()
    patient = Patient(
        id=patient_id,
        mrn="MRN-1001",
        date_of_birth=date(1985, 4, 12),
        sex="female",
        egfr=45.0,
        hepatic_impairment=None,
        allergies="Penicillin",
    )
    patient.medications = []
    fake_session.add(patient)
    return patient_id, patient


@pytest.fixture
def seeded_medication(fake_session):
    med = Medication(rxcui="855332", name="Aspirin", generic_name="acetylsalicylic acid", drug_class="NSAID")
    fake_session.add(med)
    return med


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_auth_me_endpoint(client, sample_user):
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 200
    assert response.json()["sub"] == sample_user["sub"]
    assert response.json()["roles"] == sample_user["roles"]


def test_create_patient_and_get_patient(client):
    payload = {
        "mrn": "MRN-2001",
        "date_of_birth": "1990-01-15",
        "sex": "male",
        "egfr": 60.0,
        "hepatic_impairment": "mild",
        "allergies": "Sulfa",
    }

    create_response = client.post("/api/v1/patients", json=payload)
    assert create_response.status_code == 201

    created_patient = create_response.json()
    assert created_patient["mrn"] == payload["mrn"]
    assert created_patient["sex"] == payload["sex"]

    patient_id = created_patient["id"]
    get_response = client.get(f"/api/v1/patients/{patient_id}")

    assert get_response.status_code == 200
    assert get_response.json()["mrn"] == payload["mrn"]


def test_medication_endpoints(client, seeded_patient, seeded_medication):
    patient_id, _ = seeded_patient

    add_payload = {
        "rxcui": seeded_medication.rxcui,
        "dose": "81 mg",
        "frequency": "daily",
    }

    add_response = client.post(
        f"/api/v1/patients/{patient_id}/medications",
        json=add_payload,
    )

    assert add_response.status_code == 201
    assert add_response.json()["rxcui"] == seeded_medication.rxcui
    assert add_response.json()["name"] == seeded_medication.name

    list_response = client.get(f"/api/v1/patients/{patient_id}/medications")

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert list_response.json()[0]["rxcui"] == seeded_medication.rxcui


def test_interactions_check_endpoint(client, fake_session, seeded_patient, monkeypatch):
    patient_id, _ = seeded_patient

    async def fake_run_interaction_check(db, patient_id, triggered_by_user_id):
        return SimpleNamespace(
            id=uuid4(),
            findings=[
                {
                    "id": uuid4(),
                    "drug_pair": ["855332", "861007"],
                    "severity": "high",
                    "status": "pending_review",
                    "mechanism": "Combined antiplatelet effect",
                    "clinical_recommendation": "Monitor closely",
                    "evidence": [],
                    "critique_notes": None,
                }
            ],
        )

    monkeypatch.setattr(interactions_endpoint, "run_interaction_check", fake_run_interaction_check)

    response = client.post(
        "/api/v1/interactions/check",
        json={"patient_id": str(patient_id)},
    )

    assert response.status_code == 200
    assert response.json()["findings"][0]["severity"] == "high"
    assert response.json()["findings"][0]["drug_pair"] == ["855332", "861007"]


def test_agent_run_trace_endpoint(client, fake_session):
    agent_run_id = uuid4()
    fake_session.agent_runs[agent_run_id] = SimpleNamespace(
        id=agent_run_id,
        status="completed",
        steps=[
            SimpleNamespace(
                step_index=0,
                node_name="patient_context_agent",
                input_payload={"patient_id": str(uuid4())},
                output_payload={"retrieved_context": {"egfr": 45}},
                duration_ms=13,
            )
        ],
    )

    response = client.get(f"/api/v1/agent-runs/{agent_run_id}/trace")

    assert response.status_code == 200
    assert response.json()["agent_run_id"] == str(agent_run_id)
    assert response.json()["status"] == "completed"
    assert response.json()["steps"][0]["node_name"] == "patient_context_agent"
