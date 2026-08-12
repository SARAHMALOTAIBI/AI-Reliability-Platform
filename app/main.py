import uuid

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    Diagnosis,
    EvaluationMetric,
    HealthCheck,
    RecommendationRecord,
    RetrievedContext,
)
from app.schemas.evaluation_result import (
    DiagnosisResponse,
    EvaluationResultResponse,
    HealthCheckResponse,
    RecommendationResponse,
)
from app.schemas.health_check import HealthCheckRequest
from app.routers.history import router as history_router
from evaluation.pipeline import run_evaluation
from recommendation_engine.engine import (
    generate_recommendations,
)
from reporting.health_score import (
    calculate_health_score,
)
from root_cause.rules.pipeline import (
    run_rules_pipeline,
)


app = FastAPI(
    title="AI Reliability Platform",
    version="0.7.0",
)


app.include_router(history_router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message":
            "AI Reliability Platform is running"
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "ai-reliability-platform",
    }


@app.post(
    "/api/v1/health-checks",
    response_model=HealthCheckResponse,
)
def create_health_check(
    payload: HealthCheckRequest,
    db: Session = Depends(get_db),
) -> HealthCheckResponse:
    context_texts = [
        context.text
        for context in payload.contexts
    ]

    # Step 1 — Evaluation Engine
    result = run_evaluation(
        question=payload.question,
        answer=payload.answer,
        contexts=context_texts,
        reference_answer=payload.reference_answer,
    )

    # Step 2 — Root Cause Engine
    root_cause_metrics = {
        "context_precision":
            result.context_precision_score,
        "faithfulness":
            result.faithfulness_score,
        "answer_relevancy":
            result.answer_relevancy_score,
    }

    if result.context_recall_score is not None:
        root_cause_metrics[
            "context_recall"
        ] = result.context_recall_score

    diagnosis_dict = run_rules_pipeline(
        root_cause_metrics
    )

    # Step 3 — Overall Health Score
    health_metrics = {
        "faithfulness":
            result.faithfulness_score,
        "answer_relevancy":
            result.answer_relevancy_score,
        "answer_correctness":
            result.correctness_score,
        "context_precision":
            result.context_precision_score,
        "context_recall":
            result.context_recall_score,
    }

    health_score = calculate_health_score(
        health_metrics
    )

    # Step 4 — Recommendation Engine
    recommendations = generate_recommendations(
        diagnosis_dict
    )

    # Step 5 — Health Check record
    db_health_check = HealthCheck(
        id=uuid.uuid4(),
        project_id=payload.project_id,
        application_version=(
            payload.application_version
        ),
        question=payload.question,
        answer=payload.answer,
        reference_answer=(
            payload.reference_answer
        ),
        prompt=payload.prompt,
        model_config_data=(
            payload.model.model_dump()
        ),
        retriever_config=(
            payload.retriever.model_dump()
            if payload.retriever
            else None
        ),
        performance=(
            payload.performance.model_dump()
            if payload.performance
            else None
        ),
        status="COMPLETED",
    )

    diagnosis_response = None

    try:
        db.add(db_health_check)
        db.flush()

        # Retrieved contexts
        for context in payload.contexts:
            db.add(
                RetrievedContext(
                    id=uuid.uuid4(),
                    health_check_id=(
                        db_health_check.id
                    ),
                    text=context.text,
                    source=context.source,
                    rank=context.rank,
                    retrieval_score=(
                        context.retrieval_score
                    ),
                )
            )

        # Evaluation metrics + health score
        db.add(
            EvaluationMetric(
                id=uuid.uuid4(),
                health_check_id=(
                    db_health_check.id
                ),
                correctness_score=(
                    result.correctness_score
                ),
                faithfulness_score=(
                    result.faithfulness_score
                ),
                context_precision_score=(
                    result.context_precision_score
                ),
                context_recall_score=(
                    result.context_recall_score
                ),
                answer_relevancy_score=(
                    result.answer_relevancy_score
                ),
                hallucination_risk=(
                    result.hallucination_risk
                ),
                overall_health_score=(
                    health_score.score
                ),
                health_status=(
                    health_score.status
                ),
                evaluation_status=(
                    result.status
                ),
                explanation=(
                    result.explanation
                ),
            )
        )

        # Diagnosis
        if diagnosis_dict:
            db.add(
                Diagnosis(
                    id=uuid.uuid4(),
                    health_check_id=(
                        db_health_check.id
                    ),
                    category=(
                        diagnosis_dict["category"]
                    ),
                    subcategory=(
                        diagnosis_dict.get(
                            "subcategory"
                        )
                    ),
                    severity=(
                        diagnosis_dict["severity"]
                    ),
                    confidence=(
                        diagnosis_dict["confidence"]
                    ),
                    explanation=(
                        diagnosis_dict["explanation"]
                    ),
                )
            )

            diagnosis_response = (
                DiagnosisResponse(
                    **diagnosis_dict
                )
            )

        # Recommendations
        for item in recommendations:
            db.add(
                RecommendationRecord(
                    id=uuid.uuid4(),
                    health_check_id=(
                        db_health_check.id
                    ),
                    priority=item.priority,
                    action=item.action,
                    expected_impact=(
                        item.expected_impact
                    ),
                    difficulty=item.difficulty,
                    affected_component=(
                        item.affected_component
                    ),
                    supporting_evidence=(
                        item.supporting_evidence
                    ),
                )
            )

        db.commit()

    except Exception:
        db.rollback()
        raise

    recommendation_responses = [
        RecommendationResponse(
            priority=item.priority,
            action=item.action,
            expected_impact=(
                item.expected_impact
            ),
            difficulty=item.difficulty,
            affected_component=(
                item.affected_component
            ),
            supporting_evidence=(
                item.supporting_evidence
            ),
        )
        for item in recommendations
    ]

    return HealthCheckResponse(
        health_check_id=db_health_check.id,
        project_id=payload.project_id,
        status="COMPLETED",
        overall_health_score=(
            health_score.score
        ),
        health_status=(
            health_score.status
        ),
        question=payload.question,
        answer=payload.answer,
        evaluation=EvaluationResultResponse(
            correctness_score=(
                result.correctness_score
            ),
            faithfulness_score=(
                result.faithfulness_score
            ),
            context_precision_score=(
                result.context_precision_score
            ),
            context_recall_score=(
                result.context_recall_score
            ),
            answer_relevancy_score=(
                result.answer_relevancy_score
            ),
            hallucination_risk=(
                result.hallucination_risk
            ),
            status=result.status,
            explanation=result.explanation,
        ),
        diagnosis=diagnosis_response,
        recommendations=(
            recommendation_responses
        ),
    )