from evaluation.pipeline import run_evaluation


def test_exact_supported_answer_is_healthy() -> None:
    result = run_evaluation(
        question="What is the refund period?",
        answer=(
            "Customers may request a refund "
            "within 14 days."
        ),
        contexts=[
            (
                "Customers may request a refund "
                "within 14 days."
            )
        ],
        reference_answer=(
            "Customers may request a refund "
            "within 14 days."
        ),
    )

    assert result.status == "HEALTHY"
    assert result.correctness_score >= 0.95
    assert result.faithfulness_score >= 0.95

    assert (
        result.context_recall_score
        is not None
    )

    assert (
        result.context_recall_score
        >= 0.95
    )

    assert (
        0.0
        <= result.answer_relevancy_score
        <= 1.0
    )

    assert result.hallucination_risk <= 0.05


def test_numeric_contradiction_is_critical() -> None:
    result = run_evaluation(
        question="What is the refund period?",
        answer=(
            "Customers have 30 days "
            "to request a refund."
        ),
        contexts=[
            (
                "Customers may request a refund "
                "within 14 days."
            )
        ],
        reference_answer=(
            "The refund period is 14 days."
        ),
    )

    assert result.status == "CRITICAL"
    assert result.correctness_score <= 0.20
    assert result.faithfulness_score <= 0.20
    assert result.hallucination_risk >= 0.80


def test_context_recall_is_none_without_reference() -> None:
    result = run_evaluation(
        question="What is the refund period?",
        answer="Refunds are available.",
        contexts=[
            "Refunds are available."
        ],
        reference_answer=None,
    )

    assert result.context_recall_score is None
