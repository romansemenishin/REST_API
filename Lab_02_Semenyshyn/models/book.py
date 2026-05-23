import uuid
from enum import Enum
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class BookStatus(str, Enum):
    AVAILABLE = "наявна в бібліотеці"
    ISSUED = "видана комусь"

class Book(Base):
    __tablename__ = "books"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, default=BookStatus.AVAILABLE.value, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)