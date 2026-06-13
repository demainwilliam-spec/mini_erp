from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.book import Book
from models.category import Category


class BookController:

    @staticmethod
    def create(
        session: Session,
        title: str,
        price: Decimal,
        stock: int,
        author_id: int,
        supplier_id: int,
        category_ids: list[int] | None = None,
    ) -> Book:
        book = Book(
            title=title,
            price=price,
            stock_quantity=stock,
            author_id=author_id,
            supplier_id=supplier_id,
        )
        if category_ids:
            stmt = select(Category).where(Category.id.in_(category_ids))
            cats = session.execute(stmt).scalars().all()
            book.categories = cats
        session.add(book)
        session.flush()
        return book
    
    @staticmethod
    def get(session: Session, book_id: int) -> Book:
        book = session.get(Book, book_id)
        if not book:
            raise ValueError(f"Livre introuvable : id={book_id}")
        return book

    @staticmethod
    def list_all(session: Session) -> list[Book]:
        stmt = select(Book)
        return session.execute(stmt).scalars().all()
    
    @staticmethod
    def update_price(session: Session, book_id: int, new_price: Decimal) -> Book:
        book = session.get(Book, book_id)
        if not book:
            raise ValueError(f"Livre introuvable : id={book_id}")
        book.price = new_price
        return book

    @staticmethod
    def delete(session: Session, book_id: int) -> None:
        book = session.get(Book, book_id)
        if not book:
            raise ValueError(f"Livre introuvable : id={book_id}")
        session.delete(book)