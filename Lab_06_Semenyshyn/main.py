from fastapi import FastAPI
import auth
import books

app = FastAPI(title="Бібліотека API 6 з JWT", description="Лабораторна робота №6 Семенишин Роман")

app.include_router(auth.router)
app.include_router(books.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)