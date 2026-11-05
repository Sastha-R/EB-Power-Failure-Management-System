import logging
import time
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger: logging.Logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next
    ) -> Response:

        start_time: float = time.perf_counter()

        response: Response = await call_next(request)

        process_time: float = time.perf_counter() - start_time

        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.4f} seconds"
        )

        return response
