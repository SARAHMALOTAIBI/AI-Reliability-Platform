from evaluation.evaluators.hallucination import (
    HallucinationRiskEvaluator,
)
from evaluation.evaluators.status import (
    StatusClassifier,
)


def test_high_faithfulness_has_low_risk() -> None:
    evaluator = HallucinationRiskEvaluator()

    result = evaluator.evaluate(
        faithfulness_score=0.90,
        numeric_contradiction=False,
    )

    assert result.score == 0.10


def test_numeric_contradiction_increases_risk() -> None:
    evaluator = HallucinationRiskEvaluator()

    result = evaluator.evaluate(
        faithfulness_score=0.75,
        numeric_contradiction=True,
    )

    assert result.score >= 0.80


def test_healthy_scores_are_classified_healthy() -> None:
    classifier = StatusClassifier()

    result = classifier.classify(
        correctness_score=0.90,
        faithfulness_score=0.85,
        numeric_contradiction=False,
    )

    assert result.status == "HEALTHY"


def test_numeric_contradiction_is_critical() -> None:
    classifier = StatusClassifier()

    result = classifier.classify(
        correctness_score=0.95,
        faithfulness_score=0.95,
        numeric_contradiction=True,
    )

    assert result.status == "CRITICAL"