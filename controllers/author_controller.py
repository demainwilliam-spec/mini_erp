from sqlalchemy.orm import Session
from models.author import Author
from repositories.author_repository import AuthorRepository

class AuthorController:

    @staticmethod
    def create(session: Session, name: str) -> Author:
        author = Author(name=name)
        return AuthorRepository.add(session, author)
    

    @staticmethod
    def get(session: Session, author_id: int) -> Author | None:
        return AuthorRepository.get_by_id(session, author_id)


    @staticmethod
    def list_all(session: Session) -> list[Author]:
        return AuthorRepository.get_all(session)


    @staticmethod
    def update(session: Session, author_id: int, name: str) -> Author:
        author = AuthorRepository.get_by_id(session, author_id)
        if not author:
            raise ValueError(f"Auteur introuvable : id={author_id}")
        author.name = name
        return author


    @staticmethod
    def delete(session: Session, author_id: int) -> None:
        author = AuthorRepository.get_by_id(session, author_id)
        if not author:
            raise ValueError(f"Auteur introuvable : id={author_id}")
        AuthorRepository.delete(session, author)