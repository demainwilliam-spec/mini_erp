from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.order import Order, OrderLine
from models.book import Book
from models.customer import Customer
from services.order_service import confirm_order, close_order
from decimal import Decimal, ROUND_HALF_UP

def to_decimal(value) -> Decimal:
            return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class OrderController:

    @staticmethod
    def create_draft(session: Session, customer_id: int) -> Order:
        customer = session.get(Customer, customer_id)
        if not customer:
            raise ValueError(f"Client introuvable : id={customer_id}")
        order = Order(date=date.today(), status="draft", customer_id=customer_id)
        session.add(order)
        session.flush()
        return order
    

    @staticmethod
    def add_line(
        session: Session,
        order: Order,
        book_id: int,
        quantity: int,
    ) -> OrderLine:
        if order.status != "draft":
            raise ValueError("Impossible de modifier une commande non-draft.")
        book = session.get(Book, book_id)
        if not book:
            raise ValueError(f"Livre introuvable : id={book_id}")
        line = OrderLine(
            order_id=order.id,
            book_id=book_id,
            quantity=quantity,
            unit_price=book.price,
        )
        session.add(line)
        return line
    

    @staticmethod
    def confirm(session: Session, order: Order) -> None:
        confirm_order(session, order)
    
    @staticmethod
    def close(session: Session, order: Order) -> None:
        close_order(session, order)

    @staticmethod
    def get(session: Session, order_id: int) -> Order:
        order = session.get(Order, order_id)
        if not order:
            raise ValueError(f"Commande introuvable : id={order_id}")
        return order
    
    @staticmethod
    def list_by_customer(session: Session, customer_id: int) -> list[Order]:
        stmt = select(Order).where(Order.customer_id == customer_id)
        return session.execute(stmt).scalars().all()
    
    @staticmethod
    def summary(order: Order) -> dict:
    
        return {
            "order_id": order.id,
            "customer_name": order.customer.name,
            "date": str(order.date),
            "status": order.status,
            "total_amount": to_decimal(order.total),
            "lines": [
                {
                    "book": line.book.title,
                    "quantity": line.quantity,
                    "unit_price": to_decimal(line.unit_price),
                    "subtotal": to_decimal(line.quantity * line.unit_price),
                }
                for line in order.order_lines
            ],
        }