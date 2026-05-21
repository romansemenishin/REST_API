from repository.book_repo import BookRepository
import uuid

class BookService:
    def __init__(self):
        self.repo = BookRepository()

    async def get_books(self, status: str = None, author: str = None, sort_by: str = None):
        books = await self.repo.get_all()
        
        # Робимо фільтрацію
        filtered_books = []
        for b in books:
            match = True
            if status and b["status"] != status:
                match = False
            # Шукаємо підрядок в імені автора, ігноруючи регістр
            if author and author.lower() not in b["author"].lower():
                match = False
                
            if match:
                filtered_books.append(b)

        # Сортування
        if sort_by == "title":
            filtered_books.sort(key=lambda x: x["title"])
        elif sort_by == "year":
            filtered_books.sort(key=lambda x: x["year"])
            
        return filtered_books

    async def get_book(self, book_id: str):
        return await self.repo.get_by_id(book_id)

    async def create_book(self, book_data):
        # Перетворюємо pydantic модель у словник
        book_dict = book_data.model_dump()
        
        # Генеруємо рандомний ID у вигляді рядка
        book_dict["id"] = str(uuid.uuid4())
        
        return await self.repo.add(book_dict)

    async def delete_book(self, book_id: str):
        await self.repo.delete(book_id)