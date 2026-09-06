from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedBase


class User(TimestampedBase):
    """Clinician / admin / auditor account, backed by the OIDC provider."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(256))
    roles: Mapped[list[str]] = mapped_column(ARRAY(String(32)), default=list)
