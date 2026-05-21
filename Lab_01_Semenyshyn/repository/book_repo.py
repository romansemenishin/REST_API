from models.data import books_db

class BookRepository:
    async def get_all(self):
        return books_db

    async def get_by_id(self, book_id: str):
        # Шукаємо книгу
        for book in books_db:
            if book["id"] == book_id:
                return book
        return None

    async def add(self, book_data: dict):
        books_db.append(book_data)
        return book_data

    async def delete(self, book_id: str):
        # Знаходимо індекс книги і видаляємо її
        for i in range(len(books_db)):
            if books_db[i]["id"] == book_id:
                del books_db[i]
                break # Зупиняємо цикл, бо книгу вже видалили