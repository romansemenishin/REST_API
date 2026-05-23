import uuid
from typing import List, Optional
from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession
from models.book import Book, BookStatus

class BookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(
        self, 
        limit: int, 
        cursor: Optional[uuid.UUID] = None,  # замінив offset на cursor
        status: Optional[BookStatus] = None, 
        author: Optional[str] = None, 
        sort_by: Optional[str] = None
    ) -> List[Book]:
        stmt = select(Book)
        
        # Фільтрація
        if status:
            stmt = stmt.where(Book.status == status.value)
        if author:
            stmt = stmt.where(Book.author == author)
            
        # Логіка Курсора (Cursor-based пагінація)
        if cursor:
            # Повертаємо лише ті книги, чий ID більший за переданий курсор.
            stmt = stmt.where(Book.id > cursor)
            
        # Сортування
        if sort_by == "title":
            stmt = stmt.order_by(asc(Book.title), asc(Book.id))
        elif sort_by == "year":
            stmt = stmt.order_by(asc(Book.year), asc(Book.id))
        else:
            # За замовчуванням сортує суто за ID
            stmt = stmt.order_by(asc(Book.id))
            
        # Лімітуємо кількість результатів
        stmt = stmt.limit(limit)
        
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, book_id: uuid.UUID) -> Optional[Book]:
        stmt = select(Book).where(Book.id == book_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def add(self, book: Book) -> Book:
        self.db.add(book)
        await self.db.commit()
        await self.db.refresh(book)
        return book

    async def delete(self, book_id: uuid.UUID) -> None:
        book = await self.get_by_id(book_id)
        if book:
            await self.db.delete(book)
            await self.db.commit()