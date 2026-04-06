# =============================================================================
# (c) 2026 Caldera Technologies Ltd.
# Proprietary and confidential.
# Unauthorized copying or distribution is prohibited.
# =============================================================================

"""PlatformXe Python SDK — messaging, storage, authorization, identity resolution."""

from .client import PlatformXeClient
from .exceptions import PlatformXeError, PlatformXeAPIError

__version__ = "1.0.0"
__all__ = ["PlatformXeClient", "PlatformXeError", "PlatformXeAPIError"]
