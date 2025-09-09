import json
import logging
import time
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("structured_logger")
if not logger.hasHandlers():
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)

REQUEST_ID_HEADER = "X-Request-ID"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds") + "Z"


def _level_by_status(status_code: int) -> str:
    if status_code < 300:
        return "info"

    if 300 <= status_code < 400:
        return "warning"

    return "error"


class JsonLoggingMiddleware(BaseHTTPMiddleware):
    """
    Логгер с полями:
    ts, level, method, path, status, latency_ms, request_id
    """

    async def dispatch(self, request: Request, call_next):
        start_ts = time.time()

        request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid4())

        try:
            response: Response = await call_next(request)
            status_code = getattr(response, "status_code", 500)
        except Exception as exc:
            latency_ms = round((time.time() - start_ts) * 1000, 3)
            log_record = {
                "ts": _now_iso(),
                "level": "error",
                "method": request.method,
                "path": request.url.path,
                "status": 500,
                "latency_ms": latency_ms,
                "request_id": request_id,
                "msg": str(exc),
            }
            logger.error(json.dumps(log_record, ensure_ascii=False))
            raise
        else:
            latency_ms = round((time.time() - start_ts) * 1000, 3)
            level = _level_by_status(status_code)
            log_record = {
                "ts": _now_iso(),
                "level": level,
                "method": request.method,
                "path": request.url.path,
                "status": status_code,
                "latency_ms": latency_ms,
                "request_id": request_id,
                "msg": f"{request.method} {request.url.path} -> {status_code}",
            }

            log_level = {
                "info": logging.INFO,
                "warning": logging.WARNING,
                "error": logging.ERROR,
            }[level]

            match log_level:
                case logging.INFO:
                    logger.log(
                        log_level,
                        "\033[32m"
                        + json.dumps(log_record, ensure_ascii=False)
                        + "\033[0m",
                    )
                case logging.WARNING:
                    logger.log(
                        log_level,
                        "\033[33m"
                        + json.dumps(log_record, ensure_ascii=False)
                        + "\033[0m",
                    )
                case logging.ERROR:
                    logger.log(
                        log_level,
                        "\033[31m"
                        + json.dumps(log_record, ensure_ascii=False)
                        + "\033[0m",
                    )
                case _:
                    logger.log(log_level, json.dumps(log_record, ensure_ascii=False))

            response.headers[REQUEST_ID_HEADER] = request_id
            return response
