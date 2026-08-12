from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class APIClientError(RuntimeError):
    pass


def normalize_base_url(base_url: str) -> str:
    return base_url.rstrip("/")


def request_json(
    base_url: str,
    path: str,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
    timeout: int = 180,
) -> dict[str, Any]:
    url = (
        f"{normalize_base_url(base_url)}"
        f"{path}"
    )

    body = None

    headers = {
        "Accept": "application/json",
    }

    if payload is not None:
        body = json.dumps(
            payload
        ).encode("utf-8")

        headers["Content-Type"] = (
            "application/json"
        )

    request = Request(
        url=url,
        data=body,
        headers=headers,
        method=method,
    )

    try:
        with urlopen(
            request,
            timeout=timeout,
        ) as response:
            raw = response.read().decode(
                "utf-8"
            )

            if not raw:
                return {}

            return json.loads(raw)

    except HTTPError as exc:
        try:
            detail = exc.read().decode(
                "utf-8"
            )
        except Exception:
            detail = str(exc)

        raise APIClientError(
            f"API returned HTTP "
            f"{exc.code}: {detail}"
        ) from exc

    except URLError as exc:
        raise APIClientError(
            "Could not connect to FastAPI. "
            "Make sure the API server is running."
        ) from exc


def get_health(
    base_url: str,
) -> dict[str, Any]:
    return request_json(
        base_url,
        "/health",
    )


def get_history(
    base_url: str,
    limit: int = 200,
) -> dict[str, Any]:
    return request_json(
        base_url,
        (
            "/api/v1/health-checks"
            f"?limit={limit}"
        ),
    )


def get_health_check(
    base_url: str,
    health_check_id: str,
) -> dict[str, Any]:
    return request_json(
        base_url,
        (
            "/api/v1/health-checks/"
            f"{health_check_id}"
        ),
    )


def create_health_check(
    base_url: str,
    payload: dict[str, Any],
) -> dict[str, Any]:
    return request_json(
        base_url,
        "/api/v1/health-checks",
        method="POST",
        payload=payload,
    )