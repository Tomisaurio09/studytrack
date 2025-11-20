from flask import request
from app.utils.limiters import limiter


@limiter.request_filter
def internal_request_exempt():
    """Return True to exempt internal/health requests from rate limiting.

    - Exempts localhost (::1 and 127.0.0.1).
    - Exempts a `/health` endpoint if you add one.
    - Return False to let limiter evaluate limits normally.
    """
    try:
        # Exempt local requests (useful for internal tooling/tests)
        #if request.remote_addr in ("127.0.0.1", "::1"):
        #   return True

        # Exempt health check endpoint if present
        if request.path == "/health":
            return True
    except RuntimeError:
        # No request context — don't exempt
        return False

    return False


