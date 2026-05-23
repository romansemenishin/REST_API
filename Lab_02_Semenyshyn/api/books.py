from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.book import BookCreate, BookResponse
from services.book_service import BookService
from models.book import BookStatus

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[BookResponse], status_code=status.HTTP_200_OK)
async def get_books(
    limit: int = Query(10, ge=1, le=100, description="Limit"),
    offset: int = Query(0, ge=0, description="Offset"),
    status_filter: Optional[BookStatus] = Query(None, alias="status"),
    author: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None, description="Сортування за: 'title' або 'year'"),
    db: AsyncSession = Depends(get_db)
):
    service = BookService(db)
    return await service.get_all(limit=limit, offset=offset, status=status_filter, author=author, sort_by=sort_by)

@router.get("/{book_id}", response_model=BookResponse, status_code=status.HTTP_200_OK)
async def get_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    book = await service.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книгу не знайдено")
    return book

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    return await service.add(book)

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    await service.delete(book_id)
    return