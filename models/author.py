from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db import Base


class Author(Base):
    __tablename__ = "authors"

    id:   Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="author")

    def __repr__(self) -> str:
        return f"<Author id={self.id} name={self.name!r}>"