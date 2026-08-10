"""
Retrieval Rules
================
Layer 1 deterministic rules for diagnosing retrieval-related failures.
Based on architecture.md section 8.
"""

from typing import Optional


def check_retrieval_failure(context_precision: float, threshold: float = 0.5) -> Optional[dict]:
    """
    Rule: If context precision is low, the retrieval step likely failed
    to find relevant information.

    Args:
        context_precision: Score between 0 and 1 (from the Evaluation Engine)
        threshold: Minimum acceptable precision (default 0.5)

    Returns:
        A diagnosis dict if the rule triggers, otherwise None
    """
    if context_precision < threshold:
        return {
            "category": "RETRIEVAL_FAILURE",
            "subcategory": "LOW_CONTEXT_PRECISION",
            "severity": "HIGH" if context_precision < 0.3 else "MEDIUM",
            "confidence": 0.85,
            "explanation": (
                f"Context precision is {context_precision:.2f}, below the "
                f"threshold of {threshold}. The retriever is likely returning "
                f"irrelevant or low-quality chunks."
            ),
        }
    return None


def check_generation_hallucination(
    context_precision: float,
    faithfulness: float,
    precision_threshold: float = 0.6,
    faithfulness_threshold: float = 0.5,
) -> Optional[dict]:
    """
    Rule: If retrieval was good (high context precision) but faithfulness
    is low, the model is hallucinating despite having the right information.

    Args:
        context_precision: Score between 0 and 1
        faithfulness: Score between 0 and 1
    """
    if context_precision >= precision_threshold and faithfulness < faithfulness_threshold:
        return {
            "category": "GENERATION_FAILURE",
            "subcategory": "UNSUPPORTED_CLAIM",
            "severity": "HIGH" if faithfulness < 0.3 else "MEDIUM",
            "confidence": 0.9,
            "explanation": (
                f"Context precision is high ({context_precision:.2f}) but "
                f"faithfulness is low ({faithfulness:.2f}). The retrieved "
                f"context was relevant, but the model generated an answer "
                f"not grounded in it."
            ),
        }
    return None

def check_knowledge_gap(
    context_recall: float,
    context_precision: float,
    recall_threshold: float = 0.5,
) -> Optional[dict]:
    """
    Rule: If context recall is low but precision is fine, the retriever
    found relevant chunks, but the knowledge base is missing information
    needed to fully answer the question.

    Args:
        context_recall: Score between 0 and 1 — how much of the needed
                         information was actually retrieved
        context_precision: Score between 0 and 1 — how relevant the
                            retrieved chunks were
    """
    if context_recall < recall_threshold and context_precision >= 0.5:
        return {
            "category": "KNOWLEDGE_BASE_FAILURE",
            "subcategory": "MISSING_INFORMATION",
            "severity": "HIGH" if context_recall < 0.3 else "MEDIUM",
            "confidence": 0.8,
            "explanation": (
                f"Context recall is {context_recall:.2f}, below the "
                f"threshold of {recall_threshold}, while context precision "
                f"is acceptable ({context_precision:.2f}). The retrieved "
                f"chunks are relevant, but the knowledge base likely lacks "
                f"the full information needed to answer the question."
            ),
        }
    return None

def check_prompt_failure(
    context_precision: float,
    answer_relevancy: float,
    precision_threshold: float = 0.6,
    relevancy_threshold: float = 0.5,
) -> Optional[dict]:
    """
    Rule: If retrieval was good (high context precision) but the answer
    is not relevant to the question, the issue is likely with the prompt
    or the model's reasoning, not the retrieved information.

    Args:
        context_precision: Score between 0 and 1
        answer_relevancy: Score between 0 and 1 — how well the answer
                           addresses the actual question asked
    """
    if context_precision >= precision_threshold and answer_relevancy < relevancy_threshold:
        return {
            "category": "PROMPT_FAILURE",
            "subcategory": "LOW_ANSWER_RELEVANCY",
            "severity": "HIGH" if answer_relevancy < 0.3 else "MEDIUM",
            "confidence": 0.75,
            "explanation": (
                f"Context precision is high ({context_precision:.2f}) but "
                f"answer relevancy is low ({answer_relevancy:.2f}). The "
                f"retriever found relevant information, but the answer "
                f"does not properly address the question. This suggests "
                f"a prompt clarity issue or a model reasoning failure."
            ),
        }
    return None
