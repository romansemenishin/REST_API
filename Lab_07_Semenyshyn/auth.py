from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from security import verify_password, get_password_hash, create_access_token, create_refresh_token, verify_token, REFRESH_SECRET_KEY

router = APIRouter(prefix="/auth", tags=["Authentication"])

# база користувачів (пароль: admin)
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": get_password_hash("admin")
    }
}

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильний логін або пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["username"]})
    refresh_token = create_refresh_token(data={"sub": user["username"]})
    
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshRequest):
    # перевірка старого refresh токен
    payload = verify_token(request.refresh_token, REFRESH_SECRET_KEY, "refresh")
    username = payload.get("sub")
    
    if username not in fake_users_db:
        raise HTTPException(status_code=401, detail="Користувача не знайдено")
    
    # генерація нової пари токенів
    new_access_token = create_access_token(data={"sub": username})
    new_refresh_token = create_refresh_token(data={"sub": username})
    
    return {"access_token": new_access_token, "refresh_token": new_refresh_token}