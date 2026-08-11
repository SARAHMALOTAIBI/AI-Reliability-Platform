from dataclasses import dataclass
from typing import Mapping


BASE_WEIGHTS = {
    "faithfulness": 0.25,
    "answer_relevancy": 0.15,
    "answer_correctness": 0.20,
    "context_precision": 0.15,
    "context_recall": 0.10,
}


@dataclass(frozen=True)
class HealthScoreResult:
    score: int
    status: str
    weights_used: dict[str, float]


def classify_health_score(score: int) -> str:
    if not 0 <= score <= 100:
        raise ValueError(
            "Health score must be between 0 and 100."
        )

    if score >= 90:
        return "EXCELLENT"

    if score >= 80:
        return "GOOD"

    if score >= 65:
        return "WARNING"

    if score >= 40:
        return "POOR"

    return "CRITICAL"


def calculate_health_score(
    metrics: Mapping[str, float | None],
) -> HealthScoreResult:
    """
    Calculate the overall reliability score.

    Only available metrics are included.
    Their configured weights are re-normalized
    so missing optional metrics do not count
    as zero.
    """

    available: dict[str, tuple[float, float]] = {}

    for name, weight in BASE_WEIGHTS.items():
        value = metrics.get(name)

        if value is None:
            continue

        if not 0.0 <= value <= 1.0:
            raise ValueError(
                f"{name} must be between 0 and 1."
            )

        available[name] = (
            float(value),
            weight,
        )

    if not available:
        raise ValueError(
            "At least one health metric is required."
        )

    total_weight = sum(
        weight
        for _, weight in available.values()
    )

    weighted_value = sum(
        value * weight
        for value, weight in available.values()
    )

    normalized_score = (
        weighted_value
        / total_weight
    )

    score = round(
        normalized_score * 100
    )

    normalized_weights = {
        name: round(
            weight / total_weight,
            4,
        )
        for name, (_, weight)
        in available.items()
    }

    return HealthScoreResult(
        score=score,
        status=classify_health_score(score),
        weights_used=normalized_weights,
    )
