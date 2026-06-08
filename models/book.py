from decimal import Decimal
from sqlalchemy import String, Numeric, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db import Base
from models.category import book_category


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))

    author: Mapped["Author"] = relationship("Author",   back_populates="books")
    supplier: Mapped["Supplier"] = relationship("Supplier", back_populates="books")
    categories: Mapped[list["Category"]] = relationship("Category", secondary=book_category, back_populates="books")

    def __repr__(self) -> str:
        return f"<Book id={self.id} title={self.title!r} stock={self.stock_quantity}>"