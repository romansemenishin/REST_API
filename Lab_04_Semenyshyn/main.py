from fastapi import FastAPI
from api.endpoints import router

app = FastAPI(title="Бібліотека API 4 MongoDB", description="Лабораторна робота №4 Семенишин Роман")

app.include_router(router, prefix="/books")