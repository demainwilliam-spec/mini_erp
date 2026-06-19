from sqlalchemy import select
from sqlalchemy.orm import Session
from models.order import Order, OrderLine


class OrderRepository:

    @staticmethod
    def add(session: Session, order: Order) -> Order:
        session.add(order)
        session.flush()
        return order

    @staticmethod
    def get_by_id(session: Session, order_id: int) -> Order | None:
        return session.get(Order, order_id)

    @staticmethod
    def get_all(session: Session) -> list[Order]:
        stmt = select(Order)
        return session.execute(stmt).scalars().all()

    @staticmethod
    def get_by_customer(session: Session, customer_id: int) -> list[Order]:
        stmt = select(Order).where(Order.customer_id == customer_id)
        return session.execute(stmt).scalars().all()

    @staticmethod
    def delete(session: Session, order: Order) -> None:
        session.delete(order)

    @staticmethod
    def add_line(session: Session, line: OrderLine) -> OrderLine:
        session.add(line)
        session.flush()
        return line