from typing import Any

from pydantic import BaseModel, Field


class RetrievedContext(BaseModel):
    text: str = Field(..., min_length=1)
    source: str | None = None
    rank: int | None = Field(default=None, ge=1)
    retrieval_score: float | None = Field(default=None, ge=0, le=1)


class ModelConfiguration(BaseModel):
    provider: str
    name: str
    temperature: float | None = Field(default=None, ge=0, le=2)


class RetrieverConfiguration(BaseModel):
    embedding_model: str | None = None
    top_k: int | None = Field(default=None, ge=1)
    chunk_size: int | None = Field(default=None, ge=1)
    chunk_overlap: int | None = Field(default=None, ge=0)


class PerformanceData(BaseModel):
    latency_ms: int | None = Field(default=None, ge=0)
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    estimated_cost: float | None = Field(default=None, ge=0)


class HealthCheckRequest(BaseModel):
    project_id: str
    application_version: str | None = None

    question: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)
    contexts: list[RetrievedContext] = Field(default_factory=list)

    reference_answer: str | None = None
    prompt: str | None = None

    model: ModelConfiguration
    retriever: RetrieverConfiguration | None = None
    performance: PerformanceData | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)