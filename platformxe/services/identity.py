# =============================================================================
# (c) 2026 Caldera Technologies Ltd.
# Proprietary and confidential.
# Unauthorized copying or distribution is prohibited.
# =============================================================================

"""Identity service — resolve, verify, lookup."""

from __future__ import annotations
from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import PlatformXeClient


class IdentityService:
    def __init__(self, client: PlatformXeClient):
        self._client = client

    def resolve(self, type: str, value: str, resolve_linked: bool = True, consent_reference: str = "", consent_obtained_at: str = "") -> Dict[str, Any]:
        return self._client.post("/api/v1/identity/resolve", json={
            "type": type, "value": value, "resolveLinked": resolve_linked,
            "consent": {"granted": True, "reference": consent_reference, "obtainedAt": consent_obtained_at},
        })

    def verify(self, type: str, value: str, first_name: str, last_name: str, date_of_birth: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "type": type, "value": value,
            "matchAgainst": {"firstName": first_name, "lastName": last_name},
        }
        if date_of_birth:
            body["matchAgainst"]["dateOfBirth"] = date_of_birth
        return self._client.post("/api/v1/identity/verify", json=body)

    def lookup(self, type: str, value: str) -> Dict[str, Any]:
        return self._client.get("/api/v1/identity/lookup", params={"type": type, "value": value})

    def providers(self) -> Dict[str, Any]:
        return self._client.get("/api/v1/identity/providers")
