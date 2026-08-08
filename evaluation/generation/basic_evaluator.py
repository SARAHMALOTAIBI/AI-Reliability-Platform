from dataclasses import dataclass


@dataclass
class EvaluationResult:
    correctness_score: float
    faithfulness_score: float
    hallucination_risk: float
    status: str
    explanation: str


def normalize_text(text: str) -> str:
    return " ".join(text.lower().strip().split())


def evaluate_answer(
    answer: str,
    contexts: list[str],
    reference_answer: str | None = None,
) -> EvaluationResult:
    normalized_answer = normalize_text(answer)
    normalized_context = normalize_text(" ".join(contexts))

    faithfulness_score = 1.0 if normalized_answer in normalized_context else 0.0

    if reference_answer:
        normalized_reference = normalize_text(reference_answer)
        correctness_score = (
            1.0 if normalized_answer == normalized_reference else 0.0
        )
    else:
        correctness_score = faithfulness_score

    hallucination_risk = 1.0 - faithfulness_score

    if correctness_score == 1.0 and faithfulness_score == 1.0:
        status = "HEALTHY"
        explanation = "The answer matches the reference answer and is supported by the context."
    elif faithfulness_score == 0.0:
        status = "CRITICAL"
        explanation = "The answer is not supported by the retrieved context."
    else:
        status = "WARNING"
        explanation = "The answer may be incomplete or partially incorrect."

    return EvaluationResult(
        correctness_score=correctness_score,
        faithfulness_score=faithfulness_score,
        hallucination_risk=hallucination_risk,
        status=status,
        explanation=explanation,
    )