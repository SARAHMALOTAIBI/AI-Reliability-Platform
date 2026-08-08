from evaluation.evaluators.models import (
    ScoreResult,
)
from evaluation.generation.embedding_service import (
    semantic_similarity,
)


class CorrectnessEvaluator:
    def evaluate(
        self,
        answer: str,
        reference_answer: str | None,
        fallback_context: str,
    ) -> ScoreResult:
        clean_reference = (
            reference_answer.strip()
            if reference_answer
            else ""
        )

        clean_fallback = fallback_context.strip()

        evidence = (
            clean_reference
            or clean_fallback
        )

        if not evidence:
            return ScoreResult(
                score=0.0,
                explanation=(
                    "Correctness could not be evaluated "
                    "because no reference answer or "
                    "fallback context was provided."
                ),
            )

        score = semantic_similarity(
            answer,
            evidence,
        )

        evidence_type = (
            "reference answer"
            if clean_reference
            else "retrieved context used as a proxy"
        )

        return ScoreResult(
            score=score,
            explanation=(
                "Correctness was estimated using "
                "semantic similarity against the "
                f"{evidence_type}."
            ),
        )