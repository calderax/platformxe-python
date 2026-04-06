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

## Services

| Service | Access | Methods |
|---------|--------|---------|
| Permissions | `client.permissions` | check, resolve, roles, overrides, policies, federation |
| Identity | `client.identity` | resolve, verify, lookup, providers |
| Messaging | `client.messaging` | send_email, send_sms, send_whatsapp, health |
| Webhooks | `client.webhooks` | list, create, update, delete, rotate, test |
| Templates | `client.templates` | list, create, render, send |
| Storage | `client.storage` | upload, files, documents, folders |
| Workflows | `client.workflows` | list, create, evaluate |
| Domains | `client.domains` | list, add, verify, delete |
| Subscriptions | `client.subscriptions` | list, create, replay, emit |
| Misc | `client.misc` | exports, usage, OCR, QR, telemetry, health |

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
