import time
from collections import defaultdict
from typing import Dict, Tuple
from fastapi import Request, HTTPException
from fastapi import status

class TokenBucket:
    def __init__(self, rate: int, capacity: int):
        self.rate = rate
        self.capacity = capacity
        self.tokens: Dict[str, float] = defaultdict(lambda: capacity)
        self.last_refill: Dict[str, float] = defaultdict(time.time)
    
    async def consume(self, key: str, tokens: int = 1) -> Tuple[bool, int, int]:
        now = time.time()
        
        if key not in self.last_refill:
            self.last_refill[key] = now
            self.tokens[key] = self.capacity
        
        elapsed = now - self.last_refill[key]
        new_tokens = elapsed * self.rate
        self.tokens[key] = min(self.capacity, self.tokens[key] + new_tokens)
        self.last_refill[key] = now
        
        if self.tokens[key] >= tokens:
            self.tokens[key] -= tokens
            remaining = int(self.tokens[key])
            reset = int(now + (self.capacity - self.tokens[key]) / self.rate)
            return True, remaining, reset
        else:
            reset = int(now + (tokens - self.tokens[key]) / self.rate)
            return False, 0, reset

rate_limiters = {
    "default": TokenBucket(rate=100, capacity=100),
    "products": TokenBucket(rate=100, capacity=100),
    "cart": TokenBucket(rate=60, capacity=60),
    "cart_write": TokenBucket(rate=30, capacity=30),
    "login": TokenBucket(rate=10, capacity=10),
    "register": TokenBucket(rate=5, capacity=5)
}

async def rate_limit(
    request: Request,
    limiter_name: str = "default"
):
    client_ip = request.client.host if request.client else "unknown"
    key = f"{client_ip}:{limiter_name}"
    
    limiter = rate_limiters.get(limiter_name, rate_limiters["default"])
    allowed, remaining, reset_at = await limiter.consume(key)
    
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later.",
            headers={
                "X-RateLimit-Limit": str(limiter.capacity),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(reset_at),
                "Retry-After": str(reset_at - int(time.time()))
            }
        )
    
    return {
        "X-RateLimit-Limit": str(limiter.capacity),
        "X-RateLimit-Remaining": str(remaining),
        "X-RateLimit-Reset": str(reset_at)
    }