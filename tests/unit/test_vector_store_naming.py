from knowledge_base.vector_store import (
    collection_name_for_project,
)


def test_collection_name_is_stable_and_safe() -> None:
    first = collection_name_for_project(
        "customer-support-rag"
    )
    second = collection_name_for_project(
        "customer-support-rag"
    )

    assert first == second
    assert first.startswith("kb_v2_")
    assert len(first) < 64
