# =============================================================================
# (c) 2026 Caldera Technologies Ltd.
# Proprietary and confidential.
# Unauthorized copying or distribution is prohibited.
# =============================================================================

"""PlatformXe API client — synchronous and asynchronous."""

from __future__ import annotations
import mimetypes
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, TYPE_CHECKING
import httpx

from .exceptions import PlatformXeError, PlatformXeAPIError
from .services.permissions import PermissionsService
from .services.identity import IdentityService
from .services.messaging import MessagingService
from .services.webhooks import WebhooksService
from .services.templates import TemplatesService
from .services.storage import StorageService
from .services.documents import DocumentsService
from .services.workflows import WorkflowsService
from .services.domains import DomainsService
from .services.events import EventsService
from .services.threads import ThreadsService
from .services.exports import ExportsService
from .services.ocr import OcrService
from .services.pdf import PdfService
from .services.qr import QrService
from .services.usage import UsageService


def _parse_response(response: httpx.Response) -> Dict[str, Any]:
    """Parse an API response, raising on error."""
    content_type = response.headers.get("content-type", "")
    if "application/json" not in content_type:
        text = response.text[:200]
        if not response.is_success:
            raise PlatformXeAPIError(
                code=f"HTTP_{response.status_code}",
                message=text or response.reason_phrase,
                status_code=response.status_code,
            )
        raise PlatformXeError(f"Expected JSON but received {content_type}: {text}")

    data = response.json()

    if not data.get("success", False):
        error = data.get("error", {})
        raise PlatformXeAPIError(
            code=error.get("code", "UNKNOWN"),
            message=error.get("message", "Unknown error"),
            status_code=response.status_code,
        )

    return data.get("data", data)


def _build_file_tuple(path: Path) -> tuple:
    """Build an (filename, file_bytes, content_type) tuple for multipart upload."""
    content_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    return (path.name, path.read_bytes(), content_type)


