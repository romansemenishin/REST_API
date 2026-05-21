from fastapi import APIRouter, HTTPException, Query, status
from schemas.book import BookResponse, BookCreate
from services.book_service import BookService

router = APIRouter(prefix="/books", tags=["Books"])
book_service = BookService()

# 1. Отримати всі книги
@router.get("/", response_model=list[BookResponse], status_code=status.HTTP_200_OK)
async def get_all_books(
    status: str = Query(None, description="Фільтр: наявні або видані"),
    author: str = Query(None, description="Фільтр по автору"),
    sort_by: str = Query(None, description="Сортування: title або year")
):
    return await book_service.get_books(status, author, sort_by)

# 2. Отримати книгу по ID
@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: str):
    book = await book_service.get_book(book_id)
    if book is None:
        # Повертаємо 404, якщо книги немає
        raise HTTPException(status_code=404, detail="Книгу з таким ID не знайдено")
    return book

# 3. Додати книгу
@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def add_book(book: BookCreate):
    return await book_service.create_book(book)

# 4. Видалити книгу
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str):
    # Метод ідемпотентний: якщо книги вже немає, ми просто нічого не робимо,
    # сервер все одно поверне статус 204
    await book_service.delete_book(book_id)
    return