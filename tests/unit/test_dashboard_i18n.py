from dashboard.i18n import (
    localize_action,
    localize_value,
    tr,
)


def test_arabic_platform_title() -> None:
    assert (
        tr(
            "ar",
            "platform_title",
        )
        == "منصة موثوقية الذكاء الاصطناعي"
    )


def test_generation_failure_translation() -> None:
    assert (
        localize_value(
            "GENERATION_FAILURE",
            "ar",
        )
        == "فشل التوليد"
    )


def test_unsupported_claim_translation() -> None:
    assert (
        localize_value(
            "UNSUPPORTED_CLAIM",
            "ar",
        )
        == "ادعاء غير مدعوم"
    )


def test_generation_recommendation_translation() -> None:
    english = (
        "Strengthen grounding instructions "
        "so the model answers only from "
        "retrieved evidence."
    )

    arabic = localize_action(
        english,
        "ar",
    )

    assert (
        "السياق المسترجع"
        in arabic
    )