from fastapi import FastAPI

from app.schemas.health_check import HealthCheckRequest


app = FastAPI(
    title="AI Reliability Platform",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "ai-reliability-platform",
    }


@app.post("/api/v1/health-checks")
def create_health_check(payload: HealthCheckRequest) -> dict:
    return {
        "message": "Health check request received successfully.",
        "project_id": payload.project_id,
        "question": payload.question,
        "contexts_count": len(payload.contexts),
        "model": payload.model.name,
    }