"""Add hashed_password to users for local JWT auth.

Revision ID: 0003
Revises: 0002
Create Date: 2026-09-13
"""
import sqlalchemy as sa
from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("hashed_password", sa.String(256), nullable=False, server_default=""))
    op.alter_column("users", "hashed_password", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "hashed_password")