from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    Index,
    Integer,
    String,
    UniqueConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


def utc_now() -> datetime:
    return datetime.now(
        timezone.utc
    ).replace(
        tzinfo=None
    )


class KnowledgeBaseDocument(Base):
    __tablename__ = (
        "knowledge_base_documents"
    )

    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "content_sha256",
            name=(
                "uq_kb_documents_"
                "project_sha256"
            ),
        ),
        Index(
            "ix_kb_documents_project_id",
            "project_id",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    project_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    source_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    content_sha256: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    chunks_indexed: Mapped[int] = (
        mapped_column(
            Integer,
            nullable=False,
        )
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    created_at: Mapped[datetime] = (
        mapped_column(
            DateTime,
            nullable=False,
            default=utc_now,
        )
    )
