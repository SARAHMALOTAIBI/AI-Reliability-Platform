from evaluation.evaluators.models import (
    ScoreResult,
)
from evaluation.generation.embedding_service import (
    semantic_similarity,
)


class FaithfulnessEvaluator:
    def evaluate(
        self,
        answer: str,
        combined_context: str,
    ) -> ScoreResult:
        clean_context = combined_context.strip()

        if not clean_context:
            return ScoreResult(
                score=0.0,
                explanation=(
                    "Faithfulness could not be "
                    "evaluated because no retrieved "
                    "context was provided."
                ),
            )

        score = semantic_similarity(
            answer,
            clean_context,
        )

        return ScoreResult(
            score=score,
            explanation=(
                "Faithfulness was estimated using "
                "semantic similarity between the "
                "answer and the retrieved context."
            ),
        )