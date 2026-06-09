from decimal import Decimal
from sqlalchemy.orm import Session
from models.order import Order
from services.stock_service import check_stock, decrement_stock


def compute_order_total(order: Order) -> Decimal:
    return sum(line.quantity * line.unit_price for line in order.order_lines)


def confirm_order(session: Session, order: Order) -> None:
    if order.status != "draft":
        raise ValueError(f"Seules les commandes 'draft' peuvent être confirmées (statut actuel: {order.status!r}).")

    for line in order.order_lines:
        check_stock(session, line.book_id, line.quantity)

    for line in order.order_lines:
        decrement_stock(session, line.book_id, line.quantity)

    order.status = "confirmed"

def close_order(session: Session, order: Order) -> None:
    if order.status != "confirmed":
        raise ValueError(f"Seules les commandes 'confirmed' peuvent être clôturées (statut actuel: {order.status!r}).")

    order.status = "closed"