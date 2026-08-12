"""Add evaluation metrics and recommendations.

Revision ID: 8b2c4d7e9f10
Revises: 54469687b35c
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "8b2c4d7e9f10"
down_revision: Union[str, Sequence[str], None] = (
    "54469687b35c"
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "evaluation_metrics",
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
            "correctness_score",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "faithfulness_score",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "context_precision_score",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "context_recall_score",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "answer_relevancy_score",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "hallucination_risk",
            sa.Float(),
            nullable=False,
        ),
        sa.Column(
            "overall_health_score",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "health_status",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "evaluation_status",
            sa.String(length=20),
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
            name="uq_evaluation_metrics_health_check_id",
        ),
    )

    op.create_index(
        "ix_evaluation_metrics_health_check_id",
        "evaluation_metrics",
        ["health_check_id"],
        unique=False,
    )

    op.create_table(
        "recommendations",
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
            "priority",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "action",
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            "expected_impact",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "difficulty",
            sa.String(length=20),
            nullable=False,
        ),
        sa.Column(
            "affected_component",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "supporting_evidence",
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
    )

    op.create_index(
        "ix_recommendations_health_check_id",
        "recommendations",
        ["health_check_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_recommendations_health_check_id",
        table_name="recommendations",
    )
    op.drop_table("recommendations")

    op.drop_index(
        "ix_evaluation_metrics_health_check_id",
        table_name="evaluation_metrics",
    )
    op.drop_table("evaluation_metrics")