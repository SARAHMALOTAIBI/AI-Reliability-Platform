from fastapi import FastAPI

from app.schemas.evaluation_result import (
    EvaluationResultResponse,
    HealthCheckResponse,
)
from app.schemas.health_check import HealthCheckRequest
from evaluation.pipeline import run_evaluation


app = FastAPI(
    title="AI Reliability Platform",
    version="0.2.0",
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "AI Reliability Platform is running"
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
) -> HealthCheckResponse:
    context_texts = [
        context.text
        for context in payload.contexts
    ]

    result = run_evaluation(
        answer=payload.answer,
        contexts=context_texts,
        reference_answer=payload.reference_answer,
    )

    return HealthCheckResponse(
        project_id=payload.project_id,
        question=payload.question,
        answer=payload.answer,
        evaluation=EvaluationResultResponse(
            correctness_score=result.correctness_score,
            faithfulness_score=result.faithfulness_score,
            hallucination_risk=result.hallucination_risk,
            status=result.status,
            explanation=result.explanation,
        ),
    )
