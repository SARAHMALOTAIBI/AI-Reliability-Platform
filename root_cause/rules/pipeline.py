"""
Rules Pipeline
==============

Runs Layer 1 deterministic root-cause rules
in priority order.
"""

from typing import Optional

from root_cause.rules.retrieval_rules import (
    check_retrieval_failure,
    check_generation_hallucination,
    check_knowledge_gap,
    check_prompt_failure,
    check_verified_knowledge_gap,
)



def run_rules_pipeline(
    metrics: dict,
) -> Optional[dict]:
    """
    Run deterministic diagnosis rules and return
    the highest-priority diagnosis.
    """

    context_precision = metrics.get(
        "context_precision"
    )

    faithfulness = metrics.get(
        "faithfulness"
    )

    if context_precision is None:
        return None

    # Priority 1 — Retrieval failure
    retrieval_diagnosis = (
        check_retrieval_failure(
            context_precision
        )
    )

    if retrieval_diagnosis is not None:
        return retrieval_diagnosis

    # Priority 2 — Generation hallucination
    if faithfulness is not None:
        hallucination_diagnosis = (
            check_generation_hallucination(
                context_precision=(
                    context_precision
                ),
                faithfulness=faithfulness,
            )
        )

        if hallucination_diagnosis is not None:
            return hallucination_diagnosis

    # Priority 3 — Knowledge-base gap
    context_recall = metrics.get(
        "context_recall"
    )

    if context_recall is not None:
        knowledge_gap_diagnosis = (
            check_knowledge_gap(
                context_recall=context_recall,
                context_precision=(
                    context_precision
                ),
            )
        )

        if knowledge_gap_diagnosis is not None:
            return knowledge_gap_diagnosis

    # Priority 4 — Prompt failure
    answer_relevancy = metrics.get(
        "answer_relevancy"
    )

    if answer_relevancy is not None:
        prompt_failure_diagnosis = (
            check_prompt_failure(
                context_precision=(
                    context_precision
                ),
                answer_relevancy=(
                    answer_relevancy
                ),
            )
        )

        if prompt_failure_diagnosis is not None:
            return prompt_failure_diagnosis
        
    # Priority 5: Check verified knowledge base gap (highest confidence,
    # only used if the Knowledge Base Verification Agent was run)
    is_supported = metrics.get("is_supported")
    if is_supported is not None:
        verified_gap_diagnosis = check_verified_knowledge_gap(
            is_supported=is_supported,
            similarity_distance=metrics.get("similarity_distance", 1.0),
            explanation=metrics.get("verification_explanation", ""),
        )
        if verified_gap_diagnosis is not None:
            return verified_gap_diagnosis


    return None
