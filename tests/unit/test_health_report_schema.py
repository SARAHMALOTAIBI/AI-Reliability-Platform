import uuid

from app.schemas.evaluation_result import (
    EvaluationResultResponse,
    HealthCheckResponse,
    RecommendationResponse,
)


def test_health_report_schema() -> None:
    response = HealthCheckResponse(
        health_check_id=uuid.uuid4(),
        project_id="test-project",
        status="COMPLETED",
        overall_health_score=85,
        health_status="GOOD",
        question="What is the refund period?",
        answer="14 days.",
        evaluation=EvaluationResultResponse(
            correctness_score=1.0,
            faithfulness_score=1.0,
            context_precision_score=1.0,
            context_recall_score=1.0,
            answer_relevancy_score=1.0,
            hallucination_risk=0.0,
            status="HEALTHY",
            explanation="Healthy result.",
        ),
        diagnosis=None,
        recommendations=[
            RecommendationResponse(
                priority=1,
                action="Keep current configuration.",
                expected_impact="LOW",
                difficulty="LOW",
                affected_component="SYSTEM",
                supporting_evidence="Healthy result.",
            )
        ],
    )

    assert response.overall_health_score == 85
    assert response.health_status == "GOOD"
    assert len(response.recommendations) == 1
