import pytest
from uuid import uuid4

pytestmark = pytest.mark.asyncio

async def test_create_book(client):
    response = await client.post("/books/", json={
        "title": "Колонія",
        "author": "Макс Кідрук",
        "description": "Нові Темні Віки",
        "status": "наявна в бібліотеці",
        "year": 2023
    })
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Колонія"

async def test_get_books_pagination_and_filter(client):
    for i in range(5):
        await client.post("/books/", json={
            "title": f"Бот {i}",
            "author": "Макс Кідрук",
            "status": "наявна в бібліотеці",
            "year": 2012 + i
        })

    # Перевірка роботи Limit та Offset
    response = await client.get("/books/?limit=2&offset=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    response_filter = await client.get("/books/?author=Макс Кідрук")
    assert response_filter.status_code == 200
    assert len(response_filter.json()) >= 5

async def test_get_book_by_id_not_found(client):
    random_uuid = str(uuid4())
    response = await client.get(f"/books/{random_uuid}")
    assert response.status_code == 404

async def test_delete_book_idempotent(client):
    create_resp = await client.post("/books/", json={
        "title": "Твердиня",
        "author": "Макс Кідрук",
        "status": "наявна в бібліотеці",
        "year": 2013
    })
    book_id = create_resp.json()["id"]

    del_resp1 = await client.delete(f"/books/{book_id}")
    assert del_resp1.status_code == 204

    # Другий DELETE запит повинен відпрацювати так само ідемпотентно (204)
    del_resp2 = await client.delete(f"/books/{book_id}")
    assert del_resp2.status_code == 204