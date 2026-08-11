from evaluation.evaluators.answer_relevancy import (
    AnswerRelevancyEvaluator,
)
from evaluation.evaluators.context_precision import (
    ContextPrecisionEvaluator,
)
from evaluation.evaluators.context_recall import (
    ContextRecallEvaluator,
)


def test_context_precision_exact_match_is_high() -> None:
    evaluator = ContextPrecisionEvaluator()

    result = evaluator.evaluate(
        question=(
            "Customers may request refunds "
            "within 14 days."
        ),
        contexts=[
            (
                "Customers may request refunds "
                "within 14 days."
            )
        ],
    )

    assert result.score >= 0.99


def test_context_precision_empty_context_is_zero() -> None:
    evaluator = ContextPrecisionEvaluator()

    result = evaluator.evaluate(
        question="What is the refund period?",
        contexts=[],
    )

    assert result.score == 0.0


def test_context_recall_exact_reference_is_high() -> None:
    evaluator = ContextRecallEvaluator()

    result = evaluator.evaluate(
        reference_answer=(
            "Customers may request refunds "
            "within 14 days."
        ),
        contexts=[
            (
                "Customers may request refunds "
                "within 14 days."
            )
        ],
    )

    assert result is not None
    assert result.score >= 0.99


def test_context_recall_without_reference_is_none() -> None:
    evaluator = ContextRecallEvaluator()

    result = evaluator.evaluate(
        reference_answer=None,
        contexts=[
            "Refunds are available."
        ],
    )

    assert result is None


def test_answer_relevancy_exact_match_is_high() -> None:
    evaluator = AnswerRelevancyEvaluator()

    result = evaluator.evaluate(
        question="What is the refund period?",
        answer="What is the refund period?",
    )

    assert result.score >= 0.99
