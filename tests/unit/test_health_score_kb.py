from reporting.health_score import calculate_health_score


def test_kb_metric_is_optional_for_backward_compatibility() -> None:
    without_kb = calculate_health_score(
        {
            "faithfulness": 0.8,
            "answer_relevancy": 0.8,
            "answer_correctness": 0.8,
            "context_precision": 0.8,
            "context_recall": 0.8,
            "knowledge_base_support": None,
        }
    )

    assert without_kb.score == 80


def test_kb_contradiction_can_reduce_health_score() -> None:
    without_kb = calculate_health_score(
        {
            "faithfulness": 1.0,
            "answer_relevancy": 1.0,
            "answer_correctness": 1.0,
            "context_precision": 1.0,
            "context_recall": 1.0,
            "knowledge_base_support": None,
        }
    )

    with_kb_failure = calculate_health_score(
        {
            "faithfulness": 1.0,
            "answer_relevancy": 1.0,
            "answer_correctness": 1.0,
            "context_precision": 1.0,
            "context_recall": 1.0,
            "knowledge_base_support": 0.0,
        }
    )

    assert without_kb.score == 100
    assert with_kb_failure.score < 100
