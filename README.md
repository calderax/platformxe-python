# PlatformXe Python SDK

Official Python SDK for the [PlatformXe](https://platformxe.com) API — messaging, storage, OCR, PDF, identity, fraud detection, webhooks, workflows, custom events, and authorization (RBAC + ABAC + ReBAC + Federation).

[![PyPI version](https://img.shields.io/badge/pypi-v1.5.1-blue)](https://pypi.org/project/platformxe/)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)

## Install

```bash
pip install platformxe
```

The SDK supports Python 3.9+ and ships with `httpx` as its only runtime dependency.

## Quick start

```python
from platformxe import PlatformXeClient

client = PlatformXeClient(api_key="pxk_live_…")

# Send a transactional email
client.messaging.send_email(
    to="user@example.com",
    subject="Welcome",
    html="<h1>Hello</h1>",
)

# Check a permission
result = client.permissions.check(
    admin_id="usr_123",
    path="chat/session",
    action="READ",
)

# Resolve a Nigerian identity
profile = client.identity.resolve(
    type="BVN",
    value="22012345678",
    consent_reference="consent_abc",
)
```

## Async usage

```python
from platformxe import AsyncPlatformXeClient

async with AsyncPlatformXeClient(api_key="pxk_live_…") as client:
    decision = await client.permissions.check(
        admin_id="usr_123",
        path="chat/session",
        action="READ",
    )
```

## Configuration

```python
client = PlatformXeClient(
    api_key="pxk_live_…",                # required
    base_url="https://platformxe.com",   # optional — defaults to production
    timeout=10.0,                         # optional — seconds
    retries=2,                            # optional — retried on 5xx + network errors
    fail_open=False,                      # optional — return error dict instead of raising
)
```

`base_url` accepts the regional production endpoint or a self-hosted PlatformXe instance.

## Surface

| Namespace | Domain |
|-----------|--------|
| `client.messaging` | Transactional email, SMS, WhatsApp click-to-chat |
| `client.storage` / `client.documents` | Media + fixed-storage upload, signed URLs |
| `client.ocr` / `client.pdf` / `client.qr` | OCR, PDF generation, QR encoding |
| `client.identity` | Identity resolution + Nigerian KYC (BVN, NIN, liveness, face match) |
| `client.fraud` | Fraud Detection — rules, screens, devices, federation, terms |
| `client.permissions` | RBAC + ABAC + ReBAC + Federation. `check`, `check_batch`, `resolve`, roles, modules, overrides, policies, relationships |
| `client.audit` | Decision + mutation audit log query/export |
| `client.webhooks` | Outbound webhook endpoints |
| `client.templates` | Content templates |
| `client.workflows` | Event-driven automations |
| `client.domains` | Sending domain management |
| `client.events` | Built-in event ingestion + log + subscriptions |
| `client.events.custom` | Tenant-defined custom events (Phase 9A) |
| `client.events.custom.marketplace` | Cross-tenant marketplace (Phase 9C, PRO+) |
| `client.events.custom.federation` | Cross-org event fan-out (Phase 9D + Pattern 3, ENTERPRISE) |
| `client.threads` | Caldera Threads contextual messaging |
| `client.exports` | Async data export jobs |
| `client.usage` | Usage + billing reads |
| `client.search` | Federated search query |
| `client.issues` | Tenant-reported issues / support cases |
| `client.whoami` | API-key resolution + telemetry helpers |
| `register()` | Module-level standalone bootstrap helper |

## Pattern 3 — external webhook peers (1.5.0)

Custom Event Federation supports peers addressed by URL + HMAC secret instead of a tenant org id — useful when the receiving system isn't on PlatformXe.

```python
result = client.events.custom.federation.add_external_peer(
    group_id,
    label="Booking.com",
    webhook_url="https://booking.example.com/inbound/platformxe",
    headers={"Authorization": "Bearer xyz"},
)
secret = result["data"]["secret"]   # 'whsec_…' — store immediately, shown ONCE
peer_id = result["data"]["peer"]["id"]

# Remove later:
client.events.custom.federation.remove_external_peer(peer_id)
```

The receiving endpoint verifies inbound POSTs with `HMAC-SHA256(raw_body, secret)` matched against `X-Caldera-Signature: sha256=<hex>`. See the [federation reference](https://docs.platformxe.com/sdk/federation) for the full wire format.

## Error handling

Every method raises `PlatformXeAPIError` on 4xx/5xx responses, or `PlatformXeError` on transport failures. Set `fail_open=True` to receive the API's error envelope as a dict instead — useful for non-blocking permission checks.

```python
from platformxe import PlatformXeError, PlatformXeAPIError

try:
    client.messaging.send_email(to="user@example.com", subject="…", html="…")
except PlatformXeAPIError as err:
    # err.code, err.message, err.status_code
    ...
except PlatformXeError as err:
    # Network / configuration error
    ...
```

## Versioning

| Package | Version |
|---------|---------|
| `platformxe` (this) | **1.5.1** |
| `@caldera/platformxe-sdk` (TypeScript) | 1.5.1 |
| `@caldera/platformxe-types` (TypeScript shapes) | 2.7.1 |
| `github.com/calderax/platformxe-go` (Go) | v1.5.1 |
| `calderax/platformxe` (Terraform) | 1.5.1 |

The PlatformXe ecosystem ships **5 published artefacts** that move in lockstep against every API change (the NO-DRIFT policy). The full coverage matrix lives at [docs.platformxe.com/sdk/alignment](https://docs.platformxe.com/sdk/alignment).

## Distribution

The Python SDK is published to PyPI as `platformxe`. The source lives in this monorepo at `packages/sdk-python/` and is mirrored to GitHub at [`calderax/platformxe-python`](https://github.com/calderax/platformxe-python) on every `sdk-python/v*` tag push.

## Documentation

- **API reference + per-domain SDK guides:** [docs.platformxe.com](https://docs.platformxe.com)
- **OpenAPI 3.1 spec:** `https://api.platformxe.com/api/docs/openapi.json`
- **Status + incidents:** [status.platformxe.com](https://status.platformxe.com)

## License

Proprietary — © 2026 Caldera Technologies Ltd. All rights reserved.
