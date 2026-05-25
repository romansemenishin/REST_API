import os
import redis.asyncio as aioredis
from fastapi import Request, HTTPException, status
from security import verify_token, SECRET_KEY

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)

async def check_rate_limit(request: Request):
    auth_header = request.headers.get("Authorization")
    username = None

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = verify_token(token, SECRET_KEY, "access")
            username = payload.get("sub")
        except Exception:
            pass

    if username:
        limit = 10
        key = f"rate_limit:user:{username}"
    else:
        limit = 2
        client_ip = request.client.host if request.client else "127.0.0.1"
        key = f"rate_limit:anon:{client_ip}"

    current_count = await redis_client.incr(key)
    
    if current_count == 1:
        await redis_client.expire(key, 60)

    if current_count > limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, 
            detail="Too Many Requests"
        )