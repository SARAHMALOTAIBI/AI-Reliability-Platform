from dataclasses import dataclass

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from evaluation.rules.numeric_consistency import check_duration_consistency


MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

_model = SentenceTransformer(MODEL_NAME)


@dataclass
class SemanticEvaluationResult:
    correctness_score: float
    faithfulness_score: float
    hallucination_risk: float
    status: str
    explanation: str


def calculate_similarity(text_a: str, text_b: str) -> float:
    embeddings = _model.encode(
        [text_a, text_b],
        normalize_embeddings=True,
    )

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]],
    )[0][0]

    return float(score)


def evaluate_semantically(
    answer: str,
    contexts: list[str],
    reference_answer: str | None = None,
) -> SemanticEvaluationResult:
    combined_context = " ".join(contexts).strip()

    if combined_context:
        faithfulness_score = calculate_similarity(
            answer,
            combined_context,
        )
    else:
        faithfulness_score = 0.0

    if reference_answer:
        correctness_score = calculate_similarity(
            answer,
            reference_answer,
        )
    else:
        correctness_score = faithfulness_score

    evidence_text = reference_answer or combined_context

    duration_check = check_duration_consistency(
        answer=answer,
        evidence=evidence_text,
    )

    if duration_check.contradiction:
        correctness_score = min(correctness_score, 0.2)
        faithfulness_score = min(faithfulness_score, 0.2)
        hallucination_risk = max(
            0.8,
            1.0 - faithfulness_score,
        )

        return SemanticEvaluationResult(
            correctness_score=round(correctness_score, 4),
            faithfulness_score=round(faithfulness_score, 4),
            hallucination_risk=round(hallucination_risk, 4),
            status="CRITICAL",
            explanation=(
                "A numeric contradiction was detected. "
                + duration_check.explanation
            ),
        )

    hallucination_risk = max(
        0.0,
        1.0 - faithfulness_score,
    )

    if correctness_score >= 0.80 and faithfulness_score >= 0.70:
        status = "HEALTHY"
        explanation = (
            "The answer is semantically similar to the reference answer "
            "and supported by the retrieved context."
        )
    elif correctness_score >= 0.60 and faithfulness_score >= 0.50:
        status = "WARNING"
        explanation = (
            "The answer is partially correct or only partially supported "
            "by the retrieved context."
        )
    else:
        status = "CRITICAL"
        explanation = (
            "The answer has low semantic similarity to the expected answer "
            "or is not sufficiently supported by the context."
        )

    return SemanticEvaluationResult(
        correctness_score=round(correctness_score, 4),
        faithfulness_score=round(faithfulness_score, 4),
        hallucination_risk=round(hallucination_risk, 4),
        status=status,
        explanation=explanation,
    )
