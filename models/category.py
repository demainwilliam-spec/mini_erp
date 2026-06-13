from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.book import Book    

book_category = Table(
    "book_category",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    books: Mapped[list["Book"]] = relationship("Book", secondary=book_category, back_populates="categories")

    def __repr__(self) -> str:
        return f"<Category id={self.id} name={self.name!r}>"