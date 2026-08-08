"""
Rules Pipeline
==============
Runs all Layer 1 deterministic rules against a set of metrics
and returns the most relevant diagnosis (if any).
"""

from typing import Optional

from root_cause.rules.retrieval_rules import (
    check_retrieval_failure,
    check_generation_hallucination,
    check_knowledge_gap,
)



def run_rules_pipeline(metrics: dict) -> Optional[dict]:
    """
    Runs all available Layer 1 rules in priority order and returns
    the first diagnosis that triggers.

    Args:
        metrics: dict containing evaluation scores, e.g.:
            {
                "context_precision": 0.92,
                "faithfulness": 0.35,
            }

    Returns:
        A diagnosis dict if any rule triggers, otherwise None.
    """
    context_precision = metrics.get("context_precision")
    faithfulness = metrics.get("faithfulness")

    if context_precision is None:
        return None

    # Priority 1: Check retrieval failure first — if retrieval itself
    # is broken, there's no point diagnosing generation issues yet.
    retrieval_diagnosis = check_retrieval_failure(context_precision)
    if retrieval_diagnosis is not None:
        return retrieval_diagnosis

    # Priority 2: Only check hallucination if retrieval was good
    if faithfulness is not None:
        hallucination_diagnosis = check_generation_hallucination(
            context_precision=context_precision,
            faithfulness=faithfulness,
        )
        if hallucination_diagnosis is not None:
            return hallucination_diagnosis

    # Priority 3: Check for knowledge base gaps
    context_recall = metrics.get("context_recall")
    if context_recall is not None:
        knowledge_gap_diagnosis = check_knowledge_gap(
            context_recall=context_recall,
            context_precision=context_precision,
        )
        if knowledge_gap_diagnosis is not None:
            return knowledge_gap_diagnosis

    return None


    # Priority 1: Check retrieval failure first — if retrieval itself
    # is broken, there's no point diagnosing generation issues yet.
    retrieval_diagnosis = check_retrieval_failure(context_precision)
    if retrieval_diagnosis is not None:
        return retrieval_diagnosis

    # Priority 2: Only check hallucination if retrieval was good
    if faithfulness is not None:
        hallucination_diagnosis = check_generation_hallucination(
            context_precision=context_precision,
            faithfulness=faithfulness,
        )
        if hallucination_diagnosis is not None:
            return hallucination_diagnosis

    return None