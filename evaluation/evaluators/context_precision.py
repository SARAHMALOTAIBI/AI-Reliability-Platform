from evaluation.evaluators.models import (
    ScoreResult,
)
from evaluation.generation.embedding_service import (
    pairwise_semantic_similarity,
)


class ContextPrecisionEvaluator:
    """
    Estimates retrieval precision as the average
    semantic relevance of retrieved chunks to
    the user question.

    This is a deterministic semantic proxy,
    not label-based IR precision.
    """

    def evaluate(
        self,
        question: str,
        contexts: list[str],
    ) -> ScoreResult:
        clean_question = question.strip()

        clean_contexts = [
            context.strip()
            for context in contexts
            if context and context.strip()
        ]

        if not clean_question:
            return ScoreResult(
                score=0.0,
                explanation=(
                    "Context precision could not be "
                    "evaluated because the question "
                    "was empty."
                ),
            )

        if not clean_contexts:
            return ScoreResult(
                score=0.0,
                explanation=(
                    "Context precision could not be "
                    "evaluated because no retrieved "
                    "contexts were provided."
                ),
            )

        matrix = pairwise_semantic_similarity(
            [clean_question],
            clean_contexts,
        )

        relevance_scores = [
            float(score)
            for score in matrix[0]
        ]

        score = (
            sum(relevance_scores)
            / len(relevance_scores)
        )

        return ScoreResult(
            score=round(
                max(
                    0.0,
                    min(1.0, score),
                ),
                4,
            ),
            explanation=(
                "Context precision is a semantic "
                "proxy calculated as the average "
                "question relevance of the retrieved "
                "context chunks."
            ),
        )
