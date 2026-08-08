from evaluation.rules.numeric_consistency import (
    check_duration_consistency,
)


def test_two_weeks_matches_fourteen_days() -> None:
    result = check_duration_consistency(
        answer=(
            "Customers have two weeks "
            "to request a refund."
        ),
        evidence=(
            "Customers have 14 days "
            "to request a refund."
        ),
    )

    assert result.contradiction is False
    assert result.answer_values_in_days == [14.0]
    assert result.evidence_values_in_days == [14.0]


def test_thirty_days_contradicts_fourteen_days() -> None:
    result = check_duration_consistency(
        answer=(
            "Customers have 30 days "
            "to request a refund."
        ),
        evidence=(
            "Customers have 14 days "
            "to request a refund."
        ),
    )

    assert result.contradiction is True
    assert result.unsupported_answer_values == [30.0]


def test_arabic_duration_equivalence() -> None:
    result = check_duration_consistency(
        answer="مدة الاسترجاع أسبوعين.",
        evidence="مدة الاسترجاع 14 يوم.",
    )

    assert result.contradiction is False
