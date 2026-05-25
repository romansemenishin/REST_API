from fastapi import FastAPI

app = FastAPI(title="Library API for Load Testing")

books_db = [
    {"id": 1, "title": "Інтернат", "author": "Сергій Жадан"},
    {"id": 2, "title": "Колонія", "author": "Макс Кідрук"}
]

@app.get("/books/")
async def get_books():
    return {"books": books_db}