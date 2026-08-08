"""
Unit tests for retrieval_rules.py
"""

from root_cause.rules.retrieval_rules import (
    check_retrieval_failure,
    check_generation_hallucination,
)


def test_retrieval_failure_triggers_on_low_precision():
    result = check_retrieval_failure(context_precision=0.2)
    assert result is not None
    assert result["category"] == "RETRIEVAL_FAILURE"
    assert result["severity"] == "HIGH"


def test_retrieval_failure_does_not_trigger_on_good_precision():
    result = check_retrieval_failure(context_precision=0.9)
    assert result is None


def test_hallucination_triggers_on_good_retrieval_low_faithfulness():
    result = check_generation_hallucination(
        context_precision=0.92,
        faithfulness=0.35,
    )
    assert result is not None
    assert result["category"] == "GENERATION_FAILURE"
    assert result["subcategory"] == "UNSUPPORTED_CLAIM"


def test_hallucination_does_not_trigger_when_retrieval_is_bad():
    # Low precision means the issue is retrieval, not generation
    result = check_generation_hallucination(
        context_precision=0.3,
        faithfulness=0.3,
    )
    assert result is None
