import pytest
from fastapi.testclient import TestClient
from main import app
from models.data import books_db

client = TestClient(app)

# Ця функція очищає базу перед кожним тестом, 
# щоб тести не заважали один одному
@pytest.fixture(autouse=True)
def reset_db():
    books_db.clear()

def test_add_book():
    data = {
        "title": "Тіні забутих предків",
        "author": "Михайло Коцюбинський",
        "description": "Повість",
        "status": "наявні",
        "year": 1911
    }
    response = client.post("/books/", json=data)
    
    assert response.status_code == 201
    assert response.json()["title"] == "Тіні забутих предків"
    assert "id" in response.json()

def test_get_all_books():
    # Спочатку додаємо книгу
    client.post("/books/", json={
        "title": "Книга 1", "author": "Автор 1", "status": "наявні", "year": 2000
    })
    
    # Потім отримуємо список
    response = client.get("/books/")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_book_not_found():
    # Шукаємо вигаданий ID
    response = client.get("/books/12345-67890")
    assert response.status_code == 404

def test_delete_book():
    # Додаємо книгу
    res_post = client.post("/books/", json={
        "title": "Тестова книга", "author": "Тест", "status": "видані", "year": 2025
    })
    book_id = res_post.json()["id"]

    # Видаляємо її
    res_del1 = client.delete(f"/books/{book_id}")
    assert res_del1.status_code == 204

    # Пробуємо видалити ще раз (перевіряємо ідемпотентність)
    res_del2 = client.delete(f"/books/{book_id}")
    assert res_del2.status_code == 204
    
    # Перевіряємо чи її точно немає
    res_get = client.get(f"/books/{book_id}")
    assert res_get.status_code == 404