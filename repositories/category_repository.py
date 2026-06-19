from sqlalchemy import select
from sqlalchemy.orm import Session
from models.category import Category


class CategoryRepository:

    @staticmethod
    def add(session: Session, category: Category) -> Category:
        session.add(category)
        session.flush()
        return category

    @staticmethod
    def get_by_id(session: Session, category_id: int) -> Category | None:
        return session.get(Category, category_id)

    @staticmethod
    def get_all(session: Session) -> list[Category]:
        stmt = select(Category)
        return session.execute(stmt).scalars().all()

    @staticmethod
    def get_by_ids(session: Session, category_ids: list[int]) -> list[Category]:
        stmt = select(Category).where(Category.id.in_(category_ids))
        return session.execute(stmt).scalars().all()

    @staticmethod
    def delete(session: Session, category: Category) -> None:
        session.delete(category)
