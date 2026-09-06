from fastapi import APIRouter

from app.api.v1.endpoints import agent_runs, auth, interactions, medications, patients

api_router = APIRouter()
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(medications.router, prefix="/patients", tags=["medications"])
api_router.include_router(interactions.router, prefix="/interactions", tags=["interactions"])
api_router.include_router(agent_runs.router, prefix="/agent-runs", tags=["agent-runs"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
