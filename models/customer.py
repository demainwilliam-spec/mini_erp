from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.db import Base

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="customer")

    def __repr__(self) -> str:
        return f"<Customer id={self.id} name={self.name!r} email={self.email!r}>"