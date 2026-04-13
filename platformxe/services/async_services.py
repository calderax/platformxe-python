# =============================================================================
# (c) 2026 Caldera Technologies Ltd.
# Proprietary and confidential.
# Unauthorized copying or distribution is prohibited.
# =============================================================================

"""Async service implementations for AsyncPlatformXeClient."""

from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import AsyncPlatformXeClient


class AsyncPermissionsService:
    """Async permissions service — RBAC, ABAC, ReBAC, Federation."""

    def __init__(self, client: AsyncPlatformXeClient):
        self._client = client

    async def check(self, admin_id: str, path: str, action: str, resource: Optional[Dict] = None, context: Optional[Dict] = None) -> Dict[str, Any]:
        return await self._client.post("/api/v1/permissions/check", json={
            "adminId": admin_id, "path": path, "action": action,
            "resource": resource, "context": context,
        })

    async def check_batch(self, checks: List[Dict]) -> Dict[str, Any]:
        return await self._client.post("/api/v1/permissions/check-batch", json={"checks": checks})

    async def resolve(self, admin_id: str) -> Dict[str, Any]:
        return await self._client.get(f"/api/v1/permissions/resolve/{admin_id}")

    async def list_roles(self) -> Dict[str, Any]:
        return await self._client.get("/api/v1/permissions/roles")

    async def create_role(self, name: str, description: Optional[str] = None, model: str = "SIMPLE") -> Dict[str, Any]:
        return await self._client.post("/api/v1/permissions/roles", json={
            "name": name, "description": description, "model": model,
        })

    async def get_role(self, role_id: str) -> Dict[str, Any]:
        return await self._client.get(f"/api/v1/permissions/roles/{role_id}")

    async def update_role(self, role_id: str, name: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {}
        if name is not None:
            body["name"] = name
        if description is not None:
            body["description"] = description
        return await self._client.patch(f"/api/v1/permissions/roles/{role_id}", json=body)

    async def delete_role(self, role_id: str) -> Dict[str, Any]:
        return await self._client.delete(f"/api/v1/permissions/roles/{role_id}")

    async def get_role_capabilities(self, role_id: str) -> Dict[str, Any]:
        return await self._client.get(f"/api/v1/permissions/roles/{role_id}/capabilities")

    async def set_role_capabilities(self, role_id: str, capabilities: List[str]) -> Dict[str, Any]:
        return await self._client.put(f"/api/v1/permissions/roles/{role_id}/capabilities", json={"capabilities": capabilities})

    async def get_role_module_permissions(self, role_id: str) -> Dict[str, Any]:
        return await self._client.get(f"/api/v1/permissions/roles/{role_id}/modules")

    async def set_role_module_permissions(self, role_id: str, modules: List[Dict]) -> Dict[str, Any]:
        return await self._client.put(f"/api/v1/permissions/roles/{role_id}/modules", json={"modules": modules})

    async def list_overrides(self, admin_id: str) -> Dict[str, Any]:
        return await self._client.get(f"/api/v1/permissions/overrides/{admin_id}")

    async def create_override(self, admin_id: str, path: str, action: str, effect: str, reason: str, expires_at: Optional[str] = None) -> Dict[str, Any]:
        return await self._client.post("/api/v1/permissions/overrides", json={
            "adminId": admin_id, "path": path, "action": action,
            "effect": effect, "reason": reason, "expiresAt": expires_at,
        })

    async def delete_override(self, override_id: str) -> Dict[str, Any]:
        return await self._client.delete(f"/api/v1/permissions/overrides/remove/{override_id}")

    async def list_policies(self) -> Dict[str, Any]:
        return await self._client.get("/api/v1/permissions/policies")

    async def create_policy(self, path: str, action: str, condition: Dict, effect: str, priority: int = 0, description: Optional[str] = None) -> Dict[str, Any]:
        return await self._client.post("/api/v1/permissions/policies", json={
            "path": path, "action": action, "condition": condition,
            "effect": effect, "priority": priority, "description": description,
        })

    async def update_policy(self, policy_id: str, **kwargs: Any) -> Dict[str, Any]:
        return await self._client.patch(f"/api/v1/permissions/policies/{policy_id}", json=kwargs)

    async def delete_policy(self, policy_id: str) -> Dict[str, Any]:
        return await self._client.delete(f"/api/v1/permissions/policies/{policy_id}")

    async def list_relationships(self, **params: Any) -> Dict[str, Any]:
        return await self._client.get("/api/v1/permissions/relationships", params=params)

    async def update_relationships(self, operations: List[Dict]) -> Dict[str, Any]:
        return await self._client.post("/api/v1/permissions/relationships", json=operations)

    async def register_module(self, id: str, app: str, name: str, paths: List[str], description: Optional[str] = None) -> Dict[str, Any]:
        return await self._client.post("/api/v1/permissions/modules", json={
            "id": id, "app": app, "name": name, "paths": paths, "description": description,
        })

    async def list_modules(self) -> Dict[str, Any]:
        return await self._client.get("/api/v1/permissions/modules")

    async def get_audit_logs(self, admin_id: Optional[str] = None, path: Optional[str] = None, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, str] = {}
        if admin_id:
            params["adminId"] = admin_id
        if path:
            params["path"] = path
        if page:
            params["page"] = str(page)
        if limit:
            params["limit"] = str(limit)
        return await self._client.get("/api/v1/permissions/audit", params=params)

    async def list_change_logs(self, entity_type: Optional[str] = None, entity_id: Optional[str] = None, changed_by: Optional[str] = None, limit: Optional[int] = None, offset: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, str] = {}
        if entity_type:
            params["entityType"] = entity_type
        if entity_id:
            params["entityId"] = entity_id
        if changed_by:
            params["changedBy"] = changed_by
        if limit:
            params["limit"] = str(limit)
        if offset:
            params["offset"] = str(offset)
        return await self._client.get("/api/v1/permissions/audit/changes", params=params)

    async def export_audit(self, from_date: Optional[str] = None, to_date: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, str] = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        return await self._client.get("/api/v1/permissions/audit/export", params=params)

    async def shadow_check(self, admin_id: str, path: str, action: str, local_decision: bool, context: Optional[Dict] = None) -> Dict[str, Any]:
        return await self._client.post("/api/v1/permissions/shadow-check", json={
            "adminId": admin_id, "path": path, "action": action,
            "localDecision": local_decision, "context": context,
        })

    # Federation

    async def create_federation_group(self, name: str) -> Dict[str, Any]:
        return await self._client.post("/api/v1/permissions/federation/groups", json={"name": name})

    async def list_federation_groups(self) -> Dict[str, Any]:
        return await self._client.get("/api/v1/permissions/federation/groups")

    async def get_federation_group(self, group_id: str) -> Dict[str, Any]:
        return await self._client.get(f"/api/v1/permissions/federation/groups/{group_id}")

    async def delete_federation_group(self, group_id: str) -> Dict[str, Any]:
        return await self._client.delete(f"/api/v1/permissions/federation/groups/{group_id}")

    async def add_federation_member(self, group_id: str, organization_id: str, prefix: str) -> Dict[str, Any]:
        return await self._client.post(f"/api/v1/permissions/federation/groups/{group_id}/members", json={
            "organizationId": organization_id, "prefix": prefix,
        })

    async def remove_federation_member(self, group_id: str, organization_id: str) -> Dict[str, Any]:
        return await self._client.delete(f"/api/v1/permissions/federation/groups/{group_id}/members?organizationId={organization_id}")

    async def pull_federation_modules(self, group_id: str, target_org_id: Optional[str] = None) -> Dict[str, Any]:
        return await self._client.post(f"/api/v1/permissions/federation/groups/{group_id}/pull", json={"targetOrgId": target_org_id})

    async def push_federation_permissions(self, group_id: str, admin_ids: List[str], target_org_id: Optional[str] = None) -> Dict[str, Any]:
        return await self._client.post(f"/api/v1/permissions/federation/groups/{group_id}/push", json={
            "adminIds": admin_ids, "targetOrgId": target_org_id,
        })

    async def get_federation_status(self, group_id: str) -> Dict[str, Any]:
        return await self._client.get(f"/api/v1/permissions/federation/groups/{group_id}/status")


class AsyncIdentityService:
    """Async identity service — resolve, verify, lookup."""

    def __init__(self, client: AsyncPlatformXeClient):
        self._client = client

    async def resolve(self, type: str, value: str, resolve_linked: bool = True, consent_reference: str = "", consent_obtained_at: str = "") -> Dict[str, Any]:
        return await self._client.post("/api/v1/identity/resolve", json={
            "type": type, "value": value, "resolveLinked": resolve_linked,
            "consent": {"granted": True, "reference": consent_reference, "obtainedAt": consent_obtained_at},
        })

    async def verify(self, type: str, value: str, first_name: str, last_name: str, date_of_birth: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "type": type, "value": value,
            "matchAgainst": {"firstName": first_name, "lastName": last_name},
        }
        if date_of_birth:
            body["matchAgainst"]["dateOfBirth"] = date_of_birth
        return await self._client.post("/api/v1/identity/verify", json=body)

    async def lookup(self, type: str, value: str) -> Dict[str, Any]:
        return await self._client.get("/api/v1/identity/lookup", params={"type": type, "value": value})

    async def providers(self) -> Dict[str, Any]:
        return await self._client.get("/api/v1/identity/providers")

    async def get_processor(self) -> Dict[str, Any]:
        """Get the identity processor configuration."""
        return await self._client.get("/api/v1/identity/processor")

    async def update_processor(self, enabled: Optional[bool] = None, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update the identity processor configuration."""
        body: Dict[str, Any] = {}
        if enabled is not None:
            body["enabled"] = enabled
        if config is not None:
            body["config"] = config
        return await self._client.put("/api/v1/identity/processor", json=body)


class AsyncMessagingService:
    """Async messaging service — email, SMS, WhatsApp."""

    def __init__(self, client: AsyncPlatformXeClient):
        self._client = client

    async def send_email(self, to: Union[str, List[str]], subject: str, html: str, reply_to: Optional[str] = None, attachments: Optional[List[Dict]] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "to": to if isinstance(to, list) else [to],
            "subject": subject,
            "html": html,
        }
        if reply_to:
            body["replyTo"] = reply_to
        if attachments:
            body["attachments"] = attachments
        return await self._client.post("/api/v1/messaging/email/send", json=body)

    async def send_sms(self, to: str, message: str, region_code: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"to": to, "message": message}
        if region_code:
            body["regionCode"] = region_code
        return await self._client.post("/api/v1/messaging/sms", json=body)

    async def send_whatsapp(self, to: str, template_id: Optional[str] = None, message: Optional[str] = None, phone_number_id: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"to": to}
        if template_id:
            body["templateId"] = template_id
        if message:
            body["message"] = message
        if phone_number_id:
            body["phoneNumberId"] = phone_number_id
        return await self._client.post("/api/v1/messaging/whatsapp", json=body)

    async def email_health(self) -> Dict[str, Any]:
        return await self._client.get("/api/v1/messaging/email/health")

    async def sms_health(self) -> Dict[str, Any]:
        return await self._client.get("/api/v1/messaging/sms/health")

    async def queue_stats(self) -> Dict[str, Any]:
        return await self._client.get("/api/v1/messaging/queue/stats")

    async def process_queue(self) -> Dict[str, Any]:
        return await self._client.post("/api/v1/messaging/queue/process")

    async def get_processor(self) -> Dict[str, Any]:
        """Get the messaging processor configuration."""
        return await self._client.get("/api/v1/messaging/processor")

    async def update_processor(self, enabled: Optional[bool] = None, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update the messaging processor configuration."""
        body: Dict[str, Any] = {}
        if enabled is not None:
            body["enabled"] = enabled
        if config is not None:
            body["config"] = config
        return await self._client.put("/api/v1/messaging/processor", json=body)


class AsyncWebhooksService:
    """Async webhooks service — CRUD, rotate, test."""

    def __init__(self, client: AsyncPlatformXeClient):
        self._client = client

    async def list(self) -> Dict[str, Any]:
        return await self._client.get("/api/v1/webhooks")

    async def create(self, name: str, url: str, events: List[str]) -> Dict[str, Any]:
        return await self._client.post("/api/v1/webhooks", json={"name": name, "url": url, "events": events})

    async def get(self, webhook_id: str) -> Dict[str, Any]:
        return await self._client.get(f"/api/v1/webhooks/{webhook_id}")

    async def update(self, webhook_id: str, **kwargs: Any) -> Dict[str, Any]:
        return await self._client.patch(f"/api/v1/webhooks/{webhook_id}", json=kwargs)

    async def delete(self, webhook_id: str) -> Dict[str, Any]:
        return await self._client.delete(f"/api/v1/webhooks/{webhook_id}")

    async def rotate_secret(self, webhook_id: str) -> Dict[str, Any]:
        return await self._client.post(f"/api/v1/webhooks/{webhook_id}/rotate")

    async def test(self, webhook_id: str) -> Dict[str, Any]:
        return await self._client.post(f"/api/v1/webhooks/{webhook_id}/test")


class AsyncTemplatesService:
    """Async templates service — CRUD, render, send."""

    def __init__(self, client: AsyncPlatformXeClient):
        self._client = client

    async def list(self) -> Dict[str, Any]:
        return await self._client.get("/api/v1/templates")

    async def create(self, name: str, subject: str, html: str, **kwargs: Any) -> Dict[str, Any]:
        return await self._client.post("/api/v1/templates", json={"name": name, "subject": subject, "html": html, **kwargs})

    async def get(self, template_id: str) -> Dict[str, Any]:
        return await self._client.get(f"/api/v1/templates/{template_id}")

    async def update(self, template_id: str, **kwargs: Any) -> Dict[str, Any]:
        return await self._client.patch(f"/api/v1/templates/{template_id}", json=kwargs)

    async def delete(self, template_id: str) -> Dict[str, Any]:
        return await self._client.delete(f"/api/v1/templates/{template_id}")

    async def render(self, template_id: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        return await self._client.post(f"/api/v1/templates/{template_id}/render", json={"variables": variables})

    async def send(self, template_id: str, to: Union[str, List[str]], variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self._client.post(f"/api/v1/templates/{template_id}/send", json={"to": to, "variables": variables or {}})


class AsyncStorageService:
    """Async storage service — media file uploads and management."""

    def __init__(self, client: AsyncPlatformXeClient):
        self._client = client

    # Media — direct uploads

    async def upload_file(
        self,
        file_path: Union[str, Path],
        *,
        module: Optional[str] = None,
        entity_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Upload a single file via multipart form data."""
        path = Path(file_path)
        fields: Dict[str, Any] = {}
        if module:
            fields["module"] = module
        if entity_id:
            fields["entityId"] = entity_id
        return await self._client.upload("/api/v1/storage/media/upload", path, fields=fields)

    async def batch_upload(
        self,
        file_paths: Sequence[Union[str, Path]],
        *,
        module: Optional[str] = None,
        entity_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Upload multiple files in a single request via multipart form data."""
        paths = [Path(p) for p in file_paths]
        fields: Dict[str, Any] = {}
        if module:
            fields["module"] = module
        if entity_id:
            fields["entityId"] = entity_id
        return await self._client.upload_many("/api/v1/storage/media/upload/batch", paths, fields=fields)

    # Media — signed upload flow

    async def sign_upload(self, filename: str, content_type: str) -> Dict[str, Any]:
        return await self._client.post("/api/v1/storage/media/sign-upload", json={"filename": filename, "contentType": content_type})

    async def register_url(self, url: str, filename: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"url": url}
        if filename:
            body["filename"] = filename
        return await self._client.post("/api/v1/storage/media/register", json=body)

    async def list_files(self, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, str] = {}
        if page:
            params["page"] = str(page)
        if limit:
            params["limit"] = str(limit)
        return await self._client.get("/api/v1/storage/media/files", params=params)

    async def get_file(self, file_id: str) -> Dict[str, Any]:
        return await self._client.get(f"/api/v1/storage/media/files/{file_id}")

    async def delete_file(self, file_id: str) -> Dict[str, Any]:
        return await self._client.delete(f"/api/v1/storage/media/files/{file_id}")

    async def reorder_files(self, file_ids: List[str]) -> Dict[str, Any]:
        return await self._client.post("/api/v1/storage/media/files/reorder", json={"fileIds": file_ids})

    async def get_processor(self) -> Dict[str, Any]:
        """Get the storage processor configuration."""
        return await self._client.get("/api/v1/storage/processor")

    async def update_processor(self, enabled: Optional[bool] = None, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update the storage processor configuration."""
        body: Dict[str, Any] = {}
        if enabled is not None:
            body["enabled"] = enabled
        if config is not None:
            body["config"] = config
        return await self._client.put("/api/v1/storage/processor", json=body)


class AsyncDocumentsService:
    """Async documents service — fixed documents, folders, and deletion overrides."""

    def __init__(self, client: AsyncPlatformXeClient):
        self._client = client

    async def list_documents(self, folder_id: Optional[str] = None, page: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, str] = {}
        if folder_id:
            params["folderId"] = folder_id
        if page:
            params["page"] = str(page)
        return await self._client.get("/api/v1/storage/fixed/documents", params=params)

    async def get_document(self, document_id: str) -> Dict[str, Any]:
        return await self._client.get(f"/api/v1/storage/fixed/documents/{document_id}")

    async def create_document(self, **kwargs: Any) -> Dict[str, Any]:
        """Create a new fixed document."""
        return await self._client.post("/api/v1/storage/fixed/documents", json=kwargs)

    async def update_document(self, document_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Update a fixed document."""
        return await self._client.patch(f"/api/v1/storage/fixed/documents/{document_id}", json=kwargs)

    async def delete_document(self, document_id: str) -> Dict[str, Any]:
        """Delete a fixed document (may require override if protected)."""
        return await self._client.delete(f"/api/v1/storage/fixed/documents/{document_id}")

    async def list_folders(self) -> Dict[str, Any]:
        return await self._client.get("/api/v1/storage/fixed/folders")

    async def get_folder(self, folder_id: str) -> Dict[str, Any]:
        return await self._client.get(f"/api/v1/storage/fixed/folders/{folder_id}")

    async def create_folder(
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
        return await self._client.post("/api/v1/storage/fixed/folders", json=body)

    async def request_override(self, **kwargs: Any) -> Dict[str, Any]:
        """Request a deletion override for a protected document."""
        return await self._client.post("/api/v1/storage/fixed/overrides", json=kwargs)

    async def process_override(self, override_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Approve or reject a deletion override request."""
        return await self._client.patch(f"/api/v1/storage/fixed/overrides/{override_id}", json=kwargs)


class AsyncWorkflowsService:
    """Async workflows service — event-driven automation."""

    def __init__(self, client: AsyncPlatformXeClient):
        self._client = client

    async def list(self) -> Dict[str, Any]:
        return await self._client.get("/api/v1/workflows")

    async def create(self, **kwargs: Any) -> Dict[str, Any]:
        return await self._client.post("/api/v1/workflows", json=kwargs)

    async def get(self, workflow_id: str) -> Dict[str, Any]:
        return await self._client.get(f"/api/v1/workflows/{workflow_id}")

    async def update(self, workflow_id: str, **kwargs: Any) -> Dict[str, Any]:
        return await self._client.patch(f"/api/v1/workflows/{workflow_id}", json=kwargs)

    async def delete(self, workflow_id: str) -> Dict[str, Any]:
        return await self._client.delete(f"/api/v1/workflows/{workflow_id}")

    async def evaluate(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self._client.post("/api/v1/workflows/evaluate", json={"eventType": event_type, "payload": payload})

    async def dry_run(self, workflow_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Dry-run a trigger against a context (no side effects)."""
        return await self._client.post(f"/api/v1/workflows/{workflow_id}/dry-run", json=context)


class AsyncDomainsService:
    """Async domains service — sending domain management."""

    def __init__(self, client: AsyncPlatformXeClient):
        self._client = client

    async def list(self) -> Dict[str, Any]:
        return await self._client.get("/api/v1/domains")

    async def add(self, domain: str) -> Dict[str, Any]:
        return await self._client.post("/api/v1/domains", json={"domain": domain})

    async def get(self, domain_id: str) -> Dict[str, Any]:
        return await self._client.get(f"/api/v1/domains/{domain_id}")

    async def delete(self, domain_id: str) -> Dict[str, Any]:
        return await self._client.delete(f"/api/v1/domains/{domain_id}")

    async def verify(self, domain_id: str) -> Dict[str, Any]:
        return await self._client.post(f"/api/v1/domains/{domain_id}/verify")


class AsyncEventsService:
    """Async events service — ingest, log, subscriptions, replay."""

    def __init__(self, client: AsyncPlatformXeClient):
        self._client = client

    async def ingest(self, event_type: str, entity_type: str, entity_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return await self._client.post("/api/v1/events", json={
            "eventType": event_type, "entityType": entity_type,
            "entityId": entity_id, "payload": payload,
        })

    async def log(self, event_type: Optional[str] = None, page: Optional[int] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        params: Dict[str, str] = {}
        if event_type:
            params["eventType"] = event_type
        if page:
            params["page"] = str(page)
        if limit:
            params["limit"] = str(limit)
        return await self._client.get("/api/v1/event-log", params=params)

    async def list_subscriptions(self) -> Dict[str, Any]:
        return await self._client.get("/api/v1/event-subscriptions")

    async def create_subscription(self, event_types: List[str], webhook_url: str, secret: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"eventTypes": event_types, "webhookUrl": webhook_url}
        if secret:
            body["secret"] = secret
        return await self._client.post("/api/v1/event-subscriptions", json=body)

    async def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        return await self._client.get(f"/api/v1/event-subscriptions/{subscription_id}")

    async def update_subscription(self, subscription_id: str, **kwargs: Any) -> Dict[str, Any]:
        return await self._client.patch(f"/api/v1/event-subscriptions/{subscription_id}", json=kwargs)

    async def delete_subscription(self, subscription_id: str) -> Dict[str, Any]:
        return await self._client.delete(f"/api/v1/event-subscriptions/{subscription_id}")

    async def replay(self, subscription_id: str, from_date: str, to_date: str) -> Dict[str, Any]:
        return await self._client.post(f"/api/v1/event-subscriptions/{subscription_id}/replay", json={"from": from_date, "to": to_date})


class AsyncThreadsService:
    """Async contextual messaging (Threads) service — channels, threads, messages, flags, escalation."""

    def __init__(self, client: AsyncPlatformXeClient):
        self._client = client

    # ── Channels ──────────────────────────────────────────────────────────

    async def create_channel(
        self,
        slug: str,
        display_name: str,
        entity_type: str,
        participant_roles: List[str],
        default_visibility: List[str],
        lifecycle_rules: Optional[Dict[str, Any]] = None,
        escalation_config: Optional[Dict[str, Any]] = None,
        webhook_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        return await self._client.post("/api/v1/threads/channels", json={
            "slug": slug,
            "displayName": display_name,
            "entityType": entity_type,
            "participantRoles": participant_roles,
            "defaultVisibility": default_visibility,
            "lifecycleRules": lifecycle_rules,
            "escalationConfig": escalation_config,
            "webhookUrl": webhook_url,
        })

    async def list_channels(self) -> Dict[str, Any]:
        return await self._client.get("/api/v1/threads/channels")

    async def update_channel(self, channel_id: str, **kwargs: Any) -> Dict[str, Any]:
        return await self._client.patch(f"/api/v1/threads/channels/{channel_id}", json=kwargs)

    async def get_escalation_config(self, channel_id: str) -> Dict[str, Any]:
        return await self._client.get(f"/api/v1/threads/channels/{channel_id}/escalation")

    async def set_escalation_config(self, channel_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        return await self._client.put(f"/api/v1/threads/channels/{channel_id}/escalation", json=config)

    # ── Threads ───────────────────────────────────────────────────────────

    async def create_thread(
        self,
        channel_slug: str,
        entity_id: str,
        participants: List[Dict[str, str]],
        subject: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        return await self._client.post("/api/v1/threads", json={
            "channelSlug": channel_slug,
            "entityId": entity_id,
            "subject": subject,
            "metadata": metadata,
            "participants": participants,
        })

    async def list_threads(self, **params: Any) -> Dict[str, Any]:
        return await self._client.get("/api/v1/threads", params=params)

    async def get_thread(self, thread_id: str) -> Dict[str, Any]:
        return await self._client.get(f"/api/v1/threads/{thread_id}")

    async def close_thread(self, thread_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
        return await self._client.post(f"/api/v1/threads/{thread_id}/close", json={"reason": reason})

    async def reopen_thread(self, thread_id: str) -> Dict[str, Any]:
        return await self._client.post(f"/api/v1/threads/{thread_id}/reopen")

    async def entity_event(
        self,
        channel_slug: str,
        entity_id: str,
        event: str,
        new_status: Optional[str] = None,
    ) -> Dict[str, Any]:
        return await self._client.post("/api/v1/threads/entity-event", json={
            "channelSlug": channel_slug,
            "entityId": entity_id,
            "event": event,
            "newStatus": new_status,
        })

    # ── Messages ──────────────────────────────────────────────────────────

    async def send_message(
        self,
        thread_id: str,
        sender_external_id: str,
        sender_role: str,
        content: str,
        visibility: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        return await self._client.post(f"/api/v1/threads/{thread_id}/messages", json={
            "senderExternalId": sender_external_id,
            "senderRole": sender_role,
            "content": content,
            "visibility": visibility,
        })

    async def list_messages(
        self,
        thread_id: str,
        role: str,
        page: int = 1,
        limit: int = 50,
    ) -> Dict[str, Any]:
        return await self._client.get(
            f"/api/v1/threads/{thread_id}/messages",
            params={"page": page, "limit": limit},
            headers={"x-participant-role": role},
        )

    async def send_system_message(
        self,
        thread_id: str,
        content: str,
        visibility: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        return await self._client.post(f"/api/v1/threads/{thread_id}/messages/system", json={
            "content": content,
            "visibility": visibility or ["ALL"],
        })

    async def edit_message(self, message_id: str, content: str) -> Dict[str, Any]:
        return await self._client.patch(f"/api/v1/threads/messages/{message_id}", json={"content": content})

    async def delete_message(self, message_id: str) -> Dict[str, Any]:
        return await self._client.delete(f"/api/v1/threads/messages/{message_id}")

    # ── Read State & Inbox ────────────────────────────────────────────────

    async def mark_read(
        self,
        thread_id: str,
        external_id: str,
        role: str,
        message_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        return await self._client.post(f"/api/v1/threads/{thread_id}/read", json={
            "participantExternalId": external_id,
            "participantRole": role,
            "messageId": message_id,
        })

    async def get_read_states(self, thread_id: str) -> Dict[str, Any]:
        return await self._client.get(f"/api/v1/threads/{thread_id}/read-state")

    async def inbox(
        self,
        external_id: str,
        role: str,
        status: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {"externalId": external_id, "role": role, "page": page, "limit": limit}
        if status:
            params["status"] = status
        return await self._client.get("/api/v1/threads/inbox", params=params)

    async def unread_count(self, external_id: str, role: str) -> Dict[str, Any]:
        return await self._client.get("/api/v1/threads/inbox/unread-count", params={
            "externalId": external_id,
            "role": role,
        })

    # ── Flags & Escalation ────────────────────────────────────────────────

    async def flag_message(
        self,
        thread_id: str,
        message_id: str,
        reason: str,
        flagged_by_external_id: str,
        flagged_by_role: str,
        note: Optional[str] = None,
    ) -> Dict[str, Any]:
        return await self._client.post(
            f"/api/v1/threads/{thread_id}/messages/{message_id}/flag",
            json={
                "reason": reason,
                "note": note,
                "flaggedByExternalId": flagged_by_external_id,
                "flaggedByRole": flagged_by_role,
            },
        )

    async def escalate_thread(
        self,
        thread_id: str,
        reason: str,
        escalated_by_external_id: str,
        escalated_by_role: str,
    ) -> Dict[str, Any]:
        return await self._client.post(f"/api/v1/threads/{thread_id}/escalate", json={
            "reason": reason,
            "escalatedByExternalId": escalated_by_external_id,
            "escalatedByRole": escalated_by_role,
        })

    async def review_flag(
        self,
        flag_id: str,
        status: str,
        reviewed_by_external_id: str,
        note: Optional[str] = None,
    ) -> Dict[str, Any]:
        return await self._client.patch(f"/api/v1/threads/flags/{flag_id}", json={
            "status": status,
            "reviewedByExternalId": reviewed_by_external_id,
            "note": note,
        })

    async def list_flags(self, thread_id: str, status: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if status:
            params["status"] = status
        return await self._client.get(f"/api/v1/threads/{thread_id}/flags", params=params)

    async def list_flags_across_threads(
        self,
        status: Optional[str] = None,
        channel_slug: Optional[str] = None,
        page: int = 1,
        limit: int = 20,
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {"page": page, "limit": limit}
        if status:
            params["status"] = status
        if channel_slug:
            params["channelSlug"] = channel_slug
        return await self._client.get("/api/v1/threads/flags", params=params)

    # ── Participants ─────────────────────────────────────────────────────

    async def add_participant(
        self,
        thread_id: str,
        role: str,
        external_id: str,
        display_name: str,
        avatar_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "role": role,
            "externalId": external_id,
            "displayName": display_name,
        }
        if avatar_url is not None:
            body["avatarUrl"] = avatar_url
        return await self._client.post(f"/api/v1/threads/{thread_id}/participants", json=body)

    async def remove_participant(self, thread_id: str, participant_id: str) -> Dict[str, Any]:
        return await self._client.delete(f"/api/v1/threads/{thread_id}/participants/{participant_id}")

    async def update_participant(
        self,
        thread_id: str,
        participant_id: str,
        display_name: Optional[str] = None,
        avatar_url: Optional[str] = None,
        is_muted: Optional[bool] = None,
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {}
        if display_name is not None:
            body["displayName"] = display_name
        if avatar_url is not None:
            body["avatarUrl"] = avatar_url
        if is_muted is not None:
            body["isMuted"] = is_muted
        return await self._client.patch(
            f"/api/v1/threads/{thread_id}/participants/{participant_id}",
            json=body,
        )

    async def update_thread(
        self,
        thread_id: str,
        subject: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {}
        if subject is not None:
            body["subject"] = subject
        if metadata is not None:
            body["metadata"] = metadata
        return await self._client.patch(f"/api/v1/threads/{thread_id}", json=body)


class AsyncExportsService:
    """Async exports service — data export creation and retrieval."""

    def __init__(self, client: AsyncPlatformXeClient):
        self._client = client

    async def create_export(self, **kwargs: Any) -> Dict[str, Any]:
        return await self._client.post("/api/v1/exports", json=kwargs)

    async def get_export(self, export_id: str) -> Dict[str, Any]:
        return await self._client.get(f"/api/v1/exports/{export_id}")

    async def get_processor(self) -> Dict[str, Any]:
        """Get the exports processor configuration."""
        return await self._client.get("/api/v1/exports/processor")

    async def update_processor(self, enabled: Optional[bool] = None, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update the exports processor configuration."""
        body: Dict[str, Any] = {}
        if enabled is not None:
            body["enabled"] = enabled
        if config is not None:
            body["config"] = config
        return await self._client.put("/api/v1/exports/processor", json=body)


class AsyncOcrService:
    """Async OCR service — identity document verification."""

    def __init__(self, client: AsyncPlatformXeClient):
        self._client = client

    async def verify_identity(self, document_url: Optional[str] = None, document_base64: Optional[str] = None, profile_name: Optional[Dict[str, str]] = None, expected_type: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {}
        if document_url:
            body["documentUrl"] = document_url
        if document_base64:
            body["documentBase64"] = document_base64
        if profile_name:
            body["profileName"] = profile_name
        if expected_type:
            body["expectedDocumentType"] = expected_type
        return await self._client.post("/api/v1/ocr/verify-identity", json=body)

    async def get_processor(self) -> Dict[str, Any]:
        """Get the OCR processor configuration."""
        return await self._client.get("/api/v1/ocr/processor")

    async def update_processor(self, enabled: Optional[bool] = None, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update the OCR processor configuration."""
        body: Dict[str, Any] = {}
        if enabled is not None:
            body["enabled"] = enabled
        if config is not None:
            body["config"] = config
        return await self._client.put("/api/v1/ocr/processor", json=body)


class AsyncPdfService:
    """Async PDF service — document generation."""

    def __init__(self, client: AsyncPlatformXeClient):
        self._client = client

    async def generate_offer_letter(self, **kwargs: Any) -> Dict[str, Any]:
        """Generate an offer letter PDF."""
        return await self._client.post("/api/v1/pdf/offer-letter", json=kwargs)

    async def generate_property_flyer(self, **kwargs: Any) -> Dict[str, Any]:
        """Generate a property flyer PDF."""
        return await self._client.post("/api/v1/pdf/property-flyer", json=kwargs)

    async def get_processor(self) -> Dict[str, Any]:
        """Get the PDF processor configuration."""
        return await self._client.get("/api/v1/pdf/processor")

    async def update_processor(self, enabled: Optional[bool] = None, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update the PDF processor configuration."""
        body: Dict[str, Any] = {}
        if enabled is not None:
            body["enabled"] = enabled
        if config is not None:
            body["config"] = config
        return await self._client.put("/api/v1/pdf/processor", json=body)


class AsyncQrService:
    """Async QR service — QR code generation."""

    def __init__(self, client: AsyncPlatformXeClient):
        self._client = client

    async def generate(self, data: str, size: Optional[int] = None, format: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"data": data}
        if size:
            body["size"] = size
        if format:
            body["format"] = format
        return await self._client.post("/api/v1/qr", json=body)

    async def generate_batch(self, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate QR codes in batch."""
        return await self._client.post("/api/v1/qr/batch", json={"items": items})

    async def get_processor(self) -> Dict[str, Any]:
        """Get the QR processor configuration."""
        return await self._client.get("/api/v1/qr/processor")

    async def update_processor(self, enabled: Optional[bool] = None, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update the QR processor configuration."""
        body: Dict[str, Any] = {}
        if enabled is not None:
            body["enabled"] = enabled
        if config is not None:
            body["config"] = config
        return await self._client.put("/api/v1/qr/processor", json=body)


class AsyncUsageService:
    """Async usage service — metering and usage summaries."""

    def __init__(self, client: AsyncPlatformXeClient):
        self._client = client

    async def summary(self, month: Optional[str] = None) -> Dict[str, Any]:
        params: Dict[str, str] = {"month": month} if month else {}
        return await self._client.get("/api/v1/usage/summary", params=params)
