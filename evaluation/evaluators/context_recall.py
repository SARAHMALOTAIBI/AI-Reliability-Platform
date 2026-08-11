import re

from evaluation.evaluators.models import (
    ScoreResult,
)
from evaluation.generation.embedding_service import (
    pairwise_semantic_similarity,
)


_REFERENCE_SPLIT_PATTERN = re.compile(
    r"(?<=[.!?؟])\s+|\n+"
)


class ContextRecallEvaluator:
    """
    Reference-grounded semantic coverage proxy.

    For every sentence in the reference answer,
    find the best matching retrieved context.

    The final score is the average coverage
    across reference-answer statements.

    Returns None when no reference answer exists,
    because recall cannot be estimated reliably
    without expected evidence.
    """

    def evaluate(
        self,
        reference_answer: str | None,
        contexts: list[str],
    ) -> ScoreResult | None:
        if (
            reference_answer is None
            or not reference_answer.strip()
        ):
            return None

        clean_contexts = [
            context.strip()
            for context in contexts
            if context and context.strip()
        ]

        if not clean_contexts:
            return ScoreResult(
                score=0.0,
                explanation=(
                    "Context recall is zero because "
                    "a reference answer exists but "
                    "no retrieved context was provided."
                ),
            )

        reference_units = [
            unit.strip()
            for unit in _REFERENCE_SPLIT_PATTERN.split(
                reference_answer.strip()
            )
            if unit.strip()
        ]

        if not reference_units:
            return None

        matrix = pairwise_semantic_similarity(
            reference_units,
            clean_contexts,
        )

        coverage_scores = [
            float(row.max())
            for row in matrix
        ]

        score = (
            sum(coverage_scores)
            / len(coverage_scores)
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
                "Context recall is a reference-grounded "
                "semantic coverage proxy calculated from "
                "how well the retrieved contexts cover "
                "the reference-answer statements."
            ),
        )
