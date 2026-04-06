# =============================================================================
# (c) 2026 Caldera Technologies Ltd.
# Proprietary and confidential.
# Unauthorized copying or distribution is prohibited.
# =============================================================================

"""PlatformXe API client."""

from __future__ import annotations
import time
from typing import Any, Optional, Dict
import httpx

from .exceptions import PlatformXeError, PlatformXeAPIError
from .services.permissions import PermissionsService
from .services.identity import IdentityService
from .services.messaging import MessagingService
from .services.webhooks import WebhooksService
from .services.templates import TemplatesService
from .services.storage import StorageService
from .services.workflows import WorkflowsService
from .services.domains import DomainsService
from .services.subscriptions import EventSubscriptionsService
from .services.misc import MiscService


class PlatformXeClient:
    """Client for the PlatformXe API.

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
        self.permissions = PermissionsService(self)
        self.identity = IdentityService(self)
        self.messaging = MessagingService(self)
        self.webhooks = WebhooksService(self)
        self.templates = TemplatesService(self)
        self.storage = StorageService(self)
        self.workflows = WorkflowsService(self)
        self.domains = DomainsService(self)
        self.subscriptions = EventSubscriptionsService(self)
        self.misc = MiscService(self)

    def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        """Make an HTTP request with retry and error handling."""
        last_error: Optional[Exception] = None

        for attempt in range(self.retries + 1):
            try:
                response = self._client.request(method, path, **kwargs)
                data = response.json()

                if not data.get("success", False):
                    error = data.get("error", {})
                    raise PlatformXeAPIError(
                        code=error.get("code", "UNKNOWN"),
                        message=error.get("message", "Unknown error"),
                        status_code=response.status_code,
                    )

                return data.get("data", data)

            except PlatformXeAPIError:
                raise  # Don't retry API errors (4xx)
            except Exception as e:
                last_error = e
                if attempt < self.retries:
                    time.sleep(0.2 * (2 ** attempt))  # Exponential backoff

        if self.fail_open:
            return {"error": str(last_error), "_failed": True}
        raise PlatformXeError(f"Request failed after {self.retries + 1} attempts: {last_error}")

    def get(self, path: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("GET", path, params=params)

    def post(self, path: str, json: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("POST", path, json=json or {})

    def put(self, path: str, json: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("PUT", path, json=json or {})

    def patch(self, path: str, json: Optional[Dict] = None) -> Dict[str, Any]:
        return self._request("PATCH", path, json=json or {})

    def delete(self, path: str) -> Dict[str, Any]:
        return self._request("DELETE", path)

    def close(self):
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
