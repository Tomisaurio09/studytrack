from app.utils.limiters import limiter

@limiter.request_filter
def too_many_requests():
    return {"error": "Too Many Requests"}, 429
