# =============================================================================
# (c) 2026 Caldera Technologies Ltd.
# Proprietary and confidential.
# Unauthorized copying or distribution is prohibited.
# =============================================================================

"""PlatformXe Python SDK — messaging, storage, authorization, identity resolution."""

from .client import PlatformXeClient, AsyncPlatformXeClient
from .exceptions import PlatformXeError, PlatformXeAPIError
from .types import APIResponse, PaginationMeta

__version__ = "1.0.0"
__all__ = [
    "PlatformXeClient",
    "AsyncPlatformXeClient",
    "PlatformXeError",
    "PlatformXeAPIError",
    "APIResponse",
    "PaginationMeta",
]
