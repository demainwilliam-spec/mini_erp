from sqlalchemy import String, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.book import Book

class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="supplier")

    def __repr__(self) -> str:
        return f"<Supplier id={self.id} name={self.name!r} email={self.email!r}>"