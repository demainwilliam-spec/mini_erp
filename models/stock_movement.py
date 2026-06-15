import enum
from datetime import date
from sqlalchemy import Integer, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Identity
import sqlalchemy as sa
from database.db import Base

class MovementReason(enum.Enum):
    ORDER_CONFIRMED = "order_confirmed"
    RESTOCK = "restock"

class StockMovement(Base):
    __tablename__ = "stock_movements"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[MovementReason] = mapped_column(sa.Enum(MovementReason, values_callable=lambda x: [e.value for e in x]), nullable=False)
    date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)

    book: Mapped["Book"] = relationship("Book")

    def __repr__(self) -> str:
        return (
            f"<StockMovement book_id={self.book_id} "
            f"qty={self.quantity} reason={self.reason}>"
        )