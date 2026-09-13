"""Add first_name/last_name to patients for search and display.

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-12
"""
import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("patients", sa.Column("first_name", sa.String(128), nullable=False, server_default="Unknown"))
    op.add_column("patients", sa.Column("last_name", sa.String(128), nullable=False, server_default="Unknown"))
    op.alter_column("patients", "first_name", server_default=None)
    op.alter_column("patients", "last_name", server_default=None)


def downgrade() -> None:
    op.drop_column("patients", "last_name")
    op.drop_column("patients", "first_name")
