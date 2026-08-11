import pytest

from recommendation_engine.engine import (
    generate_recommendations,
)


@pytest.mark.parametrize(
    "category",
    [
        "RETRIEVAL_FAILURE",
        "GENERATION_FAILURE",
        "KNOWLEDGE_BASE_FAILURE",
        "PROMPT_FAILURE",
    ],
)
def test_known_diagnosis_generates_recommendations(
    category: str,
) -> None:
    recommendations = generate_recommendations(
        {
            "category": category,
            "explanation": "Test evidence.",
        }
    )

    assert len(recommendations) == 3

    priorities = [
        item.priority
        for item in recommendations
    ]

    assert priorities == [1, 2, 3]

    assert all(
        item.supporting_evidence
        == "Test evidence."
        for item in recommendations
    )


def test_no_diagnosis_returns_no_recommendations() -> None:
    assert generate_recommendations(None) == []


def test_unknown_diagnosis_returns_no_recommendations() -> None:
    result = generate_recommendations(
        {
            "category": "UNKNOWN_FAILURE",
        }
    )

    assert result == []
