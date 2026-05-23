from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from models.book import BookStatus

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, description="Назва книги")
    author: str = Field(..., min_length=1, description="Автор книги")
    description: Optional[str] = None
    status: BookStatus = BookStatus.AVAILABLE
    year: int = Field(..., gt=0, description="Рік випуску")

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: UUID

    class Config:
        from_attributes = True