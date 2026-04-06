# =============================================================================
# (c) 2026 Caldera Technologies Ltd.
# Proprietary and confidential.
# Unauthorized copying or distribution is prohibited.
# =============================================================================

"""Messaging service — email, SMS, WhatsApp."""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import PlatformXeClient


class MessagingService:
    def __init__(self, client: PlatformXeClient):
        self._client = client

    def send_email(self, to: Union[str, List[str]], subject: str, html: str, reply_to: Optional[str] = None, attachments: Optional[List[Dict]] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "to": to if isinstance(to, list) else [to],
            "subject": subject,
            "html": html,
        }
        if reply_to:
            body["replyTo"] = reply_to
        if attachments:
            body["attachments"] = attachments
        return self._client.post("/api/v1/messaging/email/send", json=body)

    def send_sms(self, to: str, message: str, region_code: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"to": to, "message": message}
        if region_code:
            body["regionCode"] = region_code
        return self._client.post("/api/v1/messaging/sms", json=body)

    def send_whatsapp(self, to: str, template_id: Optional[str] = None, message: Optional[str] = None, phone_number_id: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"to": to}
        if template_id:
            body["templateId"] = template_id
        if message:
            body["message"] = message
        if phone_number_id:
            body["phoneNumberId"] = phone_number_id
        return self._client.post("/api/v1/messaging/whatsapp", json=body)

    def email_health(self) -> Dict[str, Any]:
        return self._client.get("/api/v1/messaging/email/health")

    def sms_health(self) -> Dict[str, Any]:
        return self._client.get("/api/v1/messaging/sms/health")

    def queue_stats(self) -> Dict[str, Any]:
        return self._client.get("/api/v1/messaging/queue/stats")

    def process_queue(self) -> Dict[str, Any]:
        return self._client.post("/api/v1/messaging/queue/process")
