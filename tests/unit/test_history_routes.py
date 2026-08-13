from app.main import app


def test_history_list_route_is_registered() -> None:
    schema = app.openapi()

    path = schema["paths"].get(
        "/api/v1/health-checks"
    )

    assert path is not None
    assert "get" in path
    assert "post" in path


def test_history_detail_route_is_registered() -> None:
    schema = app.openapi()

    path = schema["paths"].get(
        "/api/v1/health-checks/{health_check_id}"
    )

    assert path is not None
    assert "get" in path


def test_api_version_is_0_7_0() -> None:
    assert app.version == "0.8.0"