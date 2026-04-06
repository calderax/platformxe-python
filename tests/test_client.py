# =============================================================================
# (c) 2026 Caldera Technologies Ltd.
# Proprietary and confidential.
# Unauthorized copying or distribution is prohibited.
# =============================================================================

"""Basic tests for PlatformXe Python SDK."""

import pytest
from platformxe import PlatformXeClient


def test_client_initialization():
    client = PlatformXeClient(api_key="test_key")
    assert client.api_key == "test_key"
    assert client.base_url == "https://platformxe.com"
    assert client.timeout == 10.0
    assert client.retries == 2
    assert client.fail_open is True
    client.close()


def test_client_custom_config():
    client = PlatformXeClient(
        api_key="test",
        base_url="http://localhost:3000",
        timeout=5.0,
        retries=0,
        fail_open=False,
    )
    assert client.base_url == "http://localhost:3000"
    assert client.timeout == 5.0
    assert client.retries == 0
    assert client.fail_open is False
    client.close()


def test_service_namespaces():
    client = PlatformXeClient(api_key="test")
    assert hasattr(client, "permissions")
    assert hasattr(client, "identity")
    assert hasattr(client, "messaging")
    assert hasattr(client, "webhooks")
    assert hasattr(client, "templates")
    assert hasattr(client, "storage")
    assert hasattr(client, "workflows")
    assert hasattr(client, "domains")
    assert hasattr(client, "subscriptions")
    assert hasattr(client, "misc")
    client.close()


def test_context_manager():
    with PlatformXeClient(api_key="test") as client:
        assert client.api_key == "test"


# -- Method existence tests --

def test_permissions_methods():
    """Permissions service has all expected methods."""
    client = PlatformXeClient(api_key="test")
    methods = ['check', 'check_batch', 'resolve', 'list_roles', 'create_role',
               'get_role', 'update_role', 'delete_role', 'get_role_capabilities',
               'set_role_capabilities', 'list_overrides', 'create_override',
               'delete_override', 'list_policies', 'create_policy', 'update_policy',
               'delete_policy', 'list_relationships', 'register_module', 'list_modules',
               'get_audit_logs', 'shadow_check', 'create_federation_group',
               'list_federation_groups', 'get_federation_group']
    for method in methods:
        assert hasattr(client.permissions, method), f"Missing method: permissions.{method}"
    client.close()


def test_identity_methods():
    """Identity service has all expected methods."""
    client = PlatformXeClient(api_key="test")
    methods = ['resolve', 'verify', 'lookup', 'providers']
    for method in methods:
        assert hasattr(client.identity, method), f"Missing method: identity.{method}"
    client.close()


def test_messaging_methods():
    """Messaging service has all expected methods."""
    client = PlatformXeClient(api_key="test")
    methods = ['send_email', 'send_sms', 'send_whatsapp', 'email_health',
               'sms_health', 'queue_stats', 'process_queue']
    for method in methods:
        assert hasattr(client.messaging, method), f"Missing method: messaging.{method}"
    client.close()


def test_webhooks_methods():
    client = PlatformXeClient(api_key="test")
    methods = ['list', 'create', 'get', 'update', 'delete', 'rotate_secret', 'test']
    for method in methods:
        assert hasattr(client.webhooks, method), f"Missing method: webhooks.{method}"
    client.close()


def test_templates_methods():
    client = PlatformXeClient(api_key="test")
    methods = ['list', 'create', 'get', 'update', 'delete', 'render', 'send']
    for method in methods:
        assert hasattr(client.templates, method), f"Missing method: templates.{method}"
    client.close()


def test_storage_methods():
    client = PlatformXeClient(api_key="test")
    methods = ['sign_upload', 'register_url', 'list_files', 'get_file',
               'delete_file', 'list_documents', 'get_document', 'list_folders', 'get_folder']
    for method in methods:
        assert hasattr(client.storage, method), f"Missing method: storage.{method}"
    client.close()


def test_workflows_methods():
    client = PlatformXeClient(api_key="test")
    methods = ['list', 'create', 'get', 'update', 'delete', 'evaluate']
    for method in methods:
        assert hasattr(client.workflows, method), f"Missing method: workflows.{method}"
    client.close()


def test_domains_methods():
    client = PlatformXeClient(api_key="test")
    methods = ['list', 'add', 'get', 'delete', 'verify']
    for method in methods:
        assert hasattr(client.domains, method), f"Missing method: domains.{method}"
    client.close()


def test_subscriptions_methods():
    client = PlatformXeClient(api_key="test")
    methods = ['list', 'create', 'get', 'update', 'delete', 'replay']
    for method in methods:
        assert hasattr(client.subscriptions, method), f"Missing method: subscriptions.{method}"
    client.close()


def test_misc_methods():
    client = PlatformXeClient(api_key="test")
    methods = ['create_export', 'get_export', 'usage_summary', 'verify_identity_document',
               'generate_qr', 'send_telemetry', 'health_check']
    for method in methods:
        assert hasattr(client.misc, method), f"Missing method: misc.{method}"
    client.close()
