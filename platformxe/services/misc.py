# =============================================================================
# (c) 2026 Caldera Technologies Ltd.
# Proprietary and confidential.
# Unauthorized copying or distribution is prohibited.
# =============================================================================

"""Misc service — exports, usage, QR, OCR, telemetry, health."""

from __future__ import annotations
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import PlatformXeClient


class MiscService:
    def __init__(self, client: PlatformXeClient):
        self._client = client

    def create_export(self, **kwargs: Any) -> Dict[str, Any]:
        return self._client.post("/api/v1/exports", json=kwargs)

    def get_export(self, export_id: str) -> Dict[str, Any]:
        return self._client.get(f"/api/v1/exports/{export_id}")

    def usage_summary(self, month: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, str] = {"month": month} if month else {}
        return self._client.get("/api/v1/usage/summary", params=params)

    def verify_identity_document(self, document_url: Optional[str] = None, document_base64: Optional[str] = None, profile_name: Optional[Dict[str, str]] = None, expected_type: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {}
        if document_url:
            body["documentUrl"] = document_url
        if document_base64:
            body["documentBase64"] = document_base64
        if profile_name:
            body["profileName"] = profile_name
        if expected_type:
            body["expectedDocumentType"] = expected_type
        return self._client.post("/api/v1/ocr/verify-identity", json=body)

    def generate_qr(self, data: str, size: Optional[int] = None, format: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"data": data}
        if size:
            body["size"] = size
        if format:
            body["format"] = format
        return self._client.post("/api/v1/qr", json=body)

    def send_telemetry(self, metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
        return self._client.post("/api/v1/telemetry", json={"metrics": metrics})

    def health_check(self) -> Dict[str, Any]:
        return self._client.get("/api/health")
