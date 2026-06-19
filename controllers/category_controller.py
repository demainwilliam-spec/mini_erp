
from sqlalchemy.orm import Session
from models.category import Category
from repositories.category_repository import CategoryRepository


class CategoryController:

    @staticmethod
    def create(session: Session, name: str) -> Category:
        category = Category(name=name)
        return CategoryRepository.add(session, category)

    @staticmethod
    def get(session: Session, category_id: int) -> Category | None:
        return CategoryRepository.get_by_id(session, category_id)

    @staticmethod
    def list_all(session: Session) -> list[Category]:
        return CategoryRepository.get_all(session)

    @staticmethod
    def update(session: Session, category_id: int, name: str) -> Category:
        category = CategoryRepository.get_by_id(session, category_id)
        if not category:
            raise ValueError(f"Catégorie introuvable : id={category_id}")
        category.name = name
        return category

    @staticmethod
    def delete(session: Session, category_id: int) -> None:
        category = CategoryRepository.get_by_id(session, category_id)
        if not category:
            raise ValueError(f"Catégorie introuvable : id={category_id}")
        CategoryRepository.delete(session, category)