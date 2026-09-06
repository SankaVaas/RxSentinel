"""Initial schema: patients, medications, agent runs, interaction findings, users.

Revision ID: 0001
Revises:
Create Date: 2026-09-06
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("email", sa.String(256), nullable=False, unique=True),
        sa.Column("display_name", sa.String(256), nullable=False),
        sa.Column("roles", postgresql.ARRAY(sa.String(32)), nullable=False, server_default="{}"),
    )

    op.create_table(
        "patients",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("mrn", sa.String(64), nullable=False, unique=True),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("sex", sa.String(16), nullable=False),
        sa.Column("egfr", sa.Float(), nullable=True),
        sa.Column("hepatic_impairment", sa.String(32), nullable=True),
        sa.Column("allergies", sa.String(512), nullable=True),
    )

    op.create_table(
        "medications",
        sa.Column("rxcui", sa.String(32), primary_key=True),
        sa.Column("name", sa.String(256), nullable=False),
        sa.Column("generic_name", sa.String(256), nullable=True),
        sa.Column("drug_class", sa.String(128), nullable=True),
    )

    op.create_table(
        "patient_medications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id"), nullable=False),
        sa.Column("rxcui", sa.String(32), sa.ForeignKey("medications.rxcui"), nullable=False),
        sa.Column("dose", sa.String(64), nullable=True),
        sa.Column("frequency", sa.String(64), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    op.create_table(
        "agent_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id"), nullable=False),
        sa.Column(
            "status",
            sa.Enum("running", "completed", "failed", name="runstatus"),
            nullable=False,
            server_default="running",
        ),
        sa.Column("triggered_by_user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
    )

    op.create_table(
        "agent_run_steps",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("agent_run_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("agent_runs.id"), nullable=False),
        sa.Column("step_index", sa.Integer(), nullable=False),
        sa.Column("node_name", sa.String(64), nullable=False),
        sa.Column("input_payload", postgresql.JSONB(), nullable=False),
        sa.Column("output_payload", postgresql.JSONB(), nullable=False),
        sa.Column("reasoning_trace", sa.Text(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
    )

    op.create_table(
        "interaction_findings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("agent_run_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("agent_runs.id"), nullable=False),
        sa.Column("patient_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patients.id"), nullable=False),
        sa.Column("drug_pair", postgresql.ARRAY(sa.String(32)), nullable=False),
        sa.Column(
            "severity",
            sa.Enum("low", "moderate", "high", "contraindicated", name="severity"),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum(
                "auto_cleared", "pending_review", "escalated", "acknowledged", name="findingstatus"
            ),
            nullable=False,
        ),
        sa.Column("mechanism", sa.Text(), nullable=False),
        sa.Column("clinical_recommendation", sa.Text(), nullable=False),
        sa.Column("evidence", postgresql.JSONB(), nullable=False),
        sa.Column("critique_notes", sa.Text(), nullable=True),
    )

    op.create_table(
        "literature_chunks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("source", sa.String(64), nullable=False),
        sa.Column("rxcui", sa.String(32), nullable=True),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("embedding", sa.dialects.postgresql.ARRAY(sa.Float), nullable=True),  # replaced below by Vector
    )
    # NOTE: the `embedding` column above is a structural placeholder; once
    # pgvector's SQLAlchemy type is wired in (`from pgvector.sqlalchemy import Vector`),
    # replace with sa.Column("embedding", Vector(1536)) and add an ivfflat index.


def downgrade() -> None:
    op.drop_table("literature_chunks")
    op.drop_table("interaction_findings")
    op.drop_table("agent_run_steps")
    op.drop_table("agent_runs")
    op.drop_table("patient_medications")
    op.drop_table("medications")
    op.drop_table("patients")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS findingstatus")
    op.execute("DROP TYPE IF EXISTS severity")
    op.execute("DROP TYPE IF EXISTS runstatus")
