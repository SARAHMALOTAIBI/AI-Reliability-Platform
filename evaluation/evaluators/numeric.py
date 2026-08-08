from evaluation.evaluators.models import (
    NumericEvaluationResult,
)
from evaluation.rules.numeric_consistency import (
    check_duration_consistency,
)


class NumericConsistencyEvaluator:
    def evaluate(
        self,
        answer: str,
        evidence: str,
    ) -> NumericEvaluationResult:
        if not evidence.strip():
            return NumericEvaluationResult(
                score=0.0,
                contradiction=False,
                explanation=(
                    "Numeric consistency could not "
                    "be evaluated because no evidence "
                    "was provided."
                ),
                unsupported_answer_values=(),
            )

        result = check_duration_consistency(
            answer=answer,
            evidence=evidence,
        )

        numeric_score = (
            0.0
            if result.contradiction
            else 1.0
        )

        return NumericEvaluationResult(
            score=numeric_score,
            contradiction=result.contradiction,
            explanation=result.explanation,
            unsupported_answer_values=tuple(
                result.unsupported_answer_values
            ),
        )