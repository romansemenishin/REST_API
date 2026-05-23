from fastapi import FastAPI
from api.books import router as books_router
from database import Base, engine

app = FastAPI(title="Бібліотека API 3", description="Лабораторна робота №3 Семенишин Роман")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(books_router)