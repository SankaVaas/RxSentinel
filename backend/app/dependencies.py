"""Shared FastAPI dependencies: DB session, current user, agent service."""
from collections.abc import AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import Settings, get_settings
from app.core.security import decode_and_verify_token

_bearer_scheme = HTTPBearer(auto_error=False)


def get_engine(settings: Settings = Depends(get_settings)):
    return create_async_engine(settings.database_url, pool_pre_ping=True)


async def get_db_session(
    settings: Settings = Depends(get_settings),
) -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(settings.database_url, pool_pre_ping=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session


async def get_current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    settings: Settings = Depends(get_settings),
) -> dict:
    if creds is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing credentials")
    try:
        claims = decode_and_verify_token(creds.credentials, settings)
    except ValueError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(exc)) from exc
    return claims


def require_role(role: str):
    def _checker(user: dict = Depends(get_current_user)) -> dict:
        roles = user.get("roles", [])
        if role not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"Requires role: {role}")
        return user

    return _checker
