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
    # створюю дві унікальні книги одну за одною
    await client.post("/books/", json={
        "title": "Бот 1", "author": "Макс Кідрук", "status": "наявна в бібліотеці", "year": 2012
    })
    
    await client.post("/books/", json={
        "title": "Бот 2", "author": "Макс Кідрук", "status": "наявна в бібліотеці", "year": 2013
    })

    # запит із лімітом 1, щоб отримати першу книгу з бази
    response_page1 = await client.get("/books/?limit=1")
    assert response_page1.status_code == 200
    page1_data = response_page1.json()
    assert len(page1_data) == 1
    
    # ID книги, яка повернулася першою
    first_returned_id = page1_data[0]["id"]

    # Передаємо цей ID як cursor. База даних гарантовано поверне НАСТУПНУ книгу
    response_page2 = await client.get(f"/books/?limit=1&cursor={first_returned_id}")
    assert response_page2.status_code == 200
    page2_data = response_page2.json()
    assert len(page2_data) == 1
    
    # Перевіряємо, що ID другої книги не дорівнює першій 
    assert page2_data[0]["id"] != first_returned_id

    # Перевірка фільтрації за автором
    response_filter = await client.get("/books/?author=Макс Кідрук")
    assert response_filter.status_code == 200
    assert len(response_filter.json()) >= 2

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