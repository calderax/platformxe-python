# =============================================================================
# (c) 2026 Caldera Technologies Ltd.
# Proprietary and confidential.
# Unauthorized copying or distribution is prohibited.
# =============================================================================

"""Webhooks service — CRUD, rotate, test."""

from __future__ import annotations
from typing import Any, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import PlatformXeClient


class WebhooksService:
    def __init__(self, client: PlatformXeClient):
        self._client = client

    def list(self) -> Dict[str, Any]:
        return self._client.get("/api/v1/webhooks")

    def create(self, name: str, url: str, events: List[str]) -> Dict[str, Any]:
        return self._client.post("/api/v1/webhooks", json={"name": name, "url": url, "events": events})

    def get(self, webhook_id: str) -> Dict[str, Any]:
        return self._client.get(f"/api/v1/webhooks/{webhook_id}")

    def update(self, webhook_id: str, **kwargs: Any) -> Dict[str, Any]:
        return self._client.patch(f"/api/v1/webhooks/{webhook_id}", json=kwargs)

    def delete(self, webhook_id: str) -> Dict[str, Any]:
        return self._client.delete(f"/api/v1/webhooks/{webhook_id}")

    def rotate_secret(self, webhook_id: str) -> Dict[str, Any]:
        return self._client.post(f"/api/v1/webhooks/{webhook_id}/rotate")

    def test(self, webhook_id: str) -> Dict[str, Any]:
        return self._client.post(f"/api/v1/webhooks/{webhook_id}/test")
