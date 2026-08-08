from pydantic import BaseModel, Field


class EvaluationResultResponse(BaseModel):
    correctness_score: float = Field(ge=0, le=1)
    faithfulness_score: float = Field(ge=0, le=1)
    hallucination_risk: float = Field(ge=0, le=1)
    status: str
    explanation: str


class HealthCheckResponse(BaseModel):
    project_id: str
    question: str
    answer: str
    evaluation: EvaluationResultResponse
