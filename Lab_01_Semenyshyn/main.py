from fastapi import FastAPI
from api.endpoints import router

app = FastAPI(title="Бібліотека API", description="Лабораторна робота 1")

app.include_router(router)