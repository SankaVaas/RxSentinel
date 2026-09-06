import pytest


@pytest.fixture
def sample_patient_context() -> dict:
    return {
        "patient_id": "00000000-0000-0000-0000-000000000001",
        "egfr": 45.0,
        "hepatic_impairment": None,
        "age": 74,
        "active_rxcuis": ["855332", "861007"],  # example RxCUIs
    }
