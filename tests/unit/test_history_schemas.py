import uuid
from datetime import datetime

from app.schemas.history import (
    HealthCheckDetailResponse,
    HealthCheckHistoryItem,
    HealthCheckHistoryResponse,
)


def test_history_item_allows_legacy_record_without_metrics() -> None:
    item = HealthCheckHistoryItem(
        health_check_id=uuid.uuid4(),
        project_id="legacy-project",
        application_version="1.0.0",
        status="COMPLETED",
        overall_health_score=None,
        health_status=None,
        evaluation_status=None,
        diagnosis_category=None,
        created_at=datetime.now(),
    )

    assert item.overall_health_score is None
    assert item.health_status is None


def test_history_response_contains_pagination_data() -> None:
    response = HealthCheckHistoryResponse(
        total=0,
        limit=50,
        offset=0,
        items=[],
    )

    assert response.total == 0
    assert response.limit == 50
    assert response.offset == 0


def test_detail_response_allows_legacy_record_without_evaluation() -> None:
    detail = HealthCheckDetailResponse(
        health_check_id=uuid.uuid4(),
        project_id="legacy-project",
        application_version=None,
        status="COMPLETED",
        overall_health_score=None,
        health_status=None,
        question="Question",
        answer="Answer",
        reference_answer=None,
        prompt=None,
        model=None,
        retriever=None,
        performance=None,
        evaluation=None,
        diagnosis=None,
        contexts=[],
        recommendations=[],
        created_at=datetime.now(),
    )

    assert detail.evaluation is None
    assert detail.recommendations == []
    assert detail.contexts == []