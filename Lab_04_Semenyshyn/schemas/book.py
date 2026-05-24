from pydantic import BaseModel
from typing import Optional

# базова схема з усіма полями
class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    status: str
    year: int

# схема для створення книги
class BookCreate(BookBase):
    pass

# схема для відповіді 
class BookResponse(BookBase):
    id: str