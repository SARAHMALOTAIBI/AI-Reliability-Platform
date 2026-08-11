import pytest

from reporting.health_score import (
    calculate_health_score,
    classify_health_score,
)


def test_perfect_metrics_are_excellent() -> None:
    result = calculate_health_score(
        {
            "faithfulness": 1.0,
            "answer_relevancy": 1.0,
            "answer_correctness": 1.0,
            "context_precision": 1.0,
            "context_recall": 1.0,
        }
    )

    assert result.score == 100
    assert result.status == "EXCELLENT"


def test_missing_optional_metric_is_normalized() -> None:
    result = calculate_health_score(
        {
            "faithfulness": 1.0,
            "answer_relevancy": 1.0,
            "answer_correctness": 1.0,
            "context_precision": 1.0,
            "context_recall": None,
        }
    )

    assert result.score == 100
    assert result.status == "EXCELLENT"


def test_zero_metrics_are_critical() -> None:
    result = calculate_health_score(
        {
            "faithfulness": 0.0,
            "answer_relevancy": 0.0,
            "answer_correctness": 0.0,
            "context_precision": 0.0,
            "context_recall": 0.0,
        }
    )

    assert result.score == 0
    assert result.status == "CRITICAL"


@pytest.mark.parametrize(
    ("score", "expected"),
    [
        (100, "EXCELLENT"),
        (90, "EXCELLENT"),
        (89, "GOOD"),
        (80, "GOOD"),
        (79, "WARNING"),
        (65, "WARNING"),
        (64, "POOR"),
        (40, "POOR"),
        (39, "CRITICAL"),
        (0, "CRITICAL"),
    ],
)
def test_health_status_thresholds(
    score: int,
    expected: str,
) -> None:
    assert (
        classify_health_score(score)
        == expected
    )


def test_invalid_metric_raises_error() -> None:
    with pytest.raises(ValueError):
        calculate_health_score(
            {
                "faithfulness": 1.5,
            }
        )
