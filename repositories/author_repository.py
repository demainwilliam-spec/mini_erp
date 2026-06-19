from sqlalchemy import select
from sqlalchemy.orm import Session
from models.author import Author


class AuthorRepository:

    @staticmethod
    def add(session: Session, author: Author) -> Author:
        session.add(author)
        session.flush()
        return author

    @staticmethod
    def get_by_id(session: Session, author_id: int) -> Author | None:
        return session.get(Author, author_id)

    @staticmethod
    def get_all(session: Session) -> list[Author]:
        stmt = select(Author)
        return session.execute(stmt).scalars().all()

    @staticmethod
    def delete(session: Session, author: Author) -> None:
        session.delete(author)