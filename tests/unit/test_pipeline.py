"""
Unit tests for the rules pipeline (root_cause/rules/pipeline.py)
"""

from root_cause.rules.pipeline import run_rules_pipeline


def test_pipeline_detects_retrieval_failure():
    metrics = {
        "context_precision": 0.2,
        "faithfulness": 0.8,
    }
    result = run_rules_pipeline(metrics)
    assert result is not None
    assert result["category"] == "RETRIEVAL_FAILURE"


def test_pipeline_detects_hallucination_when_retrieval_is_good():
    metrics = {
        "context_precision": 0.92,
        "faithfulness": 0.35,
    }
    result = run_rules_pipeline(metrics)
    assert result is not None
    assert result["category"] == "GENERATION_FAILURE"


def test_pipeline_returns_none_when_everything_is_healthy():
    metrics = {
        "context_precision": 0.9,
        "faithfulness": 0.9,
    }
    result = run_rules_pipeline(metrics)
    assert result is None


def test_pipeline_returns_none_when_context_precision_missing():
    metrics = {
        "faithfulness": 0.9,
    }
    result = run_rules_pipeline(metrics)
    assert result is None


def test_pipeline_prioritizes_retrieval_over_hallucination():
    # Both retrieval AND faithfulness are bad — retrieval should win
    # because it's checked first (root cause priority)
    metrics = {
        "context_precision": 0.2,
        "faithfulness": 0.2,
    }
    result = run_rules_pipeline(metrics)
    assert result["category"] == "RETRIEVAL_FAILURE"
