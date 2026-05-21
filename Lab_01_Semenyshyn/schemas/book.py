from pydantic import BaseModel, Field
from enum import Enum

# Статуси книг
class BookStatus(str, Enum):
    AVAILABLE = "наявні"
    BORROWED = "видані"

class BookBase(BaseModel):
    title: str = Field(..., description="Назва книги")
    author: str = Field(..., description="Автор")
    description: str | None = None  # Опис може бути порожнім
    status: BookStatus
    year: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: str