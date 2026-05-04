# =============================================================================
# (c) 2026 Caldera Technologies Ltd.
# Proprietary and confidential.
# Unauthorized copying or distribution is prohibited.
# =============================================================================

"""PlatformXe SDK exceptions."""


class PlatformXeError(Exception):
    """Base exception for PlatformXe SDK."""
    pass


class PlatformXeAPIError(PlatformXeError):
    """API returned an error response."""
    def __init__(self, code: str, message: str, status_code: int):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(f"[{code}] {message} (HTTP {status_code})")
