from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from fastapi import Depends
from database import get_books_collection
from typing import List, Optional

class MongoRepository:
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    # Реалізація Limit-Offset пагінації за допомогою skip() та limit()
    async def get_all(self, limit: int, offset: int) -> List[dict]:
        cursor = self.collection.find().skip(offset).limit(limit)
        books = await cursor.to_list(length=limit)
        
        # Перетворюємо внутрішній _id типу ObjectId у рядок id для Pydantic
        for book in books:
            book["id"] = str(book["_id"])
        return books

    async def get_by_id(self, book_id: str) -> Optional[dict]:
        if not ObjectId.is_valid(book_id):
            return None
        book = await self.collection.find_one({"_id": ObjectId(book_id)})
        if book:
            book["id"] = str(book["_id"])
        return book

    async def create(self, book_data: dict) -> dict:
        result = await self.collection.insert_one(book_data)
        book_data["id"] = str(result.inserted_id)
        return book_data

    async def delete(self, book_id: str) -> bool:
        if not ObjectId.is_valid(book_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(book_id)})
        return result.deleted_count > 0

# Функція-депенденсі для прокидання репозиторію в ендпоінти
def get_repository(collection=Depends(get_books_collection)) -> MongoRepository:
    return MongoRepository(collection)