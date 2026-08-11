import uuid

from pydantic import BaseModel, Field


class EvaluationResultResponse(BaseModel):
    correctness_score: float = Field(
        ge=0,
        le=1,
    )

    faithfulness_score: float = Field(
        ge=0,
        le=1,
    )

    context_precision_score: float = Field(
        ge=0,
        le=1,
    )

    context_recall_score: float | None = Field(
        default=None,
        ge=0,
        le=1,
    )

    answer_relevancy_score: float = Field(
        ge=0,
        le=1,
    )

    hallucination_risk: float = Field(
        ge=0,
        le=1,
    )

    status: str
    explanation: str


class DiagnosisResponse(BaseModel):
    category: str
    subcategory: str | None = None
    severity: str

    confidence: float = Field(
        ge=0,
        le=1,
    )

    explanation: str


class RecommendationResponse(BaseModel):
    priority: int = Field(
        ge=1,
    )

    action: str
    expected_impact: str
    difficulty: str
    affected_component: str
    supporting_evidence: str


class HealthCheckResponse(BaseModel):
    health_check_id: uuid.UUID
    project_id: str
    status: str

    overall_health_score: int = Field(
        ge=0,
        le=100,
    )

    health_status: str

    question: str
    answer: str

    evaluation: EvaluationResultResponse

    diagnosis: DiagnosisResponse | None = None

    recommendations: list[
        RecommendationResponse
    ] = Field(
        default_factory=list,
    )
