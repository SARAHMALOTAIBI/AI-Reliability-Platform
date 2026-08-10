import uuid

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.health_check import HealthCheck
from app.models.retrieved_context import RetrievedContext
from app.models.diagnosis import Diagnosis
from app.schemas.evaluation_result import (
    EvaluationResultResponse,
    DiagnosisResponse,
    HealthCheckResponse,
)
from app.schemas.health_check import HealthCheckRequest
from evaluation.pipeline import run_evaluation
from root_cause.rules.pipeline import run_rules_pipeline


app = FastAPI(
    title="AI Reliability Platform",
    version="0.3.0",
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
    db: Session = Depends(get_db),
) -> HealthCheckResponse:
    context_texts = [
        context.text
        for context in payload.contexts
    ]

    # Step 1: Run the Evaluation Engine
    result = run_evaluation(
        question=payload.question,
        answer=payload.answer,
        contexts=context_texts,
        reference_answer=payload.reference_answer,
    )

    # Step 2: Run the Root Cause Engine using the evaluation output
    metrics = {
        "context_precision": result.context_precision_score,
        "faithfulness": result.faithfulness_score,
    }
    diagnosis_dict = run_rules_pipeline(metrics)

    # Step 3: Persist the health check to the database
    db_health_check = HealthCheck(
        id=uuid.uuid4(),
        project_id=payload.project_id,
        question=payload.question,
        answer=payload.answer,
        reference_answer=payload.reference_answer,
        status="COMPLETED",
    )
    db.add(db_health_check)
    db.flush()  # assigns db_health_check.id before commit

    for context in payload.contexts:
        db_context = RetrievedContext(
            id=uuid.uuid4(),
            health_check_id=db_health_check.id,
            text=context.text,
        )
        db.add(db_context)

    diagnosis_response = None
    if diagnosis_dict:
        db_diagnosis = Diagnosis(
            id=uuid.uuid4(),
            health_check_id=db_health_check.id,
            category=diagnosis_dict["category"],
            subcategory=diagnosis_dict.get("subcategory"),
            severity=diagnosis_dict["severity"],
            confidence=diagnosis_dict["confidence"],
            explanation=diagnosis_dict["explanation"],
        )
        db.add(db_diagnosis)
        diagnosis_response = DiagnosisResponse(**diagnosis_dict)

    db.commit()

    # Step 4: Return the full response
    return HealthCheckResponse(
        project_id=payload.project_id,
        question=payload.question,
        answer=payload.answer,
        evaluation=EvaluationResultResponse(
            correctness_score=result.correctness_score,
            faithfulness_score=result.faithfulness_score,
            context_precision_score=result.context_precision_score,
            hallucination_risk=result.hallucination_risk,
            status=result.status,
            explanation=result.explanation,
        ),
        diagnosis=diagnosis_response,
    )
