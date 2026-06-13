from sqlalchemy.orm import Session
from models.author import Author
from sqlalchemy import select

class AuthorController:

    @staticmethod
    def create(session: Session, name: str) -> Author:
        author = Author(name=name)
        session.add(author)
        session.flush()
        return author
    

    @staticmethod
    def get(session: Session, author_id: int) -> Author:
        author = session.get(Author, author_id)
        if not author:
            raise ValueError(f"Auteur introuvable : id={author_id}")
        return author


    @staticmethod
    def list_all(session: Session) -> list[Author]:
        stmt = select(Author)
        return session.execute(stmt).scalars().all()


    @staticmethod
    def update(session: Session, author_id: int, name: str) -> Author:
        author = session.get(Author, author_id)
        if not author:
            raise ValueError(f"Auteur introuvable : id={author_id}")
        author.name = name
        return author


    @staticmethod
    def delete(session: Session, author_id: int) -> None:
        author = session.get(Author, author_id)
        if not author:
            raise ValueError(f"Auteur introuvable : id={author_id}")
        session.delete(author)