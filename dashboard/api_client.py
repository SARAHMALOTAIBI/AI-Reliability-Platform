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

from urllib.parse import urlencode
import mimetypes
import uuid


def request_form(
    base_url: str,
    path: str,
    data: dict[str, str],
    timeout: int = 180,
) -> dict[str, Any]:
    url = (
        f"{normalize_base_url(base_url)}"
        f"{path}"
    )

    body = urlencode(data).encode("utf-8")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    request = Request(
        url=url,
        data=body,
        headers=headers,
        method="POST",
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}

    except HTTPError as exc:
        try:
            detail = exc.read().decode("utf-8")
        except Exception:
            detail = str(exc)
        raise APIClientError(
            f"API returned HTTP {exc.code}: {detail}"
        ) from exc

    except URLError as exc:
        raise APIClientError(
            "Could not connect to FastAPI. "
            "Make sure the API server is running."
        ) from exc


def request_multipart(
    base_url: str,
    path: str,
    fields: dict[str, str],
    file_field_name: str,
    file_bytes: bytes,
    filename: str,
    timeout: int = 180,
) -> dict[str, Any]:
    url = (
        f"{normalize_base_url(base_url)}"
        f"{path}"
    )

    boundary = uuid.uuid4().hex
    content_type = (
        mimetypes.guess_type(filename)[0]
        or "application/octet-stream"
    )

    parts = []

    for key, value in fields.items():
        parts.append(
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{key}"\r\n\r\n'
            f"{value}\r\n".encode("utf-8")
        )

    parts.append(
        (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{file_field_name}"; '
            f'filename="{filename}"\r\n'
            f"Content-Type: {content_type}\r\n\r\n"
        ).encode("utf-8")
        + file_bytes
        + b"\r\n"
    )

    parts.append(f"--{boundary}--\r\n".encode("utf-8"))

    body = b"".join(parts)

    headers = {
        "Accept": "application/json",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }

    request = Request(
        url=url,
        data=body,
        headers=headers,
        method="POST",
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}

    except HTTPError as exc:
        try:
            detail = exc.read().decode("utf-8")
        except Exception:
            detail = str(exc)
        raise APIClientError(
            f"API returned HTTP {exc.code}: {detail}"
        ) from exc

    except URLError as exc:
        raise APIClientError(
            "Could not connect to FastAPI. "
            "Make sure the API server is running."
        ) from exc


def upload_knowledge_base_document(
    base_url: str,
    project_id: str,
    file_bytes: bytes,
    filename: str,
) -> dict[str, Any]:
    return request_multipart(
        base_url,
        "/api/v1/knowledge-base/upload",
        fields={"project_id": project_id},
        file_field_name="file",
        file_bytes=file_bytes,
        filename=filename,
    )


def verify_knowledge_base_answer(
    base_url: str,
    project_id: str,
    question: str,
) -> dict[str, Any]:
    return request_form(
        base_url,
        "/api/v1/knowledge-base/verify",
        data={
            "project_id": project_id,
            "question": question,
        },
    )
