from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from repository.mongo_repo import MongoRepository, get_repository
from schemas.book import BookCreate, BookResponse

router = APIRouter(tags=["Books"])

@router.get("/", response_model=List[BookResponse])
async def get_all_books(
    limit: int = 10, 
    offset: int = 0, 
    repo: MongoRepository = Depends(get_repository)
):
    return await repo.get_all(limit=limit, offset=offset)

@router.get("/{book_id}", response_model=BookResponse)
async def get_book_by_id(book_id: str, repo: MongoRepository = Depends(get_repository)):
    book = await repo.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return book

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_new_book(book: BookCreate, repo: MongoRepository = Depends(get_repository)):
    # Перетворюємо Pydantic схему в словник dict для вставки в MongoDB
    return await repo.create(book.model_dump())

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_by_id(book_id: str, repo: MongoRepository = Depends(get_repository)):
    success = await repo.delete(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return None