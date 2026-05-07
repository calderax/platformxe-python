# =============================================================================
# (c) 2026 Caldera Technologies Ltd.
# Proprietary and confidential.
# Unauthorized copying or distribution is prohibited.
# =============================================================================

"""Documents service — fixed documents, folders, and deletion overrides."""

from __future__ import annotations
from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import PlatformXeClient


class DocumentsService:
    def __init__(self, client: PlatformXeClient):
        self._client = client

    def list_documents(self, folder_id: Optional[str] = None, page: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, str] = {}
        if folder_id:
            params["folderId"] = folder_id
        if page:
            params["page"] = str(page)
        return self._client.get("/api/v1/storage/fixed/documents", params=params)

    def get_document(self, document_id: str) -> Dict[str, Any]:
        return self._client.get(f"/api/v1/storage/fixed/documents/{document_id}")

    def create_document(self, **kwargs: Any) -> Dict[str, Any]:
        """Create a new fixed document."""
        return self._client.post("/api/v1/storage/fixed/documents", json=kwargs)

    def update_document(self, document_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Update a fixed document."""
        return self._client.patch(f"/api/v1/storage/fixed/documents/{document_id}", json=kwargs)

    def delete_document(self, document_id: str) -> Dict[str, Any]:
        """Delete a fixed document (may require override if protected)."""
        return self._client.delete(f"/api/v1/storage/fixed/documents/{document_id}")

    def list_folders(self) -> Dict[str, Any]:
        return self._client.get("/api/v1/storage/fixed/folders")

    def get_folder(self, folder_id: str) -> Dict[str, Any]:
        return self._client.get(f"/api/v1/storage/fixed/folders/{folder_id}")

    def create_folder(
        self,
        name: str,
        parent_id: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a folder for fixed documents."""
        body: Dict[str, Any] = {"name": name}
        if parent_id is not None:
            body["parentId"] = parent_id
        if description is not None:
            body["description"] = description
        return self._client.post("/api/v1/storage/fixed/folders", json=body)

    def request_override(self, **kwargs: Any) -> Dict[str, Any]:
        """Request a deletion override for a protected document."""
        return self._client.post("/api/v1/storage/fixed/overrides", json=kwargs)

    def process_override(self, override_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Approve or reject a deletion override request."""
        return self._client.patch(f"/api/v1/storage/fixed/overrides/{override_id}", json=kwargs)
