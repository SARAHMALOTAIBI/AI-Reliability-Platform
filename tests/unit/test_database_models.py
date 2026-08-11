from app.models import (
    Base,
    Diagnosis,
    HealthCheck,
    RetrievedContext,
)


def test_database_models_are_registered() -> None:
    tables = set(
        Base.metadata.tables.keys()
    )

    assert "health_checks" in tables
    assert "retrieved_contexts" in tables
    assert "diagnoses" in tables


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
