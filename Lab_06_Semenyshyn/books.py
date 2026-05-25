from fastapi import APIRouter, Depends, HTTPException
from security import oauth2_scheme, verify_token, SECRET_KEY

router = APIRouter(prefix="/books", tags=["Books"])

# база даних книг
books_db = {
    1: {"id": 1, "title": "Інтернат", "author": "Сергій Жадан"},
    2: {"id": 2, "title": "Я бачу, вас цікавить пітьма", "author": "Ілларіон Павлюк"},
    3: {"id": 3, "title": "Колонія", "author": "Макс Кідрук"},
    4: {"id": 4, "title": "Записки українського самашедшого", "author": "Ліна Костенко"}
}

# перевірка токена перед кожним запитом
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token, SECRET_KEY, "access")
    return payload.get("sub")

@router.get("/")
async def get_books(current_user: str = Depends(get_current_user)):
    return {"user": current_user, "books": books_db}

@router.post("/")
async def add_book(title: str, author: str, current_user: str = Depends(get_current_user)):
    new_book = {"id": len(books_db) + 1, "title": title, "author": author}
    books_db.append(new_book)
    return new_book