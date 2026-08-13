"""Add knowledge-base documents and verification tracking.

Revision ID: c4d5e6f7a8b9
Revises: 8b2c4d7e9f10
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c4d5e6f7a8b9"
down_revision: Union[
    str,
    Sequence[str],
    None,
] = "8b2c4d7e9f10"
branch_labels: Union[
    str,
    Sequence[str],
    None,
] = None
depends_on: Union[
    str,
    Sequence[str],
    None,
] = None


def upgrade() -> None:
    op.create_table(
        "knowledge_base_documents",
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "project_id",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "source_name",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "content_sha256",
            sa.String(length=64),
            nullable=False,
        ),
        sa.Column(
            "chunks_indexed",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "project_id",
            "content_sha256",
            name=(
                "uq_kb_documents_"
                "project_sha256"
            ),
        ),
    )

    op.create_index(
        "ix_kb_documents_project_id",
        "knowledge_base_documents",
        ["project_id"],
        unique=False,
    )

    op.create_table(
        "knowledge_base_verifications",
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "health_check_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "evidence_found",
            sa.Boolean(),
            nullable=False,
        ),
        sa.Column(
            "is_supported",
            sa.Boolean(),
            nullable=True,
        ),
        sa.Column(
            "best_match_text",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "best_match_source",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "similarity_distance",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "question_relevance_score",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "answer_support_score",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "context_alignment_score",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "numeric_contradiction",
            sa.Boolean(),
            nullable=False,
        ),
        sa.Column(
            "explanation",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["health_check_id"],
            ["health_checks.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "health_check_id",
            name=(
                "uq_kb_verifications_"
                "health_check_id"
            ),
        ),
    )

    op.create_index(
        "ix_kb_verifications_health_check_id",
        "knowledge_base_verifications",
        ["health_check_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_kb_verifications_health_check_id",
        table_name=(
            "knowledge_base_verifications"
        ),
    )
    op.drop_table(
        "knowledge_base_verifications"
    )

    op.drop_index(
        "ix_kb_documents_project_id",
        table_name=(
            "knowledge_base_documents"
        ),
    )
    op.drop_table(
        "knowledge_base_documents"
    )
