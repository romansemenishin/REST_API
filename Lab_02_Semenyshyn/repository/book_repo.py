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
        offset: int, 
        status: Optional[BookStatus] = None, 
        author: Optional[str] = None, 
        sort_by: Optional[str] = None
    ) -> List[Book]:
        stmt = select(Book)
        
        if status:
            stmt = stmt.where(Book.status == status.value)
        if author:
            stmt = stmt.where(Book.author == author)
            
        if sort_by == "title":
            stmt = stmt.order_by(asc(Book.title))
        elif sort_by == "year":
            stmt = stmt.order_by(asc(Book.year))
            
        # Limit-Offset пагінація в базі даних
        stmt = stmt.offset(offset).limit(limit)
        
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