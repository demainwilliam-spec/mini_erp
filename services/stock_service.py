from sqlalchemy.orm import Session
from models.book import Book


class StockError(Exception):
    pass


def check_stock(session: Session, book_id: int, qty: int) -> Book:
    book = session.get(Book, book_id)
    if book is None:
        raise ValueError(f"Livre introuvable : id={book_id}")
    if book.stock_quantity < qty:
        raise StockError(
            f"Stock insuffisant pour '{book.title}' "
            f"(demandé={qty}, disponible={book.stock_quantity})"
        )
    return book


def decrement_stock(session: Session, book_id: int, qty: int) -> None:
    book = check_stock(session, book_id, qty)
    book.stock_quantity -= qty


def restock(session: Session, book_id: int, qty: int) -> Book:
    if qty <= 0:
        raise ValueError(f"Quantité de réapprovisionnement invalide : {qty}")
    
    book = session.get(Book, book_id)

    if book is None:
        raise ValueError(f"Livre introuvable : id={book_id}")
    book.stock_quantity += qty
   
    return book