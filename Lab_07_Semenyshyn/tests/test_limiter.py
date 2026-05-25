import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch

from main import app

class MockRedis:
    def __init__(self):
        self.storage = {}

    async def incr(self, key):
        if key not in self.storage:
            self.storage[key] = 0
        self.storage[key] += 1
        return self.storage[key]

    async def expire(self, key, seconds):
        pass
        
    def clear(self):
        self.storage.clear()

mock_redis_instance = MockRedis()

@pytest_asyncio.fixture(autouse=True)
def reset_mock_redis():
    mock_redis_instance.clear()
    yield

@pytest_asyncio.fixture
async def client():
    with patch("limiter.redis_client", mock_redis_instance):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            yield c

@pytest.mark.asyncio
async def test_anonymous_rate_limit_ok(client: AsyncClient):
    response = await client.get("/books/")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_anonymous_rate_limit_exceeded(client: AsyncClient):
    for _ in range(2):
        await client.get("/books/")
    response = await client.get("/books/")
    assert response.status_code == 429

@pytest.mark.asyncio
async def test_authorized_rate_limit_ok(client: AsyncClient):
    login_resp = await client.post("/auth/login", data={"username": "admin", "password": "admin"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    for _ in range(10):
        response = await client.get("/books/", headers=headers)
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_authorized_rate_limit_exceeded(client: AsyncClient):
    login_resp = await client.post("/auth/login", data={"username": "admin", "password": "admin"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    for _ in range(10):
        await client.get("/books/", headers=headers)

    response = await client.get("/books/", headers=headers)
    assert response.status_code == 429