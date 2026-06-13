from sqlalchemy.orm import Session
from models.category import Category
from sqlalchemy import select

class CategoryController:

    @staticmethod
    def create(session: Session, name: str) -> Category:
        category = Category(name=name)
        session.add(category)
        session.flush()
        return category
    

    @staticmethod
    def get(session: Session, category_id: int) -> Category:
        category = session.get(Category, category_id)
        if not category:
            raise ValueError(f"Catégorie introuvable : id={category_id}")
        return category


    @staticmethod
    def list_all(session: Session) -> list[Category]:
        stmt = select(Category)
        return session.execute(stmt).scalars().all()


    @staticmethod
    def update(session: Session, category_id: int, name: str) -> Category:
        category = session.get(Category, category_id)
        if not category:
            raise ValueError(f"Catégorie introuvable : id={category_id}")
        category.name = name
        return category


    @staticmethod
    def delete(session: Session, category_id: int) -> None:
        category = session.get(Category, category_id)
        if not category:
            raise ValueError(f"Catégorie introuvable : id={category_id}")
        session.delete(category)