"""Deterministic rules for retrieval, generation, KB, and prompt failures."""

from __future__ import annotations

from typing import Optional


def check_retrieval_failure(
    context_precision: float,
    threshold: float = 0.5,
) -> Optional[dict]:
    if context_precision < threshold:
        return {
            "category": "RETRIEVAL_FAILURE",
            "subcategory": "LOW_CONTEXT_PRECISION",
            "severity": (
                "HIGH"
                if context_precision < 0.3
                else "MEDIUM"
            ),
            "confidence": 0.85,
            "explanation": (
                f"Context precision is "
                f"{context_precision:.2f}, below the "
                f"threshold of {threshold}. The retriever "
                "is likely returning irrelevant or "
                "low-quality chunks."
            ),
        }

    return None


def check_generation_hallucination(
    context_precision: float,
    faithfulness: float,
    precision_threshold: float = 0.6,
    faithfulness_threshold: float = 0.5,
) -> Optional[dict]:
    if (
        context_precision >= precision_threshold
        and faithfulness < faithfulness_threshold
    ):
        return {
            "category": "GENERATION_FAILURE",
            "subcategory": "UNSUPPORTED_CLAIM",
            "severity": (
                "HIGH"
                if faithfulness < 0.3
                else "MEDIUM"
            ),
            "confidence": 0.9,
            "explanation": (
                f"Context precision is high "
                f"({context_precision:.2f}) but "
                f"faithfulness is low "
                f"({faithfulness:.2f}). The retrieved "
                "context was relevant, but the model "
                "generated an answer not grounded in it."
            ),
        }

    return None


def check_knowledge_gap(
    context_recall: float,
    context_precision: float,
    recall_threshold: float = 0.5,
) -> Optional[dict]:
    if (
        context_recall < recall_threshold
        and context_precision >= 0.5
    ):
        return {
            "category": "KNOWLEDGE_BASE_FAILURE",
            "subcategory": "MISSING_INFORMATION",
            "severity": (
                "HIGH"
                if context_recall < 0.3
                else "MEDIUM"
            ),
            "confidence": 0.8,
            "explanation": (
                f"Context recall is {context_recall:.2f}, "
                f"below the threshold of "
                f"{recall_threshold}, while context "
                f"precision is acceptable "
                f"({context_precision:.2f}). The "
                "knowledge base may lack information "
                "needed to fully answer the question."
            ),
        }

    return None


def check_prompt_failure(
    context_precision: float,
    answer_relevancy: float,
    precision_threshold: float = 0.6,
    relevancy_threshold: float = 0.5,
) -> Optional[dict]:
    if (
        context_precision >= precision_threshold
        and answer_relevancy < relevancy_threshold
    ):
        return {
            "category": "PROMPT_FAILURE",
            "subcategory": "LOW_ANSWER_RELEVANCY",
            "severity": (
                "HIGH"
                if answer_relevancy < 0.3
                else "MEDIUM"
            ),
            "confidence": 0.75,
            "explanation": (
                f"Context precision is high "
                f"({context_precision:.2f}) but answer "
                f"relevancy is low "
                f"({answer_relevancy:.2f}). This "
                "suggests a prompt clarity issue or a "
                "model reasoning failure."
            ),
        }

    return None


def check_verified_knowledge_result(
    verification_status: str,
    context_alignment_score: float | None,
    explanation: str,
    context_alignment_threshold: float = 0.55,
) -> Optional[dict]:
    """
    Use independently retrieved company evidence before proxy-only rules.

    - Missing relevant company evidence => KB failure.
    - Company evidence exists but RAG context missed it => retrieval failure.
    - RAG context contains the evidence but answer conflicts => generation failure.
    """
    if verification_status in {
        "NOT_AVAILABLE",
        "SUPPORTED",
    }:
        return None

    if verification_status == "NO_RELEVANT_EVIDENCE":
        return {
            "category": "KNOWLEDGE_BASE_FAILURE",
            "subcategory": "VERIFIED_MISSING_INFORMATION",
            "severity": "HIGH",
            "confidence": 0.95,
            "explanation": (
                "Independent knowledge-base verification "
                f"found no relevant company evidence. "
                f"{explanation}"
            ),
        }

    if verification_status in {
        "UNSUPPORTED",
        "CONTRADICTED",
    }:
        alignment = (
            context_alignment_score
            if context_alignment_score is not None
            else 0.0
        )

        if alignment < context_alignment_threshold:
            return {
                "category": "RETRIEVAL_FAILURE",
                "subcategory": "VERIFIED_MISSED_EVIDENCE",
                "severity": "HIGH",
                "confidence": 0.95,
                "explanation": (
                    "Relevant evidence exists in the "
                    "company knowledge base, but the RAG "
                    "context does not align with that "
                    f"evidence (alignment {alignment:.2f}). "
                    f"{explanation}"
                ),
            }

        return {
            "category": "GENERATION_FAILURE",
            "subcategory": "VERIFIED_UNSUPPORTED_ANSWER",
            "severity": "HIGH",
            "confidence": 0.97,
            "explanation": (
                "The RAG context aligns with independently "
                "retrieved company evidence, but the "
                "generated answer is not supported by that "
                f"evidence. {explanation}"
            ),
        }

    return None


# Backward-compatible wrapper for older tests/imports.
def check_verified_knowledge_gap(
    is_supported: bool,
    similarity_distance: float,
    explanation: str,
) -> Optional[dict]:
    if is_supported:
        return None

    return {
        "category": "KNOWLEDGE_BASE_FAILURE",
        "subcategory": "VERIFIED_MISSING_INFORMATION",
        "severity": (
            "HIGH"
            if similarity_distance > 0.9
            else "MEDIUM"
        ),
        "confidence": 0.95,
        "explanation": (
            "Verified against the company's real "
            f"knowledge base: {explanation}"
        ),
    }
