from sqlalchemy import select
from sqlalchemy.orm import Session
from models.book import Book


class BookRepository:

    @staticmethod
    def add(session: Session, book: Book) -> Book:
        session.add(book)
        session.flush()
        return book

    @staticmethod
    def get_by_id(session: Session, book_id: int) -> Book | None:
        return session.get(Book, book_id)

    @staticmethod
    def get_all(session: Session) -> list[Book]:
        stmt = select(Book)
        return session.execute(stmt).scalars().all()

    @staticmethod
    def delete(session: Session, book: Book) -> None:
        session.delete(book)