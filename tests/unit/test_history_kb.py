import uuid
from datetime import datetime

from app.schemas.history import (
    HealthCheckDetailResponse,
    HealthCheckHistoryItem,
)


def test_history_item_exposes_kb_status() -> None:
    item = HealthCheckHistoryItem(
        health_check_id=uuid.uuid4(),
        project_id="project-a",
        status="COMPLETED",
        knowledge_base_status="SUPPORTED",
        created_at=datetime.now(),
    )
    assert item.knowledge_base_status == "SUPPORTED"


def test_history_detail_exposes_kb_verification() -> None:
    detail = HealthCheckDetailResponse(
        health_check_id=uuid.uuid4(),
        project_id="project-a",
        status="COMPLETED",
        question="What is the refund period?",
        answer="14 days",
        knowledge_base_verification={
            "status": "SUPPORTED",
            "evidence_found": True,
            "is_supported": True,
            "best_match_text": "Refunds are allowed within 14 days.",
            "best_match_source": "policy.pdf",
            "similarity_distance": 0.1,
            "question_relevance_score": 0.9,
            "answer_support_score": 0.9,
            "context_alignment_score": 0.9,
            "numeric_contradiction": False,
            "explanation": "Supported.",
        },
        created_at=datetime.now(),
    )
    assert detail.knowledge_base_verification is not None
    assert detail.knowledge_base_verification.status == "SUPPORTED"
