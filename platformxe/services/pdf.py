# =============================================================================
# (c) 2026 Caldera Technologies Ltd.
# Proprietary and confidential.
# Unauthorized copying or distribution is prohibited.
# =============================================================================

"""PDF service — document generation."""

from __future__ import annotations
from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import PlatformXeClient


class PdfService:
    def __init__(self, client: PlatformXeClient):
        self._client = client

    def generate_offer_letter(self, **kwargs: Any) -> Dict[str, Any]:
        """Generate an offer letter PDF."""
        return self._client.post("/api/v1/pdf/offer-letter", json=kwargs)

    def generate_property_flyer(self, **kwargs: Any) -> Dict[str, Any]:
        """Generate a property flyer PDF."""
        return self._client.post("/api/v1/pdf/property-flyer", json=kwargs)

    def get_processor(self) -> Dict[str, Any]:
        """Get the PDF processor configuration."""
        return self._client.get("/api/v1/pdf/processor")

    def update_processor(self, enabled: Optional[bool] = None, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update the PDF processor configuration."""
        body: Dict[str, Any] = {}
        if enabled is not None:
            body["enabled"] = enabled
        if config is not None:
            body["config"] = config
        return self._client.put("/api/v1/pdf/processor", json=body)
