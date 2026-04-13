# PlatformXe Python SDK

Python SDK for the [PlatformXe](https://platformxe.com) API — messaging, storage, authorization, identity resolution, and more.

## Installation

```bash
pip install platformxe
```

## Quick Start

```python
from platformxe import PlatformXeClient

client = PlatformXeClient(api_key="pxk_live_your_key_here")

# Send email
client.messaging.send_email(
    to="user@example.com",
    subject="Welcome",
    html="<h1>Hello!</h1>",
)

# Check permission
result = client.permissions.check(
    admin_id="usr_123",
    path="chat/session",
    action="READ",
)

# Resolve Nigerian identity
profile = client.identity.resolve(
    type="BVN",
    value="22012345678",
    consent_reference="consent_abc123",
)
```

## Async Usage

```python
from platformxe import AsyncPlatformXeClient

async with AsyncPlatformXeClient(api_key="pxk_live_...") as client:
    result = await client.permissions.check(
        admin_id="usr_123",
        path="chat/session",
        action="READ",
    )
```

## Services

| Service | Access | Methods |
|---------|--------|---------|
| Permissions | `client.permissions` | check, check_batch, resolve, roles, overrides, policies, relationships, modules, federation |
| Identity | `client.identity` | resolve, verify, lookup, providers |
| Messaging | `client.messaging` | send_email, send_sms, send_whatsapp, email_health, sms_health, queue_stats |
| Webhooks | `client.webhooks` | list, create, get, update, delete, rotate_secret, test |
| Templates | `client.templates` | list, create, get, update, delete, render, send |
| Storage | `client.storage` | upload_file, batch_upload, sign_upload, register_url, list_files, get_file, delete_file, reorder_files, list_documents, get_document, list_folders, get_folder |
| Workflows | `client.workflows` | list, create, get, update, delete, evaluate |
| Domains | `client.domains` | list, add, get, delete, verify |
| Subscriptions | `client.subscriptions` | list, create, get, update, delete, replay, get_event_log, emit_event |
| Threads | `client.threads` | create_channel, list_channels, update_channel, create_thread, list_threads, get_thread, close_thread, reopen_thread, send_message, list_messages, edit_message, delete_message, mark_read, inbox, unread_count, flag_message, escalate_thread, review_flag, list_flags |
| Misc | `client.misc` | create_export, get_export, usage_summary, verify_identity_document, generate_qr, send_telemetry, health_check |

## Configuration

```python
client = PlatformXeClient(
    api_key="pxk_live_...",
    base_url="https://platformxe.com",  # default
    timeout=10.0,                        # seconds
    retries=2,                           # retry count
    fail_open=True,                      # return error dict instead of raising
)
```

## License

Proprietary — Caldera Technologies Ltd.
