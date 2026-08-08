from evaluation.evaluators.models import (
    StatusResult,
)


class StatusClassifier:
    HEALTHY_CORRECTNESS_THRESHOLD = 0.80
    HEALTHY_FAITHFULNESS_THRESHOLD = 0.70

    WARNING_CORRECTNESS_THRESHOLD = 0.60
    WARNING_FAITHFULNESS_THRESHOLD = 0.50

    def classify(
        self,
        correctness_score: float,
        faithfulness_score: float,
        numeric_contradiction: bool,
    ) -> StatusResult:
        if numeric_contradiction:
            return StatusResult(
                status="CRITICAL",
                explanation=(
                    "The answer contains a numeric "
                    "contradiction against the "
                    "available evidence."
                ),
            )

        if (
            correctness_score
            >= self.HEALTHY_CORRECTNESS_THRESHOLD
            and faithfulness_score
            >= self.HEALTHY_FAITHFULNESS_THRESHOLD
        ):
            return StatusResult(
                status="HEALTHY",
                explanation=(
                    "The answer is semantically "
                    "similar to the expected answer "
                    "and supported by the context."
                ),
            )

        if (
            correctness_score
            >= self.WARNING_CORRECTNESS_THRESHOLD
            and faithfulness_score
            >= self.WARNING_FAITHFULNESS_THRESHOLD
        ):
            return StatusResult(
                status="WARNING",
                explanation=(
                    "The answer may be partially "
                    "correct or only partially "
                    "supported by the context."
                ),
            )

        return StatusResult(
            status="CRITICAL",
            explanation=(
                "The answer has low semantic "
                "similarity to the expected answer "
                "or weak support from the context."
            ),
        )