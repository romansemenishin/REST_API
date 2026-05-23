import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from repository.book_repo import BookRepository
from models.book import Book, BookStatus
from schemas.book import BookCreate

class BookService:
    def __init__(self, db: AsyncSession):
        self.repo = BookRepository(db)

    async def get_all(
        self, 
        limit: int, 
        offset: int, 
        status: Optional[BookStatus] = None, 
        author: Optional[str] = None, 
        sort_by: Optional[str] = None
    ) -> List[Book]:
        return await self.repo.get_all(limit=limit, offset=offset, status=status, author=author, sort_by=sort_by)

    async def get_by_id(self, book_id: uuid.UUID) -> Optional[Book]:
        return await self.repo.get_by_id(book_id)

    async def add(self, book_in: BookCreate) -> Book:
        db_book = Book(
            title=book_in.title,
            author=book_in.author,
            description=book_in.description,
            status=book_in.status.value,
            year=book_in.year
        )
        return await self.repo.add(db_book)

    async def delete(self, book_id: uuid.UUID) -> None:
        await self.repo.delete(book_id)