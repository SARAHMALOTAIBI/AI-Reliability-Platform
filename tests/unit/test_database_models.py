from app.models import (
    Base,
    Diagnosis,
    EvaluationMetric,
    HealthCheck,
    RecommendationRecord,
    RetrievedContext,
)


def test_database_models_are_registered() -> None:
    tables = set(
        Base.metadata.tables.keys()
    )

    assert "health_checks" in tables
    assert "retrieved_contexts" in tables
    assert "diagnoses" in tables
    assert "evaluation_metrics" in tables
    assert "recommendations" in tables


def test_model_table_names() -> None:
    assert (
        HealthCheck.__tablename__
        == "health_checks"
    )

    assert (
        RetrievedContext.__tablename__
        == "retrieved_contexts"
    )

    assert (
        Diagnosis.__tablename__
        == "diagnoses"
    )

    assert (
        EvaluationMetric.__tablename__
        == "evaluation_metrics"
    )

    assert (
        RecommendationRecord.__tablename__
        == "recommendations"
    )


def test_evaluation_metric_columns() -> None:
    columns = {
        column.name
        for column in EvaluationMetric.__table__.columns
    }

    expected = {
        "id",
        "health_check_id",
        "correctness_score",
        "faithfulness_score",
        "context_precision_score",
        "context_recall_score",
        "answer_relevancy_score",
        "hallucination_risk",
        "overall_health_score",
        "health_status",
        "evaluation_status",
        "explanation",
        "created_at",
    }

    assert expected <= columns


def test_recommendation_columns() -> None:
    columns = {
        column.name
        for column in RecommendationRecord.__table__.columns
    }

    expected = {
        "id",
        "health_check_id",
        "priority",
        "action",
        "expected_impact",
        "difficulty",
        "affected_component",
        "supporting_evidence",
        "created_at",
    }

    assert expected <= columns