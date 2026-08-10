from evaluation.evaluators.models import (
    ScoreResult,
)
from evaluation.generation.embedding_service import (
    semantic_similarity,
)


class ContextPrecisionEvaluator:
    def evaluate(
        self,
        question: str,
        combined_context: str,
    ) -> ScoreResult:
        clean_context = combined_context.strip()

        if not clean_context:
            return ScoreResult(
                score=0.0,
                explanation=(
                    "Context precision could not be "
                    "evaluated because no retrieved "
                    "context was provided."
                ),
            )

        score = semantic_similarity(
            question,
            clean_context,
        )

        return ScoreResult(
            score=score,
            explanation=(
                "Context precision was estimated using "
                "semantic similarity between the question "
                "and the retrieved context."
            ),
        )
