from app.models import (
    Base,
    KnowledgeBaseDocument,
    KnowledgeBaseVerification,
)


def test_knowledge_base_models_are_registered() -> None:
    tables = set(
        Base.metadata.tables.keys()
    )

    assert "knowledge_base_documents" in tables
    assert "knowledge_base_verifications" in tables


def test_knowledge_base_model_table_names() -> None:
    assert (
        KnowledgeBaseDocument.__tablename__
        == "knowledge_base_documents"
    )
    assert (
        KnowledgeBaseVerification.__tablename__
        == "knowledge_base_verifications"
    )
