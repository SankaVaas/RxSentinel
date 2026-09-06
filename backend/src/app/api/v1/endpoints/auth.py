from fastapi import APIRouter, Depends

from app.dependencies import get_current_user

router = APIRouter()


@router.get("/me")
async def whoami(user: dict = Depends(get_current_user)) -> dict:
    return user
