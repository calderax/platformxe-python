# =============================================================================
# (c) 2026 Caldera Technologies Ltd.
# Proprietary and confidential.
# Unauthorized copying or distribution is prohibited.
# =============================================================================

"""Events service — ingest, log, subscriptions, replay."""

from __future__ import annotations
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import PlatformXeClient


class EventsService:
    def __init__(self, client: PlatformXeClient):
        self._client = client

    def ingest(self, event_type: str, entity_type: str, entity_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._client.post("/api/v1/events", json={
            "eventType": event_type, "entityType": entity_type,
            "entityId": entity_id, "payload": payload,
        })

    def log(self, event_type: Optional[str] = None, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, str] = {}
        if event_type:
            params["eventType"] = event_type
        if page:
            params["page"] = str(page)
        if limit:
            params["limit"] = str(limit)
        return self._client.get("/api/v1/event-log", params=params)

    def list_subscriptions(self) -> Dict[str, Any]:
        return self._client.get("/api/v1/event-subscriptions")

    def create_subscription(self, event_types: List[str], webhook_url: str, secret: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"eventTypes": event_types, "webhookUrl": webhook_url}
        if secret:
            body["secret"] = secret
        return self._client.post("/api/v1/event-subscriptions", json=body)

    def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        return self._client.get(f"/api/v1/event-subscriptions/{subscription_id}")

    def update_subscription(self, subscription_id: str, **kwargs: Any) -> Dict[str, Any]:
        return self._client.patch(f"/api/v1/event-subscriptions/{subscription_id}", json=kwargs)

    def delete_subscription(self, subscription_id: str) -> Dict[str, Any]:
        return self._client.delete(f"/api/v1/event-subscriptions/{subscription_id}")

    def replay(self, subscription_id: str, from_date: str, to_date: str) -> Dict[str, Any]:
        return self._client.post(f"/api/v1/event-subscriptions/{subscription_id}/replay", json={"from": from_date, "to": to_date})
