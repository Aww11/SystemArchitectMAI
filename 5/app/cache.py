import json
from functools import wraps
from typing import Any, Callable, Optional
from app.redis_client import get_redis

def cache(ttl: int = 60, key_prefix: str = ""):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            redis = await get_redis()
            
            cache_key = f"{key_prefix}:"
            if args:
                cache_key += str(args[0]) if args else ""
            for k, v in kwargs.items():
                cache_key += f":{k}={v}"
            
            cached = await redis.get(cache_key)
            if cached:
                return json.loads(cached)
            
            result = await func(*args, **kwargs)
            
            await redis.setex(cache_key, ttl, json.dumps(result, default=str))
            return result
        return wrapper
    return decorator

async def invalidate_cache(pattern: str):
    redis = await get_redis()
    keys = await redis.keys(f"{pattern}*")
    if keys:
        await redis.delete(*keys)

async def invalidate_all_products_cache():
    await invalidate_cache("products")

async def invalidate_user_cart_cache(user_id: str):
    await invalidate_cache(f"cart:user_id={user_id}")