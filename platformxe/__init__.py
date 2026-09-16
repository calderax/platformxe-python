# =============================================================================
# (c) 2026 Caldera Technologies Ltd.
# Proprietary and confidential.
# Unauthorized copying or distribution is prohibited.
# =============================================================================

"""PlatformXe Python SDK — messaging, storage, authorization, identity resolution."""

from .client import PlatformXeClient, AsyncPlatformXeClient
from .exceptions import PlatformXeError, PlatformXeAPIError
from .types import APIResponse, PaginationMeta
from .register import register

__version__ = "1.6.0"
__all__ = [
    "PlatformXeClient",
    "AsyncPlatformXeClient",
    "PlatformXeError",
    "PlatformXeAPIError",
    "APIResponse",
    "PaginationMeta",
    # v1.1.0
    "register",
]

# v1.6.0 (2026-09-15): documents.create_folder/list_folders and
# documents.request_override/process_override now send the real
# ownerType/ownerId and overrideReason/action shapes the fixed-storage API
# actually accepts, instead of fields it always rejected (create_folder,
# list_folders) or undocumented camelCase kwargs (request_override,
# process_override). list_folders is renamed get_folder_by_owner — the old
# name always 400'd against the live API, so there was no working behavior
# to preserve under the old name.
