from root_cause.rules.retrieval_rules import (
    check_verified_knowledge_result,
)


def test_verified_missing_information_is_kb_failure() -> None:
    result = check_verified_knowledge_result(
        verification_status="NO_RELEVANT_EVIDENCE",
        context_alignment_score=None,
        explanation="No evidence.",
    )

    assert result is not None
    assert result["category"] == "KNOWLEDGE_BASE_FAILURE"
    assert result["subcategory"] == "VERIFIED_MISSING_INFORMATION"


def test_verified_missed_evidence_is_retrieval_failure() -> None:
    result = check_verified_knowledge_result(
        verification_status="CONTRADICTED",
        context_alignment_score=0.2,
        explanation="Company evidence contradicts the answer.",
    )

    assert result is not None
    assert result["category"] == "RETRIEVAL_FAILURE"
    assert result["subcategory"] == "VERIFIED_MISSED_EVIDENCE"


def test_verified_answer_failure_is_generation_failure() -> None:
    result = check_verified_knowledge_result(
        verification_status="CONTRADICTED",
        context_alignment_score=0.9,
        explanation="Company evidence contradicts the answer.",
    )

    assert result is not None
    assert result["category"] == "GENERATION_FAILURE"
    assert result["subcategory"] == "VERIFIED_UNSUPPORTED_ANSWER"


def test_supported_verification_does_not_force_failure() -> None:
    result = check_verified_knowledge_result(
        verification_status="SUPPORTED",
        context_alignment_score=0.9,
        explanation="Supported.",
    )

    assert result is None
