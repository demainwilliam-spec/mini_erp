from decimal import Decimal
from sqlalchemy.orm import Session
from models.book import Book
from repositories.book_repository import BookRepository
from repositories.category_repository import CategoryRepository


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
            book.categories = CategoryRepository.get_by_ids(session, category_ids)
        return BookRepository.add(session, book)

    @staticmethod
    def get(session: Session, book_id: int) -> Book | None:
        return BookRepository.get_by_id(session, book_id)

    @staticmethod
    def list_all(session: Session) -> list[Book]:
        return BookRepository.get_all(session)

    @staticmethod
    def update_price(session: Session, book_id: int, new_price: Decimal) -> Book:
        book = BookRepository.get_by_id(session, book_id)
        if not book:
            raise ValueError(f"Livre introuvable : id={book_id}")
        book.price = new_price
        return book

    @staticmethod
    def delete(session: Session, book_id: int) -> None:
        book = BookRepository.get_by_id(session, book_id)
        if not book:
            raise ValueError(f"Livre introuvable : id={book_id}")
        BookRepository.delete(session, book)