from evaluation.evaluators.models import (
    ScoreResult,
)


class HallucinationRiskEvaluator:
    CONTRADICTION_MINIMUM_RISK = 0.80

    def evaluate(
        self,
        faithfulness_score: float,
        numeric_contradiction: bool,
    ) -> ScoreResult:
        base_risk = (
            1.0 - faithfulness_score
        )

        if numeric_contradiction:
            risk = max(
                self.CONTRADICTION_MINIMUM_RISK,
                base_risk,
            )

            explanation = (
                "Hallucination risk was increased "
                "because a numeric contradiction "
                "was detected."
            )
        else:
            risk = base_risk

            explanation = (
                "Hallucination risk is a heuristic "
                "derived from the answer's "
                "faithfulness score."
            )

        normalized_risk = round(
            max(
                0.0,
                min(1.0, risk),
            ),
            4,
        )

        return ScoreResult(
            score=normalized_risk,
            explanation=explanation,
        )