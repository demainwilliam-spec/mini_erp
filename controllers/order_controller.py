from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.orm import Session
from models.order import Order, OrderLine
from repositories.order_repository import OrderRepository
from repositories.book_repository import BookRepository
from repositories.customer_repository import CustomerRepository
from services.order_service import confirm_order, close_order


def to_decimal(value) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class OrderController:

    @staticmethod
    def create_draft(session: Session, customer_id: int) -> Order:
        customer = CustomerRepository.get_by_id(session, customer_id)
        if not customer:
            raise ValueError(f"Client introuvable : id={customer_id}")
        order = Order(date=date.today(), customer_id=customer_id)
        return OrderRepository.add(session, order)

    @staticmethod
    def add_line(session: Session, order: Order, book_id: int, quantity: int) -> OrderLine:
        from models.order import OrderStatus
        if order.status != OrderStatus.DRAFT:
            raise ValueError("Impossible de modifier une commande non-draft.")
        book = BookRepository.get_by_id(session, book_id)
        if not book:
            raise ValueError(f"Livre introuvable : id={book_id}")
        line = OrderLine(
            order_id=order.id,
            book_id=book_id,
            quantity=quantity,
            unit_price=book.price,
        )
        return OrderRepository.add_line(session, line)

    @staticmethod
    def confirm(session: Session, order: Order) -> None:
        confirm_order(session, order)

    @staticmethod
    def close(session: Session, order: Order) -> None:
        close_order(session, order)

    @staticmethod
    def get(session: Session, order_id: int) -> Order:
        order = OrderRepository.get_by_id(session, order_id)
        if not order:
            raise ValueError(f"Commande introuvable : id={order_id}")
        return order

    @staticmethod
    def list_by_customer(session: Session, customer_id: int) -> list[Order]:
        return OrderRepository.get_by_customer(session, customer_id)

    @staticmethod
    def summary(order: Order) -> dict:
        return {
            "order_id": order.id,
            "customer_name": order.customer.name,
            "date": str(order.date),
            "status": order.status.value,
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