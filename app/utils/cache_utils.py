# Step 5: Create app/utils/cache_utils.py
from flask_jwt_extended import get_jwt_identity
from app import cache

def cache_key_user_subjects(page=1, per_page=10):
    """Generate cache key for user's subjects"""
    user_id = get_jwt_identity()
    return f"user:{user_id}:subjects:page:{page}:per_page:{per_page}"

def cache_key_user_sessions(page=1, per_page=10):
    """Generate cache key for user's sessions"""
    user_id = get_jwt_identity()
    return f"user:{user_id}:sessions:page:{page}:per_page:{per_page}"

def invalidate_user_subjects_cache():
    """Delete all subject cache entries for current user"""
    user_id = get_jwt_identity()
    for page in range(1, 11): # Assuming max 10 pages for simplicity
        for per_page in [10, 20, 50]:
            key = f"user:{user_id}:subjects:page:{page}:per_page:{per_page}"
            cache.delete(key)

def invalidate_user_sessions_cache():
    """Delete all session cache entries for current user"""
    user_id = get_jwt_identity()
    for page in range(1, 11):
        for per_page in [10, 20, 50]:
            key = f"user:{user_id}:sessions:page:{page}:per_page:{per_page}"
            cache.delete(key)