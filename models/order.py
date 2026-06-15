from __future__ import annotations
from datetime import date
from decimal import Decimal
from sqlalchemy import Date, String, ForeignKey, Numeric, Integer, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db import Base
import enum
import sqlalchemy as sa

class OrderStatus(enum.Enum):
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    CLOSED = "closed"

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(sa.Enum(OrderStatus, values_callable=lambda x: [e.value for e in x]), default=OrderStatus.DRAFT, nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))

    customer: Mapped["Customer"] = relationship("Customer", back_populates="orders")
    order_lines: Mapped[list["OrderLine"]] = relationship(
        "OrderLine", back_populates="order", cascade="all, delete-orphan"
    )

    @property
    def total(self) -> Decimal:
        return sum(line.quantity * line.unit_price for line in self.order_lines)

    def __repr__(self) -> str:
        return f"<Order id={self.id} status={self.status!r} total={self.total}>"
    


class OrderLine(Base):
    __tablename__ = "order_lines"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="order_lines")
    book: Mapped["Book"] = relationship("Book")

    def __repr__(self) -> str:
        return (
            f"<OrderLine book_id={self.book_id} "
            f"qty={self.quantity} unit_price={self.unit_price}>"
        )