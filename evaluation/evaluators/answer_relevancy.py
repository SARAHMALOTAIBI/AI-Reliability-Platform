from evaluation.evaluators.models import (
    ScoreResult,
)
from evaluation.generation.embedding_service import (
    semantic_similarity,
)


class AnswerRelevancyEvaluator:
    """
    Measures whether the generated answer
    addresses the user's question.
    """

    def evaluate(
        self,
        question: str,
        answer: str,
    ) -> ScoreResult:
        clean_question = question.strip()
        clean_answer = answer.strip()

        if not clean_question or not clean_answer:
            return ScoreResult(
                score=0.0,
                explanation=(
                    "Answer relevancy could not be "
                    "evaluated because the question "
                    "or answer was empty."
                ),
            )

        score = semantic_similarity(
            clean_question,
            clean_answer,
        )

        return ScoreResult(
            score=score,
            explanation=(
                "Answer relevancy was estimated using "
                "semantic similarity between the user "
                "question and the generated answer."
            ),
        )
