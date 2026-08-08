from evaluation.pipeline import run_evaluation


def test_exact_supported_answer_is_healthy() -> None:
    result = run_evaluation(
        answer=(
            "Customers may request a refund "
            "within 14 days."
        ),
        contexts=[
            "Customers may request a refund "
            "within 14 days."
        ],
        reference_answer=(
            "Customers may request a refund "
            "within 14 days."
        ),
    )

    assert result.status == "HEALTHY"
    assert result.correctness_score >= 0.95
    assert result.faithfulness_score >= 0.95
    assert result.hallucination_risk <= 0.05


def test_numeric_contradiction_is_critical() -> None:
    result = run_evaluation(
        answer=(
            "Customers have 30 days "
            "to request a refund."
        ),
        contexts=[
            "Customers may request a refund "
            "within 14 days."
        ],
        reference_answer=(
            "The refund period is 14 days."
        ),
    )

    assert result.status == "CRITICAL"
    assert result.correctness_score <= 0.20
    assert result.faithfulness_score <= 0.20
    assert result.hallucination_risk >= 0.80
