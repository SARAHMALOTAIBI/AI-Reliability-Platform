from dashboard.api_client import (
    normalize_base_url,
)


def test_normalize_base_url_removes_trailing_slash() -> None:
    assert (
        normalize_base_url(
            "http://127.0.0.1:8002/"
        )
        == "http://127.0.0.1:8002"
    )


def test_normalize_base_url_keeps_clean_url() -> None:
    assert (
        normalize_base_url(
            "http://127.0.0.1:8002"
        )
        == "http://127.0.0.1:8002"
    )