from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from security import verify_token, SECRET_KEY, oauth2_scheme
from limiter import check_rate_limit

router = APIRouter(prefix="/books", tags=["Books"])

# база даних книг
books_db = {
    1: {"id": 1, "title": "Інтернат", "author": "Сергій Жадан"},
    2: {"id": 2, "title": "Я бачу, вас цікавить пітьма", "author": "Ілларіон Павлюк"},
    3: {"id": 3, "title": "Колонія", "author": "Макс Кідрук"},
    4: {"id": 4, "title": "Записки українського самашедшого", "author": "Ліна Костенко"}
}

oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)

def get_optional_user(token: Optional[str] = Depends(oauth2_scheme_optional)):
    if token:
        try:
            payload = verify_token(token, SECRET_KEY, "access")
            return payload.get("sub")
        except Exception:
            return None
    return None

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token, SECRET_KEY, "access")
    return payload.get("sub")

@router.get("/", dependencies=[Depends(check_rate_limit)])
async def get_books(current_user: Optional[str] = Depends(get_optional_user)):
    return {"user": current_user or "anonymous", "books": books_db}

@router.post("/", dependencies=[Depends(check_rate_limit)])
async def add_book(title: str, author: str, current_user: str = Depends(get_current_user)):
    new_book = {"id": len(books_db) + 1, "title": title, "author": author}
    books_db.append(new_book)
    return new_book