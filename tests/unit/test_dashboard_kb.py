from inspect import signature

from dashboard.api_client import verify_knowledge_base_answer
from dashboard.i18n import localize_kb_explanation, localize_value, tr


def test_kb_dashboard_client_requires_answer() -> None:
    parameters = signature(verify_knowledge_base_answer).parameters
    assert "answer" in parameters
    assert "rag_context" in parameters


def test_kb_arabic_labels() -> None:
    assert tr("ar", "knowledge_base") == "قاعدة المعرفة"
    assert localize_value("CONTRADICTED", "ar") == "متعارض"
    assert localize_value("VERIFIED_MISSED_EVIDENCE", "ar") == "فشل في استرجاع دليل موجود"


def test_kb_arabic_explanation_for_contradiction() -> None:
    text = localize_kb_explanation(
        {"status": "CONTRADICTED", "explanation": "Numeric contradiction."},
        "ar",
    )
    assert "تعارض رقمي" in text
