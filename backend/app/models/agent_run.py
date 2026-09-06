import enum

from sqlalchemy import Enum, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import TimestampedBase


class RunStatus(str, enum.Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentRun(TimestampedBase):
    """One end-to-end execution of the interaction-check agent graph.

    This is the audit-trail root: every node's input/output is a child
    AgentRunStep, and it is append-only — rows are never mutated after
    creation, only superseded by a new run.
    """

    __tablename__ = "agent_runs"

    patient_id: Mapped[UUID] = mapped_column(ForeignKey("patients.id"))
    status: Mapped[RunStatus] = mapped_column(Enum(RunStatus), default=RunStatus.RUNNING)
    triggered_by_user_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    steps: Mapped[list["AgentRunStep"]] = relationship(
        back_populates="agent_run", cascade="all, delete-orphan", order_by="AgentRunStep.step_index"
    )
    findings: Mapped[list["InteractionFinding"]] = relationship(back_populates="agent_run")


class AgentRunStep(TimestampedBase):
    """A single node execution within an agent run (retrieve/verify/critique/...).

    Powers the AgentTraceViewer in the frontend and the eval harness.
    """

    __tablename__ = "agent_run_steps"

    agent_run_id: Mapped[UUID] = mapped_column(ForeignKey("agent_runs.id"))
    step_index: Mapped[int] = mapped_column(Integer)
    node_name: Mapped[str] = mapped_column(String(64))  # e.g. "critique_agent"

    input_payload: Mapped[dict] = mapped_column(JSONB)
    output_payload: Mapped[dict] = mapped_column(JSONB)
    reasoning_trace: Mapped[str | None] = mapped_column(Text, nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    agent_run: Mapped["AgentRun"] = relationship(back_populates="steps")
