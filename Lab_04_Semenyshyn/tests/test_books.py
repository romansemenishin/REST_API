import pytest
import pytest_asyncio
import os
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient

from main import app
from database import get_books_collection

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

def override_get_books_collection():
    client = AsyncIOMotorClient(MONGO_URL)
    return client["test_library_db"]["books"]

app.dependency_overrides[get_books_collection] = override_get_books_collection

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    test_collection = override_get_books_collection()
    
    await test_collection.delete_many({})
    yield
    await test_collection.delete_many({})
    
    test_collection.database.client.close()

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test", 
        follow_redirects=True
    ) as c:
        yield c



# ТЕСТИ
@pytest.mark.asyncio
async def test_add_new_book(client: AsyncClient):
    book_data = {
        "title": "Монго для початківців",
        "author": "Автор Авторович",
        "status": "наявні",
        "year": 2024
    }
    
    response = await client.post("/books/", json=book_data)
    assert response.status_code == 201
    
    data = response.json()
    assert "id" in data 
    assert data["title"] == "Монго для початківців"

@pytest.mark.asyncio
async def test_get_books_pagination(client: AsyncClient):
    await client.post("/books/", json={"title": "Книга 1", "author": "А1", "status": "наявні", "year": 2001})
    await client.post("/books/", json={"title": "Книга 2", "author": "А2", "status": "видані", "year": 2002})
    await client.post("/books/", json={"title": "Книга 3", "author": "А3", "status": "наявні", "year": 2003})
    
    # тест ліміту, беремо тільки 2
    response_limit = await client.get("/books/?limit=2&offset=0")
    assert response_limit.status_code == 200
    data_limit = response_limit.json()
    assert len(data_limit) == 2
    
    # тест зсуву, пропускаємо перші 2, має залишитись 1
    response_offset = await client.get("/books/?limit=2&offset=2")
    assert response_offset.status_code == 200
    data_offset = response_offset.json()
    assert len(data_offset) == 1
    assert data_offset[0]["title"] == "Книга 3"