class PlatformXeClient:
    """Synchronous client for the PlatformXe API.

    Usage:
        client = PlatformXeClient(api_key="pxk_live_...")
        result = client.permissions.check(admin_id="usr_123", path="chat/session", action="READ")
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://platformxe.com",
        timeout: float = 10.0,
        retries: int = 2,
        fail_open: bool = True,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries
        self.fail_open = fail_open
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={
                "x-api-key": self.api_key,
                "Accept": "application/json",
            },
            timeout=self.timeout,
        )

        # Service namespaces
        self.documents = DocumentsService(self)
        self.domains = DomainsService(self)
        self.events = EventsService(self)
        self.exports = ExportsService(self)
        self.identity = IdentityService(self)
        self.messaging = MessagingService(self)
        self.ocr = OcrService(self)
        self.pdf = PdfService(self)
        self.permissions = PermissionsService(self)
        self.qr = QrService(self)
        self.storage = StorageService(self)
        self.templates = TemplatesService(self)
        self.threads = ThreadsService(self)
        self.usage = UsageService(self)
        self.webhooks = WebhooksService(self)
        self.workflows = WorkflowsService(self)

    # ── Utility methods (not part of a service resource) ────────────────

    def send_telemetry(
        self,
        source_app: str,
        package_name: str,
        metrics: List[Dict[str, Any]],
        period_start: str,
        period_end: str,
        package_version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send SDK telemetry metrics."""
        return self.post("/api/v1/telemetry", json={
            "sourceApp": source_app,
            "packageName": package_name,
            "packageVersion": package_version,
            "metrics": metrics,
            "periodStart": period_start,
            "periodEnd": period_end,
        })

    def health_check(self) -> Dict[str, Any]:
        """Check platform health."""
        return self.get("/api/health")

    # ── HTTP internals ───────────────────────────────────────────────────

    def _request(self, method: str, path: str, **kwargs: Any) -> Dict[str, Any]:
        """Make an HTTP request with retry and error handling."""
        last_error: Optional[Exception] = None

        for attempt in range(self.retries + 1):
            try:
                response = self._client.request(method, path, **kwargs)
                return _parse_response(response)

            except PlatformXeAPIError:
                raise  # Don't retry API errors (4xx)
            except Exception as e:
                last_error = e
                if attempt < self.retries:
                    time.sleep(0.2 * (2 ** attempt))  # Exponential backoff

        if self.fail_open:
            return {"error": str(last_error), "_failed": True}
        raise PlatformXeError(f"Request failed after {self.retries + 1} attempts: {last_error}")

    def get(self, path: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return self._request("GET", path, params=params)

    def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request("POST", path, json=json or {})

    def put(self, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request("PUT", path, json=json or {})

    def patch(self, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request("PATCH", path, json=json or {})

    def delete(self, path: str) -> Dict[str, Any]:
        return self._request("DELETE", path)

    def upload(self, path: str, file_path: Path, *, fields: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Upload a single file via multipart form data."""
        files = {"file": _build_file_tuple(file_path)}
        data = fields or {}
        return self._request("POST", path, files=files, data=data)

    def upload_many(self, path: str, file_paths: Sequence[Path], *, fields: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Upload multiple files via multipart form data."""
        files = [("files", _build_file_tuple(p)) for p in file_paths]
        data = fields or {}
        return self._request("POST", path, files=files, data=data)

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> "PlatformXeClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()


class AsyncPlatformXeClient:
    """Asynchronous client for the PlatformXe API.

    Usage:
        async with AsyncPlatformXeClient(api_key="pxk_live_...") as client:
            result = await client.permissions.check(admin_id="usr_123", path="chat/session", action="READ")
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://platformxe.com",
        timeout: float = 10.0,
        retries: int = 2,
        fail_open: bool = True,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries
        self.fail_open = fail_open
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "x-api-key": self.api_key,
                "Accept": "application/json",
            },
            timeout=self.timeout,
        )

        # Async service namespaces
        from .services.async_services import (
            AsyncDocumentsService,
            AsyncDomainsService,
            AsyncEventsService,
            AsyncExportsService,
            AsyncIdentityService,
            AsyncMessagingService,
            AsyncOcrService,
            AsyncPdfService,
            AsyncPermissionsService,
            AsyncQrService,
            AsyncStorageService,
            AsyncTemplatesService,
            AsyncThreadsService,
            AsyncUsageService,
            AsyncWebhooksService,
            AsyncWorkflowsService,
        )
        self.documents = AsyncDocumentsService(self)
        self.domains = AsyncDomainsService(self)
        self.events = AsyncEventsService(self)
        self.exports = AsyncExportsService(self)
        self.identity = AsyncIdentityService(self)
        self.messaging = AsyncMessagingService(self)
        self.ocr = AsyncOcrService(self)
        self.pdf = AsyncPdfService(self)
        self.permissions = AsyncPermissionsService(self)
        self.qr = AsyncQrService(self)
        self.storage = AsyncStorageService(self)
        self.templates = AsyncTemplatesService(self)
        self.threads = AsyncThreadsService(self)
        self.usage = AsyncUsageService(self)
        self.webhooks = AsyncWebhooksService(self)
        self.workflows = AsyncWorkflowsService(self)

    # ── Utility methods (not part of a service resource) ────────────────

    async def send_telemetry(
        self,
        source_app: str,
        package_name: str,
        metrics: List[Dict[str, Any]],
        period_start: str,
        period_end: str,
        package_version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send SDK telemetry metrics."""
        return await self.post("/api/v1/telemetry", json={
            "sourceApp": source_app,
            "packageName": package_name,
            "packageVersion": package_version,
            "metrics": metrics,
            "periodStart": period_start,
            "periodEnd": period_end,
        })

    async def health_check(self) -> Dict[str, Any]:
        """Check platform health."""
        return await self.get("/api/health")

    # ── HTTP internals ───────────────────────────────────────────────────

    async def _request(self, method: str, path: str, **kwargs: Any) -> Dict[str, Any]:
        """Make an async HTTP request with retry and error handling."""
        import asyncio

        last_error: Optional[Exception] = None

        for attempt in range(self.retries + 1):
            try:
                response = await self._client.request(method, path, **kwargs)
                return _parse_response(response)

            except PlatformXeAPIError:
                raise
            except Exception as e:
                last_error = e
                if attempt < self.retries:
                    await asyncio.sleep(0.2 * (2 ** attempt))

        if self.fail_open:
            return {"error": str(last_error), "_failed": True}
        raise PlatformXeError(f"Request failed after {self.retries + 1} attempts: {last_error}")

    async def get(self, path: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        return await self._request("GET", path, params=params)

    async def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self._request("POST", path, json=json or {})

    async def put(self, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self._request("PUT", path, json=json or {})

    async def patch(self, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self._request("PATCH", path, json=json or {})

    async def delete(self, path: str) -> Dict[str, Any]:
        return await self._request("DELETE", path)

    async def upload(self, path: str, file_path: Path, *, fields: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Upload a single file via multipart form data."""
        files = {"file": _build_file_tuple(file_path)}
        data = fields or {}
        return await self._request("POST", path, files=files, data=data)

    async def upload_many(self, path: str, file_paths: Sequence[Path], *, fields: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Upload multiple files via multipart form data."""
        files = [("files", _build_file_tuple(p)) for p in file_paths]
        data = fields or {}
        return await self._request("POST", path, files=files, data=data)

    async def close(self) -> None:
        """Close the async HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncPlatformXeClient":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()
