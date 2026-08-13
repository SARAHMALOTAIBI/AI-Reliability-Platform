from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base import Base


def utc_now() -> datetime:
    return datetime.now(
        timezone.utc
    ).replace(
        tzinfo=None
    )


class KnowledgeBaseVerification(Base):
    __tablename__ = (
        "knowledge_base_verifications"
    )

    __table_args__ = (
        UniqueConstraint(
            "health_check_id",
            name=(
                "uq_kb_verifications_"
                "health_check_id"
            ),
        ),
        Index(
            "ix_kb_verifications_health_check_id",
            "health_check_id",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    health_check_id: Mapped[
        uuid.UUID
    ] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey(
            "health_checks.id"
        ),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    evidence_found: Mapped[bool] = (
        mapped_column(
            Boolean,
            nullable=False,
        )
    )

    is_supported: Mapped[
        bool | None
    ] = mapped_column(
        Boolean,
        nullable=True,
    )

    best_match_text: Mapped[
        str | None
    ] = mapped_column(
        Text,
        nullable=True,
    )

    best_match_source: Mapped[
        str | None
    ] = mapped_column(
        String(255),
        nullable=True,
    )

    similarity_distance: Mapped[
        float | None
    ] = mapped_column(
        Float,
        nullable=True,
    )

    question_relevance_score: Mapped[
        float | None
    ] = mapped_column(
        Float,
        nullable=True,
    )

    answer_support_score: Mapped[
        float | None
    ] = mapped_column(
        Float,
        nullable=True,
    )

    context_alignment_score: Mapped[
        float | None
    ] = mapped_column(
        Float,
        nullable=True,
    )

    numeric_contradiction: Mapped[
        bool
    ] = mapped_column(
        Boolean,
        nullable=False,
    )

    explanation: Mapped[str] = (
        mapped_column(
            Text,
            nullable=False,
        )
    )

    created_at: Mapped[datetime] = (
        mapped_column(
            DateTime,
            nullable=False,
            default=utc_now,
        )
    )

    health_check: Mapped[
        "HealthCheck"
    ] = relationship(
        back_populates=(
            "knowledge_base_verification"
        ),
    )
