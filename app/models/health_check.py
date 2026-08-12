from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class HealthCheck(Base):
    __tablename__ = "health_checks"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    project_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    application_version: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    question: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    answer: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    reference_answer: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    prompt: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    model_config_data: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    retriever_config: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    performance: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=utc_now,
    )

    contexts: Mapped[list["RetrievedContext"]] = relationship(
        back_populates="health_check",
        cascade="all, delete-orphan",
    )

    diagnoses: Mapped[list["Diagnosis"]] = relationship(
        back_populates="health_check",
        cascade="all, delete-orphan",
    )

    evaluation_metric: Mapped["EvaluationMetric"] = relationship(
        back_populates="health_check",
        cascade="all, delete-orphan",
        uselist=False,
    )

    recommendations: Mapped[
        list["RecommendationRecord"]
    ] = relationship(
        back_populates="health_check",
        cascade="all, delete-orphan",
    )