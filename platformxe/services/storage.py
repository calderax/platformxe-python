# =============================================================================
# (c) 2026 Caldera Technologies Ltd.
# Proprietary and confidential.
# Unauthorized copying or distribution is prohibited.
# =============================================================================

"""Storage service — media files and fixed documents."""

from __future__ import annotations
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import PlatformXeClient


class StorageService:
    def __init__(self, client: PlatformXeClient):
        self._client = client

    # Media

    def sign_upload(self, filename: str, content_type: str) -> Dict[str, Any]:
        return self._client.post("/api/v1/storage/media/sign-upload", json={"filename": filename, "contentType": content_type})

    def register_url(self, url: str, filename: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"url": url}
        if filename:
            body["filename"] = filename
        return self._client.post("/api/v1/storage/media/register", json=body)

    def list_files(self, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, str] = {}
        if page:
            params["page"] = str(page)
        if limit:
            params["limit"] = str(limit)
        return self._client.get("/api/v1/storage/media/files", params=params)

    def get_file(self, file_id: str) -> Dict[str, Any]:
        return self._client.get(f"/api/v1/storage/media/files/{file_id}")

    def delete_file(self, file_id: str) -> Dict[str, Any]:
        return self._client.delete(f"/api/v1/storage/media/files/{file_id}")

    def reorder_files(self, file_ids: List[str]) -> Dict[str, Any]:
        return self._client.post("/api/v1/storage/media/files/reorder", json={"fileIds": file_ids})

    # Fixed / Documents

    def list_documents(self, folder_id: Optional[str] = None, page: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, str] = {}
        if folder_id:
            params["folderId"] = folder_id
        if page:
            params["page"] = str(page)
        return self._client.get("/api/v1/storage/fixed/documents", params=params)

    def get_document(self, document_id: str) -> Dict[str, Any]:
        return self._client.get(f"/api/v1/storage/fixed/documents/{document_id}")

    def list_folders(self) -> Dict[str, Any]:
        return self._client.get("/api/v1/storage/fixed/folders")

    def get_folder(self, folder_id: str) -> Dict[str, Any]:
        return self._client.get(f"/api/v1/storage/fixed/folders/{folder_id}")
